from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


class SpecializedTrack(Enum):
    MATH_FOR_AI = "math_for_ai"
    MACHINE_LEARNING_PYTORCH = "machine_learning_pytorch"
    ROS2_ROBOTICS_ENGINEERING = "ros2_robotics_engineering"

    @property
    def display_name(self) -> str:
        names = {
            "math_for_ai": "📐 Math for AI (Linear Algebra, Calculus, Kalman Filters)",
            "machine_learning_pytorch": "🧠 Machine Learning & PyTorch Autograd",
            "ros2_robotics_engineering": "🤖 ROS 2 Architecture & Kinematics Simulator",
        }
        return names.get(self.value, self.value)


@dataclass
class RoboticsTopicMessage:
    topic_name: str
    msg_type: str
    data: Dict[str, Any]
    timestamp: float = 0.0


@dataclass
class RoboticsNode:
    name: str
    published_topics: List[str] = field(default_factory=list)
    subscribed_topics: List[str] = field(default_factory=list)


@dataclass
class TransformationMatrix:
    matrix_data: List[List[float]]
    frame_from: str
    frame_to: str
