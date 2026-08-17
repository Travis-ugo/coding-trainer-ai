from typing import List, Optional
from coding_trainer_ai.syntax_drills.models import SyntaxDrill, DrillType


class DrillBank:
    """
    Pre-loaded bank of Anti-Copilot syntax drills, UK written exam challenges,
    fill-in-the-blank templates, and code tracing output predictions.
    """

    def __init__(self):
        self._drills: List[SyntaxDrill] = self._init_default_drills()

    def _init_default_drills(self) -> List[SyntaxDrill]:
        return [
            # ------------------------------------------------------------------
            # Anti-Copilot Raw Typing Drills (Muscle Memory Builder)
            # ------------------------------------------------------------------
            SyntaxDrill(
                id="drill_ac_01",
                drill_type=DrillType.ANTI_COPILOT_TYPING,
                title="Anti-Copilot Drill: List Comprehension with Condition",
                description="Type out the exact raw single-line list comprehension filtering even squares.",
                target_syntax="squares = [x**2 for x in range(10) if x % 2 == 0]",
                explanation="List comprehensions follow [transform for item in iterable if condition].",
                uk_msc_distinction_tip="Type every character from memory without relying on autocomplete squiggles.",
            ),
            SyntaxDrill(
                id="drill_ac_02",
                drill_type=DrillType.ANTI_COPILOT_TYPING,
                title="Anti-Copilot Drill: Class Definition & __init__ Method",
                description="Type out a clean Python class definition with an __init__ method.",
                target_syntax=(
                    "class Node:\n"
                    "    def __init__(self, val=0, next=None):\n"
                    "        self.val = val\n"
                    "        self.next = next"
                ),
                explanation="Classes use `__init__(self, ...)` to initialize instance attributes.",
                uk_msc_distinction_tip="Notice proper 4-space indentation and exact colon usage after class and def lines.",
            ),

            # ------------------------------------------------------------------
            # No-Compiler Written Exam Challenges
            # ------------------------------------------------------------------
            SyntaxDrill(
                id="drill_exam_01",
                drill_type=DrillType.NO_COMPILER_EXAM,
                title="UK Written Exam: Reverse a List In-Place (Two Pointers)",
                description=(
                    "Write a Python function `reverse_in_place(lst)` that reverses a list in-place "
                    "using a two-pointer approach without calling `.reverse()` or `lst[::-1]`. "
                    "Assume no compiler/IDE auto-formatting."
                ),
                target_syntax=(
                    "def reverse_in_place(lst):\n"
                    "    left, right = 0, len(lst) - 1\n"
                    "    while left < right:\n"
                    "        lst[left], lst[right] = lst[right], lst[left]\n"
                    "        left += 1\n"
                    "        right -= 1\n"
                    "    return lst"
                ),
                test_cases=[
                    {
                        "function_name": "reverse_in_place",
                        "inputs": [[1, 2, 3, 4, 5]],
                        "expected_output": [5, 4, 3, 2, 1],
                    },
                    {
                        "function_name": "reverse_in_place",
                        "inputs": [["A", "B"]],
                        "expected_output": ["B", "A"],
                    },
                ],
                explanation="Two-pointer swapping operates in O(N) time and O(1) auxiliary space.",
                uk_msc_distinction_tip="In-place mutations demonstrate O(1) space efficiency on written MSc exam papers.",
            ),

            # ------------------------------------------------------------------
            # Fill-in-the-Blank Code Completion
            # ------------------------------------------------------------------
            SyntaxDrill(
                id="drill_blank_01",
                drill_type=DrillType.FILL_IN_BLANK,
                title="Fill-in-the-Blank: Context Manager File Handling",
                description="Fill in the missing keyword for deterministic file handling:",
                template_code="____ open('file.txt', 'r') as f:\n    content = f.read()",
                target_syntax="with",
                explanation="The `with` keyword invokes context managers ensuring resource closure.",
                uk_msc_distinction_tip="Context managers guarantee clean-up even if exceptions occur.",
            ),

            # ------------------------------------------------------------------
            # Code Tracing & Output Prediction
            # ------------------------------------------------------------------
            SyntaxDrill(
                id="drill_trace_01",
                drill_type=DrillType.CODE_TRACING,
                title="Code Tracing: Default Argument Mutation Trap",
                description="Manually trace the code and predict the final printed output:",
                template_code=(
                    "def append_to(element, target=[]):\n"
                    "    target.append(element)\n"
                    "    return target\n\n"
                    "print(append_to(1))\n"
                    "print(append_to(2))"
                ),
                expected_output="[1, 2]",
                target_syntax="[1, 2]",
                explanation="Default list argument `target=[]` is evaluated ONCE when defined. Both calls mutate the exact same list instance.",
                uk_msc_distinction_tip="Classic UK exam code tracing trap regarding mutable default parameters.",
            ),
        ]

    def get_all_drills(self) -> List[SyntaxDrill]:
        return self._drills

    def get_drills_by_type(self, drill_type: DrillType) -> List[SyntaxDrill]:
        return [d for d in self._drills if d.drill_type == drill_type]
