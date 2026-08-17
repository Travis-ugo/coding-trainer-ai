import unittest
import os
import tempfile
from coding_trainer_ai.analytics_studio import (
    GradeAnalyticsEngine,
    DailyRoutineGenerator,
    WebStudioServer,
)


class TestAnalyticsStudio(unittest.TestCase):

    def setUp(self):
        self.analytics_engine = GradeAnalyticsEngine()
        self.routine_gen = DailyRoutineGenerator()
        self.web_studio = WebStudioServer()
        self.temp_dir = tempfile.mkdtemp()

    # -------------------------------------------------------------------------
    # Grade Analytics Engine Tests
    # -------------------------------------------------------------------------
    def test_grade_analytics_distinction(self):
        scores = {"py_mod_01": 90.0, "py_mod_02": 85.0, "dsa_two_pointers": 75.0}
        analytics = self.analytics_engine.generate_analytics(scores)

        self.assertIn("DISTINCTION", analytics.predicted_grade)
        self.assertGreaterEqual(analytics.overall_percentage, 70.0)
        self.assertGreaterEqual(analytics.distinction_badges_count, 1)

        heatmap_ascii = self.analytics_engine.render_ascii_heatmap(analytics)
        self.assertIn("READINESS DASHBOARD", heatmap_ascii)

    # -------------------------------------------------------------------------
    # Daily Routine Generator Tests
    # -------------------------------------------------------------------------
    def test_daily_routine_generation(self):
        routine = self.routine_gen.generate_daily_routine()
        self.assertEqual(routine.total_minutes, 15)
        self.assertEqual(len(routine.tasks), 3)

        task_types = [t.task_type for t in routine.tasks]
        self.assertIn("SRS_FLASHCARDS", task_types)
        self.assertIn("ANTI_COPILOT_SYNTAX", task_types)
        self.assertIn("UK_EXAM_QUESTION", task_types)

    # -------------------------------------------------------------------------
    # Web Studio Dashboard Tests
    # -------------------------------------------------------------------------
    def test_web_studio_html_generation(self):
        analytics = self.analytics_engine.generate_analytics({})
        routine = self.routine_gen.generate_daily_routine()

        html = self.web_studio.generate_html_dashboard(analytics, routine)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Coding Trainer AI", html)
        self.assertIn("UK MSc Predicted Grade Heatmap", html)

        out_file = os.path.join(self.temp_dir, "test_web_studio.html")
        saved_path = self.web_studio.export_html_file(analytics, routine, out_file)
        self.assertTrue(os.path.exists(saved_path))


if __name__ == "__main__":
    unittest.main()
