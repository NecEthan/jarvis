from langchain_openai import ChatOpenAI
from schemas.agent_schemas import OrchestratorState, OrchestratorOutput
from prompts.orchestrator_prompt import ORCHESTRATOR_PROMPT

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
orchestrator_chain = ORCHESTRATOR_PROMPT | llm.with_structured_output(
    OrchestratorOutput, method="function_calling"
)

def orchestrator_node(state: OrchestratorState) -> dict:
    output: OrchestratorOutput = orchestrator_chain.invoke({
        "text": state.messages[-1]["content"],
    })

    return {
        "messages": state.messages + [
            {"role": "ai", "content": f"route={output.route} | intent={output.intent}"}
        ],
        "additional_context": {"route": output.route, "intent": output.intent},
    }
