import unittest
from coding_trainer_ai.python_trainer import PythonCurriculum, PracticeEngine


class TestCumulativeSpacedMemoryTrainer(unittest.TestCase):

    def setUp(self):
        self.curriculum = PythonCurriculum()
        self.engine = PracticeEngine()
        self.modules = self.curriculum.get_all_modules()

    def test_module_1_cumulative_set(self):
        # Module 1 should only contain questions from Module 1
        q_set = self.engine.build_cumulative_question_set(self.modules, 1)
        self.assertGreaterEqual(len(q_set), 2)
        for q, label in q_set:
            self.assertIn("CURRENT TOPIC", label)
            self.assertEqual(q.topic_id, "py_mod_01")

    def test_module_2_cumulative_set(self):
        # Module 2 must contain questions from Module 1 AND Module 2
        q_set = self.engine.build_cumulative_question_set(self.modules, 2)
        self.assertGreaterEqual(len(q_set), 4)

        topics_in_quiz = set(q.topic_id for q, _ in q_set)
        self.assertIn("py_mod_01", topics_in_quiz, "Cumulative quiz for Mod 2 must include Mod 1 questions!")
        self.assertIn("py_mod_02", topics_in_quiz, "Cumulative quiz for Mod 2 must include Mod 2 questions!")

        # Verify labels
        mod1_labels = [label for q, label in q_set if q.topic_id == "py_mod_01"]
        mod2_labels = [label for q, label in q_set if q.topic_id == "py_mod_02"]

        for label in mod1_labels:
            self.assertIn("CUMULATIVE RECALL", label)
        for label in mod2_labels:
            self.assertIn("CURRENT TOPIC", label)

    def test_module_5_cumulative_set(self):
        # Module 5 must contain questions from Modules 1, 2, 3, 4, and 5
        q_set = self.engine.build_cumulative_question_set(self.modules, 5)
        topics_in_quiz = set(q.topic_id for q, _ in q_set)

        for mod_num in [1, 2, 3, 4, 5]:
            expected_mod_id = f"py_mod_0{mod_num}"
            self.assertIn(expected_mod_id, topics_in_quiz, f"Module 5 cumulative set missing {expected_mod_id}")

    def test_topic_breakdown_tracking(self):
        self.engine.reset_session()
        q_set = self.engine.build_cumulative_question_set(self.modules, 2)

        for q, _ in q_set:
            self.engine.evaluate_answer(q, q.correct_answer)

        stats = self.engine.get_stats()
        self.assertEqual(stats["score"], len(q_set))
        self.assertEqual(stats["percentage"], 100.0)
        self.assertIn("py_mod_01", stats["topic_breakdown"])
        self.assertIn("py_mod_02", stats["topic_breakdown"])


if __name__ == "__main__":
    unittest.main()
