import { NextResponse } from "next/server";
import type { ApiError } from "@/types/api";

export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message);
    this.name = "AppError";
  }
}

export class NotImplementedError extends AppError {
  constructor(feature: string) {
    super(`Not implemented: ${feature}`, 501, "NOT_IMPLEMENTED");
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400, "VALIDATION_ERROR");
  }
}

/** Wraps a route handler and returns a consistent JSON error on failure. */
export function withErrorHandler(
  handler: () => Promise<NextResponse>
): Promise<NextResponse> {
  return handler().catch((err) => {
    const isApp = err instanceof AppError;
    const statusCode = isApp ? err.statusCode : 500;
    const body: ApiError = {
      error: err.message ?? "Internal server error",
      code: isApp ? err.code : "INTERNAL_ERROR",
      statusCode,
    };
    return NextResponse.json(body, { status: statusCode });
  });
}
