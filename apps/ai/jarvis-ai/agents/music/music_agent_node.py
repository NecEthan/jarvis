# Music Agent Node
# Handles all music-related actions (play, pause, skip, volume, queue).

# TODO: import Sonos client or music service integration

def music_agent_node(state) -> dict:
    """
    LangGraph node: handles music commands.
    """
    intent = state.additional_context.get("intent", "unknown")
    # TODO: call Sonos / streaming service API based on intent
    result = f"[music stub] received intent: '{intent}'"
    return {
        "messages": state.messages + [{"role": "ai", "content": result}],
        "additional_context": {**state.additional_context, "result": result},
    }
