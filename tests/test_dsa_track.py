import unittest
from coding_trainer_ai.dsa_track import (
    DSARepository,
    WhiteboardEvaluator,
    WhiteboardSubmission,
    DSAPattern,
)


class TestDSATrack(unittest.TestCase):

    def setUp(self):
        self.repo = DSARepository()
        self.evaluator = WhiteboardEvaluator()

    def test_repository_problems_exist(self):
        problems = self.repo.get_all_problems()
        self.assertGreaterEqual(len(problems), 3)

    def test_repository_pattern_filter(self):
        tp_problems = self.repo.get_problems_by_pattern(DSAPattern.TWO_POINTERS)
        self.assertGreaterEqual(len(tp_problems), 1)
        self.assertEqual(tp_problems[0].pattern, DSAPattern.TWO_POINTERS)

    def test_whiteboard_perfect_submission(self):
        problem = self.repo.get_problem_by_id("dsa_two_pointers_01")
        self.assertIsNotNone(problem)

        submission = WhiteboardSubmission(
            problem_id=problem.id,
            step1_examples="Input: [2, 7, 11, 15], 9 -> Output: [1, 2]",
            step2_edge_cases="Array length 2, negative values",
            step3_plain_logic="Initialize left and right pointers. Sum numbers. Adjust left or right.",
            step4_complexity="Time Complexity: O(N), Space Complexity: O(1)",
            step5_code=problem.solution_code,
        )

        res = self.evaluator.evaluate_submission(problem, submission)
        self.assertTrue(res.passed_all_steps)
        self.assertTrue(res.code_passed)
        self.assertIn("Distinction", res.uk_grade)

    def test_whiteboard_incomplete_documentation(self):
        problem = self.repo.get_problem_by_id("dsa_two_pointers_01")
        submission = WhiteboardSubmission(
            problem_id=problem.id,
            step1_examples="",  # Incomplete!
            step2_edge_cases="",
            step3_plain_logic="",
            step4_complexity="",
            step5_code=problem.solution_code,
        )

        res = self.evaluator.evaluate_submission(problem, submission)
        self.assertFalse(res.passed_all_steps)
        self.assertTrue(res.code_passed)  # Code passed test cases, but steps failed!
        self.assertIn("Merit", res.uk_grade)


if __name__ == "__main__":
    unittest.main()
