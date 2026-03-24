import { NextRequest, NextResponse } from "next/server";

export function middleware(req: NextRequest) {
  const requestId = crypto.randomUUID();

  const headers = new Headers(req.headers);
  headers.set("x-request-id", requestId);

  const response = NextResponse.next({ request: { headers } });
  response.headers.set("x-request-id", requestId);
  return response;
}

export const config = {
  matcher: ["/api/:path*"],
};
