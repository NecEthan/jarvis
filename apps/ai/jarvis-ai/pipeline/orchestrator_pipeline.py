from langgraph.graph import StateGraph, END
from schemas.agent_schemas import OrchestratorState
from agents.orchestrator.orchestrator_node import orchestrator_node
from agents.music.music_agent_node import music_agent_node
from agents.briefing.briefing_agent_node import briefing_agent_node


workflow = StateGraph(OrchestratorState)

workflow.add_node("Orchestrator", orchestrator_node)
workflow.add_node("MusicAgent", music_agent_node)
workflow.add_node("BriefingAgent", briefing_agent_node)

workflow.set_entry_point("Orchestrator")

def route(state: OrchestratorState):
    route_name = state.additional_context.get("route")
    if route_name == "music":
        return "MusicAgent"
    elif route_name == "briefing":
        return "BriefingAgent"
    return END

workflow.add_conditional_edges("Orchestrator", route)
workflow.add_edge("MusicAgent", END)
workflow.add_edge("BriefingAgent", END)

app = workflow.compile()  