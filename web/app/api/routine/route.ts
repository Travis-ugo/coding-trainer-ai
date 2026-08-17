import { NextResponse } from "next/server";
import { execSync } from "child_process";

export async function GET() {
  try {
    const output = execSync(
      `python3 -c "
from coding_trainer_ai.analytics_studio import DailyRoutineGenerator
import json
gen = DailyRoutineGenerator()
routine = gen.generate_daily_routine()
res = {
    'date_str': routine.date_str,
    'total_minutes': routine.total_minutes,
    'tasks': [{'title': t.title, 'duration_minutes': t.duration_minutes, 'task_type': t.task_type, 'details': t.details} for t in routine.tasks]
}
print(json.dumps(res))
"`,
      { cwd: "/Users/travis/Software/coding-trainer-ai" }
    ).toString();

    return NextResponse.json(JSON.parse(output));
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
