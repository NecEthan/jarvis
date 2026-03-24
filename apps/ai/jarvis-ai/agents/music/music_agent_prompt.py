from langchain_core.prompts import ChatPromptTemplate


MUSIC_AGENT_SYSTEM_PROMPT = """You are the Music Agent for Jarvis.

Your job is to interpret music-related user requests and produce a structured music action.

Rules:
- Prefer action=play when user asks to play music.
- Extract a concise song_query from the request (genre, mood, artist, or song title).
- Keep user-facing message short and helpful.
"""


MUSIC_AGENT_PROMPT = ChatPromptTemplate.from_messages(
	[
		("system", MUSIC_AGENT_SYSTEM_PROMPT),
		(
			"human",
			"User content: {content}\nDetected intent: {intent}",
		),
	]
)

