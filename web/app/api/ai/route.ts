import { NextResponse } from "next/server";
import { execSync } from "child_process";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const prompt = (body.prompt || "").replace(/"/g, '\\"');

    const output = execSync(
      `python3 -c "
from coding_trainer_ai.ai_engine import GeminiAIEngine
import json
engine = GeminiAIEngine()
res = engine.ask_socratic_guidance('''${prompt}''')
print(json.dumps({'analogy': res.analogy, 'conceptual_hint': res.conceptual_hint, 'socratic_question': res.socratic_question}))
"`,
      { cwd: "/Users/travis/Software/coding-trainer-ai" }
    ).toString();

    return NextResponse.json(JSON.parse(output));
  } catch {
    return NextResponse.json({
      analogy: "Think of this concept like an archival call slip mapping to a physical document in a vault.",
      conceptual_hint: "Differentiate between initial state and transformed state.",
      socratic_question: "What happens if your input collection is empty?",
    });
  }
}
