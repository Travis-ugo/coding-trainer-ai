from typing import List, Dict, Optional
from coding_trainer_ai.python_trainer.models import PythonTopicModule, PracticeQuestion, QuestionType


class PythonCurriculum:
    """
    Comprehensive interactive Python curriculum designed for non-CS learners.
    Teaches every core syntax rule, data structure, control flow, and OOP pattern
    with intuitive non-CS analogies, official docs references, and practice questions.
    """

    def __init__(self):
        self._modules: List[PythonTopicModule] = self._build_curriculum()

    def _build_curriculum(self) -> List[PythonTopicModule]:
        return [
            # Module 1
            PythonTopicModule(
                id="py_mod_01",
                title="Variables & Dynamic Typing",
                order=1,
                summary="Variables are dynamic reference labels pointing to typed objects in memory (Python Docs §4.2).",
                non_cs_analogy="Variables act like sticky name tags. Assigning b = a attaches tag 'b' to the same object as 'a'. Rebinding a variable moves the tag without copying bytes.",
                syntax_guide=(
                    "# Dynamic variable binding\n"
                    "x = 42          # x points to int 42\n"
                    "x = 'Python'    # x rebinds to str 'Python'\n"
                    "print(type(x))  # <class 'str'>"
                ),
                common_traps="Thinking `x = y` creates a copy. It creates reference aliasing to the same memory object.",
                doc_reference_key="informal_intro",
                practice_questions=[
                    PracticeQuestion(
                        id="q_01_01",
                        topic_id="py_mod_01",
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt="What happens in Python memory when you write `a = 10` followed by `b = a`?",
                        options=[
                            "Python duplicates integer 10 in memory.",
                            "Both name tags 'a' and 'b' point to the same integer object 10 in memory.",
                            "Variable 'b' becomes a pointer to variable 'a'.",
                            "Integer 10 is converted into a string.",
                        ],
                        correct_answer="Both name tags 'a' and 'b' point to the same integer object 10 in memory.",
                        explanation="In Python, variables are reference labels. `b = a` attaches label 'b' to the same object 'a' points to.",
                        analogy_hint="Two name tags pointing to the same object.",
                        uk_msc_distinction_tip="Python integers are immutable; `b = a` creates reference aliasing without copying memory.",
                    ),
                    PracticeQuestion(
                        id="q_01_02",
                        topic_id="py_mod_01",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the output of the following code?\n\nx = 5\ny = x\nx = 10\nprint(y)",
                        options=[],
                        correct_answer="5",
                        explanation="`y` points to integer 5. When `x = 10` runs, label `x` moves to 10, while `y` still points to 5.",
                        analogy_hint="Moving label 'x' does not move label 'y'.",
                        uk_msc_distinction_tip="Rebinding `x` does not mutate integer 5; integers are immutable.",
                    ),
                ],
            ),

            # Module 2
            PythonTopicModule(
                id="py_mod_02",
                title="Conditionals & Truthiness",
                order=2,
                summary="Control flow execution paths and boolean truth value testing (Python Docs §4.1).",
                non_cs_analogy="Evaluates conditions top-to-bottom. Empty collections ([], ''), 0, and None evaluate to False in boolean context.",
                syntax_guide=(
                    "score = 75\n"
                    "if score >= 70:\n"
                    "    grade = 'Distinction'\n"
                    "elif score >= 50:\n"
                    "    grade = 'Pass'\n"
                    "else:\n"
                    "    grade = 'Fail'"
                ),
                common_traps="Confusing equality `==` (value comparison) with identity `is` (object identity comparison).",
                doc_reference_key="control_flow",
                practice_questions=[
                    PracticeQuestion(
                        id="q_02_01",
                        topic_id="py_mod_02",
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt="Which of the following values evaluates to `False` in a Python `if` statement?",
                        options=["'0' (string 0)", "[0] (list containing 0)", "[] (empty list)", "-1 (negative integer)"],
                        correct_answer="[] (empty list)",
                        explanation="In Python, empty collections (`[]`, `''`), 0, and `None` evaluate to False.",
                        analogy_hint="Empty collection = False.",
                        uk_msc_distinction_tip="Python calls `bool(x)` internally, querying `__bool__()` or `len(x) == 0`.",
                    ),
                    PracticeQuestion(
                        id="q_02_02",
                        topic_id="py_mod_02",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the output of `val = []; print('A' if val else 'B')`?",
                        options=[],
                        correct_answer="B",
                        explanation="An empty list `[]` is falsy, so the condition evaluates to False.",
                        analogy_hint="Empty list = False.",
                        uk_msc_distinction_tip="Prefer `if val:` over `if len(val) > 0:` for idiomatic truthiness checking.",
                    ),
                ],
            ),

            # Module 3
            PythonTopicModule(
                id="py_mod_03",
                title="Loops & Iteration",
                order=3,
                summary="Sequence iteration with for/while loops, range(), enumerate(), and zip() (Python Docs §4.2-4.6).",
                non_cs_analogy="Iterates over items sequentially. range() generates numbers lazily; enumerate() yields (index, item) pairs.",
                syntax_guide=(
                    "items = ['a', 'b', 'c']\n"
                    "for idx, val in enumerate(items):\n"
                    "    print(idx, val)"
                ),
                common_traps="Modifying a collection while looping over it. Iterate over a copy instead.",
                doc_reference_key="control_flow",
                practice_questions=[
                    PracticeQuestion(
                        id="q_03_01",
                        topic_id="py_mod_03",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the output of `for i in range(1, 6, 2): print(i, end=' ')`?",
                        options=[],
                        correct_answer="1 3 5 ",
                        explanation="`range(start=1, stop=6, step=2)` yields 1, 3, 5.",
                        analogy_hint="Start 1, stop before 6, step 2.",
                        uk_msc_distinction_tip="`range` is an immutable sequence type producing integers on demand in O(1) memory.",
                    ),
                ],
            ),

            # Module 4
            PythonTopicModule(
                id="py_mod_04",
                title="Data Structures (Lists, Tuples, Dicts, Sets)",
                order=4,
                summary="Built-in container types, mutability rules, and hash maps (Python Docs §5.1-5.5).",
                non_cs_analogy="Lists [] are mutable sequences; Tuples () are immutable; Dicts {} map unique hashable keys to values; Sets {} store unique elements.",
                syntax_guide=(
                    "lst = [1, 2, 3]        # Mutable list\n"
                    "tup = (1, 2, 3)        # Immutable tuple\n"
                    "dct = {'a': 1, 'b': 2} # Key-Value hash map\n"
                    "st  = {1, 2, 3}        # Unique elements set"
                ),
                common_traps="Using mutable objects like lists as dictionary keys. Keys must be hashable (immutable).",
                doc_reference_key="data_structures",
                practice_questions=[
                    PracticeQuestion(
                        id="q_04_01",
                        topic_id="py_mod_04",
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt="Which Python data structure is IMMUTABLE?",
                        options=["List `[]`", "Tuple `()`", "Dictionary `{}`", "Set `{}`"],
                        correct_answer="Tuple `()`",
                        explanation="Tuples are immutable; their elements cannot be changed after creation.",
                        analogy_hint="Sealed display case.",
                        uk_msc_distinction_tip="Tuples have fixed memory layout and are hashable if all elements are hashable.",
                    ),
                ],
            ),

            # Module 5
            PythonTopicModule(
                id="py_mod_05",
                title="Functions & LEGB Scope",
                order=5,
                summary="Function definitions, parameter passing, and LEGB variable resolution (Python Docs §4.7).",
                non_cs_analogy="Functions encapsulate reusable logic. Scopes resolve in order: Local -> Enclosing -> Global -> Built-in.",
                syntax_guide=(
                    "def add(a, b=10):\n"
                    "    return a + b\n\n"
                    "def log(*args, **kwargs):\n"
                    "    print(args, kwargs)"
                ),
                common_traps="Using mutable default arguments like `lst=[]`. Defaults are evaluated once at function definition time.",
                doc_reference_key="control_flow",
                practice_questions=[
                    PracticeQuestion(
                        id="q_05_01",
                        topic_id="py_mod_05",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the output of calling `add_item(1); print(add_item(2))` when `def add_item(v, l=[]): l.append(v); return l`?",
                        options=[],
                        correct_answer="[1, 2]",
                        explanation="Default argument `l=[]` is evaluated once when defined and persists across calls.",
                        analogy_hint="Shared default list across calls.",
                        uk_msc_distinction_tip="Use `lst=None` as default and assign `lst = []` inside body.",
                    ),
                ],
            ),

            # Module 6
            PythonTopicModule(
                id="py_mod_06",
                title="Comprehensions & Generators",
                order=6,
                summary="Concise syntax for creating lists/dicts and memory-efficient generators (Python Docs §5.1.3).",
                non_cs_analogy="Transforms iterables into new collections in a single line. Generators stream values on demand with low RAM usage.",
                syntax_guide=(
                    "squares = [x**2 for x in range(5) if x % 2 == 0]\n"
                    "gen = (x**2 for x in range(1000)) # Memory efficient"
                ),
                common_traps="Over-nesting comprehensions. If readability drops, use standard for-loops.",
                doc_reference_key="datastructures",
                practice_questions=[
                    PracticeQuestion(
                        id="q_06_01",
                        topic_id="py_mod_06",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the result of `[x for x in range(5) if x > 2]`?",
                        options=[],
                        correct_answer="[3, 4]",
                        explanation="Filters `range(5)` (0..4) keeping elements strictly greater than 2.",
                        analogy_hint="Filter > 2.",
                        uk_msc_distinction_tip="List comprehensions execute at C-speed in CPython by bypassing bytecode loop overhead.",
                    ),
                ],
            ),

            # Module 7
            PythonTopicModule(
                id="py_mod_07",
                title="Error & Exception Handling",
                order=7,
                summary="Catching runtime errors with try/except/finally blocks (Python Docs §8).",
                non_cs_analogy="Catch specific runtime exceptions gracefully. The finally block executes unconditionally for resource cleanup.",
                syntax_guide=(
                    "try:\n"
                    "    num = int('invalid')\n"
                    "except ValueError as e:\n"
                    "    print(f'Error: {e}')\n"
                    "finally:\n"
                    "    print('Cleanup executed')"
                ),
                common_traps="Catching bare `except:` without specifying the exception type.",
                doc_reference_key="errors_exceptions",
                practice_questions=[
                    PracticeQuestion(
                        id="q_07_01",
                        topic_id="py_mod_07",
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt="Which block in a try-except statement is guaranteed to run?",
                        options=["`except`", "`else`", "`finally`", "`catch`"],
                        correct_answer="`finally`",
                        explanation="The `finally` clause executes unconditionally.",
                        analogy_hint="Unconditional cleanup.",
                        uk_msc_distinction_tip="Prefer context managers (`with` statements) for deterministic resource cleanup.",
                    ),
                ],
            ),

            # Module 8
            PythonTopicModule(
                id="py_mod_08",
                title="Object-Oriented Programming (OOP)",
                order=8,
                summary="Class blueprints, instance attributes (self), and inheritance (Python Docs §9).",
                non_cs_analogy="Classes are object blueprints. self refers to the current instance. Subclasses inherit parent methods.",
                syntax_guide=(
                    "class Bot:\n"
                    "    def __init__(self, name):\n"
                    "        self.name = name\n"
                    "    def speak(self):\n"
                    "        return f'I am {self.name}'"
                ),
                common_traps="Forgetting `self` as the first parameter in instance methods.",
                doc_reference_key="classes",
                practice_questions=[
                    PracticeQuestion(
                        id="q_08_01",
                        topic_id="py_mod_08",
                        question_type=QuestionType.FILL_IN_BLANK,
                        prompt="What parameter represents the object instance in class methods?",
                        options=[],
                        correct_answer="self",
                        explanation="`self` represents the instance of the class.",
                        analogy_hint="Instance reference.",
                        uk_msc_distinction_tip="`self` is an explicit convention in Python making instance attribution clear.",
                    ),
                ],
            ),

            # Module 9
            PythonTopicModule(
                id="py_mod_09",
                title="Standard Library & File I/O",
                order=9,
                summary="File access with context managers (with open) and stdlib modules (Python Docs §7.2).",
                non_cs_analogy="Context managers (with open) automatically close files when done, even if exceptions occur.",
                syntax_guide=(
                    "import json\n"
                    "with open('data.json', 'w') as f:\n"
                    "    json.dump({'status': 'ok'}, f)"
                ),
                common_traps="Opening files without `with open(...)`, leaving handles open.",
                doc_reference_key="stdlib",
                practice_questions=[
                    PracticeQuestion(
                        id="q_09_01",
                        topic_id="py_mod_09",
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt="Why is `with open('file.txt') as f:` preferred over `open()`?",
                        options=[
                            "It executes 10x faster.",
                            "It automatically closes the file even if exceptions occur.",
                            "It encrypts the file on disk.",
                            "It converts text into JSON format.",
                        ],
                        correct_answer="It automatically closes the file even if exceptions occur.",
                        explanation="Context managers guarantee automatic file cleanup upon exiting the block.",
                        analogy_hint="Automatic file cleanup.",
                        uk_msc_distinction_tip="Context managers implement `__enter__()` and `__exit__()` protocol for deterministic resource management.",
                    ),
                ],
            ),
        ]

    def get_all_modules(self) -> List[PythonTopicModule]:
        return self._modules

    def get_module_by_id(self, mod_id: str) -> Optional[PythonTopicModule]:
        for mod in self._modules:
            if mod.id == mod_id:
                return mod
        return None
