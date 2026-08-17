import unittest
from coding_trainer_ai.uk_exam_studio import (
    UKExamEngine,
    CourseworkReportGenerator,
    SocraticTutor,
    ExamSection,
)


class TestUKExamStudio(unittest.TestCase):

    def setUp(self):
        self.exam_engine = UKExamEngine()
        self.report_gen = CourseworkReportGenerator()
        self.socratic_tutor = SocraticTutor()

    # -------------------------------------------------------------------------
    # UK Exam Engine Tests
    # -------------------------------------------------------------------------
    def test_exam_paper_structure_100_marks(self):
        paper = self.exam_engine.generate_sample_exam_paper()
        self.assertEqual(paper.total_marks, 100)
        self.assertEqual(paper.time_limit_minutes, 120)

        sections = set(q.section for q in paper.questions)
        self.assertIn(ExamSection.PART_A_CONCEPTUAL, sections)
        self.assertIn(ExamSection.PART_B_TRACING, sections)
        self.assertIn(ExamSection.PART_C_ALGORITHM, sections)
        self.assertIn(ExamSection.PART_D_ESSAY, sections)

    def test_exam_submission_evaluation_distinction(self):
        paper = self.exam_engine.generate_sample_exam_paper()
        user_answers = {q.id: q.model_answer + " detailed identity, memory allocation and complexity O(N)" for q in paper.questions}

        res = self.exam_engine.evaluate_exam_submission(paper, user_answers)
        self.assertGreaterEqual(res.percentage, 70.0)
        self.assertIn("DISTINCTION", res.uk_classification)

    # -------------------------------------------------------------------------
    # Coursework Report Generator Tests
    # -------------------------------------------------------------------------
    def test_latex_template_generation(self):
        template = self.report_gen.generate_latex_template("Robotics Kinematics Evaluation")
        self.assertIn("\\documentclass", template.full_latex_code)
        self.assertIn("Robotics Kinematics Evaluation", template.full_latex_code)
        self.assertIn("1. Introduction", template.sections)

        benchmark_code = self.report_gen.get_matplotlib_benchmark_code()
        self.assertIn("import matplotlib.pyplot as plt", benchmark_code)

    # -------------------------------------------------------------------------
    # Socratic AI Tutor Tests
    # -------------------------------------------------------------------------
    def test_socratic_guidance(self):
        guidance = self.socratic_tutor.generate_socratic_guidance("How do pointers work in C++ memory?")
        self.assertIn("🏛️", guidance["non_cs_analogy"])
        self.assertIn("conceptual_hint", guidance)
        self.assertGreaterEqual(len(guidance["socratic_questions"]), 2)


if __name__ == "__main__":
    unittest.main()
