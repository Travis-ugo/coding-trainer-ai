from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


class ReviewRating(IntEnum):
    BLACKOUT = 0
    INCORRECT = 1
    HESITANT = 2
    GOOD = 3
    EASY = 4
    PERFECT = 5

    @property
    def label(self) -> str:
        labels = {
            0: "0 - Complete Blackout (Forgot)",
            1: "1 - Incorrect",
            2: "2 - Hesitant / Hard",
            3: "3 - Good (Correct with difficulty)",
            4: "4 - Easy (Correct with slight hesitation)",
            5: "5 - Perfect Recall",
        }
        return labels.get(self.value, str(self.value))


@dataclass
class Flashcard:
    id: str
    deck_id: str
    front: str
    back: str
    non_cs_analogy: str = ""
    ease_factor: float = 2.5
    interval_days: int = 0
    repetitions: int = 0
    due_date: str = ""
    last_reviewed: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "deck_id": self.deck_id,
            "front": self.front,
            "back": self.back,
            "non_cs_analogy": self.non_cs_analogy,
            "ease_factor": self.ease_factor,
            "interval_days": self.interval_days,
            "repetitions": self.repetitions,
            "due_date": self.due_date,
            "last_reviewed": self.last_reviewed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Flashcard":
        return cls(
            id=data.get("id", ""),
            deck_id=data.get("deck_id", ""),
            front=data.get("front", ""),
            back=data.get("back", ""),
            non_cs_analogy=data.get("non_cs_analogy", ""),
            ease_factor=data.get("ease_factor", 2.5),
            interval_days=data.get("interval_days", 0),
            repetitions=data.get("repetitions", 0),
            due_date=data.get("due_date", ""),
            last_reviewed=data.get("last_reviewed", ""),
        )


@dataclass
class FlashcardDeck:
    id: str
    name: str
    description: str
    cards: List[Flashcard] = field(default_factory=list)
