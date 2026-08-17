import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/analytics", "GET");
    return NextResponse.json(data);
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
