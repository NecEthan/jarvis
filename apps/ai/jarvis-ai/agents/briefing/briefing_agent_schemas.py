from pydantic import BaseModel
from typing import List, Optional


class CalendarEvent(BaseModel):
    title: str
    time: str
    location: Optional[str] = None


class TaskItem(BaseModel):
    task: str
    priority: Optional[str] = None


class WeatherInfo(BaseModel):
    summary: str
    temperature: str


class BriefingState(BaseModel):
    time_of_day: str

    calendar_events: List[CalendarEvent] = []
    tasks: List[TaskItem] = []
    weather: Optional[WeatherInfo] = None

    briefing_length: str = "short" 
    preferred_tone: str = "calm"

    last_briefing_summary: Optional[str] = None

    script: Optional[str] = None
    audio_url: Optional[str] = None

class BriefingOutput(BaseModel):
    script: str
    audio_url: str