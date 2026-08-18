from typing import List, Dict, Any
from coding_trainer_ai.analytics_studio.models import TopicGrade, StudentAnalytics


class GradeAnalyticsEngine:
    """
    Aggregates student topic scores, predicts overall UK Postgraduate degree classification,
    and generates visual grade heatmap analytics.
    """

    def generate_analytics(
        self,
        scores_by_topic: Dict[str, float],
        user_name: str = "MSc Student",
        background: str = "History & International Studies",
        selected_track: str = "MSc AI & Robotics",
    ) -> StudentAnalytics:
        default_topics = {
            "py_mod_01": ("Python Syntax & Memory Models", 0.0),
            "py_mod_02": ("Conditionals & Control Flow", 0.0),
            "py_mod_03": ("Loops & Iterators", 0.0),
            "py_mod_04": ("Data Structures & Hash Maps", 0.0),
            "py_mod_05": ("Functions & Scope Rules", 0.0),
            "dsa_two_pointers": ("DSA Two Pointers Pattern", 0.0),
            "dsa_bfs_graphs": ("DSA BFS & Graph Traversal", 0.0),
            "math_linear_alg": ("Math SE(3) Transformations", 0.0),
            "math_kalman": ("1D Kalman Filter Estimation", 0.0),
            "pytorch_autograd": ("PyTorch Autograd & Tensors", 0.0),
            "ros2_nodes": ("ROS 2 Pub/Sub Architecture", 0.0),
            "uk_written_exam": ("UK Written Exam Essay Mode", 0.0),
        }

        merged_scores = {}
        for t_id, (t_name, def_sc) in default_topics.items():
            sc = scores_by_topic.get(t_id, def_sc)
            merged_scores[t_id] = (t_name, float(sc))

        topic_grades = []
        attempted_scores = []
        distinction_count = 0

        for t_id, (t_name, pct) in merged_scores.items():
            if pct > 0.0:
                attempted_scores.append(pct)

            if pct >= 70.0:
                label = "Distinction"
                color = "#22c55e"  # Green
                distinction_count += 1
            elif pct >= 60.0:
                label = "Merit"
                color = "#3b82f6"  # Blue
            elif pct >= 50.0:
                label = "Pass"
                color = "#eab308"  # Yellow
            elif pct > 0.0:
                label = "Fail"
                color = "#ef4444"  # Red
            else:
                label = "Unattempted"
                color = "#666666"  # Neutral Gray

            topic_grades.append(
                TopicGrade(
                    topic_id=t_id,
                    topic_name=t_name,
                    score_percentage=round(pct, 1),
                    grade_label=label,
                    color_hex=color,
                )
            )

        # Compute overall percentage from attempted scores if available
        if attempted_scores:
            overall_pct = sum(attempted_scores) / len(attempted_scores)
        else:
            overall_pct = 0.0

        if overall_pct >= 70.0:
            pred_grade = f"🏆 DISTINCTION ({overall_pct:.1f}%)"
        elif overall_pct >= 60.0:
            pred_grade = f"📜 MERIT ({overall_pct:.1f}%)"
        elif overall_pct >= 50.0:
            pred_grade = f"✅ PASS ({overall_pct:.1f}%)"
        elif overall_pct > 0.0:
            pred_grade = f"❌ FAIL ({overall_pct:.1f}%)"
        else:
            pred_grade = "🆕 NOT EVALUATED YET (0.0%)"

        return StudentAnalytics(
            user_name=user_name,
            background=background,
            selected_track=selected_track,
            overall_percentage=round(overall_pct, 1),
            predicted_grade=pred_grade,
            distinction_badges_count=distinction_count,
            streak_days=1,
            topic_grades=topic_grades,
        )

    def render_ascii_heatmap(self, analytics: StudentAnalytics) -> str:
        lines = []
        lines.append("=" * 68)
        lines.append(f" 📊 UK MSC PREDICTED GRADE HEATMAP & READINESS DASHBOARD")
        lines.append(f" Candidate: {analytics.user_name} | Background: {analytics.background}")
        lines.append(f" Selected Track: {analytics.selected_track}")
        lines.append(f" Predicted Degree Result: {analytics.predicted_grade}")
        lines.append(f" Distinction Badges: {analytics.distinction_badges_count} | Daily Streak: {analytics.streak_days} Days")
        lines.append("=" * 68)
        lines.append(" TOPIC-BY-TOPIC READINESS HEATMAP:")
        lines.append("-" * 68)

        for tg in analytics.topic_grades:
            badge = "🏆" if tg.grade_label == "Distinction" else ("📜" if tg.grade_label == "Merit" else ("✅" if tg.grade_label == "Pass" else "❌"))
            bar_len = int(tg.score_percentage / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            lines.append(f" {badge} [{bar}] {tg.score_percentage:5.1f}% | {tg.topic_name:<32} ({tg.grade_label})")

        lines.append("=" * 68)
        return "\n".join(lines)
