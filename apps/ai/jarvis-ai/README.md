# Jarvis AI — LangGraph Multi-Agent Service

Python multi-agent backend powering Jarvis. Built with FastAPI and LangGraph.

## Structure

```
jarvis-ai/
├── agents/
│   ├── orchestrator/   ← routes requests to sub-agents
│   ├── music/          ← Sonos / music playback control
│   ├── briefing/       ← calendar, weather, news summary
│   ├── device/         ← smart home device control
│   ├── memory/         ← long-term memory read/write
│   └── planner/        ← multi-step task decomposition
├── schemas/
│   └── agent_schemas.py  ← AgentState, Intent, AgentResponse
├── context/
│   └── system_context.py ← ambient user/env context
├── graph/
│   └── langgraph_pipeline.py  ← graph wiring & compilation
└── utils/
    └── helpers.py
```

## Setup

```bash
cd apps/ai
python -m venv .venv
source .venv/bin/activate
pip install -r jarvis-ai/requirements.txt
```

## Run Tests

```bash
pytest jarvis-ai/
```

## Graph Flow (planned)

```
user message
    ↓
memory_agent   ← inject relevant past context
    ↓
orchestrator   ← classify intent, route to sub-agent(s)
    ↓
[music | briefing | device | planner]
    ↓
output         ← format final response
```
