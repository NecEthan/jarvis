# Briefing Agent Node
# Composes a morning/evening briefing from calendar, news, weather, etc.

# TODO: import data source integrations (calendar, weather, news)

def briefing_agent_node(state) -> dict:
    """
    LangGraph node: composes a briefing summary.
    """
    intent = state.additional_context.get("intent", "unknown")
    # TODO: fetch calendar events, weather, news then compose summary
    result = f"[briefing stub] received intent: '{intent}'"
    return {
        "messages": state.messages + [{"role": "ai", "content": result}],
        "additional_context": {**state.additional_context, "result": result},
    }
