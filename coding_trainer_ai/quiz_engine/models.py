from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


class QuestionCategory(Enum):
    MULTIPLE_CHOICE_THEORY = "multiple_choice_theory"
    CODE_OUTPUT_PREDICTION = "code_output_prediction"
    SYNTAX_CORRECTION = "syntax_correction"
    COMPLEXITY_IDENTIFICATION = "complexity_identification"
    CONCEPTUAL_EXPLANATION = "conceptual_explanation"

    @property
    def display_name(self) -> str:
        names = {
            "multiple_choice_theory": "Multiple Choice Theory",
            "code_output_prediction": "Code Output Prediction",
            "syntax_correction": "Syntax Correction",
            "complexity_identification": "Complexity Identification O(N)",
            "conceptual_explanation": "Conceptual Short Explanation",
        }
        return names.get(self.value, self.value)


@dataclass
class DynamicQuizQuestion:
    id: str
    module_id: str
    category: QuestionCategory
    prompt: str
    code_snippet: str = ""
    options: List[str] = field(default_factory=list)
    correct_answer: str = ""
    explanation: str = ""
    distinction_tip: str = ""
    variation_seed: int = 1


@dataclass
class QuizAttemptResult:
    module_id: str
    score: int
    total_questions: int
    percentage: float
    passed: bool
    earned_distinction: bool
    grade_label: str
    total_duration_seconds: float = 0.0
    avg_seconds_per_question: float = 0.0
    pacing_rating: str = ""
    question_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class UserProgress:
    unlocked_modules: List[str] = field(default_factory=list)
    distinction_badges: List[str] = field(default_factory=list)
    module_scores: Dict[str, float] = field(default_factory=dict)
