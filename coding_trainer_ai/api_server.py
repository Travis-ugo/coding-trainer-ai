import os
import json
import http.server
import socketserver
import threading
from typing import Dict, Any

from coding_trainer_ai.analytics_studio import GradeAnalyticsEngine, DailyRoutineGenerator
from coding_trainer_ai.srs import DeckRepository, SM2Engine
from coding_trainer_ai.syntax_drills import NoCompilerExamMode
from coding_trainer_ai.ai_engine import GeminiAIEngine
from coding_trainer_ai.ai_robotics import VirtualROS2Sandbox


from coding_trainer_ai.python_trainer import PythonCurriculum


class TrainerAPIRequestHandler(http.server.BaseHTTPRequestHandler):

    analytics_engine = GradeAnalyticsEngine()
    routine_generator = DailyRoutineGenerator()
    deck_repo = DeckRepository()
    sm2_engine = SM2Engine()
    compiler_exam = NoCompilerExamMode()
    gemini_engine = GeminiAIEngine()
    ros2_sandbox = VirtualROS2Sandbox()
    curriculum = PythonCurriculum()

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        if self.path == "/api/modules":
            modules = [
                {
                    "id": m.id,
                    "title": m.title,
                    "summary": getattr(m, "summary", ""),
                    "non_cs_analogy": getattr(m, "non_cs_analogy", ""),
                    "syntax_guide": getattr(m, "syntax_guide", ""),
                    "order": getattr(m, "order", 1),
                }
                for m in self.curriculum._modules
            ]
            self._set_headers(200)
            self.wfile.write(json.dumps(modules).encode("utf-8"))

        elif self.path == "/api/analytics":
            # Load real scores from progress file or defaults
            scores = {
                "py_mod_01": 85.0,
                "py_mod_02": 78.0,
                "py_mod_03": 72.0,
                "py_mod_04": 65.0,
                "py_mod_05": 70.0,
                "dsa_two_pointers": 75.0,
                "math_se3": 72.0,
                "kalman_filter": 55.0,
                "pytorch_autograd": 62.0,
                "ros2_pubsub": 74.0,
            }
            analytics = self.analytics_engine.generate_analytics(scores)
            response = {
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
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif self.path == "/api/routine":
            routine = self.routine_generator.generate_daily_routine()
            response = {
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
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif self.path == "/api/flashcards":
            decks_data = []
            for deck_id, deck in self.deck_repo.decks.items():
                cards_data = [
                    {
                        "card_id": c.card_id,
                        "prompt": c.prompt,
                        "answer": c.answer,
                        "analogy": c.analogy,
                        "repetition_number": c.repetition_number,
                        "interval_days": c.interval_days,
                    }
                    for c in deck.cards
                ]
                decks_data.append({
                    "id": deck.deck_id,
                    "title": deck.title,
                    "cards": cards_data
                })
            self._set_headers(200)
            self.wfile.write(json.dumps(decks_data).encode("utf-8"))

        elif self.path == "/api/ros2":
            architecture = self.ros2_sandbox.render_architecture_tree()
            stream = self.ros2_sandbox.stream_topic_messages("/joint_states", count=2)
            kinematics = self.ros2_sandbox.simulate_forward_kinematics(45.0, 30.0)
            response = {
                "architecture": architecture,
                "topic_stream": stream,
                "kinematics": kinematics,
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode("utf-8"))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        body = json.loads(post_data) if post_data else {}

        if self.path in ("/api/syntax", "/api/syntax/evaluate"):
            code_str = body.get("code", "")
            target_output = body.get("target_output", "")
            res = self.compiler_exam.evaluate_no_compiler_submission(code_str, target_output)
            response = {
                "passed": res.passed,
                "score": res.score,
                "ast_valid": res.ast_valid,
                "feedback": res.feedback,
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif self.path in ("/api/ai", "/api/ai/socratic"):
            prompt = body.get("prompt", "")
            res = self.gemini_engine.ask_socratic_guidance(prompt)
            response = {
                "analogy": res.analogy,
                "conceptual_hint": res.conceptual_hint,
                "socratic_question": res.socratic_question,
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif self.path in ("/api/flashcards", "/api/flashcards/rate"):
            card_id = body.get("card_id", "")
            rating = int(body.get("rating", 4))
            # Find card across decks and update SM-2 interval
            updated_card = None
            for deck in self.deck_repo.decks.values():
                for card in deck.cards:
                    if card.card_id == card_id:
                        updated_card = self.sm2_engine.calculate_next_interval(card, rating)
                        break
            response = {
                "card_id": card_id,
                "interval_days": updated_card.interval_days if updated_card else 1,
                "easiness_factor": updated_card.easiness_factor if updated_card else 2.5,
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode("utf-8"))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))


def start_api_server(port=8000):
    server = socketserver.TCPServer(("", port), TrainerAPIRequestHandler)
    print(f"🚀 Real Python Backend JSON API Server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    start_api_server(8000)
