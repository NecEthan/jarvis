import { NextRequest, NextResponse } from "next/server";
import { withErrorHandler, AppError, ValidationError } from "@/lib/errors";
import { exchangeSpotifyCode } from "@/lib/spotify";

export async function GET(req: NextRequest) {
  return withErrorHandler(async () => {
    const code = req.nextUrl.searchParams.get("code");
    const error = req.nextUrl.searchParams.get("error");

    if (error) {
      throw new AppError(`Spotify auth failed: ${error}`, 400, "SPOTIFY_AUTH_FAILED");
    }

    if (!code) {
      throw new ValidationError("Missing authorization code in callback URL");
    }

    const data = await exchangeSpotifyCode(code);

    return NextResponse.json({
      ok: true,
      message:
        "Save refresh_token as SPOTIFY_REFRESH_TOKEN in apps/server/.env and restart server.",
      refreshToken: data.refresh_token ?? null,
      accessToken: data.access_token ?? null,
      expiresIn: data.expires_in ?? null,
      tokenType: data.token_type ?? null,
    });
  });
}
