from dataclasses import dataclass, field
from typing import Any

# TODO: populate from env, user profile store, or config file


@dataclass
class SystemContext:
    """
    Ambient context available to all agents throughout a session.
    Injected once at graph startup and threaded through state.
    """
    user_name: str = ""
    timezone: str = "UTC"
    location: str = ""
    preferences: dict[str, Any] = field(default_factory=dict)
    # TODO: add device list, calendar access token, music service config

    @classmethod
    def from_env(cls) -> "SystemContext":
        """Build context from environment variables."""
        # TODO: load from os.environ / config
        return cls()
