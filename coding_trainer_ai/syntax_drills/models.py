from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


class DrillType(Enum):
    ANTI_COPILOT_TYPING = "anti_copilot_typing"
    NO_COMPILER_EXAM = "no_compiler_exam"
    FILL_IN_BLANK = "fill_in_blank"
    CODE_TRACING = "code_tracing"


@dataclass
class SyntaxDrill:
    id: str
    drill_type: DrillType
    title: str
    description: str
    target_syntax: str = ""
    template_code: str = ""
    expected_output: str = ""
    test_cases: List[Dict[str, Any]] = field(default_factory=list)
    explanation: str = ""
    uk_msc_distinction_tip: str = ""


@dataclass
class DrillResult:
    drill_id: str
    is_perfect: bool
    user_code: str
    target_syntax: str
    diff_feedback: str
    ast_valid: bool
    error_message: str
    uk_grade: str
