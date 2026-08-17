from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


class DSAPattern(Enum):
    TWO_POINTERS = "two_pointers"
    SLIDING_WINDOW = "sliding_window"
    PREFIX_SUM = "prefix_sum"
    FAST_SLOW_POINTERS = "fast_slow_pointers"
    MONOTONIC_STACK = "monotonic_stack"
    BFS_DFS_GRAPHS = "bfs_dfs_graphs"
    DIJKSTRA_A_STAR = "dijkstra_a_star"
    DYNAMIC_PROGRAMMING = "dynamic_programming"
    HEAPS_HASH = "heaps_hash"

    @property
    def display_name(self) -> str:
        names = {
            "two_pointers": "Arrays & Strings: Two Pointers",
            "sliding_window": "Arrays & Strings: Sliding Window",
            "prefix_sum": "Arrays & Strings: Prefix Sum",
            "fast_slow_pointers": "LinkedLists: Fast & Slow Pointers",
            "monotonic_stack": "Stacks & Queues: Monotonic Stack",
            "bfs_dfs_graphs": "Trees & Graphs: BFS / DFS Traversal",
            "dijkstra_a_star": "Graphs & Robotics: Dijkstra & A* Search",
            "dynamic_programming": "Recursion & DP: Memoization & Tabulation",
            "heaps_hash": "Heaps & Hash Tables: Top K Elements",
        }
        return names.get(self.value, self.value)


@dataclass
class DSAProblem:
    id: str
    title: str
    pattern: DSAPattern
    difficulty: str  # "Foundation", "MSc Intermediate", "MSc Distinction"
    problem_statement: str
    sample_input_output: str
    edge_cases: List[str] = field(default_factory=list)
    plain_english_logic: str = ""
    time_complexity: str = "O(N)"
    space_complexity: str = "O(1)"
    solution_code: str = ""
    non_cs_analogy: str = ""
    test_cases: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class WhiteboardSubmission:
    problem_id: str
    step1_examples: str
    step2_edge_cases: str
    step3_plain_logic: str
    step4_complexity: str
    step5_code: str


@dataclass
class WhiteboardEvaluation:
    problem_id: str
    passed_all_steps: bool
    step_scores: Dict[str, bool]
    code_passed: bool
    feedback: str
    uk_grade: str
