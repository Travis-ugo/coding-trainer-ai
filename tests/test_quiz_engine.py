import unittest
import os
import tempfile
from coding_trainer_ai.quiz_engine import (
    DynamicQuizGenerator,
    QuizManager,
    QuestionCategory,
    DynamicQuizQuestion,
)


class TestQuizEngine(unittest.TestCase):

    def setUp(self):
        self.generator = DynamicQuizGenerator()
        self.temp_dir = tempfile.mkdtemp()
        self.progress_file = os.path.join(self.temp_dir, "test_progress.json")
        self.manager = QuizManager(progress_file=self.progress_file)

    # -------------------------------------------------------------------------
    # Dynamic Quiz Generator Tests
    # -------------------------------------------------------------------------
    def test_generate_quiz_5_categories(self):
        questions = self.generator.generate_quiz_for_module("py_mod_01", seed=42)
        self.assertEqual(len(questions), 5, "Dynamic quiz should produce 5 questions across categories.")

        categories = set(q.category for q in questions)
        self.assertIn(QuestionCategory.MULTIPLE_CHOICE_THEORY, categories)
        self.assertIn(QuestionCategory.CODE_OUTPUT_PREDICTION, categories)
        self.assertIn(QuestionCategory.SYNTAX_CORRECTION, categories)
        self.assertIn(QuestionCategory.COMPLEXITY_IDENTIFICATION, categories)
        self.assertIn(QuestionCategory.CONCEPTUAL_EXPLANATION, categories)

    def test_parameter_mutation_different_seeds(self):
        q_seed1 = self.generator.generate_quiz_for_module("py_mod_01", seed=100)
        q_seed2 = self.generator.generate_quiz_for_module("py_mod_01", seed=999)

        # Code output prediction prompt or correct answer should vary with seed
        output_q1 = next(q for q in q_seed1 if q.category == QuestionCategory.CODE_OUTPUT_PREDICTION)
        output_q2 = next(q for q in q_seed2 if q.category == QuestionCategory.CODE_OUTPUT_PREDICTION)

        self.assertNotEqual(output_q1.correct_answer, output_q2.correct_answer, "Retakes with different seeds must mutate parameters!")

    # -------------------------------------------------------------------------
    # Quiz Manager Pass-Gating & Progress Persistence Tests
    # -------------------------------------------------------------------------
    def test_quiz_evaluation_distinction(self):
        questions = self.generator.generate_quiz_for_module("py_mod_01", seed=1)
        answers = [q.correct_answer for q in questions]  # All correct -> 100%

        res = self.manager.evaluate_quiz_attempt("py_mod_01", questions, answers)
        self.assertTrue(res.passed)
        self.assertTrue(res.earned_distinction)
        self.assertEqual(res.percentage, 100.0)
        self.assertIn("DISTINCTION", res.grade_label)

        # Check Module 2 unlocked
        self.assertTrue(self.manager.is_module_unlocked("py_mod_02"))
        self.assertIn("py_mod_01", self.manager.progress.distinction_badges)

    def test_quiz_evaluation_fail(self):
        questions = self.generator.generate_quiz_for_module("py_mod_01", seed=1)
        answers = ["wrong"] * len(questions)  # 0%

        res = self.manager.evaluate_quiz_attempt("py_mod_01", questions, answers)
        self.assertFalse(res.passed)
        self.assertFalse(res.earned_distinction)
        self.assertEqual(res.percentage, 0.0)

    def test_progress_persistence(self):
        # Pass module 1 in manager 1
        questions = self.generator.generate_quiz_for_module("py_mod_01", seed=1)
        answers = [q.correct_answer for q in questions]
        self.manager.evaluate_quiz_attempt("py_mod_01", questions, answers)

        # Reload manager from same state file
        manager2 = QuizManager(progress_file=self.progress_file)
        self.assertTrue(manager2.is_module_unlocked("py_mod_02"))
        self.assertIn("py_mod_01", manager2.progress.distinction_badges)


if __name__ == "__main__":
    unittest.main()
