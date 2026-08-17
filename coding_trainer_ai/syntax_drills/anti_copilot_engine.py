import ast
import difflib
from typing import Tuple
from coding_trainer_ai.syntax_drills.models import SyntaxDrill, DrillResult


class AntiCopilotEngine:
    """
    Evaluates character-by-character syntax accuracy, AST parsing, and indentation correctness.
    Zero autocompletion allowed!
    """

    def evaluate_typing_drill(self, drill: SyntaxDrill, user_input: str) -> DrillResult:
        cleaned_user = user_input.strip()
        cleaned_target = drill.target_syntax.strip()

        # Check AST syntax validity
        ast_valid = True
        error_msg = ""
        try:
            ast.parse(cleaned_user)
        except SyntaxError as e:
            ast_valid = False
            error_msg = f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}"

        # Exact match check
        is_perfect = (cleaned_user == cleaned_target)

        # Generate character/line diff
        diff_feedback = self._generate_diff(cleaned_target, cleaned_user)

        # Determine UK MSc Grade
        if is_perfect:
            uk_grade = "Distinction (100% - Perfect Memory Recall)"
        elif ast_valid and self._similarity_score(cleaned_target, cleaned_user) >= 0.8:
            uk_grade = "Merit (Solid syntax with minor formatting difference)"
        elif ast_valid:
            uk_grade = "Pass (Valid syntax but differs from optimal target)"
        else:
            uk_grade = "Fail (SyntaxError detected - Retake drill)"

        return DrillResult(
            drill_id=drill.id,
            is_perfect=is_perfect,
            user_code=cleaned_user,
            target_syntax=cleaned_target,
            diff_feedback=diff_feedback,
            ast_valid=ast_valid,
            error_message=error_msg,
            uk_grade=uk_grade,
        )

    def _generate_diff(self, target: str, user: str) -> str:
        target_lines = target.splitlines()
        user_lines = user.splitlines()

        diff = difflib.ndiff(target_lines, user_lines)
        diff_output = []
        for line in diff:
            if line.startswith("- "):
                diff_output.append(f"  ❌ Missing / Expected : {line[2:]}")
            elif line.startswith("+ "):
                diff_output.append(f"  ⚠️ You Typed         : {line[2:]}")
            elif line.startswith("  "):
                diff_output.append(f"  ✅ Correct Line      : {line[2:]}")
        return "\n".join(diff_output)

    def _similarity_score(self, target: str, user: str) -> float:
        return difflib.SequenceMatcher(None, target, user).ratio()
