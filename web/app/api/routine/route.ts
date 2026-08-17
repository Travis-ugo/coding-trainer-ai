import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/routine", "GET");
    return NextResponse.json(data);
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : "Failed to generate daily 15-minute routine";
    return NextResponse.json({ error: errorMsg }, { status: 500 });
  }
}
