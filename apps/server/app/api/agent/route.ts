import { NextRequest, NextResponse } from "next/server";
import { withErrorHandler, NotImplementedError, ValidationError } from "@/lib/errors";
import { logger } from "@/lib/logger";
import type { AgentRequest } from "@/types/api";

export async function POST(req: NextRequest) {
  return withErrorHandler(async () => {
    const requestId = req.headers.get("x-request-id") ?? "unknown";
    const body = (await req.json()) as Partial<AgentRequest>;

    if (!body.message) {
      throw new ValidationError("'message' is required");
    }

    logger.info("agent request", { requestId, message: body.message });

    // TODO: call FastAPI LangGraph service
    // const response = await callAgent({ message: body.message, conversationId: body.conversationId });
    // return NextResponse.json(response);

    throw new NotImplementedError("agent");
  });
}
