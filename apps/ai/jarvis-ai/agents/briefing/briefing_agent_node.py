import os
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone

import httpx
from openai import OpenAI
from tavily import TavilyClient


def get_weather(location: str = "auto") -> dict:
    url = f"https://wttr.in/{location}?format=j1"
    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers={"User-Agent": "jarvis-briefing/1.0"})
            response.raise_for_status()
            data = response.json()

        current = data["current_condition"][0]
        area = data["nearest_area"][0]
        city = area["areaName"][0]["value"]
        country = area["country"][0]["value"]

        return {
            "location": f"{city}, {country}",
            "temp_c": current["temp_C"],
            "temp_f": current["temp_F"],
            "description": current["weatherDesc"][0]["value"],
            "feels_like_c": current["FeelsLikeC"],
            "humidity": current["humidity"],
        }
    except Exception as e:
        return {"error": str(e)}


def get_top_story_yesterday() -> dict:
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return {"error": "TAVILY_API_KEY is not set"}

        client = TavilyClient(api_key=api_key)
        yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat()
        query = (
            f"What was the single biggest world news story on {yesterday}? "
            "Return one authoritative article from a major news outlet with title"
        )

        result = client.search(
            query=query,
            topic="news",
            search_depth="advanced",
            max_results=5,
            include_answer=True,
            include_raw_content=False,
        )

        answer = (result.get("answer") or "").strip()
        results = result.get("results", [])

        if results:
            top = results[0]
            return {
                "title": top.get("title", "Top news story yesterday"),
                "url": top.get("url", ""),
                "summary": answer or top.get("content", ""),
            }

        if answer:
            return {
                "title": "Top news story yesterday",
                "url": "",
                "summary": answer,
            }

        return {"error": "No Tavily results found"}
    except Exception as e:
        return {"error": str(e)}


def speak(text: str) -> None:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        audio_path = f.name

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text,
    ) as response:
        response.stream_to_file(audio_path)

    subprocess.run(["afplay", audio_path], check=True)
    os.unlink(audio_path)


def briefing_agent_node(state) -> dict:
    parts = []

    weather = get_weather(os.getenv("BRIEFING_LOCATION", "London"))
    if "error" not in weather:
        parts.append(
            f"Weather in {weather['location']}: {weather['description']}, "
            f"{weather['temp_c']}°C ({weather['temp_f']}°F), "
            f"feels like {weather['feels_like_c']}°C, humidity {weather['humidity']}%."
        )
    else:
        parts.append(f"Weather unavailable: {weather['error']}")

    news = get_top_story_yesterday()
    if "error" not in news:
        summary = news.get("summary", "")
        source = f" Source: {news['url']}" if news.get("url") else ""
        parts.append(
            f"Top story yesterday: {news['title']}. {summary}{source}".strip()
        )
    else:
        parts.append(f"News unavailable: {news['error']}")

    content = "\n\n".join(parts)
    speak(content)
    return {"content": content}
