import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/analytics", "GET");
    return NextResponse.json(data);
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : "Failed to fetch analytics from Python engine";
    return NextResponse.json({ error: errorMsg }, { status: 500 });
  }
}
