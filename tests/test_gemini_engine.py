import unittest
import os
import tempfile
from coding_trainer_ai.ai_engine import GeminiAIEngine, AIConfig


class TestGeminiEngine(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_ai_config.json")
        self.ai_engine = GeminiAIEngine(config_file=self.config_file)
        # Ensure tests run in deterministic offline mode
        self.ai_engine.config.is_active = False

    def test_api_key_configuration(self):
        self.ai_engine.config.api_key = "test_api_key_12345"
        self.assertEqual(self.ai_engine.config.api_key, "test_api_key_12345")

    def test_socratic_guidance_fallback(self):
        res = self.ai_engine.generate_socratic_guidance("How do pointers work?")
        self.assertIn("analogy", res.non_cs_analogy.lower())
        self.assertGreaterEqual(len(res.socratic_questions), 2)

    def test_uk_exam_essay_evaluation_fallback(self):
        res = self.ai_engine.evaluate_uk_exam_essay("Explain Kalman Filters", "Kalman filters compute Gaussian state estimates.", max_marks=20)
        self.assertEqual(res.max_marks, 20)
        self.assertIn("DISTINCTION", res.uk_grade)


if __name__ == "__main__":
    unittest.main()
