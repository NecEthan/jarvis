from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from agents.orchestrator.orchestrator_schemas import OrchestratorState, OrchestratorOutput

ORCHESTRATOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Orchestrator for Jarvis, a personal AI assistant.

Analyze the user's message and decide which agent should handle it.

Available routes:
- music    → play, pause, skip, volume, queue music
- briefing → morning/evening briefing, calendar, weather, news
- device   → lights, thermostat, smart home control
- planner  → multi-step tasks that require planning
- memory   → recall or store personal information

Respond with the correct route and a concise intent description."""),
    ("human", "{text}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
orchestrator_chain = ORCHESTRATOR_PROMPT | llm.with_structured_output(
    OrchestratorOutput, method="function_calling"
)

def orchestrator_node(state: OrchestratorState) -> dict:
    output: OrchestratorOutput = orchestrator_chain.invoke({
        "text": state.content,
    })

    return {
        "content": f"route={output.route} | intent={output.intent}",
        "route":  output.route,
        "intent": output.intent,
    }
