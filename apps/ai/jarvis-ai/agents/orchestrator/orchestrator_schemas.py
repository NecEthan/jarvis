from typing import Optional
from pydantic import BaseModel


class OrchestratorState(BaseModel):
    content:  str
    route:    Optional[str] = None
    intent:   Optional[str] = None


class OrchestratorOutput(BaseModel):
    route:  str
    intent: str
    state:  OrchestratorState
