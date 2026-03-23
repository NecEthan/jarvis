# Memory Agent

Manages long-term memory and conversation history for personalized responses.

## Responsibilities
- Retrieve relevant past context via semantic search
- Persist new facts and preferences
- Summarize and prune old memories

## TODO
- [ ] Choose memory backend (Redis, Pinecone, pgvector)
- [ ] Implement embedding + retrieval pipeline
- [ ] Define what is worth persisting vs. ephemeral
