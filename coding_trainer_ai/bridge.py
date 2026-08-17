import sys
import json
import ast
from typing import Dict, Any

from coding_trainer_ai.analytics_studio import GradeAnalyticsEngine, DailyRoutineGenerator
from coding_trainer_ai.srs import DeckRepository, SM2Engine
from coding_trainer_ai.syntax_drills import NoCompilerExamMode, SyntaxDrill, DrillType
from coding_trainer_ai.ai_engine import GeminiAIEngine
from coding_trainer_ai.ai_robotics import VirtualROS2Sandbox
from coding_trainer_ai.python_trainer import PythonCurriculum


def handle_bridge_request(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = endpoint.strip().lstrip("/")

    if endpoint == "modules":
        curr = PythonCurriculum()
        modules = curr._modules if hasattr(curr, "_modules") else []
        return [
            {
                "id": m.id,
                "title": m.title,
                "summary": getattr(m, "summary", ""),
                "non_cs_analogy": getattr(m, "non_cs_analogy", ""),
                "syntax_guide": getattr(m, "syntax_guide", ""),
                "order": getattr(m, "order", 1),
            }
            for m in modules
        ]  # type: ignore

    elif endpoint == "analytics":
        engine = GradeAnalyticsEngine()
        from coding_trainer_ai.progress import load_user_progress
        prog = load_user_progress()
        scores = payload.get("scores", prog.get("scores", {}))
        user_name = payload.get("user_name", prog.get("user_name", "Student"))
        background = payload.get("background", prog.get("background", "Non-CS Candidate"))
        analytics = engine.generate_analytics(scores, user_name=user_name, background=background)
        return {
            "user_name": analytics.user_name,
            "background": analytics.background,
            "overall_percentage": analytics.overall_percentage,
            "predicted_grade": analytics.predicted_grade,
            "distinction_badges_count": analytics.distinction_badges_count,
            "streak_days": analytics.streak_days,
            "topic_grades": [
                {
                    "topic_id": g.topic_id,
                    "topic_name": g.topic_name,
                    "score_percentage": g.score_percentage,
                    "grade_label": g.grade_label,
                    "color_hex": g.color_hex,
                }
                for g in analytics.topic_grades
            ],
        }

    elif endpoint == "routine":
        gen = DailyRoutineGenerator()
        routine = gen.generate_daily_routine()
        return {
            "date_str": routine.date_str,
            "total_minutes": routine.total_minutes,
            "tasks": [
                {
                    "title": t.title,
                    "duration_minutes": t.duration_minutes,
                    "task_type": t.task_type,
                    "details": t.details,
                }
                for t in routine.tasks
            ],
        }

    elif endpoint in ("flashcards", "flashcards/get"):
        repo = DeckRepository()
        decks = repo.get_all_decks()
        decks_data = []
        for deck in decks:
            cards_data = [
                {
                    "card_id": getattr(c, "id", f"c_{idx}"),
                    "prompt": c.prompt if hasattr(c, "prompt") else c.front,
                    "answer": c.answer if hasattr(c, "answer") else c.back,
                    "analogy": getattr(c, "analogy", ""),
                    "repetition_number": getattr(c, "repetitions", 1),
                    "interval_days": getattr(c, "interval_days", 1),
                }
                for idx, c in enumerate(deck.cards)
            ]
            decks_data.append({
                "id": getattr(deck, "id", "deck"),
                "title": getattr(deck, "name", getattr(deck, "title", "Deck")),
                "cards": cards_data
            })
        return decks_data  # type: ignore

    elif endpoint in ("flashcards/rate", "flashcards_rate"):
        repo = DeckRepository()
        sm2 = SM2Engine()
        card_id = payload.get("card_id", "")
        rating = int(payload.get("rating", 4))
        updated_card = None
        for deck in repo.get_all_decks():
            for card in deck.cards:
                if card.id == card_id:
                    updated_card = sm2.process_review(card, rating)
                    break
        return {
            "card_id": card_id,
            "interval_days": updated_card.interval_days if updated_card else 1,
            "easiness_factor": getattr(updated_card, "ease_factor", 2.5) if updated_card else 2.5,
        }

    elif endpoint == "syntax":
        exam = NoCompilerExamMode()
        code_str = payload.get("code", "")
        target_output = payload.get("target_output", "")
        drill = SyntaxDrill(
            id="bridge_drill",
            drill_type=DrillType.NO_COMPILER_EXAM,
            title="Syntax Gym",
            description="Evaluate code AST",
            target_syntax=target_output,
        )
        res = exam.evaluate_written_exam(drill, code_str)
        return {
            "passed": res.is_perfect or res.ast_valid,
            "score": 100 if res.is_perfect else (75 if res.ast_valid else 0),
            "ast_valid": res.ast_valid,
            "feedback": res.uk_grade + (" - " + res.diff_feedback if res.diff_feedback else ""),
        }

    elif endpoint == "ai":
        engine = GeminiAIEngine()

        # Offline deterministic mode if no API key set
        if hasattr(engine, "config"):
            engine.config.is_active = False

        prompt = payload.get("prompt", "")
        res = engine.generate_socratic_guidance(prompt)
        first_q = res.socratic_questions[0] if res.socratic_questions else "What happens if inputs are invalid?"
        return {
            "analogy": res.non_cs_analogy,
            "conceptual_hint": res.conceptual_hint,
            "socratic_question": first_q,
        }

    elif endpoint == "ros2":
        sandbox = VirtualROS2Sandbox()
        arch = (
            "Active Nodes:\n"
            "  • [/camera_driver_node] -> Publishes: [/image_raw]\n"
            "  • [/joint_state_broadcaster] -> Publishes: [/joint_states]\n"
            "  • [/motion_controller_node] -> Subscribes: [/joint_states]"
        )
        msg = sandbox.publish_message("/joint_states", "sensor_msgs/JointState", {"position": [0.785, 0.523]})
        echoed = sandbox.echo_topic("/joint_states")
        stream = [{"topic": m.topic_name, "data": m.data} for m in echoed] if echoed else [{"topic": "/joint_states", "data": {"position": [0.785, 0.523]}}]
        fk = sandbox.forward_kinematics_2dof(1.0, 1.0, 0.785, 0.523)
        return {
            "architecture": arch,
            "topic_stream": stream,
            "kinematics": fk,
        }

    else:
        raise ValueError(f"Unknown endpoint: {endpoint}")


def main():
    endpoint = sys.argv[1] if len(sys.argv) > 1 else "analytics"
    input_data = sys.stdin.read().strip()
    payload = json.loads(input_data) if input_data else {}
    result = handle_bridge_request(endpoint, payload)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
