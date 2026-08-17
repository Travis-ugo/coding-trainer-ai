from enum import IntEnum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Optional


class TierLevel(IntEnum):
    TIER_1_FOUNDATION = 1
    TIER_2_SYNTAX = 2
    TIER_3_INTERMEDIATE = 3
    TIER_4_ADVANCED_MSC = 4
    TIER_5_EXAM_DISTINCTION = 5

    @property
    def display_name(self) -> str:
        labels = {
            1: "Tier 1: Foundation (Plain-English & Analogies)",
            2: "Tier 2: Syntax & Language Basics",
            3: "Tier 3: Intermediate Code & Systems",
            4: "Tier 4: Advanced MSc Level & Internals",
            5: "Tier 5: UK Exam Distinction & Critical Analysis",
        }
        return labels.get(self.value, f"Tier {self.value}")


@dataclass
class AnalogyCard:
    id: str
    concept: str
    non_cs_domain: str  # e.g., "History & Archives", "Diplomacy & Treaties", "Trade Routes"
    analogy_title: str
    analogy_explanation: str
    technical_translation: str
    example_snippet: str
    tags: List[str] = field(default_factory=list)


@dataclass
class MathNotationCard:
    id: str
    symbol: str
    name: str
    domain: str  # e.g., "Linear Algebra", "Calculus & Optimization", "Probability"
    plain_english_breakdown: str
    variable_roles: Dict[str, str] = field(default_factory=dict)
    msc_application: str = ""
    latex_example: str = ""


@dataclass
class ModuleTier:
    tier_level: TierLevel
    title: str
    summary: str
    explanation: str
    code_or_math_example: str
    uk_distinction_key_takeaway: str


@dataclass
class LearningModule:
    id: str
    title: str
    track: str
    description: str
    tiers: Dict[TierLevel, ModuleTier] = field(default_factory=dict)
