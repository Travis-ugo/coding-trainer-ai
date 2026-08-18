from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_IN_BLANK = "fill_in_blank"
    CODE_OUTPUT = "code_output"
    CODE_WRITING = "code_writing"


@dataclass
class PracticeQuestion:
    id: str
    topic_id: str
    question_type: QuestionType
    prompt: str
    options: List[str] = field(default_factory=list)  # For multiple choice
    correct_answer: str = ""
    explanation: str = ""
    analogy_hint: str = ""
    uk_msc_distinction_tip: str = ""


@dataclass
class CodeExample:
    title: str
    code: str
    output: str
    explanation: str


@dataclass
class PythonTopicModule:
    id: str
    title: str
    order: int
    summary: str
    non_cs_analogy: str
    syntax_guide: str
    common_traps: str
    doc_reference_key: str
    code_examples: List[CodeExample] = field(default_factory=list)
    practice_questions: List[PracticeQuestion] = field(default_factory=list)


@dataclass
class PracticeResult:
    question_id: str
    is_correct: bool
    user_answer: str
    correct_answer: str
    explanation: str
    distinction_tip: str
