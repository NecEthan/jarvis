from pydantic import BaseModel
from typing import Optional, Dict, Any

class OrchestratorState(BaseModel):
    last_action: Optional[str] = None
    last_agent: Optional[str] = None
    last_room: Optional[str] = None
    time_of_day: Optional[str] = "morning"
    additional_context: Dict[str, Any] = {}

class OrchestratorInput(BaseModel):
    text: str
    state: Optional[OrchestratorState] = None

class OrchestratorOutput(BaseModel):
    route: str
    intent: str
    state: OrchestratorState