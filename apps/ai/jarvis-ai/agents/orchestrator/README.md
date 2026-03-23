# Orchestrator Agent

Routes incoming requests to the appropriate sub-agent based on parsed intent.

## Responsibilities
- Receive initial user message + parsed intent from the graph state
- Decide which agent(s) to invoke (music, briefing, device, etc.)
- Merge sub-agent results back into state

## TODO
- [ ] Define routing logic
- [ ] Handle multi-intent requests
- [ ] Add fallback for unknown intents
