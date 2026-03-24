import base64
import os

import httpx
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from agents.orchestrator.orchestrator_schemas import OrchestratorState
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class TrackChoice(BaseModel):
    selected_index: int = Field(
        description="Zero-based index of the chosen track from the provided candidates."
    )
    reason: str = Field(description="Short reason for choosing this track.")


def play_spotify_uri(spotify_uri: str) -> str:
    server_url = os.getenv("JARVIS_SERVER_URL", "http://localhost:3000").rstrip("/")
    device_id = os.getenv("SPOTIFY_DEVICE_ID", "")
    device_name = os.getenv("SONOS_DEVICE_NAME", "")

    payload = {"spotifyUri": spotify_uri}
    if device_id:
        payload["deviceId"] = device_id
    if device_name:
        payload["deviceName"] = device_name

    try:
        with httpx.Client(timeout=20) as client:
            response = client.post(
                f"{server_url}/api/spotify/play",
                json=payload,
            )

        if response.is_success:
            data = response.json()
            selected_device = data.get("deviceId", "unknown")
            return f"Spotify playback started on device {selected_device}."

        return f"Spotify playback request failed ({response.status_code}): {response.text}"
    except Exception as err:
        return f"Failed to call Spotify playback route: {err}"


def get_spotify_access_token() -> str:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Missing Spotify credentials in environment")

    auth_raw = f"{client_id}:{client_secret}".encode("utf-8")
    auth_header = base64.b64encode(auth_raw).decode("utf-8")

    with httpx.Client(timeout=15) as client:
        response = client.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
        )
        response.raise_for_status()
        data = response.json()

    token = data.get("access_token")
    if not token:
        raise RuntimeError("Spotify token response missing access_token")
    return token


def search_spotify_tracks(query: str) -> list[dict]:
    token = get_spotify_access_token()

    with httpx.Client(timeout=15) as client:
        response = client.get(
            "https://api.spotify.com/v1/search",
            params={
                "q": query,
                "type": "track",
                "limit": 10,
                "market": "US",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        data = response.json()

    items = data.get("tracks", {}).get("items", [])
    if not items:
        return []

    tracks = []
    for item in items:
        artists = item.get("artists", [])
        artist_names = ", ".join(a.get("name", "") for a in artists if a.get("name"))
        tracks.append(
            {
                "name": item.get("name", "Unknown Track"),
                "artist": artist_names or "Unknown Artist",
                "url": item.get("external_urls", {}).get("spotify", ""),
                "uri": item.get("uri", ""),
                "album": item.get("album", {}).get("name", ""),
                "popularity": item.get("popularity", 0),
            }
        )

    return tracks


def choose_track_with_llm(user_input: str, genre: str, tracks: list[dict]) -> tuple[dict, str]:
    if not tracks:
        raise ValueError("No tracks provided to choose from")

    track_lines = []
    for idx, track in enumerate(tracks):
        track_lines.append(
            (
                f"{idx}. {track['name']} - {track['artist']} "
                f"(album: {track.get('album', '')}, popularity: {track.get('popularity', 0)})"
            )
        )

    prompt = (
        "You are selecting exactly one Spotify track for playback. "
        "Choose the best match for the user's intent and genre.\n\n"
        f"User input: {user_input}\n"
        f"Resolved genre/intent: {genre}\n\n"
        "Track candidates:\n"
        + "\n".join(track_lines)
        + "\n\nReturn only the selected index and a short reason."
    )

    structured_llm = llm.with_structured_output(TrackChoice, method="function_calling")
    choice = structured_llm.invoke(prompt)

    selected_index = max(0, min(choice.selected_index, len(tracks) - 1))
    return tracks[selected_index], choice.reason


def resolve_genre(state: OrchestratorState) -> str:
    intent = (state.intent or "").strip()
    if intent and intent.lower() not in {"music", "play_music", "play-music"}:
        return intent

    content = (state.content or "").strip()
    if content:
        return content

    return "music"


def music_agent_node(state: OrchestratorState):
    genre = resolve_genre(state)
    track = None
    llm_reason = ""
    spotify_note = "Spotify search skipped."
    execution_result = "No Spotify playback attempted."

    try:
        tracks = search_spotify_tracks(genre)
        if tracks:
            track, llm_reason = choose_track_with_llm(state.content, genre, tracks)
            spotify_note = (
                f"LLM selected Spotify track: {track['name']} by {track['artist']}"
            )
        else:
            spotify_note = f"No Spotify track found for: {genre}"
    except Exception as err:
        spotify_note = f"Spotify search/selection failed: {err}"

    if track and track.get("uri"):
        execution_result = play_spotify_uri(track["uri"])
    elif track:
        execution_result = (
            "Selected track has no Spotify URI, so playback was skipped."
        )

    details = spotify_note
    if track and track.get("url"):
        details = f"{spotify_note}\nSpotify URL: {track['url']}"
    if llm_reason:
        details = f"{details}\nWhy chosen: {llm_reason}"

    return {
        "content": f"Playing {genre}.\n{details}\n{execution_result}",
    }

