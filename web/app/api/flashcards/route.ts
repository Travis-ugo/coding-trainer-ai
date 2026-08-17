import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/flashcards", "GET");
    return NextResponse.json(data);
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : "Failed to fetch SRS flashcards";
    return NextResponse.json({ error: errorMsg }, { status: 500 });
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const data = await runPythonBridge("/api/flashcards/rate", "POST", body);
    return NextResponse.json(data);
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : "Failed to submit flashcard rating";
    return NextResponse.json({ error: errorMsg }, { status: 500 });
  }
}
