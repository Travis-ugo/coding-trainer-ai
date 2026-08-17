import time
import math
from typing import List, Dict, Any, Optional
from coding_trainer_ai.ai_robotics.models import RoboticsNode, RoboticsTopicMessage


class VirtualROS2Sandbox:
    """
    Virtual ROS 2 Graph & Robotics Simulator:
    - Spawns Nodes, Topics, Publishers, and Subscribers
    - Simulates `ros2 topic echo` streaming
    - Simulates 2-DOF Forward Kinematics (End-Effector [x, y] coordinates)
    """

    def __init__(self):
        self.nodes: Dict[str, RoboticsNode] = {}
        self.topic_messages: Dict[str, List[RoboticsTopicMessage]] = {}
        self.subscribers: Dict[str, List[str]] = {}  # topic_name -> list of node names

    def create_node(self, node_name: str) -> RoboticsNode:
        if node_name not in self.nodes:
            self.nodes[node_name] = RoboticsNode(name=node_name)
        return self.nodes[node_name]

    def create_publisher(self, node_name: str, topic_name: str):
        node = self.create_node(node_name)
        if topic_name not in node.published_topics:
            node.published_topics.append(topic_name)
        if topic_name not in self.topic_messages:
            self.topic_messages[topic_name] = []

    def create_subscriber(self, node_name: str, topic_name: str):
        node = self.create_node(node_name)
        if topic_name not in node.subscribed_topics:
            node.subscribed_topics.append(topic_name)
        if topic_name not in self.subscribers:
            self.subscribers[topic_name] = []
        if node_name not in self.subscribers[topic_name]:
            self.subscribers[topic_name].append(node_name)

    def publish_message(
        self, topic_name: str, msg_type: str, data: Dict[str, Any]
    ) -> RoboticsTopicMessage:
        msg = RoboticsTopicMessage(
            topic_name=topic_name,
            msg_type=msg_type,
            data=data,
            timestamp=time.time(),
        )
        if topic_name not in self.topic_messages:
            self.topic_messages[topic_name] = []
        self.topic_messages[topic_name].append(msg)
        return msg

    def echo_topic(self, topic_name: str) -> List[RoboticsTopicMessage]:
        """
        Simulates `ros2 topic echo <topic_name>`
        """
        return self.topic_messages.get(topic_name, [])

    @staticmethod
    def forward_kinematics_2dof(
        l1: float, l2: float, theta1_rad: float, theta2_rad: float
    ) -> Dict[str, float]:
        """
        Computes Forward Kinematics for 2-DOF Planar Robot Arm:
        x = L1 * cos(θ1) + L2 * cos(θ1 + θ2)
        y = L1 * sin(θ1) + L2 * sin(θ1 + θ2)
        """
        x = l1 * math.cos(theta1_rad) + l2 * math.cos(theta1_rad + theta2_rad)
        y = l1 * math.sin(theta1_rad) + l2 * math.sin(theta1_rad + theta2_rad)

        return {
            "end_effector_x": round(x, 4),
            "end_effector_y": round(y, 4),
            "joint_angle_1_deg": round(math.degrees(theta1_rad), 2),
            "joint_angle_2_deg": round(math.degrees(theta2_rad), 2),
        }
