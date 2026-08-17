import datetime
from typing import Optional
from coding_trainer_ai.srs.models import Flashcard, ReviewRating


class SM2Engine:
    """
    SuperMemo SM-2 Spaced Repetition Algorithm Implementation.
    Calculates next review interval, ease factor, and due dates based on quality ratings (0-5).
    """

    MIN_EASE_FACTOR = 1.3

    def process_review(
        self, card: Flashcard, rating: int, review_date: Optional[datetime.date] = None
    ) -> Flashcard:
        if review_date is None:
            review_date = datetime.date.today()

        q = max(0, min(5, int(rating)))

        # Update Ease Factor: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        ef_delta = 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)
        new_ef = max(self.MIN_EASE_FACTOR, round(card.ease_factor + ef_delta, 2))

        # Update Repetitions & Interval
        if q < 3:
            # Failed recall: reset repetitions to 0, schedule for tomorrow
            new_reps = 0
            new_interval = 1
        else:
            # Successful recall: advance repetitions and scale interval
            new_reps = card.repetitions + 1
            if new_reps == 1:
                new_interval = 1
            elif new_reps == 2:
                new_interval = 6
            else:
                new_interval = max(1, int(round(card.interval_days * new_ef)))

        next_due = review_date + datetime.timedelta(days=new_interval)

        card.ease_factor = new_ef
        card.repetitions = new_reps
        card.interval_days = new_interval
        card.last_reviewed = review_date.isoformat()
        card.due_date = next_due.isoformat()

        return card

    def is_due(self, card: Flashcard, check_date: Optional[datetime.date] = None) -> bool:
        if check_date is None:
            check_date = datetime.date.today()

        if not card.due_date:
            return True  # Unreviewed new cards are due immediately

        try:
            due = datetime.date.fromisoformat(card.due_date)
            return check_date >= due
        except ValueError:
            return True
