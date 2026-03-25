import os
from typing import Optional

import soco
import spotipy
from dotenv import load_dotenv
from soco.plugins.sharelink import ShareLinkPlugin
from spotipy.oauth2 import SpotifyClientCredentials

from agents.orchestrator.orchestrator_schemas import OrchestratorState

load_dotenv(
    dotenv_path=os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../../.env")
    )
)

_sp: Optional[spotipy.Spotify] = None


def _get_spotify() -> spotipy.Spotify:
    global _sp
    if _sp is None:
        _sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=os.environ["SPOTIFY_CLIENT_ID"],
                client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
            )
        )
    return _sp


def search_track(query: str) -> Optional[dict]:
    results = _get_spotify().search(q=query, type="track", limit=10)
    items = results.get("tracks", {}).get("items", [])
    if not items:
        return None
    return max(items, key=lambda t: t.get("popularity", 0))


def play_on_sonos(uri: str) -> str:
    devices = list(soco.discover() or [])
    if not devices:
        raise RuntimeError("No Sonos devices found on the network.")

    sonos_ip = os.getenv("SONOS_IP")
    if sonos_ip:
        speaker = next((d for d in devices if d.ip_address == sonos_ip), devices[0])
    else:
        speaker = devices[0]

    track_id = uri.split(":")[-1]
    share_url = f"https://open.spotify.com/track/{track_id}"
    speaker.clear_queue()
    plugin = ShareLinkPlugin(speaker)
    plugin.add_share_link_to_queue(share_url)
    speaker.play_from_queue(0)
    return speaker.player_name


def music_agent(input_data: dict) -> dict:
    song = (input_data.get("song") or "").strip()
    genre = (input_data.get("genre") or "").strip()

    query = song if song else (genre if genre else "popular music")
    track = search_track(query)

    if not track:
        return {"status": "error", "message": f"No tracks found for: {query}"}

    uri = track["uri"]
    name = track["name"]
    artist = track["artists"][0]["name"]

    try:
        speaker_name = play_on_sonos(uri)
    except RuntimeError as e:
        return {"status": "error", "message": str(e)}

    return {
        "status": "playing",
        "track": name,
        "artist": artist,
        "speaker": speaker_name,
    }


def resolve_genre(state: OrchestratorState) -> str:
    return (state.content or "music").strip().lower()


def music_agent_node(state: OrchestratorState) -> dict:
    genre = resolve_genre(state)
    result = music_agent({"intent": "play_music", "genre": genre})
    if result["status"] == "playing":
        content = f"Now playing \"{result['track']}\" by {result['artist']} on {result['speaker']}."
    else:
        content = result.get("message", "Music playback failed.")
    return {"content": content}
