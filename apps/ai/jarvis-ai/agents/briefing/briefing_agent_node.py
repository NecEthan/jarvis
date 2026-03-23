# Briefing Agent Node
# Composes a morning/evening briefing from calendar, news, weather, etc.

# TODO: import data source integrations (calendar, weather, news)

def briefing_agent_node(state: dict) -> dict:
    """
    LangGraph node: composes a briefing summary.
    Reads 'intent' and 'messages' from state, writes 'result' and appends to 'messages'.
    """
    intent = state.get("intent", "unknown")
    # TODO: fetch calendar events, weather, news then compose summary
    result = f"[briefing stub] received intent: '{intent}'"
    return {
        "result": result,
        "messages": state["messages"] + [{"role": "ai", "content": result}],
    }
