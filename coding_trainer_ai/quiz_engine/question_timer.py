import time
from typing import Dict, Any, Tuple


class QuestionTimer:
    """
    Measures per-question elapsed time, total quiz/exam session duration,
    and assigns UK Pacing Efficiency Ratings.
    """

    @staticmethod
    def start_timer() -> float:
        return time.time()

    @staticmethod
    def stop_timer(start_time: float) -> float:
        return round(max(0.0, time.time() - start_time), 2)

    @staticmethod
    def format_duration(seconds: float) -> str:
        if seconds < 60.0:
            return f"{seconds:.1f}s"
        minutes = int(seconds // 60)
        rem_seconds = int(seconds % 60)
        return f"{minutes} min{'s' if minutes > 1 else ''} {rem_seconds} sec{'s' if rem_seconds != 1 else ''}"

    @staticmethod
    def get_uk_pacing_rating(avg_seconds_per_question: float) -> Tuple[str, str]:
        """
        Returns (pacing_rating_label, advice_description) based on UK Postgraduate exam standards.
        """
        if avg_seconds_per_question <= 60.0:
            return (
                "⚡ UK DISTINCTION PACE (<60s / question)",
                "Exceptional speed and technical confidence. Optimal time allocation for distinction essays."
            )
        elif avg_seconds_per_question <= 120.0:
            return (
                "⏱️ UK MERIT PACE (60s - 120s / question)",
                "Solid steady pacing. Adequate time remaining for exam review."
            )
        else:
            return (
                "⚠️ OVER-TIME PACING WARNING (>120s / question)",
                "Pacing is slow. Recommend practicing Anti-Copilot syntax drills to build muscle memory."
            )
