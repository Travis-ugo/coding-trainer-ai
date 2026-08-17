import ast
from typing import Dict, Any
from coding_trainer_ai.dsa_track.models import DSAProblem, WhiteboardSubmission, WhiteboardEvaluation


class WhiteboardEvaluator:
    """
    Evaluates the 5 mandatory UK Whiteboard Mode steps:
    1. Input/Output Examples
    2. Edge Cases
    3. Step-by-Step Plain English Logic
    4. Time & Space Complexity (Big-O)
    5. Code Implementation & Execution
    """

    def evaluate_submission(
        self, problem: DSAProblem, submission: WhiteboardSubmission
    ) -> WhiteboardEvaluation:
        step_scores = {}

        # Step 1: Input/Output Examples Check
        step_scores["step1_examples"] = len(submission.step1_examples.strip()) >= 5

        # Step 2: Edge Cases Check
        step_scores["step2_edge_cases"] = len(submission.step2_edge_cases.strip()) >= 5

        # Step 3: Plain-English Logic Check
        step_scores["step3_plain_logic"] = len(submission.step3_plain_logic.strip()) >= 15

        # Step 4: Big-O Complexity Check
        comp_str = submission.step4_complexity.strip().upper()
        step_scores["step4_complexity"] = ("O(" in comp_str or "O" in comp_str) and len(comp_str) >= 3

        # Step 5: Code AST Parsing & Execution Check
        cleaned_code = submission.step5_code.strip()
        code_passed = False
        execution_error = ""

        try:
            ast.parse(cleaned_code)
            ast_valid = True
        except SyntaxError as e:
            ast_valid = False
            execution_error = f"SyntaxError at line {e.lineno}: {e.msg}"

        if ast_valid and problem.test_cases:
            passed_tests = 0
            for test_case in problem.test_cases:
                sandbox = {}
                try:
                    exec(cleaned_code, sandbox)
                    func_name = test_case.get("function_name")
                    inputs = test_case.get("inputs", [])
                    expected = test_case.get("expected_output")

                    if func_name in sandbox:
                        res = sandbox[func_name](*inputs)
                        if res == expected:
                            passed_tests += 1
                        else:
                            execution_error = f"{func_name}({inputs}) returned {res}, expected {expected}"
                    else:
                        execution_error = f"Function '{func_name}' not found."
                except Exception as ex:
                    execution_error = f"Runtime Exception: {ex}"
                    break

            code_passed = (passed_tests == len(problem.test_cases))
        elif ast_valid:
            code_passed = True

        step_scores["step5_code"] = code_passed

        passed_all = all(step_scores.values())

        if passed_all:
            uk_grade = "Distinction (100% - Flawless 5-Step UK Whiteboard & Passed All Test Cases)"
            feedback = "✅ PERFECT WHITEBOARD PRESENTATION! Rigorous logic, complexity analysis, and functional code."
        elif code_passed:
            uk_grade = "Merit (Passed code test cases but incomplete whiteboard documentation)"
            feedback = f"⚠️ Code runs correctly, but review whiteboard steps: {execution_error if execution_error else 'Complete all 5 steps.'}"
        else:
            uk_grade = "Fail (Code failed test cases or contains syntax error)"
            feedback = f"❌ Execution Error: {execution_error}"

        return WhiteboardEvaluation(
            problem_id=problem.id,
            passed_all_steps=passed_all,
            step_scores=step_scores,
            code_passed=code_passed,
            feedback=feedback,
            uk_grade=uk_grade,
        )
