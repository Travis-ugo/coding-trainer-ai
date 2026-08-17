from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class TopicGrade:
    topic_id: str
    topic_name: str
    score_percentage: float
    grade_label: str
    color_hex: str


@dataclass
class StudentAnalytics:
    user_name: str
    background: str
    selected_track: str
    overall_percentage: float
    predicted_grade: str
    distinction_badges_count: int
    streak_days: int
    topic_grades: List[TopicGrade] = field(default_factory=list)


@dataclass
class DailyRoutineTask:
    title: str
    duration_minutes: int
    task_type: str
    details: str


@dataclass
class DailyRoutine:
    date_str: str
    total_minutes: int
    tasks: List[DailyRoutineTask] = field(default_factory=list)
