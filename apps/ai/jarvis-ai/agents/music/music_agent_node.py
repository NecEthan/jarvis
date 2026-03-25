from agents.orchestrator.orchestrator_schemas import OrchestratorState


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
    return {
        "content": f"Music agent received request: {genre}. No playback backend configured.",
    }
