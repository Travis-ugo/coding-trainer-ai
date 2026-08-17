import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const data = await runPythonBridge("/api/ai", "POST", body);
    return NextResponse.json(data);
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : "Failed to execute AI tutor bridge";
    return NextResponse.json({ error: errorMsg }, { status: 500 });
  }
}
