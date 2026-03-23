# Music Agent Node
# Handles all music-related actions (play, pause, skip, volume, queue).

# TODO: import Sonos client or music service integration

def music_agent_node(state: dict) -> dict:
    """
    LangGraph node: handles music commands.
    Reads 'intent' and 'messages' from state, writes 'result' and appends to 'messages'.
    """
    intent = state.get("intent", "unknown")
    result = f"[music stub] received intent: '{intent}'"
    return {
        "result": result,
        "messages": state["messages"] + [{"role": "ai", "content": result}],
    }
