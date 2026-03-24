export interface AgentRequest {
  message: string;
  conversationId?: string;
}

export interface AgentResponse {
  reply: string;
  conversationId: string;
}

export interface TtsRequest {
  text: string;
  voice?: string;
}

export interface TtsResponse {
  audioUrl: string;
}

export interface SonosPlayRequest {
  audioUrl: string;
}

export type SonosCommand = "pause" | "resume" | "next" | "prev";

export interface SonosControlRequest {
  command: SonosCommand;
  value?: number; 
}

export interface SonosResponse {
  ok: boolean;
}

export interface SpotifyPlayRequest {
  spotifyUri: string;
  deviceId?: string;
  deviceName?: string;
}

export interface SpotifyPlayResponse {
  ok: boolean;
  deviceId?: string;
}


export interface ApiError {
  error: string;
  code?: string;
  statusCode: number;
}
