// ─── Agent ────────────────────────────────────────────────────────────────────

export interface AgentRequest {
  message: string;
  conversationId?: string;
}

export interface AgentResponse {
  reply: string;
  conversationId: string;
  // TODO: add tool calls, sources, etc.
}

// ─── TTS ──────────────────────────────────────────────────────────────────────

export interface TtsRequest {
  text: string;
  voice?: string;
}

export interface TtsResponse {
  audioUrl: string;
}

// ─── Sonos ────────────────────────────────────────────────────────────────────

export interface SonosPlayRequest {
  audioUrl: string;
}

export type SonosCommand = "pause" | "resume" | "next" | "prev";

export interface SonosControlRequest {
  command: SonosCommand;
  value?: number; // for volume
}

export interface SonosResponse {
  ok: boolean;
}

// ─── Generic ──────────────────────────────────────────────────────────────────

export interface ApiError {
  error: string;
  code?: string;
  statusCode: number;
}
