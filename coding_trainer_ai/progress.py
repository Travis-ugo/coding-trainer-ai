import os
import json
from typing import Dict, Any

PROGRESS_FILE_PATH = os.path.join(os.path.dirname(__file__), "resources", "user_progress.json")

DEFAULT_PROGRESS: Dict[str, Any] = {
    "user_name": "MSc Student",
    "background": "Student",
    "streak_days": 1,
    "scores": {
        "py_mod_01": 0.0,
        "py_mod_02": 0.0,
        "py_mod_03": 0.0,
        "py_mod_04": 0.0,
        "py_mod_05": 0.0,
        "dsa_two_pointers": 0.0,
        "dsa_bfs_graphs": 0.0,
        "math_linear_alg": 0.0,
        "math_kalman": 0.0,
        "pytorch_autograd": 0.0,
        "ros2_nodes": 0.0,
        "uk_written_exam": 0.0,
    }
}

def load_user_progress() -> Dict[str, Any]:
    if os.path.exists(PROGRESS_FILE_PATH):
        try:
            with open(PROGRESS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception:
            pass
    return DEFAULT_PROGRESS.copy()

def save_user_progress(progress_data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(PROGRESS_FILE_PATH), exist_ok=True)
    with open(PROGRESS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(progress_data, f, indent=2)

def update_topic_score(topic_id: str, score: float) -> Dict[str, Any]:
    progress = load_user_progress()
    scores = progress.get("scores", {})
    scores[topic_id] = max(scores.get(topic_id, 0.0), float(score))
    progress["scores"] = scores
    save_user_progress(progress)
    return progress
