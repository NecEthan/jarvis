import { NextRequest, NextResponse } from "next/server";
import { withErrorHandler, NotImplementedError, ValidationError } from "@/lib/errors";
import { logger } from "@/lib/logger";
import type { SonosControlRequest, SonosCommand } from "@/types/api";

const VALID_COMMANDS: SonosCommand[] = ["pause", "resume", "next", "prev"];

export async function POST(req: NextRequest) {
  return withErrorHandler(async () => {
    const requestId = req.headers.get("x-request-id") ?? "unknown";
    const body = (await req.json()) as Partial<SonosControlRequest>;

    if (!body.command || !VALID_COMMANDS.includes(body.command)) {
      throw new ValidationError(`'command' must be one of: ${VALID_COMMANDS.join(", ")}`);
    }

    logger.info("sonos control", { requestId, command: body.command, value: body.value });

    // TODO: use sonos client to execute command
    // await executeSonosCommand(body.command, body.value);
    // return NextResponse.json({ ok: true });

    throw new NotImplementedError("sonos/control");
  });
}
