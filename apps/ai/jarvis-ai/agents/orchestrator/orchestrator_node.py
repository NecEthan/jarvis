from prompts.orchestrator_prompt import ORCHESTRATOR_PROMPT_TEMPLATE
from schemas.agent_schemas import OrchestratorState

orchestrator_agent = create_agent(
    name="Orchestrator",
    input_schema=OrchestratorInput,
    output_schema=OrchestratorOutput,
    llm_model="gpt-4",
    prompt_template=ORCHESTRATOR_PROMPT_TEMPLATE
)

def orchestrator_node(state):
    """
    Entry point for the agent graph.
    Decides which agent(s) to invoke based on intent in state.
    """
    if not isinstance(state, OrchestratorState):
        raise ValueError("State must be an instance of OrchestratorState")
    # TODO: read intent from state
    # TODO: route to music_agent, briefing_agent, device_agent, etc.
    raise NotImplementedError


