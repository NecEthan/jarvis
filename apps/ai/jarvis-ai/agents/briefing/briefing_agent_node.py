import os

import httpx
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

    return {"content": "\n\n".join(parts)}
