from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class AIConfig:
    api_key: Optional[str] = None
    model_name: str = "gemini-3.5-flash"
    is_active: bool = False


@dataclass
class AISocraticResponse:
    query: str
    non_cs_analogy: str
    conceptual_hint: str
    socratic_questions: List[str] = field(default_factory=list)
    raw_ai_text: str = ""


@dataclass
class AIEvaluationResponse:
    question_id: str
    score: float
    max_marks: float
    percentage: float
    uk_grade: str
    feedback: str
    distinction_upgrade_tips: List[str] = field(default_factory=list)
