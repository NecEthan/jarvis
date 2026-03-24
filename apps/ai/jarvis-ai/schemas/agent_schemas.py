from pydantic import BaseModel
from typing import Optional, Dict, Any

class OrchestratorState(BaseModel):
    messages:           list = []
    additional_context: Dict[str, Any] = {}

class OrchestratorInput(BaseModel):
    text: str
    state: Optional[OrchestratorState] = None

class OrchestratorOutput(BaseModel):
    route:  str
    intent: str
    state:  OrchestratorState
