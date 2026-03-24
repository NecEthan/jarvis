# Music Agent Node
# Handles all music-related actions (play, pause, skip, volume, queue).

# TODO: import Sonos client or music service integration

def music_agent_node(state) -> dict:
    """
    LangGraph node: handles music commands.
    """
    result = f"[music stub] received intent: '{state.intent}'"
    # TODO: call Sonos / streaming service API based on state.intent
    return {
        "messages": state.messages + [{"role": "ai", "content": result}],
    }
