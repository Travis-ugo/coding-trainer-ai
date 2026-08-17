import unittest
import os
from coding_trainer_ai.ingestion import DocDownloader, DocParser
from coding_trainer_ai.python_trainer import (
    PythonCurriculum,
    PracticeEngine,
    QuestionType,
    PracticeQuestion,
)


class TestPythonTrainer(unittest.TestCase):

    def setUp(self):
        self.downloader = DocDownloader()
        self.parser = DocParser()
        self.curriculum = PythonCurriculum()
        self.engine = PracticeEngine()

    # -------------------------------------------------------------------------
    # Doc Ingestion Tests
    # -------------------------------------------------------------------------
    def test_doc_downloader_caching(self):
        docs = self.downloader.download_all()
        self.assertGreaterEqual(len(docs), 3)
        self.assertIn("control_flow", docs)
        self.assertIn("data_structures", docs)

    def test_doc_parser(self):
        raw_html = "<html><body><h1>Python Docs</h1><pre>def test():\n    return 42</pre></body></html>"
        result = self.parser.parse_doc(raw_html)
        self.assertIn("Python Docs", result["summary"])
        self.assertEqual(result["snippet_count"], "1")
        self.assertIn("def test()", result["first_example"])

    # -------------------------------------------------------------------------
    # Curriculum Tests
    # -------------------------------------------------------------------------
    def test_curriculum_modules_count(self):
        modules = self.curriculum.get_all_modules()
        self.assertEqual(len(modules), 9, "Should have 9 Python learning modules.")

    def test_curriculum_module_ordering_and_fields(self):
        modules = self.curriculum.get_all_modules()
        for idx, mod in enumerate(modules, 1):
            self.assertEqual(mod.order, idx)
            self.assertTrue(len(mod.title) > 0)
            self.assertTrue(len(mod.summary) > 0)
            self.assertTrue(len(mod.non_cs_analogy) > 0)
            self.assertTrue(len(mod.syntax_guide) > 0)
            self.assertTrue(len(mod.practice_questions) > 0)

    # -------------------------------------------------------------------------
    # Practice Engine Tests
    # -------------------------------------------------------------------------
    def test_practice_engine_multiple_choice_by_index(self):
        q = PracticeQuestion(
            id="test_q1",
            topic_id="py_mod_01",
            question_type=QuestionType.MULTIPLE_CHOICE,
            prompt="Choose answer",
            options=["Option A", "Option B", "Option C"],
            correct_answer="Option B",
            explanation="Explanation text",
            uk_msc_distinction_tip="Tip text",
        )

        res = self.engine.evaluate_answer(q, "2")  # Index 2 -> "Option B"
        self.assertTrue(res.is_correct)
        self.assertEqual(res.correct_answer, "Option B")

    def test_practice_engine_multiple_choice_by_text(self):
        q = PracticeQuestion(
            id="test_q2",
            topic_id="py_mod_01",
            question_type=QuestionType.MULTIPLE_CHOICE,
            prompt="Choose answer",
            options=["Option A", "Option B"],
            correct_answer="Option B",
        )

        res = self.engine.evaluate_answer(q, "option b")
        self.assertTrue(res.is_correct)

    def test_practice_engine_fill_in_blank(self):
        q = PracticeQuestion(
            id="test_q3",
            topic_id="py_mod_03",
            question_type=QuestionType.FILL_IN_BLANK,
            prompt="Fill in blank",
            correct_answer="enumerate",
        )

        res = self.engine.evaluate_answer(q, " enumerate ")
        self.assertTrue(res.is_correct)

    def test_practice_engine_incorrect_answer(self):
        q = PracticeQuestion(
            id="test_q4",
            topic_id="py_mod_02",
            question_type=QuestionType.CODE_OUTPUT,
            prompt="What is output?",
            correct_answer="5",
        )

        res = self.engine.evaluate_answer(q, "10")
        self.assertFalse(res.is_correct)

    def test_practice_engine_stats_tracking(self):
        q1 = PracticeQuestion(id="1", topic_id="m", question_type=QuestionType.FILL_IN_BLANK, prompt="P1", correct_answer="a")
        q2 = PracticeQuestion(id="2", topic_id="m", question_type=QuestionType.FILL_IN_BLANK, prompt="P2", correct_answer="b")

        engine = PracticeEngine()
        engine.evaluate_answer(q1, "a")  # Correct
        engine.evaluate_answer(q2, "wrong")  # Incorrect

        stats = engine.get_stats()
        self.assertEqual(stats["score"], 1)
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["percentage"], 50.0)


if __name__ == "__main__":
    unittest.main()
