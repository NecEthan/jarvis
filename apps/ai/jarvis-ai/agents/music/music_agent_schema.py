from typing import Literal

from pydantic import BaseModel, Field


class MusicState(BaseModel):
	content: str = Field(default="")
	intent: str = Field(default="music")


class MusicOutput(BaseModel):
	action: Literal["play", "pause", "next", "previous", "unknown"] = Field(
		default="play"
	)
	song_query: str = Field(default="rock song")
	message: str = Field(default="Playing music now.")

