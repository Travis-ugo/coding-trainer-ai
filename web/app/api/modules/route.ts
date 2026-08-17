import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/modules", "GET");
    return NextResponse.json(data);
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : "Failed to fetch curriculum modules";
    return NextResponse.json({ error: errorMsg }, { status: 500 });
  }
}
