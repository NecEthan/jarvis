import { NextRequest, NextResponse } from "next/server";
import { withErrorHandler, NotImplementedError, ValidationError } from "@/lib/errors";
import { logger } from "@/lib/logger";
import type { TtsRequest } from "@/types/api";

export async function POST(req: NextRequest) {
  return withErrorHandler(async () => {
    const requestId = req.headers.get("x-request-id") ?? "unknown";
    const body = (await req.json()) as Partial<TtsRequest>;

    if (!body.text) {
      throw new ValidationError("'text' is required");
    }

    logger.info("tts request", { requestId, chars: body.text.length });

    // TODO: call TTS provider (e.g. ElevenLabs, OpenAI TTS)
    // const audioUrl = await synthesizeSpeech(body.text, body.voice);
    // return NextResponse.json({ audioUrl });

    throw new NotImplementedError("tts");
  });
}
