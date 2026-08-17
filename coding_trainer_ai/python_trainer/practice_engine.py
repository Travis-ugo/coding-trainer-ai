import copy
from typing import List, Dict, Optional, Tuple
from coding_trainer_ai.python_trainer.models import (
    PracticeQuestion,
    QuestionType,
    PracticeResult,
    PythonTopicModule,
)


class PracticeEngine:
    """
    Evaluates practice questions, tracks accuracy performance, and constructs
    cumulative spaced memory question sets (M1 -> MN) across modules.
    """

    def __init__(self):
        self._score = 0
        self._total_attempted = 0
        self._topic_stats: Dict[str, Dict[str, int]] = {}

    def reset_session(self):
        self._score = 0
        self._total_attempted = 0
        self._topic_stats = {}

    def build_cumulative_question_set(
        self, all_modules: List[PythonTopicModule], current_module_order: int
    ) -> List[Tuple[PracticeQuestion, str]]:
        """
        Builds a cumulative question set containing:
        1. All practice questions from current module (current_module_order).
        2. Spaced memory review questions from ALL preceding modules (1 to current_module_order - 1).

        Returns a list of tuples: (question_object, source_label)
        """
        question_set: List[Tuple[PracticeQuestion, str]] = []

        # Find current module and prior modules
        current_mod = next((m for m in all_modules if m.order == current_module_order), None)
        prior_mods = [m for m in all_modules if m.order < current_module_order]

        # Add prior module review questions first (Cumulative Recall M1 -> MN-1)
        for prior_mod in prior_mods:
            for q in prior_mod.practice_questions:
                label = f"🔄 CUMULATIVE RECALL ({prior_mod.title.split(':')[0]})"
                question_set.append((copy.deepcopy(q), label))

        # Add current module questions (New Learning MN)
        if current_mod:
            for q in current_mod.practice_questions:
                label = f"✨ CURRENT TOPIC ({current_mod.title.split(':')[0]})"
                question_set.append((copy.deepcopy(q), label))

        return question_set

    def evaluate_answer(
        self, question: PracticeQuestion, user_answer: str
    ) -> PracticeResult:
        cleaned_user = user_answer.strip()
        cleaned_correct = question.correct_answer.strip()

        is_correct = False
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            if cleaned_user.isdigit():
                idx = int(cleaned_user) - 1
                if 0 <= idx < len(question.options):
                    selected_text = question.options[idx].strip()
                    is_correct = selected_text.lower() == cleaned_correct.lower()
            else:
                is_correct = cleaned_user.lower() == cleaned_correct.lower()
        elif question.question_type in (QuestionType.FILL_IN_BLANK, QuestionType.CODE_OUTPUT):
            is_correct = (
                cleaned_user.lower().replace(" ", "")
                == cleaned_correct.lower().replace(" ", "")
            )
        else:  # CODE_WRITING
            is_correct = (
                cleaned_user.lower().replace(" ", "")
                == cleaned_correct.lower().replace(" ", "")
            )

        self._total_attempted += 1
        if is_correct:
            self._score += 1

        topic = question.topic_id
        if topic not in self._topic_stats:
            self._topic_stats[topic] = {"correct": 0, "total": 0}
        self._topic_stats[topic]["total"] += 1
        if is_correct:
            self._topic_stats[topic]["correct"] += 1

        return PracticeResult(
            question_id=question.id,
            is_correct=is_correct,
            user_answer=cleaned_user,
            correct_answer=question.correct_answer,
            explanation=question.explanation,
            distinction_tip=question.uk_msc_distinction_tip,
        )

    def get_stats(self) -> dict:
        pct = (self._score / self._total_attempted * 100) if self._total_attempted > 0 else 0.0
        return {
            "score": self._score,
            "total": self._total_attempted,
            "percentage": pct,
            "topic_breakdown": self._topic_stats,
        }
