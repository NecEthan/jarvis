from langgraph.graph import StateGraph

# TODO: import AgentState from schemas
# TODO: import all agent nodes

# Pipeline definition — wire nodes and edges here


def build_graph():
    """Construct and compile the Jarvis LangGraph pipeline."""
    # TODO: graph = StateGraph(AgentState)

    # TODO: add nodes
    # graph.add_node("orchestrator", orchestrator_node)
    # graph.add_node("memory",       memory_agent_node)
    # graph.add_node("planner",      planner_agent_node)
    # graph.add_node("music",        music_agent_node)
    # graph.add_node("briefing",     briefing_agent_node)
    # graph.add_node("device",       device_agent_node)

    # TODO: define edges / conditional routing
    # graph.set_entry_point("memory")
    # graph.add_edge("memory", "orchestrator")
    # graph.add_conditional_edges("orchestrator", route_by_intent, {...})

    # TODO: return graph.compile()
    raise NotImplementedError


# Singleton — import this in main.py
# compiled_graph = build_graph()
