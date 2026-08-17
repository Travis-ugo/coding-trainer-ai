import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const data = await runPythonBridge("/api/ai", "POST", body);
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({
      analogy: "Think of this concept like an archival call slip mapping to a physical document in a vault.",
      conceptual_hint: "Differentiate between initial state and transformed state.",
      socratic_question: "What happens if your input collection is empty?",
    });
  }
}
