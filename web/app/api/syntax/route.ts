import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    console.log(
      `\x1b[90m[${new Date().toLocaleTimeString()}]\x1b[0m \x1b[45m\x1b[37m SYNTAX \x1b[0m 🐍 Python AST Evaluated | Code Length: ${body.code?.length || 0} chars`
    );
    const data = await runPythonBridge("/api/syntax", "POST", body);
    return NextResponse.json(data);
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : "Failed to evaluate AST syntax";
    console.error("Syntax API Error:", errorMsg);
    return NextResponse.json({ error: errorMsg }, { status: 500 });
  }
}
