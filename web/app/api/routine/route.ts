import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/routine", "GET");
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({
      date_str: "2026-08-17",
      total_minutes: 15,
      tasks: [
        { title: "🎴 5 Mins: SRS Flashcards", duration_minutes: 5, task_type: "SRS_FLASHCARDS", details: "Review due cards across Python, C++ Memory, DSA, and ROS 2 decks." },
        { title: "⚡ 5 Mins: Anti-Copilot Syntax Drill", duration_minutes: 5, task_type: "ANTI_COPILOT_SYNTAX", details: "Type out raw syntax templates with zero autocomplete allowed." },
        { title: "📝 5 Mins: 1 Master's Written Exam Question", duration_minutes: 5, task_type: "UK_EXAM_QUESTION", details: "Answer 1 written exam question with Distinction Rubric feedback." },
      ],
    });
  }
}
