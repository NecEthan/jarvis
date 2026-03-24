import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
import json
from langgraph.graph import StateGraph, END
from agents.orchestrator.orchestrator_node import orchestrator_node
from agents.orchestrator.orchestrator_schemas import OrchestratorState
from agents.music.music_agent_node import music_agent_node
from agents.briefing.briefing_agent_node import briefing_agent_node

workflow = StateGraph(OrchestratorState)

workflow.add_node("Orchestrator", orchestrator_node)
workflow.add_node("MusicAgent",   music_agent_node)
workflow.add_node("BriefingAgent", briefing_agent_node)

workflow.set_entry_point("Orchestrator")

def route(state: OrchestratorState):
    if state.route == "music":
        return "MusicAgent"
    elif state.route == "briefing":
        return "BriefingAgent"
    return END

workflow.add_conditional_edges("Orchestrator", route)
workflow.add_edge("MusicAgent",   END)
workflow.add_edge("BriefingAgent", END)

app = workflow.compile()

if __name__ == "__main__":
    result = app.invoke(OrchestratorState(
        content="play some jamaican music"
    ))
    print(json.dumps(result, indent=2, default=str))
