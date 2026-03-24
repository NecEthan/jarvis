import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const target = new URL("/api/spotify/callback", req.nextUrl.origin);
  req.nextUrl.searchParams.forEach((value, key) => {
    target.searchParams.set(key, value);
  });
  return NextResponse.redirect(target);
}
