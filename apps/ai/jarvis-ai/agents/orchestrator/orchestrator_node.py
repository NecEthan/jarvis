from prompts.orchestrator_prompt import ORCHESTRATOR_PROMPT_TEMPLATE
from schemas.agent_schemas import OrchestratorInput, OrchestratorOutput, OrchestratorState
from langgraph import create_agent
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

orchestrator_agent = create_agent(
    name="Orchestrator",
    input_schema=OrchestratorInput,
    output_schema=OrchestratorOutput,
    llm_model=llm,
    prompt_template=ORCHESTRATOR_PROMPT_TEMPLATE
)

state = OrchestratorState()
input_data = OrchestratorInput(
    text="play some lofi music",
    state=state
)

output = orchestrator_agent.run(input_data)
print(output.json())



