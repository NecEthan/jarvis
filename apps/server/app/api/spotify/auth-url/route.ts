import { NextResponse } from "next/server";
import { withErrorHandler } from "@/lib/errors";
import { getSpotifyAuthUrl } from "@/lib/spotify";

export async function GET() {
  return withErrorHandler(async () => {
    return NextResponse.json({
      ok: true,
      authUrl: getSpotifyAuthUrl(),
    });
  });
}
