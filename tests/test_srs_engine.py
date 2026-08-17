import unittest
import os
import tempfile
import datetime
from coding_trainer_ai.srs import SM2Engine, DeckRepository, Flashcard, ReviewRating


class TestSRSEngine(unittest.TestCase):

    def setUp(self):
        self.engine = SM2Engine()
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.temp_dir, "test_srs_state.json")

    # -------------------------------------------------------------------------
    # SM-2 Scheduling Math Tests
    # -------------------------------------------------------------------------
    def test_sm2_first_review_perfect(self):
        card = Flashcard(id="c1", deck_id="d1", front="Q", back="A")
        today = datetime.date(2026, 1, 1)

        updated = self.engine.process_review(card, 5, today)
        self.assertEqual(updated.repetitions, 1)
        self.assertEqual(updated.interval_days, 1)
        self.assertEqual(updated.due_date, "2026-01-02")
        self.assertGreater(updated.ease_factor, 2.5)

    def test_sm2_second_review_perfect(self):
        card = Flashcard(id="c1", deck_id="d1", front="Q", back="A", repetitions=1, interval_days=1, ease_factor=2.6)
        today = datetime.date(2026, 1, 2)

        updated = self.engine.process_review(card, 5, today)
        self.assertEqual(updated.repetitions, 2)
        self.assertEqual(updated.interval_days, 6)
        self.assertEqual(updated.due_date, "2026-01-08")

    def test_sm2_third_review_scaling(self):
        card = Flashcard(id="c1", deck_id="d1", front="Q", back="A", repetitions=2, interval_days=6, ease_factor=2.5)
        today = datetime.date(2026, 1, 8)

        updated = self.engine.process_review(card, 4, today)
        self.assertEqual(updated.repetitions, 3)
        self.assertEqual(updated.interval_days, 15)  # round(6 * 2.5) = 15

    def test_sm2_blackout_resets_reps(self):
        card = Flashcard(id="c1", deck_id="d1", front="Q", back="A", repetitions=4, interval_days=30, ease_factor=2.5)
        today = datetime.date(2026, 1, 1)

        updated = self.engine.process_review(card, 0, today)
        self.assertEqual(updated.repetitions, 0)
        self.assertEqual(updated.interval_days, 1)

    def test_sm2_minimum_ease_factor_bound(self):
        card = Flashcard(id="c1", deck_id="d1", front="Q", back="A", ease_factor=1.3)
        today = datetime.date(2026, 1, 1)

        updated = self.engine.process_review(card, 0, today)
        self.assertEqual(updated.ease_factor, 1.3)  # Bounded at 1.3

    # -------------------------------------------------------------------------
    # Deck Repository & Persistence Tests
    # -------------------------------------------------------------------------
    def test_deck_repository_6_decks(self):
        repo = DeckRepository(state_file=self.state_file)
        decks = repo.get_all_decks()
        self.assertEqual(len(decks), 6)

    def test_due_cards_retrieval(self):
        repo = DeckRepository(state_file=self.state_file)
        due = repo.get_due_cards()
        self.assertGreaterEqual(len(due), 5, "Unreviewed cards should be due initially.")

    def test_state_persistence(self):
        repo1 = DeckRepository(state_file=self.state_file)
        due_cards = repo1.get_due_cards()
        card = due_cards[0]

        # Review card and save state
        repo1.sm2.process_review(card, 5)
        repo1.save_state()

        # Load state in new repository instance
        repo2 = DeckRepository(state_file=self.state_file)
        card_reloaded = next(
            c for deck in repo2.get_all_decks() for c in deck.cards if c.id == card.id
        )
        self.assertEqual(card_reloaded.repetitions, 1)
        self.assertEqual(card_reloaded.interval_days, 1)


if __name__ == "__main__":
    unittest.main()
