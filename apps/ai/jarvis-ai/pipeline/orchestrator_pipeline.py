from langgraph import Pipeline
from agents.orchestrator.orchestrator_node import orchestrator_agent
from agents.music.music_agent_node import music_agent
from agents.briefing.briefing_agent_node import briefing_agent
from schemas.orchestrator_schemas import OrchestratorInput

pipeline = Pipeline()

pipeline.add_node(orchestrator_agent, name="Orchestrator")
pipeline.add_node(music_agent, name="MusicAgent")
pipeline.add_node(briefing_agent, name="BriefingAgent")

pipeline.connect("Orchestrator", "MusicAgent", condition=lambda out: out.route == "music")
pipeline.connect("Orchestrator", "BriefingAgent", condition=lambda out: out.route == "briefing")

def run_pipeline(input_text: str):
    input_data = OrchestratorInput(text=input_text)
    return pipeline.run(input_data)