from langchain_openai import ChatOpenAI
from schemas.agent_schemas import OrchestratorState, OrchestratorInput, OrchestratorOutput
from prompts.orchestrator_prompt import ORCHESTRATOR_PROMPT

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
orchestrator_chain = ORCHESTRATOR_PROMPT | llm.with_structured_output(
    OrchestratorOutput, method="function_calling"
)

def orchestrator_node(state: OrchestratorState) -> dict:
    """
    LangGraph node: reads the last user message, classifies intent, returns route.
    """
    input_data = OrchestratorInput(
        text=state["messages"][-1]["content"],
        state=state.get("orchestrator_state"),
    )
    ctx = input_data.state or OrchestratorState()

    output: OrchestratorOutput = orchestrator_chain.invoke({
        "text":        input_data.text,
        "last_action": ctx.last_action or "none",
        "last_agent":  ctx.last_agent  or "none",
        "last_room":   ctx.last_room   or "none",
        "time_of_day": ctx.time_of_day or "unknown",
    })

    return {
        "orchestrator_state": output.state,
        "route":  output.route,
        "intent": output.intent,
        "messages": state["messages"] + [
            {"role": "ai", "content": f"route={output.route} | intent={output.intent}"}
        ],
    }
