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
            # ------------------------------------------------------------------
            # Module 1: Variables, Dynamic Typing & Name Tags
            # ------------------------------------------------------------------
            PythonTopicModule(
                id="py_mod_01",
                title="Module 1: Variables, Dynamic Typing & Name Tag Analogy",
                order=1,
                summary="Understanding how Python stores variables as dynamic name tags pointing to objects in memory.",
                non_cs_analogy=(
                    "In C or C++, a variable is a physical metal box labeled with a fixed size (int, float).\n"
                    "In Python, a variable is simply a sticky 'Name Tag' stuck onto an object in memory!\n"
                    "Writing `x = 42` sticks the name tag 'x' onto integer 42. Writing `x = 'Treaty'` moves the sticky label "
                    "to a text string. The object has a type, but the name tag does not!"
                ),
                syntax_guide=(
                    "# Variable assignment\n"
                    "country = 'United Kingdom'\n"
                    "year = 1707\n"
                    "is_sovereign = True\n\n"
                    "# Checking types dynamically\n"
                    "print(type(country))    # <class 'str'>\n"
                    "print(type(year))       # <class 'int'>"
                ),
                common_traps="Thinking `x = y` creates a copy of object `y`. It only sticks a second name tag onto the SAME object!",
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
                        analogy_hint="Think of sticking two different sticky name tags onto the exact same historical document.",
                        uk_msc_distinction_tip="Python integers are immutable objects; assigning `b = a` creates reference aliasing without copying bytes.",
                    ),
                    PracticeQuestion(
                        id="q_01_02",
                        topic_id="py_mod_01",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the output of the following code?\n\nx = 5\ny = x\nx = 10\nprint(y)",
                        options=[],
                        correct_answer="5",
                        explanation="`y` points to integer 5. When `x = 10` is executed, label `x` moves to 10, but label `y` still points to 5.",
                        analogy_hint="Moving label 'x' to a new box doesn't move label 'y'.",
                        uk_msc_distinction_tip="Rebinding `x` does not mutate the integer object 5; integers are immutable.",
                    ),
                ],
            ),

            # ------------------------------------------------------------------
            # Module 2: Conditionals & Boolean Logic
            # ------------------------------------------------------------------
            PythonTopicModule(
                id="py_mod_02",
                title="Module 2: Conditionals (`if`/`elif`/`else`) & Truthiness",
                order=2,
                summary="Navigating decision trees, logical operators (and, or, not), and Python's Truthiness rules.",
                non_cs_analogy=(
                    "Think of diplomatic border customs checkpoint controls: "
                    "IF passport is valid AND visa is approved -> Enter;\n"
                    "ELIF diplomat pass presented -> Priority Entry;\n"
                    "ELSE -> Deny Access.\n"
                    "Python evaluates conditions sequentially from top to bottom."
                ),
                syntax_guide=(
                    "score = 75\n"
                    "if score >= 70:\n"
                    "    grade = 'Distinction'\n"
                    "elif score >= 60:\n"
                    "    grade = 'Merit'\n"
                    "elif score >= 50:\n"
                    "    grade = 'Pass'\n"
                    "else:\n"
                    "    grade = 'Fail'\n\n"
                    "# Truthiness: 0, '', [], None evaluate to False in boolean context!"
                ),
                common_traps="Confusing equality `==` (value comparison) with identity `is` (same object in memory comparison).",
                doc_reference_key="control_flow",
                practice_questions=[
                    PracticeQuestion(
                        id="q_02_01",
                        topic_id="py_mod_02",
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt="Which of the following values evaluates to `False` in a Python `if` statement?",
                        options=["'0' (string 0)", "[0] (list containing 0)", "[] (empty list)", "-1 (negative integer)"],
                        correct_answer="[] (empty list)",
                        explanation="In Python, empty collections (`[]`, `{}`, `()`, `''`), zero `0`, and `None` are falsy. String `'0'` and `[0]` are non-empty and thus truthy!",
                        analogy_hint="An empty archival folder has no contents, so it represents False.",
                        uk_msc_distinction_tip="Python calls `bool(x)` internally, which queries `x.__bool__()` or `len(x) == 0`.",
                    ),
                    PracticeQuestion(
                        id="q_02_02",
                        topic_id="py_mod_02",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the output of the following code?\n\nval = []\nif val:\n    print('A')\nelse:\n    print('B')",
                        options=[],
                        correct_answer="B",
                        explanation="An empty list `[]` is falsy, so the `else` branch executes.",
                        analogy_hint="Empty list = False.",
                        uk_msc_distinction_tip="Writing `if len(val) > 0:` is unpythonic; prefer `if val:` for truthiness checking.",
                    ),
                ],
            ),

            # ------------------------------------------------------------------
            # Module 3: Loops & Iteration
            # ------------------------------------------------------------------
            PythonTopicModule(
                id="py_mod_03",
                title="Module 3: Loops & Iteration (`for`, `while`, `enumerate`, `zip`)",
                order=3,
                summary="Mastering iteration over sequences, while loops, range(), enumerate(), and zip().",
                non_cs_analogy=(
                    "A `for` loop is an archivist reading through a stack of historical files one by one from top to bottom.\n"
                    "`enumerate()` is like having a stamp that numbers each file page (0, 1, 2...) as you read it.\n"
                    "`zip()` is like matching two parallel lists (e.g. Treaties and Treaty Signing Years) side-by-side."
                ),
                syntax_guide=(
                    "# For loop with range()\n"
                    "for i in range(3):\n"
                    "    print(f'Iteration {i}')\n\n"
                    "# Enumerate for index + value\n"
                    "treaties = ['Westphalia', 'Utrecht', 'Versailles']\n"
                    "for idx, name in enumerate(treaties, start=1):\n"
                    "    print(f'{idx}. {name}')\n\n"
                    "# Zip parallel lists\n"
                    "years = [1648, 1713, 1919]\n"
                    "for name, year in zip(treaties, years):\n"
                    "    print(f'{name} ({year})')"
                ),
                common_traps="Modifying a list while looping over it! This causes skipped elements or unexpected iteration behavior.",
                doc_reference_key="control_flow",
                practice_questions=[
                    PracticeQuestion(
                        id="q_03_01",
                        topic_id="py_mod_03",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the output of the following code?\n\nfor i in range(1, 6, 2):\n    print(i, end=' ')",
                        options=[],
                        correct_answer="1 3 5 ",
                        explanation="`range(start=1, stop=6, step=2)` generates values 1, 3, 5.",
                        analogy_hint="Start at page 1, stop before page 6, stepping 2 pages at a time.",
                        uk_msc_distinction_tip="`range` is a generator-like lazy sequence in Python 3 producing values on demand in O(1) memory.",
                    ),
                    PracticeQuestion(
                        id="q_03_02",
                        topic_id="py_mod_03",
                        question_type=QuestionType.FILL_IN_BLANK,
                        prompt="Fill in the blank function name to iterate over list `items` with index numbers:\n\nfor idx, val in ________(items):\n    print(idx, val)",
                        options=[],
                        correct_answer="enumerate",
                        explanation="`enumerate(iterable)` yields tuples of `(index, item)` during iteration.",
                        analogy_hint="The indexing stamp tool.",
                        uk_msc_distinction_tip="`enumerate(items)` avoids the unpythonic C-style `for i in range(len(items)):` antipattern.",
                    ),
                ],
            ),

            # ------------------------------------------------------------------
            # Module 4: Core Data Structures (Lists, Tuples, Dicts, Sets)
            # ------------------------------------------------------------------
            PythonTopicModule(
                id="py_mod_04",
                title="Module 4: Core Data Structures (Lists, Tuples, Dicts, Sets)",
                order=4,
                summary="Mastering Python's built-in container types, mutability, indexing, hashing, and performance characteristics.",
                non_cs_analogy=(
                    "- **List `[]`**: An expandable ring binder folder where pages can be added, removed, or replaced.\n"
                    "- **Tuple `()`**: A sealed glass display case containing fixed historical artifacts (immutable!).\n"
                    "- **Dictionary `{}`**: A library card catalog mapping Unique Index Keys -> Information Details.\n"
                    "- **Set `{}`**: A collection of unique museum coins with no duplicate entries allowed."
                ),
                syntax_guide=(
                    "# List (Mutable, Ordered)\n"
                    "fruits = ['apple', 'banana']\n"
                    "fruits.append('cherry')\n\n"
                    "# Tuple (Immutable, Ordered)\n"
                    "coords = (51.5074, 0.1278)\n\n"
                    "# Dict (Key-Value Hash Map, Fast O(1) Lookups)\n"
                    "capital = {'UK': 'London', 'France': 'Paris'}\n"
                    "print(capital['UK'])\n\n"
                    "# Set (Unique elements, Fast membership test `in`)\n"
                    "tags = {'ai', 'robotics', 'ai'} # Result: {'ai', 'robotics'}"
                ),
                common_traps="Using mutable objects like lists or dictionaries as dictionary keys or set elements. Only hashable (immutable) objects can be keys!",
                doc_reference_key="data_structures",
                practice_questions=[
                    PracticeQuestion(
                        id="q_04_01",
                        topic_id="py_mod_04",
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt="Which Python data structure is IMMUTABLE and cannot be modified after creation?",
                        options=["List `[]`", "Tuple `()`", "Dictionary `{}`", "Set `{}`"],
                        correct_answer="Tuple `()`",
                        explanation="Tuples are immutable sequences. Once created, elements cannot be added, removed, or re-assigned.",
                        analogy_hint="The sealed glass display case.",
                        uk_msc_distinction_tip="Tuples have fixed memory layout and are hashable if all their elements are hashable.",
                    ),
                    PracticeQuestion(
                        id="q_04_02",
                        topic_id="py_mod_04",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the output of the following code?\n\nd = {'a': 1, 'b': 2}\nprint(d.get('c', 0))",
                        options=[],
                        correct_answer="0",
                        explanation="`dict.get(key, default)` returns the default value (0) if the key 'c' is not found, avoiding a KeyError.",
                        analogy_hint="Asking the archivist for a file: if missing, return default 0.",
                        uk_msc_distinction_tip="Using `.get()` prevents unhandled `KeyError` exceptions when querying non-existent keys.",
                    ),
                ],
            ),

            # ------------------------------------------------------------------
            # Module 5: Functions, Scope & LEGB Rule
            # ------------------------------------------------------------------
            PythonTopicModule(
                id="py_mod_05",
                title="Module 5: Functions (`def`), Scope (LEGB Rule), `*args`, `**kwargs`",
                order=5,
                summary="Building reusable code blocks, parameter passing, positional/keyword arguments, and variable scoping.",
                non_cs_analogy=(
                    "A function is a standardized diplomatic policy template. "
                    "Parameters are blank fields on the form. "
                    "The LEGB scope rule determines where Python looks for variables: "
                    "Local desk -> Enclosing office -> Global building -> Built-in dictionary."
                ),
                syntax_guide=(
                    "def calculate_grade(score, pass_mark=50):\n"
                    "    if score >= pass_mark:\n"
                    "        return 'Pass'\n"
                    "    return 'Fail'\n\n"
                    "# Flex arguments: *args (tuple of positionals), **kwargs (dict of keywords)\n"
                    "def log_event(*args, **kwargs):\n"
                    "    print('Args:', args)\n"
                    "    print('Kwargs:', kwargs)"
                ),
                common_traps="Using a mutable object (like a list `[]`) as a default argument! Default arguments are evaluated ONCE at function definition time.",
                doc_reference_key="control_flow",
                practice_questions=[
                    PracticeQuestion(
                        id="q_05_01",
                        topic_id="py_mod_05",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the output of the following code?\n\ndef add_item(val, lst=[]):\n    lst.append(val)\n    return lst\n\nadd_item(1)\nprint(add_item(2))",
                        options=[],
                        correct_answer="[1, 2]",
                        explanation="Default argument `lst=[]` is evaluated ONCE when the function is defined. The list persists across function calls!",
                        analogy_hint="The function shares the exact same default binder across calls.",
                        uk_msc_distinction_tip="Classic Python trap! Always use `def add_item(val, lst=None): if lst is None: lst = []`.",
                    ),
                ],
            ),

            # ------------------------------------------------------------------
            # Module 6: Comprehensions & Generators
            # ------------------------------------------------------------------
            PythonTopicModule(
                id="py_mod_06",
                title="Module 6: Comprehensions (List, Dict, Set) & Generators",
                order=6,
                summary="Writing elegant, concise single-line collection transformations and memory-efficient generators.",
                non_cs_analogy=(
                    "A List Comprehension is like an automated filter conveyor belt: "
                    "Take a box of documents, filter out non-treaties, format the document titles, "
                    "and stack them into a new folder in one swift motion."
                ),
                syntax_guide=(
                    "# List Comprehension: [transform for item in iterable if condition]\n"
                    "squares = [x**2 for x in range(10) if x % 2 == 0]\n\n"
                    "# Dict Comprehension\n"
                    "capitals = {'UK': 'London', 'France': 'Paris'}\n"
                    "upper_caps = {k: v.upper() for k, v in capitals.items()}\n\n"
                    "# Generator Expression (Memory Efficient Lazy Evaluator!)\n"
                    "gen = (x**2 for x in range(1000000)) # Uses almost zero RAM!"
                ),
                common_traps="Over-nesting list comprehensions until they become unreadable. If it spans multiple complex lines, use a standard for-loop!",
                doc_reference_key="datastructures",
                practice_questions=[
                    PracticeQuestion(
                        id="q_06_01",
                        topic_id="py_mod_06",
                        question_type=QuestionType.CODE_OUTPUT,
                        prompt="What is the result of `[x for x in range(5) if x > 2]`?",
                        options=[],
                        correct_answer="[3, 4]",
                        explanation="Filters `range(5)` (0,1,2,3,4) keeping only elements strictly greater than 2.",
                        analogy_hint="Keep numbers > 2.",
                        uk_msc_distinction_tip="List comprehensions execute at C-speed in CPython by avoiding Python bytecode loop overhead.",
                    ),
                ],
            ),

            # ------------------------------------------------------------------
            # Module 7: Error & Exception Handling
            # ------------------------------------------------------------------
            PythonTopicModule(
                id="py_mod_07",
                title="Module 7: Error & Exception Handling (`try`, `except`, `finally`)",
                order=7,
                summary="Gracefully catching runtime errors, creating custom exceptions, and ensuring resource cleanup.",
                non_cs_analogy=(
                    "A `try` block is like attempting a diplomatic mission. "
                    "An `except` block is your emergency contingency protocol if a specific crisis occurs. "
                    "A `finally` block is the mandatory cleanup procedure (securing diplomatic pouches) "
                    "that MUST run regardless of success or failure."
                ),
                syntax_guide=(
                    "try:\n"
                    "    num = int('invalid_number')\n"
                    "except ValueError as e:\n"
                    "    print(f'Caught expected conversion error: {e}')\n"
                    "else:\n"
                    "    print('Success! No exceptions occurred.')\n"
                    "finally:\n"
                    "    print('Clean-up step executed unconditionally.')"
                ),
                common_traps="Catching bare `except:` without specifying the exception type! This catches `KeyboardInterrupt` (Ctrl+C) and hides critical bugs.",
                doc_reference_key="errors_exceptions",
                practice_questions=[
                    PracticeQuestion(
                        id="q_07_01",
                        topic_id="py_mod_07",
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt="Which block in a Python `try-except` statement is guaranteed to run whether an exception occurred or not?",
                        options=["`except`", "`else`", "`finally`", "`catch`"],
                        correct_answer="`finally`",
                        explanation="The `finally` clause executes unconditionally before leaving the try statement, ideal for closing files or connections.",
                        analogy_hint="The mandatory cleanup procedure.",
                        uk_msc_distinction_tip="Use context managers (`with` statements) for resource management as an idiomatic alternative to `try...finally`.",
                    ),
                ],
            ),

            # ------------------------------------------------------------------
            # Module 8: Object-Oriented Programming (OOP)
            # ------------------------------------------------------------------
            PythonTopicModule(
                id="py_mod_08",
                title="Module 8: Object-Oriented Programming (Classes, `__init__`, Inheritance)",
                order=8,
                summary="Designing custom blueprints (classes), instance attributes (`self`), inheritance, and dunder methods.",
                non_cs_analogy=(
                    "A **Class** is an architectural blueprint for an embassy building. "
                    "An **Instance / Object** is a specific physical embassy building constructed from that blueprint "
                    "(e.g. UK Embassy in Washington, UK Embassy in Tokyo). `self` refers to *this specific embassy building*."
                ),
                syntax_guide=(
                    "class Embassy:\n"
                    "    def __init__(self, country, city):\n"
                    "        self.country = country\n"
                    "        self.city = city\n\n"
                    "    def announce(self):\n"
                    "        return f'{self.country} Embassy in {self.city}'\n\n"
                    "# Inheritance\n"
                    "class Consulate(Embassy):\n"
                    "    def issue_visa(self):\n"
                    "        return 'Visa Issued'"
                ),
                common_traps="Forgetting `self` as the first parameter in instance method definitions!",
                doc_reference_key="classes",
                practice_questions=[
                    PracticeQuestion(
                        id="q_08_01",
                        topic_id="py_mod_08",
                        question_type=QuestionType.FILL_IN_BLANK,
                        prompt="What keyword is passed as the first parameter to instance methods to represent the object instance?\n\ndef method(______):\n    pass",
                        options=[],
                        correct_answer="self",
                        explanation="`self` represents the instance of the class when calling methods.",
                        analogy_hint="This specific embassy building.",
                        uk_msc_distinction_tip="`self` is an explicit convention in Python (not a reserved keyword), making instance attribution explicit.",
                    ),
                ],
            ),

            # ------------------------------------------------------------------
            # Module 9: Standard Library Essentials & File I/O
            # ------------------------------------------------------------------
            PythonTopicModule(
                id="py_mod_09",
                title="Module 9: Standard Library Essentials & File I/O (`json`, `collections`, `os`)",
                order=9,
                summary="Reading/writing files using context managers (`with`), parsing JSON, and utilizing standard library tools.",
                non_cs_analogy=(
                    "Using `with open(...)` is like opening an archive vault door with a self-locking timer: "
                    "Once you step out of the room, the vault door automatically locks itself shut (closes file)."
                ),
                syntax_guide=(
                    "import json\n"
                    "import os\n"
                    "from collections import Counter\n\n"
                    "# Safe File I/O with context manager\n"
                    "data = {'student': 'MSc AI', 'score': 85}\n"
                    "with open('result.json', 'w') as f:\n"
                    "    json.dump(data, f, indent=2)\n\n"
                    "# Frequency counter\n"
                    "words = ['treaty', 'war', 'treaty', 'peace']\n"
                    "counts = Counter(words) # Counter({'treaty': 2, 'war': 1, 'peace': 1})"
                ),
                common_traps="Forgetting to use `with open(...)` when doing file I/O, leaving open file handles dangling.",
                doc_reference_key="stdlib",
                practice_questions=[
                    PracticeQuestion(
                        id="q_09_01",
                        topic_id="py_mod_09",
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt="Why is `with open('file.txt') as f:` preferred over `f = open('file.txt')`?",
                        options=[
                            "It executes 10x faster.",
                            "It automatically closes the file even if exceptions occur during reading/writing.",
                            "It encrypts the file on disk.",
                            "It converts text files into JSON format.",
                        ],
                        correct_answer="It automatically closes the file even if exceptions occur during reading/writing.",
                        explanation="Context managers (`with`) guarantee exit cleanup (`f.close()`) automatically.",
                        analogy_hint="The self-locking vault door.",
                        uk_msc_distinction_tip="Context managers implement `__enter__()` and `__exit__()` protocol for deterministic resource cleanup.",
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
