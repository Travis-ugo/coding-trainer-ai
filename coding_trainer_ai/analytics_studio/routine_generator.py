import datetime
from typing import Optional, List
from coding_trainer_ai.analytics_studio.models import DailyRoutine, DailyRoutineTask


class DailyRoutineGenerator:
    """
    Generates a structured 15-minute daily micro-learning routine
    combining SRS Flashcards, Anti-Copilot Drills, and UK Exam Practice.
    """

    def generate_daily_routine(self, target_date: Optional[datetime.date] = None) -> DailyRoutine:
        if target_date is None:
            target_date = datetime.date.today()

        t1 = DailyRoutineTask(
            title="🎴 5 Mins: SRS Spaced Repetition Due Flashcards",
            duration_minutes=5,
            task_type="SRS_FLASHCARDS",
            details="Review due cards across Python, C++ Memory, DSA, and ROS 2 decks to reinforce SuperMemo SM-2 memory intervals.",
        )

        t2 = DailyRoutineTask(
            title="⚡ 5 Mins: Anti-Copilot Raw Syntax Typing Drill",
            duration_minutes=5,
            task_type="ANTI_COPILOT_SYNTAX",
            details="Type out complex syntax templates with zero autocomplete allowed. Character-by-character diff evaluation.",
        )

        t3 = DailyRoutineTask(
            title="📝 5 Mins: 1 UK Master's University Exam Question",
            duration_minutes=5,
            task_type="UK_EXAM_QUESTION",
            details="Answer 1 written exam question (Part A Conceptual or Part B Code Tracing) with UK Distinction Rubric Feedback.",
        )

        return DailyRoutine(
            date_str=target_date.strftime("%Y-%m-%d"),
            total_minutes=15,
            tasks=[t1, t2, t3],
        )
