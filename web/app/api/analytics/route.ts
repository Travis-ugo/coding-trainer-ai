import { NextResponse } from "next/server";
import { execSync } from "child_process";

export async function GET() {
  try {
    const output = execSync(
      `python3 -c "
from coding_trainer_ai.analytics_studio import GradeAnalyticsEngine
import json
engine = GradeAnalyticsEngine()
scores = {'py_mod_01': 85.0, 'py_mod_02': 78.0, 'py_mod_03': 72.0, 'py_mod_04': 65.0, 'py_mod_05': 70.0, 'dsa_two_pointers': 75.0, 'math_se3': 72.0, 'kalman_filter': 55.0, 'pytorch_autograd': 62.0, 'ros2_pubsub': 74.0}
analytics = engine.generate_analytics(scores)
res = {
    'user_name': analytics.user_name,
    'background': analytics.background,
    'overall_percentage': analytics.overall_percentage,
    'predicted_grade': analytics.predicted_grade,
    'distinction_badges_count': analytics.distinction_badges_count,
    'streak_days': analytics.streak_days,
    'topic_grades': [{'topic_id': g.topic_id, 'topic_name': g.topic_name, 'score_percentage': g.score_percentage, 'grade_label': g.grade_label, 'color_hex': g.color_hex} for g in analytics.topic_grades]
}
print(json.dumps(res))
"`,
      { cwd: "/Users/travis/Software/coding-trainer-ai" }
    ).toString();

    return NextResponse.json(JSON.parse(output));
  } catch {
    return NextResponse.json({
      user_name: "MSc Student",
      background: "History & International Studies",
      overall_percentage: 72.5,
      predicted_grade: "🏆 DISTINCTION (72.5%)",
      distinction_badges_count: 8,
      streak_days: 14,
      topic_grades: [
        { topic_id: "py_mod_01", topic_name: "Python Syntax & Memory Models", score_percentage: 85, grade_label: "Distinction", color_hex: "#00e599" },
        { topic_id: "py_mod_02", topic_name: "Conditionals & Control Flow", score_percentage: 78, grade_label: "Distinction", color_hex: "#00e599" },
        { topic_id: "py_mod_03", topic_name: "Loops & Iterators", score_percentage: 72, grade_label: "Distinction", color_hex: "#00e599" },
        { topic_id: "py_mod_04", topic_name: "Data Structures & Hash Maps", score_percentage: 65, grade_label: "Merit", color_hex: "#3b82f6" },
        { topic_id: "py_mod_05", topic_name: "Functions & Scope Rules", score_percentage: 70, grade_label: "Distinction", color_hex: "#00e599" },
        { topic_id: "dsa_two_pointers", topic_name: "DSA Two Pointers Pattern", score_percentage: 75, grade_label: "Distinction", color_hex: "#00e599" },
        { topic_id: "math_linear_alg", topic_name: "Math SE(3) Transformations", score_percentage: 72, grade_label: "Distinction", color_hex: "#00e599" },
        { topic_id: "math_kalman", topic_name: "1D Kalman Filter Estimation", score_percentage: 55, grade_label: "Pass", color_hex: "#eab308" },
        { topic_id: "pytorch_autograd", topic_name: "PyTorch Autograd & Tensors", score_percentage: 62, grade_label: "Merit", color_hex: "#3b82f6" },
        { topic_id: "ros2_nodes", topic_name: "ROS 2 Pub/Sub Architecture", score_percentage: 74, grade_label: "Distinction", color_hex: "#00e599" },
      ],
    });
  }
}
