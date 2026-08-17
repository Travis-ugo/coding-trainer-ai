import unittest
import os
import tempfile
import datetime
from coding_trainer_ai.foundation import AnalogyEngine, MathRosettaStone, TierPathManager
from coding_trainer_ai.ingestion import MultiFormatParser, AutoCurriculumGenerator
from coding_trainer_ai.python_trainer import PythonCurriculum, PracticeEngine
from coding_trainer_ai.syntax_drills import AntiCopilotEngine, NoCompilerExamMode, DrillBank, DrillType
from coding_trainer_ai.srs import SM2Engine, DeckRepository, Flashcard
from coding_trainer_ai.quiz_engine import DynamicQuizGenerator, QuizManager, QuestionCategory


class TestMasterIntegration(unittest.TestCase):
    """
    Master Integration Test Suite verifying end-to-end functionality across
    Phases 1 through 5 of Coding Trainer AI.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.srs_file = os.path.join(self.temp_dir, "master_srs.json")
        self.progress_file = os.path.join(self.temp_dir, "master_progress.json")

    # -------------------------------------------------------------------------
    # Integration 1: Phase 1 (Foundation) & Phase 2 (Doc Ingestion)
    # -------------------------------------------------------------------------
    def test_phase1_and_phase2_integration(self):
        analogy_engine = AnalogyEngine()
        rosetta_stone = MathRosettaStone()
        parser = MultiFormatParser()
        auto_gen = AutoCurriculumGenerator()

        # Step 1: Verify Phase 1 analogies & math lookup
        analogies = analogy_engine.get_all()
        self.assertGreaterEqual(len(analogies), 8)
        greek_alphabet = rosetta_stone.get_greek_alphabet()
        self.assertIn("∇ (Nabla)", greek_alphabet)

        # Step 2: Parse a Markdown document and auto-generate 5-tier module
        md_path = os.path.join(self.temp_dir, "sample_doc.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Robotics Kinematics\n\nTransformation matrices mapping joint frames.")

        doc_data = parser.parse_file(md_path)
        mod = auto_gen.generate_module_from_doc(doc_data)
        self.assertEqual(len(mod.tiers), 5, "Auto-generated module must contain all 5 tiers.")

    # -------------------------------------------------------------------------
    # Integration 2: Python Curriculum & Cumulative Recall (M1 -> MN)
    # -------------------------------------------------------------------------
    def test_python_curriculum_cumulative_recall(self):
        curriculum = PythonCurriculum()
        practice_engine = PracticeEngine()
        all_mods = curriculum.get_all_modules()

        self.assertEqual(len(all_mods), 9, "Python curriculum must have 9 modules.")

        # Build cumulative question set for Module 3 (should include Mod 1, Mod 2, and Mod 3)
        cum_questions = practice_engine.build_cumulative_question_set(all_mods, 3)
        topics = set(q.topic_id for q, _ in cum_questions)

        self.assertIn("py_mod_01", topics)
        self.assertIn("py_mod_02", topics)
        self.assertIn("py_mod_03", topics)

    # -------------------------------------------------------------------------
    # Integration 3: Phase 3 Anti-Copilot & No-Compiler Written Exam
    # -------------------------------------------------------------------------
    def test_syntax_drills_and_written_exam(self):
        anti_copilot = AntiCopilotEngine()
        exam_mode = NoCompilerExamMode()
        bank = DrillBank()

        # Test Anti-Copilot raw typing evaluation
        typing_drills = bank.get_drills_by_type(DrillType.ANTI_COPILOT_TYPING)
        res_typing = anti_copilot.evaluate_typing_drill(typing_drills[0], typing_drills[0].target_syntax)
        self.assertTrue(res_typing.is_perfect)

        # Test No-Compiler written exam sandbox execution
        exam_drills = bank.get_drills_by_type(DrillType.NO_COMPILER_EXAM)
        res_exam = exam_mode.evaluate_written_exam(exam_drills[0], exam_drills[0].target_syntax)
        self.assertTrue(res_exam.is_perfect)

    # -------------------------------------------------------------------------
    # Integration 4: Phase 4 SuperMemo SM-2 SRS & Persistence
    # -------------------------------------------------------------------------
    def test_srs_flashcards_persistence(self):
        repo1 = DeckRepository(state_file=self.srs_file)
        due = repo1.get_due_cards()
        self.assertGreaterEqual(len(due), 1)

        card = due[0]
        repo1.sm2.process_review(card, 5, datetime.date(2026, 1, 1))
        repo1.save_state()

        # Reload in new instance
        repo2 = DeckRepository(state_file=self.srs_file)
        reloaded_card = next(c for d in repo2.get_all_decks() for c in d.cards if c.id == card.id)
        self.assertEqual(reloaded_card.repetitions, 1)
        self.assertEqual(reloaded_card.interval_days, 1)

    # -------------------------------------------------------------------------
    # Integration 5: Phase 5 Dynamic Gated Quizzes & UK Thresholds
    # -------------------------------------------------------------------------
    def test_dynamic_quizzes_and_pass_gating(self):
        generator = DynamicQuizGenerator()
        manager = QuizManager(progress_file=self.progress_file)

        # Module 1 initially unlocked, Module 2 locked
        self.assertTrue(manager.is_module_unlocked("py_mod_01"))
        self.assertFalse(manager.is_module_unlocked("py_mod_02"))

        # Generate quiz and submit 100% correct answers
        questions = generator.generate_quiz_for_module("py_mod_01", seed=123)
        correct_answers = [q.correct_answer for q in questions]

        result = manager.evaluate_quiz_attempt("py_mod_01", questions, correct_answers)
        self.assertTrue(result.passed)
        self.assertTrue(result.earned_distinction)

        # Module 2 should now be unlocked and distinction badge awarded
        self.assertTrue(manager.is_module_unlocked("py_mod_02"))
        self.assertIn("py_mod_01", manager.progress.distinction_badges)


if __name__ == "__main__":
    unittest.main()
