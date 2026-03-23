import { config } from "@/lib/config";
import { AppError } from "@/lib/errors";
import type { AgentRequest, AgentResponse } from "@/types/api";

// Typed HTTP client for the FastAPI / LangGraph backend

async function post<TBody, TResponse>(path: string, body: TBody): Promise<TResponse> {
  const url = `${config.langGraphApiUrl}${path}`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "unknown error");
    throw new AppError(`FastAPI error [${res.status}]: ${text}`, res.status, "UPSTREAM_ERROR");
  }

  return res.json() as Promise<TResponse>;
}

// ─── Endpoints ────────────────────────────────────────────────────────────────

export async function callAgent(payload: AgentRequest): Promise<AgentResponse> {
  // TODO: implement when FastAPI /agent endpoint is ready
  return post<AgentRequest, AgentResponse>("/agent", payload);
}
