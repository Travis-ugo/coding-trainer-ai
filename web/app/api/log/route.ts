import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { category = "INFO", level = "INFO", message = "", details = null, userEmail = "Anonymous", sessionId = "N/A" } = body;

    const timeStr = new Date().toLocaleTimeString();

    // ANSI Color codes for mac/zsh terminal output
    const colors = {
      reset: "\x1b[0m",
      bright: "\x1b[1m",
      dim: "\x1b[2m",
      blue: "\x1b[34m",
      green: "\x1b[32m",
      yellow: "\x1b[33m",
      magenta: "\x1b[35m",
      cyan: "\x1b[36m",
      red: "\x1b[31m",
      bgBlue: "\x1b[44m\x1b[37m",
      bgGreen: "\x1b[42m\x1b[30m",
      bgYellow: "\x1b[43m\x1b[30m",
      bgMagenta: "\x1b[45m\x1b[37m",
    };

    let categoryBadge = `${colors.cyan}[SYSTEM]${colors.reset}`;
    let icon = "ℹ️";

    if (level === "SUCCESS") icon = "🔑";
    else if (level === "WARN") icon = "⚠️";
    else if (level === "ERROR") icon = "❌";
    else icon = "ℹ️";

    if (category === "AUTH") {
      categoryBadge = level === "ERROR" ? `${colors.red} AUTH ${colors.reset}` : `${colors.bgBlue} AUTH ${colors.reset}`;
    } else if (category === "SESSION") {
      categoryBadge = `${colors.bgGreen} SESSION ${colors.reset}`;
    } else if (category === "NAVIGATION") {
      categoryBadge = `${colors.magenta}[NAV]${colors.reset}`;
    } else if (category === "SYNTAX") {
      categoryBadge = `${colors.bgMagenta} SYNTAX ${colors.reset}`;
    } else if (category === "API") {
      categoryBadge = `${colors.bgYellow} API ${colors.reset}`;
    }

    const detailsStr = details ? ` | ${typeof details === "object" ? JSON.stringify(details) : details}` : "";

    // Print directly to terminal stdout!
    console.log(
      `\x1b[90m[${timeStr}]\x1b[0m ${categoryBadge} ${icon} \x1b[1m${message}\x1b[0m \x1b[90m(User: ${userEmail} | Session: ${sessionId})\x1b[0m${detailsStr}`
    );

    return NextResponse.json({ success: true });
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : "Logging error";
    console.error("Terminal logger API error:", errorMsg);
    return NextResponse.json({ error: errorMsg }, { status: 500 });
  }
}
