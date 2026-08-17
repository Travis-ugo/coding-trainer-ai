from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


class ExamSection(Enum):
    PART_A_CONCEPTUAL = "part_a_conceptual"
    PART_B_TRACING = "part_b_tracing"
    PART_C_ALGORITHM = "part_c_algorithm"
    PART_D_ESSAY = "part_d_essay"

    @property
    def display_name(self) -> str:
        names = {
            "part_a_conceptual": "Part A: Short Answer Conceptual Questions (20 Marks)",
            "part_b_tracing": "Part B: Code Tracing, Bug Spotting & Output Analysis (30 Marks)",
            "part_c_algorithm": "Part C: Algorithm Implementation & Pseudocode Design (30 Marks)",
            "part_d_essay": "Part D: Critical Discussion & Architectural Essay (20 Marks)",
        }
        return names.get(self.value, self.value)


@dataclass
class UKExamQuestion:
    id: str
    section: ExamSection
    question_number: int
    marks: int
    prompt: str
    code_snippet: str = ""
    model_answer: str = ""
    distinction_criteria: str = ""


@dataclass
class UKExamPaper:
    id: str
    title: str
    module_code: str
    time_limit_minutes: int = 120
    total_marks: int = 100
    questions: List[UKExamQuestion] = field(default_factory=list)


@dataclass
class ExamAttemptResult:
    paper_id: str
    total_score: float
    max_marks: float
    percentage: float
    uk_classification: str
    total_duration_seconds: float = 0.0
    avg_seconds_per_question: float = 0.0
    pacing_rating: str = ""
    section_breakdown: Dict[str, float] = field(default_factory=dict)
    upgrade_feedback: str = ""


@dataclass
class LaTeXReportTemplate:
    title: str
    author_background: str
    abstract: str
    sections: Dict[str, str] = field(default_factory=dict)
    full_latex_code: str = ""
