import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/ros2", "GET");
    return NextResponse.json(data);
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : "Failed to fetch ROS 2 virtual sandbox state";
    return NextResponse.json({ error: errorMsg }, { status: 500 });
  }
}
