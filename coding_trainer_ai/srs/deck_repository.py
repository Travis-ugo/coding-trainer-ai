import os
import json
import datetime
from typing import List, Dict, Optional
from coding_trainer_ai.srs.models import Flashcard, FlashcardDeck
from coding_trainer_ai.srs.sm2_engine import SM2Engine

SRS_STATE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "resources",
    "srs_state.json",
)


class DeckRepository:
    """
    Manages pre-loaded study decks across 6 domains and persists user SM-2 card states to disk.
    """

    def __init__(self, state_file: str = SRS_STATE_FILE):
        self.state_file = state_file
        self.sm2 = SM2Engine()
        self._decks: Dict[str, FlashcardDeck] = self._init_default_decks()
        self.load_state()

    def _init_default_decks(self) -> Dict[str, FlashcardDeck]:
        decks = {}

        # ----------------------------------------------------------------------
        # Deck 1: Python Syntax & Memory Models
        # ----------------------------------------------------------------------
        d1 = FlashcardDeck(
            id="deck_python",
            name="Deck 1: Python Syntax & Memory Models",
            description="Core Python memory references, data structures, scoping, and idiomatic syntax.",
            cards=[
                Flashcard(
                    id="fc_py_01",
                    deck_id="deck_python",
                    front="How are variables stored in Python memory?",
                    back="Variables in Python are 'Name Tags' bound to objects in memory. Variables have no fixed type; only the object has a type.",
                    non_cs_analogy="Sticky name tags stuck onto physical items.",
                ),
                Flashcard(
                    id="fc_py_02",
                    deck_id="deck_python",
                    front="What is the LEGB rule in Python variable scoping?",
                    back="LEGB stands for Local -> Enclosing -> Global -> Built-in. It defines the order Python searches for variable names.",
                    non_cs_analogy="Desk -> Office -> Building -> City Directory.",
                ),
                Flashcard(
                    id="fc_py_03",
                    deck_id="deck_python",
                    front="Why should you never use `lst=[]` as a default argument in a function definition?",
                    back="Default arguments are evaluated ONCE when the function is defined, making the default list instance shared across all function calls.",
                    non_cs_analogy="Sharing a single physical binder across multiple independent meetings.",
                ),
            ],
        )
        decks[d1.id] = d1

        # ----------------------------------------------------------------------
        # Deck 2: C++ Pointers, Memory Management & STL
        # ----------------------------------------------------------------------
        d2 = FlashcardDeck(
            id="deck_cpp",
            name="Deck 2: C++ Pointers, Memory Management & STL",
            description="Pointers, Stack vs Heap, RAII, and smart pointer mechanics.",
            cards=[
                Flashcard(
                    id="fc_cpp_01",
                    deck_id="deck_cpp",
                    front="What is a pointer in C++?",
                    back="A pointer is a variable holding a memory address where another value is stored.",
                    non_cs_analogy="An archival library call number (Box 4, Shelf 12).",
                ),
                Flashcard(
                    id="fc_cpp_02",
                    deck_id="deck_cpp",
                    front="What is the difference between Stack and Heap memory?",
                    back="Stack allocation is fast and managed automatically by compiler scope (LIFO). Heap allocation is dynamic (`new`/`delete`) and requires explicit cleanup.",
                    non_cs_analogy="Active reading room desk vs Off-site storage warehouse.",
                ),
                Flashcard(
                    id="fc_cpp_03",
                    deck_id="deck_cpp",
                    front="What is RAII in modern C++?",
                    back="RAII (Resource Acquisition Is Initialization) ties resource ownership (memory, file handles) to object lifetime, automatically releasing resources on scope exit.",
                    non_cs_analogy="A self-locking vault door that locks when you step out of the room.",
                ),
            ],
        )
        decks[d2.id] = d2

        # ----------------------------------------------------------------------
        # Deck 3: Data Structures & Algorithms Patterns
        # ----------------------------------------------------------------------
        d3 = FlashcardDeck(
            id="deck_dsa",
            name="Deck 3: Data Structures & Algorithms Patterns",
            description="Pattern recognition for two pointers, sliding window, BFS, DFS, and Dijkstra's algorithm.",
            cards=[
                Flashcard(
                    id="fc_dsa_01",
                    deck_id="deck_dsa",
                    front="When is the Two Pointers pattern optimal?",
                    back="When searching for pairs or target conditions in a sorted array or reversing sequences in-place in O(N) time and O(1) space.",
                    non_cs_analogy="Two archivists starting from opposite ends of a row of manuscripts meeting in the middle.",
                ),
                Flashcard(
                    id="fc_dsa_02",
                    deck_id="deck_dsa",
                    front="What is the key difference between BFS and DFS graph traversals?",
                    back="BFS explores level-by-level using a Queue (finds shortest unweighted path). DFS explores deep down a path first using a Stack or Recursion.",
                    non_cs_analogy="Concentric ripple rings in a pond (BFS) vs Following a single thread through a maze (DFS).",
                ),
            ],
        )
        decks[d3.id] = d3

        # ----------------------------------------------------------------------
        # Deck 4: Math for AI (Linear Algebra, Calculus, Probability)
        # ----------------------------------------------------------------------
        d4 = FlashcardDeck(
            id="deck_math_ai",
            name="Deck 4: Math for AI (Linear Algebra, Calculus, Probability)",
            description="Intuitively decoding gradients, Jacobians, Bayes' theorem, and expectation formulas.",
            cards=[
                Flashcard(
                    id="fc_math_01",
                    deck_id="deck_math_ai",
                    front="What does the Gradient Vector ∇L(θ) represent?",
                    back="A multivariable derivative vector pointing in the direction of steepest loss (error) increase.",
                    non_cs_analogy="The slope under your boots when hiking in heavy fog.",
                ),
                Flashcard(
                    id="fc_math_02",
                    deck_id="deck_math_ai",
                    front="What is the Jacobian Matrix J?",
                    back="A matrix of first-order partial derivatives mapping output velocity changes to input parameter rates.",
                    non_cs_analogy="A coordinate transformation map.",
                ),
                Flashcard(
                    id="fc_math_03",
                    deck_id="deck_math_ai",
                    front="What is Bayes' Theorem formula and core concept?",
                    back="P(A|B) = [P(B|A) * P(A)] / P(B). It updates a prior belief P(A) with new evidence B into posterior probability P(A|B).",
                    non_cs_analogy="Updating authenticity probability of a historical manuscript after carbon-dating tests.",
                ),
            ],
        )
        decks[d4.id] = d4

        # ----------------------------------------------------------------------
        # Deck 5: Robotics & ROS 2 Architecture
        # ----------------------------------------------------------------------
        d5 = FlashcardDeck(
            id="deck_ros2",
            name="Deck 5: Robotics & ROS 2 Architecture",
            description="Nodes, Topics, Services, Actions, Executors, and TF transformations.",
            cards=[
                Flashcard(
                    id="fc_ros_01",
                    deck_id="deck_ros2",
                    front="How does ROS 2 Publish/Subscribe Topic communication work?",
                    back="Nodes publish data messages asynchronously onto named channels (Topics). Subscribers receive data via callbacks without direct node pairing.",
                    non_cs_analogy="A news wire agency (Reuters) publishing to subscribing embassy radios.",
                ),
                Flashcard(
                    id="fc_ros_02",
                    deck_id="deck_ros2",
                    front="What is the difference between a ROS 2 Service and an Action?",
                    back="Services are synchronous request-response calls. Actions are non-blocking long-running goals providing continuous feedback and cancellation.",
                    non_cs_analogy="Quick diplomatic phone inquiry (Service) vs Ordering a multi-week diplomatic expedition (Action).",
                ),
            ],
        )
        decks[d5.id] = d5

        # ----------------------------------------------------------------------
        # Deck 6: UK MSc Exam Essay Key Definitions & Theory
        # ----------------------------------------------------------------------
        d6 = FlashcardDeck(
            id="deck_uk_msc",
            name="Deck 6: UK MSc Exam Essay Key Definitions & Theory",
            description="Critical evaluation terms required to earn 70%+ Distinction marks in UK written exams.",
            cards=[
                Flashcard(
                    id="fc_msc_01",
                    deck_id="deck_uk_msc",
                    front="What distinguishes a UK MSc Distinction (70%+) essay answer from a Merit (60-69%) answer?",
                    back="Distinction answers demonstrate critical evaluation of trade-offs, rigorous mathematical/algorithmic proof, and analysis of edge-case failure modes.",
                    non_cs_analogy="Providing critical historical analysis of treaty consequences rather than merely summarizing dates.",
                ),
            ],
        )
        decks[d6.id] = d6

        return decks

    def get_all_decks(self) -> List[FlashcardDeck]:
        return list(self._decks.values())

    def get_deck_by_id(self, deck_id: str) -> Optional[FlashcardDeck]:
        return self._decks.get(deck_id)

    def get_due_cards(self, deck_id: Optional[str] = None) -> List[Flashcard]:
        today = datetime.date.today()
        due_list = []

        decks_to_check = [self._decks[deck_id]] if deck_id and deck_id in self._decks else self._decks.values()
        for deck in decks_to_check:
            for card in deck.cards:
                if self.sm2.is_due(card, today):
                    due_list.append(card)
        return due_list

    def save_state(self):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        state_data = {}
        for deck_id, deck in self._decks.items():
            state_data[deck_id] = [card.to_dict() for card in deck.cards]

        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2)

    def load_state(self):
        if not os.path.exists(self.state_file):
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)

            for deck_id, cards_data in state_data.items():
                if deck_id in self._decks:
                    existing_deck = self._decks[deck_id]
                    # Update existing cards with saved SRS parameters
                    saved_dict = {c_data["id"]: c_data for c_data in cards_data}
                    for card in existing_deck.cards:
                        if card.id in saved_dict:
                            c_data = saved_dict[card.id]
                            card.ease_factor = c_data.get("ease_factor", card.ease_factor)
                            card.interval_days = c_data.get("interval_days", card.interval_days)
                            card.repetitions = c_data.get("repetitions", card.repetitions)
                            card.due_date = c_data.get("due_date", card.due_date)
                            card.last_reviewed = c_data.get("last_reviewed", card.last_reviewed)
        except Exception:
            pass  # Fallback to defaults on error
