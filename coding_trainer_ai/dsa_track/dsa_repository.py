from typing import List, Optional, Dict
from coding_trainer_ai.dsa_track.models import DSAProblem, DSAPattern


class DSARepository:
    """
    Pre-loaded repository of key DSA problems categorized by algorithmic pattern.
    """

    def __init__(self):
        self._problems: Dict[str, DSAProblem] = self._init_default_problems()

    def _init_default_problems(self) -> Dict[str, DSAProblem]:
        problems = {}

        # ----------------------------------------------------------------------
        # Pattern 1: Two Pointers
        # ----------------------------------------------------------------------
        p1 = DSAProblem(
            id="dsa_two_pointers_01",
            title="Two Sum II - Sorted Array (Two Pointers)",
            pattern=DSAPattern.TWO_POINTERS,
            difficulty="Foundation",
            problem_statement=(
                "Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, "
                "find two numbers such that they add up to a specific `target` number. "
                "Return their 1-based indices `[index1, index2]`."
            ),
            sample_input_output="Input: numbers = [2, 7, 11, 15], target = 9 -> Output: [1, 2]",
            edge_cases=["Exact two elements in array", "Negative numbers in array"],
            plain_english_logic=(
                "1. Initialize `left` pointer at start index 0 and `right` pointer at end index len-1.\n"
                "2. Calculate `current_sum = numbers[left] + numbers[right]`.\n"
                "3. If `current_sum == target`, return `[left + 1, right + 1]`.\n"
                "4. If `current_sum < target`, increment `left += 1` to increase sum.\n"
                "5. If `current_sum > target`, decrement `right -= 1` to decrease sum."
            ),
            time_complexity="O(N)",
            space_complexity="O(1)",
            solution_code=(
                "def two_sum_sorted(numbers, target):\n"
                "    left, right = 0, len(numbers) - 1\n"
                "    while left < right:\n"
                "        s = numbers[left] + numbers[right]\n"
                "        if s == target:\n"
                "            return [left + 1, right + 1]\n"
                "        elif s < target:\n"
                "            left += 1\n"
                "        else:\n"
                "            right -= 1\n"
                "    return []"
            ),
            non_cs_analogy="Two archivists reading inwards from opposite ends of a chronological list of treaties.",
            test_cases=[
                {
                    "function_name": "two_sum_sorted",
                    "inputs": [[2, 7, 11, 15], 9],
                    "expected_output": [1, 2],
                },
                {
                    "function_name": "two_sum_sorted",
                    "inputs": [[2, 3, 4], 6],
                    "expected_output": [1, 3],
                },
            ],
        )
        problems[p1.id] = p1

        # ----------------------------------------------------------------------
        # Pattern 2: Sliding Window
        # ----------------------------------------------------------------------
        p2 = DSAProblem(
            id="dsa_sliding_window_01",
            title="Max Sum Subarray of Size K (Sliding Window)",
            pattern=DSAPattern.SLIDING_WINDOW,
            difficulty="MSc Intermediate",
            problem_statement="Given an array of integers and a number K, find the maximum sum of any contiguous subarray of size K.",
            sample_input_output="Input: arr = [2, 1, 5, 1, 3, 2], K = 3 -> Output: 9 (from [5, 1, 3])",
            edge_cases=["K equals array length", "All elements negative"],
            plain_english_logic=(
                "1. Compute sum of first window of size K.\n"
                "2. Slide window one element right by adding next element and subtracting outgoing left element.\n"
                "3. Track maximum window sum seen."
            ),
            time_complexity="O(N)",
            space_complexity="O(1)",
            solution_code=(
                "def max_sub_array_of_size_k(k, arr):\n"
                "    max_sum = 0\n"
                "    window_sum = sum(arr[:k])\n"
                "    max_sum = window_sum\n"
                "    for i in range(k, len(arr)):\n"
                "        window_sum += arr[i] - arr[i - k]\n"
                "        max_sum = max(max_sum, window_sum)\n"
                "    return max_sum"
            ),
            non_cs_analogy="A 3-year rolling window measuring economic indicators in historical trade data.",
            test_cases=[
                {
                    "function_name": "max_sub_array_of_size_k",
                    "inputs": [3, [2, 1, 5, 1, 3, 2]],
                    "expected_output": 9,
                }
            ],
        )
        problems[p2.id] = p2

        # ----------------------------------------------------------------------
        # Pattern 3: BFS & Graphs
        # ----------------------------------------------------------------------
        p3 = DSAProblem(
            id="dsa_graph_bfs_01",
            title="Breadth-First Search (BFS) Shortest Distance",
            pattern=DSAPattern.BFS_DFS_GRAPHS,
            difficulty="MSc Distinction",
            problem_statement="Given an unweighted graph represented as an adjacency list, find the shortest path distance from start node to target node.",
            sample_input_output="Input: graph = {0:[1,2], 1:[0,3], 2:[0,3], 3:[1,2]}, start=0, target=3 -> Output: 2",
            edge_cases=["Start equals target (distance 0)", "Target disconnected (unreachable)"],
            plain_english_logic=(
                "1. Use a Queue `collections.deque([(start, 0)])` and `visited` set.\n"
                "2. Pop current node and distance.\n"
                "3. If node == target, return distance.\n"
                "4. For each unvisited neighbor, mark visited and push `(neighbor, distance + 1)`."
            ),
            time_complexity="O(V + E)",
            space_complexity="O(V)",
            solution_code=(
                "from collections import deque\n\n"
                "def bfs_shortest_path(graph, start, target):\n"
                "    if start == target: return 0\n"
                "    queue = deque([(start, 0)])\n"
                "    visited = {start}\n"
                "    while queue:\n"
                "        node, dist = queue.popleft()\n"
                "        for neighbor in graph.get(node, []):\n"
                "            if neighbor == target:\n"
                "                return dist + 1\n"
                "            if neighbor not in visited:\n"
                "                visited.add(neighbor)\n"
                "                queue.append((neighbor, dist + 1))\n"
                "    return -1"
            ),
            non_cs_analogy="Concentric ripples spreading outward across a pond from a splash point.",
            test_cases=[
                {
                    "function_name": "bfs_shortest_path",
                    "inputs": [{0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}, 0, 3],
                    "expected_output": 2,
                }
            ],
        )
        problems[p3.id] = p3

        return problems

    def get_all_problems(self) -> List[DSAProblem]:
        return list(self._problems.values())

    def get_problem_by_id(self, problem_id: str) -> Optional[DSAProblem]:
        return self._problems.get(problem_id)

    def get_problems_by_pattern(self, pattern: DSAPattern) -> List[DSAProblem]:
        return [p for p in self._problems.values() if p.pattern == pattern]
