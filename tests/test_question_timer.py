import unittest
import time
from coding_trainer_ai.quiz_engine.question_timer import QuestionTimer


class TestQuestionTimer(unittest.TestCase):

    def test_timer_measurement(self):
        start_t = QuestionTimer.start_timer()
        time.sleep(0.05)
        elapsed = QuestionTimer.stop_timer(start_t)
        self.assertGreaterEqual(elapsed, 0.04)

    def test_format_duration(self):
        self.assertEqual(QuestionTimer.format_duration(45.2), "45.2s")
        self.assertEqual(QuestionTimer.format_duration(135.0), "2 mins 15 secs")

    def test_uk_pacing_ratings(self):
        rating_dist, _ = QuestionTimer.get_uk_pacing_rating(45.0)
        self.assertIn("DISTINCTION PACE", rating_dist)

        rating_merit, _ = QuestionTimer.get_uk_pacing_rating(90.0)
        self.assertIn("MERIT PACE", rating_merit)

        rating_slow, _ = QuestionTimer.get_uk_pacing_rating(150.0)
        self.assertIn("OVER-TIME PACING WARNING", rating_slow)


if __name__ == "__main__":
    unittest.main()
