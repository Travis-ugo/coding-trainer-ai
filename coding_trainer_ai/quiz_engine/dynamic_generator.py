import random
from typing import List, Dict, Any, Optional
from coding_trainer_ai.quiz_engine.models import DynamicQuizQuestion, QuestionCategory


class DynamicQuizGenerator:
    """
    Generates dynamic quiz questions with randomized parameter variations on retakes
    spanning 5 distinct question categories.
    """

    def generate_quiz_for_module(
        self, module_id: str, seed: Optional[int] = None
    ) -> List[DynamicQuizQuestion]:
        if seed is not None:
            random.seed(seed)

        questions = []

        # Category 1: Multiple Choice Theory
        q1_term = random.choice(["immutable", "mutable", "hashable", "dynamic"])
        if q1_term == "immutable":
            q1_options = ["Tuple `()`", "List `[]`", "Dictionary `{}`", "Set `{}`"]
            q1_correct = "Tuple `()`"
        elif q1_term == "mutable":
            q1_options = ["List `[]`", "Tuple `()`", "String `str`", "Integer `int`"]
            q1_correct = "List `[]`"
        elif q1_term == "hashable":
            q1_options = ["Tuple of integers", "List of integers", "Dictionary", "Set"]
            q1_correct = "Tuple of integers"
        else:
            q1_options = ["Name Tag References", "Fixed C-style Stack Boxes", "Static Types", "Raw Bytes"]
            q1_correct = "Name Tag References"

        questions.append(
            DynamicQuizQuestion(
                id=f"dyn_q1_{module_id}",
                module_id=module_id,
                category=QuestionCategory.MULTIPLE_CHOICE_THEORY,
                prompt=f"Which data structure or concept represents a {q1_term.upper()} object in Python?",
                options=q1_options,
                correct_answer=q1_correct,
                explanation=f"{q1_correct} is {q1_term} in Python memory.",
                distinction_tip="Python memory models differentiate between mutable values and hashable object identities.",
            )
        )

        # Category 2: Code Output Prediction (Parameter Mutation)
        val_start = random.randint(1, 5)
        val_step = random.randint(2, 4)
        val_stop = val_start + (val_step * 3)
        expected_range_list = list(range(val_start, val_stop, val_step))
        expected_str = " ".join(str(x) for x in expected_range_list)

        questions.append(
            DynamicQuizQuestion(
                id=f"dyn_q2_{module_id}",
                module_id=module_id,
                category=QuestionCategory.CODE_OUTPUT_PREDICTION,
                prompt="What is the exact output printed by the following code snippet?",
                code_snippet=f"for i in range({val_start}, {val_stop}, {val_step}):\n    print(i, end=' ')",
                correct_answer=expected_str,
                explanation=f"range({val_start}, {val_stop}, {val_step}) generates values: {expected_str}.",
                distinction_tip="Range parameters specify `range(start, stop, step)` where stop is exclusive.",
            )
        )

        # Category 3: Syntax Correction
        missing_elem = random.choice([":", "self", "def", "in"])
        if missing_elem == ":":
            bad_code = "if x > 10\n    print(x)"
            correct_fix = ":"
            prompt_text = "What character is missing at the end of line 1?"
        elif missing_elem == "self":
            bad_code = "class Robot:\n    def speak():\n        print('Hello')"
            correct_fix = "self"
            prompt_text = "What parameter is missing in `def speak()`?"
        elif missing_elem == "def":
            bad_code = "calculate_loss(y_pred, y_true):\n    return (y_pred - y_true)**2"
            correct_fix = "def"
            prompt_text = "What keyword is missing at the start of the function definition?"
        else:
            bad_code = "for item items:\n    print(item)"
            correct_fix = "in"
            prompt_text = "What keyword is missing between `item` and `items`?"

        questions.append(
            DynamicQuizQuestion(
                id=f"dyn_q3_{module_id}",
                module_id=module_id,
                category=QuestionCategory.SYNTAX_CORRECTION,
                prompt=prompt_text,
                code_snippet=bad_code,
                correct_answer=correct_fix,
                explanation=f"Python requires '{correct_fix}' for valid AST syntax parsing.",
                distinction_tip="AST parsing validates indentation blocks and keyword placements.",
            )
        )

        # Category 4: Time/Space Complexity Identification
        comp_choice = random.choice(["lookup", "nested_loop", "binary_search", "linear_scan"])
        if comp_choice == "lookup":
            snippet = "val = hash_map[key]  # Dictionary lookup"
            correct_comp = "O(1)"
        elif comp_choice == "nested_loop":
            snippet = "for i in range(N):\n    for j in range(N):\n        matrix[i][j] = 0"
            correct_comp = "O(N^2)"
        elif comp_choice == "binary_search":
            snippet = "# Binary search dividing search space in half\nwhile low <= high:\n    mid = (low + high) // 2"
            correct_comp = "O(log N)"
        else:
            snippet = "for item in lst:\n    if item == target: return True"
            correct_comp = "O(N)"

        questions.append(
            DynamicQuizQuestion(
                id=f"dyn_q4_{module_id}",
                module_id=module_id,
                category=QuestionCategory.COMPLEXITY_IDENTIFICATION,
                prompt="What is the worst-case Time Complexity of the following snippet?",
                code_snippet=snippet,
                options=["O(1)", "O(log N)", "O(N)", "O(N^2)"],
                correct_answer=correct_comp,
                explanation=f"The algorithmic operation evaluates to time complexity {correct_comp}.",
                distinction_tip="Distinction answers demonstrate Big-O asymptotic notation for time and auxiliary memory space.",
            )
        )

        # Category 5: Conceptual Short Explanation
        questions.append(
            DynamicQuizQuestion(
                id=f"dyn_q5_{module_id}",
                module_id=module_id,
                category=QuestionCategory.CONCEPTUAL_EXPLANATION,
                prompt="What keyword is used in Python to guarantee resource clean-up (closing files/connections) even if exceptions occur?",
                correct_answer="with",
                explanation="The `with` keyword invokes context managers executing `__exit__()` clean-up.",
                distinction_tip="Context managers guarantee deterministic resource deallocation.",
            )
        )

        return questions
