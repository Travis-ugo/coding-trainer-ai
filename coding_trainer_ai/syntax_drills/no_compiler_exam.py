import ast
import traceback
from typing import Dict, Any, List
from coding_trainer_ai.syntax_drills.models import SyntaxDrill, DrillResult


class NoCompilerExamMode:
    """
    Simulates UK university written exam conditions: no IDE squiggles, no autocompletion.
    Evaluates submitted code for AST validity and functional correctness against hidden test cases.
    """

    def evaluate_written_exam(
        self, drill: SyntaxDrill, user_code: str
    ) -> DrillResult:
        cleaned_user = user_code.strip()

        # Step 1: AST Parsing Check
        try:
            parsed_ast = ast.parse(cleaned_user)
            ast_valid = True
            ast_error = ""
        except SyntaxError as e:
            ast_valid = False
            ast_error = f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}"
            return DrillResult(
                drill_id=drill.id,
                is_perfect=False,
                user_code=cleaned_user,
                target_syntax=drill.target_syntax,
                diff_feedback=f"❌ Written exam submission contains a syntax error: {ast_error}",
                ast_valid=False,
                error_message=ast_error,
                uk_grade="Fail (0% - SyntaxError on Written Exam Paper)",
            )

        # Step 2: Functional Test Case Execution in Sandbox
        passed_tests = 0
        total_tests = len(drill.test_cases)
        execution_error = ""

        if total_tests > 0:
            for test_case in drill.test_cases:
                sandbox_globals = {}
                try:
                    exec(cleaned_user, sandbox_globals)
                    func_name = test_case.get("function_name")
                    inputs = test_case.get("inputs", [])
                    expected_output = test_case.get("expected_output")

                    if func_name in sandbox_globals:
                        result = sandbox_globals[func_name](*inputs)
                        if result == expected_output:
                            passed_tests += 1
                        else:
                            execution_error = (
                                f"Test case failed: {func_name}({inputs}) returned {result}, expected {expected_output}"
                            )
                    else:
                        execution_error = f"Function '{func_name}' not found in submitted code."
                except Exception as ex:
                    execution_error = f"Runtime Exception during exam test execution: {ex}"
                    break

        is_perfect = (ast_valid and (passed_tests == total_tests if total_tests > 0 else True))

        if is_perfect:
            uk_grade = "Distinction (100% - Flawless Code & Pass All Test Cases)"
            diff_feedback = "✅ PERFECT EXAM SUBMISSION! All hidden test cases passed with zero syntax errors."
        elif passed_tests > 0:
            uk_grade = f"Merit ({int(passed_tests/total_tests*100)}% Test Cases Passed)"
            diff_feedback = f"⚠️ Minor implementation issue: {execution_error}"
        else:
            uk_grade = "Fail (0% - Functional Errors in Written Code)"
            diff_feedback = f"❌ Exam Code Execution Failed: {execution_error}"

        return DrillResult(
            drill_id=drill.id,
            is_perfect=is_perfect,
            user_code=cleaned_user,
            target_syntax=drill.target_syntax,
            diff_feedback=diff_feedback,
            ast_valid=ast_valid,
            error_message=execution_error,
            uk_grade=uk_grade,
        )
