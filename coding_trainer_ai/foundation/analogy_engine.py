from typing import List, Optional
from coding_trainer_ai.foundation.models import AnalogyCard


class AnalogyEngine:
    """
    Translates technical CS, AI, and Robotics concepts into intuitive analogies
    drawing from History, International Studies, and everyday systems.
    """

    def __init__(self):
        self._cards: List[AnalogyCard] = self._init_default_analogies()

    def _init_default_analogies(self) -> List[AnalogyCard]:
        return [
            AnalogyCard(
                id="analog_001",
                concept="Pointers & Memory Addresses",
                non_cs_domain="History & Archival Cataloging",
                analogy_title="Archive Call Numbers vs Historical Manuscripts",
                analogy_explanation=(
                    "In a national archive, duplicating a 500-page 18th-century treaty for every historian "
                    "would waste immense paper and space. Instead, the catalog gives you a 'Call Number' "
                    "(e.g., Box 42, Shelf 12). A pointer in C++ holds this call number (memory address). "
                    "Dereferencing a pointer (*ptr) means following the call number to open the physical box."
                ),
                technical_translation=(
                    "A variable stores a value directly; a pointer stores the memory address where that value resides. "
                    "Accessing the value requires dereferencing using `*ptr`, while getting the address requires `&var`."
                ),
                example_snippet=(
                    "// C++ Example\n"
                    "int treaty_year = 1648;          // The actual manuscript value\n"
                    "int* ptr = &treaty_year;         // ptr holds the memory address of treaty_year\n"
                    "std::cout << *ptr << std::endl;  // Dereferencing prints 1648"
                ),
                tags=["c++", "memory", "pointers", "foundation"],
            ),
            AnalogyCard(
                id="analog_002",
                concept="Stack vs Heap Memory Allocation",
                non_cs_domain="Desk Workstation vs Archival Warehouse",
                analogy_title="Active Workspace Desk vs Remote Storage Warehouse",
                analogy_explanation=(
                    "The Stack is like your active reading room desk: items are stacked neatly as you work, "
                    "and when a task finishes, you remove the top items (Last In, First Out). Space is quick and automatic. "
                    "The Heap is like requesting space in a large off-site archival warehouse: you can reserve as much "
                    "unstructured space as you need for large collections, but you are responsible for calling the warehouse "
                    "to free up space (delete/free) when done, otherwise the warehouse overflows (memory leak)."
                ),
                technical_translation=(
                    "Stack allocation is managed automatically by the compiler for local function variables. "
                    "Heap allocation uses `new`/`malloc` at runtime for dynamic memory, requiring manual cleanup (`delete`/`free`) "
                    "or smart pointers (`std::unique_ptr`)."
                ),
                example_snippet=(
                    "// Stack (Automatic)\n"
                    "void study() { int doc_count = 5; }\n\n"
                    "// Heap (Dynamic)\n"
                    "int* large_archive = new int[10000]; // Requested from Heap\n"
                    "delete[] large_archive;              // Must be freed!"
                ),
                tags=["c++", "memory", "stack", "heap", "pointers"],
            ),
            AnalogyCard(
                id="analog_003",
                concept="Finite State Machines (FSM)",
                non_cs_domain="Diplomacy & Treaty Ratification",
                analogy_title="Stages of an International Peace Treaty",
                analogy_explanation=(
                    "An international treaty moves through distinct, mutually exclusive states: "
                    "[Drafting] -> [Negotiation] -> [Ratification] -> [Enforcement]. "
                    "A treaty cannot jump directly from [Drafting] to [Enforcement] without receiving a specific valid trigger event "
                    "(e.g., 'All Parties Sign'). State machines enforce that systems only transition through defined, valid pathways."
                ),
                technical_translation=(
                    "A Finite State Machine consists of a finite set of states, a current state, inputs/events, and transition functions "
                    "that map (current_state, event) -> next_state. Crucial in game AI, robotics state control, and parser logic."
                ),
                example_snippet=(
                    "class TreatyFSM:\n"
                    "    def __init__(self):\n"
                    "        self.state = 'DRAFTING'\n\n"
                    "    def handle_event(self, event):\n"
                    "        if self.state == 'DRAFTING' and event == 'SIGN':\n"
                    "            self.state = 'RATIFIED'\n"
                    "        elif self.state == 'RATIFIED' and event == 'ENFORCE':\n"
                    "            self.state = 'ENFORCED'"
                ),
                tags=["python", "architecture", "state-machine", "robotics"],
            ),
            AnalogyCard(
                id="analog_004",
                concept="Graph Traversal & Shortest Path Algorithms",
                non_cs_domain="International Trade Routes & Logistics",
                analogy_title="Historical Silk Road Route Optimization",
                analogy_explanation=(
                    "Imagine merchant caravans navigating the Silk Road connecting Xi'an to Antioch. "
                    "Cities are nodes (vertices) and trade paths are connections (edges) with varying costs (distance, tariffs, hazards). "
                    "Dijkstra's algorithm is like exploring outward step-by-step to guarantee finding the lowest-cost route, "
                    "while A* search adds a geographical compass heuristic pointing toward the destination city."
                ),
                technical_translation=(
                    "Graphs represent networks of vertices connected by weighted edges. "
                    "Dijkstra's algorithm finds shortest paths in weighted graphs using a priority queue. "
                    "A* search improves Dijkstra by using a heuristic function $h(n)$ estimating cost to goal."
                ),
                example_snippet=(
                    "import heapq\n\n"
                    "def dijkstra(graph, start):\n"
                    "    distances = {node: float('inf') for node in graph}\n"
                    "    distances[start] = 0\n"
                    "    pq = [(0, start)]\n"
                    "    while pq:\n"
                    "        d, u = heapq.heappop(pq)\n"
                    "        for v, weight in graph[u]:\n"
                    "            if distances[u] + weight < distances[v]:\n"
                    "                distances[v] = distances[u] + weight\n"
                    "                heapq.heappush(pq, (distances[v], v))\n"
                    "    return distances"
                ),
                tags=["dsa", "graphs", "dijkstra", "robotics", "path-planning"],
            ),
            AnalogyCard(
                id="analog_005",
                concept="ROS 2 Publish / Subscribe Architecture",
                non_cs_domain="International Diplomatic Wire Services",
                analogy_title="News Wire Service (Reuters) vs Embassy Subscribers",
                analogy_explanation=(
                    "A diplomatic news agency (Publisher Node) continuously broadcasts updates onto a named wire topic "
                    "(e.g., 'global_trade_alerts'). Embassies around the world (Subscriber Nodes) tune in to that topic "
                    "to process updates in real time. The news agency doesn't need to know who is listening or how many embassies exist; "
                    "it just publishes data to the topic asynchronously."
                ),
                technical_translation=(
                    "In ROS 2 (Robot Operating System), nodes communicate anonymously over channels called Topics. "
                    "Publishers send data messages to a topic without targeting specific receivers. "
                    "Subscribers register interest in a topic and receive messages via callback functions whenever new data arrives."
                ),
                example_snippet=(
                    "# ROS 2 Python Publisher Example\n"
                    "import rclpy\n"
                    "from std_msgs.msg import String\n\n"
                    "publisher = node.create_publisher(String, 'diplomatic_wire', 10)\n"
                    "msg = String()\n"
                    "msg.data = 'Treaty Signed'\n"
                    "publisher.publish(msg)"
                ),
                tags=["ros2", "robotics", "pub-sub", "architecture"],
            ),
            AnalogyCard(
                id="analog_006",
                concept="Vectors & Matrix Transformations",
                non_cs_domain="Cartography & Historical Map Projections",
                analogy_title="Map Coordinate Grid Stretch & Rotation",
                analogy_explanation=(
                    "A vector is a displacement arrow (like 'travel 5 miles North-East'). "
                    "A matrix transformation acts like re-projecting a historical map (e.g. Mercator vs Azimuthal projection). "
                    "Applying a 2x2 matrix to a vector stretches, rotates, or reflects the coordinate grid, transforming "
                    "every point on the map smoothly."
                ),
                technical_translation=(
                    "A vector represents direction and magnitude in vector space $\\mathbb{R}^n$. "
                    "Matrix-vector multiplication $A\\mathbf{x} = \\mathbf{b}$ transforms vector $\\mathbf{x}$ linearly into new vector $\\mathbf{b}$ "
                    "by scaling and rotating basis vectors."
                ),
                example_snippet=(
                    "import numpy as np\n\n"
                    "# 90-degree counter-clockwise rotation matrix\n"
                    "R = np.array([[0, -1],\n"
                    "              [1,  0]])\n"
                    "v = np.array([1, 0])  # Point facing East\n"
                    "v_transformed = R @ v # Result: [0, 1] (Facing North!)"
                ),
                tags=["math", "linear-algebra", "matrices", "ai"],
            ),
            AnalogyCard(
                id="analog_007",
                concept="Gradient Descent & Loss Landscapes",
                non_cs_domain="Expedition Navigation in Heavy Fog",
                analogy_title="Hiking Down a Misty Mountain to the Lowest Valley",
                analogy_explanation=(
                    "Imagine an 18th-century geographical expedition caught in dense fog on a mountain range. "
                    "Your goal is to reach the lowest sea-level valley floor (minimum loss). "
                    "You cannot see the landscape ahead, but you can feel the slope of the ground under your boots "
                    "(the gradient $\\nabla L$). You take steps in the steepest downhill direction until the ground flattens out."
                ),
                technical_translation=(
                    "Gradient descent is an optimization algorithm used to minimize a loss function $L(\\theta)$. "
                    "It computes the gradient $\\nabla L(\\theta)$ representing the direction of steepest increase, "
                    "and updates parameters $\\theta$ iteratively: $\\theta_{new} = \\theta - \\eta \\nabla L(\\theta)$."
                ),
                example_snippet=(
                    "# Gradient Descent Step in PyTorch\n"
                    "optimizer.zero_grad()\n"
                    "loss = loss_fn(predictions, targets)\n"
                    "loss.backward()  # Calculate gradient (slope under boots)\n"
                    "optimizer.step() # Take step downhill"
                ),
                tags=["math", "ai", "calculus", "machine-learning", "pytorch"],
            ),
            AnalogyCard(
                id="analog_008",
                concept="Bayes' Theorem & Evidence Updating",
                non_cs_domain="Historical Document Verification",
                analogy_title="Evaluating Primary Source Authenticity with New Radiocarbon Evidence",
                analogy_explanation=(
                    "A historian initial believes an unverified medieval document has a 30% chance of being authentic "
                    "(Prior Probability $P(A)$). Then, a laboratory performs radiocarbon ink testing (New Evidence $B$). "
                    "Bayes' Theorem provides the exact formula to update the initial belief into a revised probability "
                    "(Posterior $P(A|B)$) by combining the prior belief with how reliable carbon testing is."
                ),
                technical_translation=(
                    "Bayes' Theorem computes conditional probability $P(A|B) = \\frac{P(B|A) P(A)}{P(B)}$. "
                    "Used extensively in probabilistic AI, Kalman filters for robotics localization, and naive Bayes classification."
                ),
                example_snippet=(
                    "# Bayes Calculation\n"
                    "prior_authentic = 0.30\n"
                    "prob_ink_given_authentic = 0.90\n"
                    "prob_ink_given_fake = 0.10\n\n"
                    "prob_ink = (prob_ink_given_authentic * prior_authentic) + (prob_ink_given_fake * (1 - prior_authentic))\n"
                    "posterior_authentic = (prob_ink_given_authentic * prior_authentic) / prob_ink\n"
                    "# posterior_authentic turns out to be ~79.4%"
                ),
                tags=["math", "probability", "bayes", "robotics", "ai"],
            ),
        ]

    def get_all(self) -> List[AnalogyCard]:
        return self._cards

    def get_by_id(self, card_id: str) -> Optional[AnalogyCard]:
        for card in self._cards:
            if card.id == card_id:
                return card
        return None

    def search(self, query: str) -> List[AnalogyCard]:
        query_lower = query.lower()
        results = []
        for card in self._cards:
            if (
                query_lower in card.concept.lower()
                or query_lower in card.non_cs_domain.lower()
                or query_lower in card.analogy_title.lower()
                or query_lower in card.analogy_explanation.lower()
                or any(query_lower in tag for tag in card.tags)
            ):
                results.append(card)
        return results

    def filter_by_tag(self, tag: str) -> List[AnalogyCard]:
        tag_lower = tag.lower()
        return [card for card in self._cards if tag_lower in [t.lower() for t in card.tags]]
