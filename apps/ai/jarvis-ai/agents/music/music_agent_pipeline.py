from langgraph.graph import END, START, StateGraph

from agents.music.music_agent_node import music_agent_node
from agents.orchestrator.orchestrator_schemas import OrchestratorState


graph = StateGraph(OrchestratorState)

graph.add_node("MusicAgent", music_agent_node)
graph.add_edge(START, "MusicAgent")
graph.add_edge("MusicAgent", END)

music_agent_app = graph.compile()

