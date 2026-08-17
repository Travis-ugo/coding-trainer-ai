import unittest
from coding_trainer_ai.syntax_drills import (
    AntiCopilotEngine,
    NoCompilerExamMode,
    DrillBank,
    DrillType,
    SyntaxDrill,
)


class TestSyntaxDrills(unittest.TestCase):

    def setUp(self):
        self.anti_copilot = AntiCopilotEngine()
        self.exam_mode = NoCompilerExamMode()
        self.bank = DrillBank()

    # -------------------------------------------------------------------------
    # Anti-Copilot Engine Tests
    # -------------------------------------------------------------------------
    def test_anti_copilot_perfect_match(self):
        drill = SyntaxDrill(
            id="d1",
            drill_type=DrillType.ANTI_COPILOT_TYPING,
            title="Test Drill",
            description="Test",
            target_syntax="x = [i for i in range(5)]",
        )

        res = self.anti_copilot.evaluate_typing_drill(drill, "x = [i for i in range(5)]")
        self.assertTrue(res.is_perfect)
        self.assertTrue(res.ast_valid)
        self.assertIn("Distinction", res.uk_grade)

    def test_anti_copilot_syntax_error(self):
        drill = SyntaxDrill(
            id="d2",
            drill_type=DrillType.ANTI_COPILOT_TYPING,
            title="Test Drill",
            description="Test",
            target_syntax="for i in range(5):\n    print(i)",
        )

        # Missing colon -> invalid AST syntax
        res = self.anti_copilot.evaluate_typing_drill(drill, "for i in range(5)\n    print(i)")
        self.assertFalse(res.is_perfect)
        self.assertFalse(res.ast_valid)
        self.assertIn("SyntaxError", res.error_message)
        self.assertIn("Fail", res.uk_grade)

    def test_anti_copilot_line_diff(self):
        drill = SyntaxDrill(
            id="d3",
            drill_type=DrillType.ANTI_COPILOT_TYPING,
            title="Test Drill",
            description="Test",
            target_syntax="val = 42",
        )

        res = self.anti_copilot.evaluate_typing_drill(drill, "val = 100")
        self.assertFalse(res.is_perfect)
        self.assertTrue(res.ast_valid)
        self.assertIn("Missing / Expected", res.diff_feedback)

    # -------------------------------------------------------------------------
    # No-Compiler Written Exam Mode Tests
    # -------------------------------------------------------------------------
    def test_no_compiler_exam_pass(self):
        drill = SyntaxDrill(
            id="d4",
            drill_type=DrillType.NO_COMPILER_EXAM,
            title="Reverse List Exam",
            description="Write reverse function",
            target_syntax="",
            test_cases=[
                {
                    "function_name": "reverse_list",
                    "inputs": [[1, 2, 3]],
                    "expected_output": [3, 2, 1],
                }
            ],
        )

        user_code = "def reverse_list(lst):\n    return lst[::-1]"
        res = self.exam_mode.evaluate_written_exam(drill, user_code)

        self.assertTrue(res.is_perfect)
        self.assertTrue(res.ast_valid)
        self.assertIn("Distinction", res.uk_grade)

    def test_no_compiler_exam_syntax_error(self):
        drill = SyntaxDrill(
            id="d5",
            drill_type=DrillType.NO_COMPILER_EXAM,
            title="Exam Drill",
            description="Write function",
            test_cases=[],
        )

        user_code = "def broken_func(\n    return 42"
        res = self.exam_mode.evaluate_written_exam(drill, user_code)

        self.assertFalse(res.is_perfect)
        self.assertFalse(res.ast_valid)
        self.assertIn("Fail", res.uk_grade)

    # -------------------------------------------------------------------------
    # Drill Bank Tests
    # -------------------------------------------------------------------------
    def test_drill_bank_types(self):
        for dtype in [
            DrillType.ANTI_COPILOT_TYPING,
            DrillType.NO_COMPILER_EXAM,
            DrillType.FILL_IN_BLANK,
            DrillType.CODE_TRACING,
        ]:
            drills = self.bank.get_drills_by_type(dtype)
            self.assertGreaterEqual(len(drills), 1, f"Missing drills for {dtype}")


if __name__ == "__main__":
    unittest.main()
