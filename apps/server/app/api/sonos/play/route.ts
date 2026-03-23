import { NextRequest, NextResponse } from "next/server";
import { withErrorHandler, NotImplementedError, ValidationError } from "@/lib/errors";
import { logger } from "@/lib/logger";
import type { SonosPlayRequest } from "@/types/api";

export async function POST(req: NextRequest) {
  return withErrorHandler(async () => {
    const requestId = req.headers.get("x-request-id") ?? "unknown";
    const body = (await req.json()) as Partial<SonosPlayRequest>;

    if (!body.audioUrl) {
      throw new ValidationError("'audioUrl' is required");
    }

    logger.info("sonos play", { requestId, audioUrl: body.audioUrl });

    // TODO: use sonos client to play track
    // await playAudio(body.audioUrl);
    // return NextResponse.json({ ok: true });

    throw new NotImplementedError("sonos/play");
  });
}
