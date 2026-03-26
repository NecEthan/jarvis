from langgraph.graph import END, START, StateGraph
from agents.briefing.briefing_agent_node import briefing_agent_node
from agents.orchestrator.orchestrator_schemas import OrchestratorState


graph = StateGraph(OrchestratorState)

graph.add_node("BriefingAgent", briefing_agent_node)
graph.add_edge(START, "BriefingAgent")
graph.add_edge("BriefingAgent", END)

briefing_agent_app = graph.compile()

