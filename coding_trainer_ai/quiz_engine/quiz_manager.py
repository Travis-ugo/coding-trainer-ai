import os
import json
from typing import List, Dict, Optional, Any
from coding_trainer_ai.quiz_engine.models import (
    DynamicQuizQuestion,
    QuizAttemptResult,
    UserProgress,
    QuestionCategory,
)
from coding_trainer_ai.quiz_engine.question_timer import QuestionTimer

PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "resources",
    "quiz_progress.json",
)


class QuizManager:
    """
    Evaluates dynamic quiz attempts, enforces pass-gating (50% Pass / 70% Distinction),
    calculates timing & UK pacing ratings, and persists unlocked module levels to disk.
    """

    PASS_THRESHOLD = 50.0
    DISTINCTION_THRESHOLD = 70.0

    def __init__(self, progress_file: str = PROGRESS_FILE):
        self.progress_file = progress_file
        self.progress = UserProgress(
            unlocked_modules=["py_mod_01"],
            distinction_badges=[],
            module_scores={},
        )
        self.load_progress()

    def evaluate_quiz_attempt(
        self,
        module_id: str,
        questions: List[DynamicQuizQuestion],
        user_answers: List[str],
        question_timings: Optional[List[float]] = None,
    ) -> QuizAttemptResult:
        score = 0
        total = len(questions)
        q_results = []

        if question_timings is None:
            question_timings = [10.0] * total

        total_duration = sum(question_timings)
        avg_seconds = (total_duration / total) if total > 0 else 0.0
        pacing_rating, _ = QuestionTimer.get_uk_pacing_rating(avg_seconds)

        for idx, (q, u_ans) in enumerate(zip(questions, user_answers)):
            cleaned_u = u_ans.strip()
            cleaned_c = q.correct_answer.strip()
            elapsed = question_timings[idx] if idx < len(question_timings) else 0.0

            is_correct = False
            if q.category in (QuestionCategory.MULTIPLE_CHOICE_THEORY, QuestionCategory.COMPLEXITY_IDENTIFICATION):
                if cleaned_u.isdigit():
                    opt_idx = int(cleaned_u) - 1
                    if 0 <= opt_idx < len(q.options):
                        selected = q.options[opt_idx].strip()
                        is_correct = selected.lower() == cleaned_c.lower()
                else:
                    is_correct = cleaned_u.lower() == cleaned_c.lower()
            else:
                is_correct = cleaned_u.lower().replace(" ", "") == cleaned_c.lower().replace(" ", "")

            if is_correct:
                score += 1

            q_results.append({
                "question_id": q.id,
                "category": q.category.display_name,
                "prompt": q.prompt,
                "is_correct": is_correct,
                "elapsed_seconds": elapsed,
                "user_answer": cleaned_u,
                "correct_answer": cleaned_c,
                "explanation": q.explanation,
            })

        pct = (score / total * 100.0) if total > 0 else 0.0
        passed = pct >= self.PASS_THRESHOLD
        earned_distinction = pct >= self.DISTINCTION_THRESHOLD

        if earned_distinction:
            grade_label = f"🏆 DISTINCTION ({pct:.1f}%)"
        elif passed:
            grade_label = f"✅ PASS ({pct:.1f}%)"
        else:
            grade_label = f"❌ FAIL ({pct:.1f}% - Retake Required)"

        # Save score & unlock next module if passed
        self.progress.module_scores[module_id] = max(
            self.progress.module_scores.get(module_id, 0.0), pct
        )

        if earned_distinction and module_id not in self.progress.distinction_badges:
            self.progress.distinction_badges.append(module_id)

        if passed:
            next_mod_id = self._get_next_module_id(module_id)
            if next_mod_id and next_mod_id not in self.progress.unlocked_modules:
                self.progress.unlocked_modules.append(next_mod_id)

        self.save_progress()

        return QuizAttemptResult(
            module_id=module_id,
            score=score,
            total_questions=total,
            percentage=pct,
            passed=passed,
            earned_distinction=earned_distinction,
            grade_label=grade_label,
            total_duration_seconds=round(total_duration, 1),
            avg_seconds_per_question=round(avg_seconds, 1),
            pacing_rating=pacing_rating,
            question_results=q_results,
        )

    def _get_next_module_id(self, current_module_id: str) -> Optional[str]:
        if current_module_id.startswith("py_mod_"):
            try:
                num = int(current_module_id.split("_")[-1])
                if num < 9:
                    return f"py_mod_0{num + 1}"
            except ValueError:
                pass
        return None

    def is_module_unlocked(self, module_id: str) -> bool:
        return module_id in self.progress.unlocked_modules

    def save_progress(self):
        os.makedirs(os.path.dirname(self.progress_file), exist_ok=True)
        data = {
            "unlocked_modules": self.progress.unlocked_modules,
            "distinction_badges": self.progress.distinction_badges,
            "module_scores": self.progress.module_scores,
        }
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_progress(self):
        if not os.path.exists(self.progress_file):
            return

        try:
            with open(self.progress_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.progress.unlocked_modules = data.get("unlocked_modules", ["py_mod_01"])
            self.progress.distinction_badges = data.get("distinction_badges", [])
            self.progress.module_scores = data.get("module_scores", {})
        except Exception:
            pass
