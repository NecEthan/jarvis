import os
import subprocess
import tempfile

import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../../.env")
    )
)


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

    weather = get_weather(os.getenv("BRIEFING_LOCATION", "auto"))
    if "error" not in weather:
        parts.append(
            f"Weather in {weather['location']}: {weather['description']}, "
            f"{weather['temp_c']}°C ({weather['temp_f']}°F), "
            f"feels like {weather['feels_like_c']}°C, humidity {weather['humidity']}%."
        )
    else:
        parts.append(f"Weather unavailable: {weather['error']}")

    content = "\n\n".join(parts)
    speak(content)
    return {"content": content}
