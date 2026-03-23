import { NextRequest, NextResponse } from "next/server";

// Runs on every request matching config.matcher.
// Use for: request ID injection, auth checks, CORS headers.

export function middleware(req: NextRequest) {
  const requestId = crypto.randomUUID();

  const headers = new Headers(req.headers);
  headers.set("x-request-id", requestId);

  // TODO: add authentication for API routes
  // const { pathname } = req.nextUrl;
  // if (pathname.startsWith("/api/") && !isAuthenticated(req)) {
  //   return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  // }

  const response = NextResponse.next({ request: { headers } });
  response.headers.set("x-request-id", requestId);
  return response;
}

export const config = {
  matcher: ["/api/:path*"],
};
