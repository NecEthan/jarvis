import { NextRequest, NextResponse } from "next/server";
import { withErrorHandler, ValidationError } from "@/lib/errors";
import { logger } from "@/lib/logger";
import { playSpotifyUri } from "@/lib/spotify";
import type { SpotifyPlayRequest, SpotifyPlayResponse } from "@/types/api";

export async function POST(req: NextRequest) {
  return withErrorHandler(async () => {
    const requestId = req.headers.get("x-request-id") ?? "unknown";
    const body = (await req.json()) as Partial<SpotifyPlayRequest>;

    if (!body.spotifyUri) {
      throw new ValidationError("'spotifyUri' is required");
    }

    if (!body.spotifyUri.startsWith("spotify:track:")) {
      throw new ValidationError("'spotifyUri' must be a spotify:track URI");
    }

    logger.info("spotify play", {
      requestId,
      spotifyUri: body.spotifyUri,
      deviceId: body.deviceId,
      deviceName: body.deviceName,
    });

    const result = await playSpotifyUri({
      spotifyUri: body.spotifyUri,
      deviceId: body.deviceId,
      deviceName: body.deviceName,
    });

    const response: SpotifyPlayResponse = { ok: true, deviceId: result.deviceId };
    return NextResponse.json(response);
  });
}
