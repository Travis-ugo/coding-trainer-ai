"""
Foundation & Non-CS Bridge Package for Coding Trainer AI.
Provides intuitive analogies, math notation Rosetta Stone, and 5-tier learning paths.
"""

from coding_trainer_ai.foundation.models import (
    TierLevel,
    AnalogyCard,
    MathNotationCard,
    ModuleTier,
    LearningModule,
)
from coding_trainer_ai.foundation.analogy_engine import AnalogyEngine
from coding_trainer_ai.foundation.rosetta_stone import MathRosettaStone
from coding_trainer_ai.foundation.tier_path import TierPathManager

__all__ = [
    "TierLevel",
    "AnalogyCard",
    "MathNotationCard",
    "ModuleTier",
    "LearningModule",
    "AnalogyEngine",
    "MathRosettaStone",
    "TierPathManager",
]
