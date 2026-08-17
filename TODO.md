# Coding Trainer AI - Master Roadmap & TODO 🎓🤖

An intelligent, active-learning software trainer designed specifically to bridge a **History & International Studies** background into a top-tier **UK Master's (MSc) Degree in AI & Robotics**.

---

## 🇬🇧 UK Higher Education Master's Marking Framework & Pass Marks

All quizzes, coursework tasks, and exam simulations in this application strictly mirror the **UK Postgraduate Taught (MSc) Grading Standards**:

```
 🏆 DISTINCTION (70% - 100%)
    - Exceptional technical accuracy, mathematical rigor, flawless code, and critical evaluation of trade-offs.
 
 📜 MERIT (60% - 69%)
    - Solid implementation, clear logical structure, good understanding of algorithms and concepts.
 
 ✅ PASS (50% - 59%) - Minimum Threshold to Unlock Next Level
    - Functional implementation meeting core requirements with basic conceptual understanding.
 
 ❌ FAIL (0% - 49%)
    - Syntax errors, incorrect algorithmic logic, or inadequate theoretical foundation. Requires Retake.
```

---

## 🏛️ System Architecture

```
                               ┌─────────────────────────────────────────┐
                               │     Coding Trainer AI Interface         │
                               │  (Interactive Web Studio & CLI Shell)   │
                               └────────────────────┬────────────────────┘
                                                    │
         ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
         ▼                                          ▼                                          ▼
┌──────────────────┐                      ┌──────────────────┐                      ┌──────────────────┐
│  Doc Ingestion   │                      │ SRS Flashcards & │                      │ UK MSc Exam      │
│  (RAG Curriculum)│                      │ Quiz Pass-Gating │                      │ Marking Simulator│
└────────┬─────────┘                      └────────┬─────────┘                      └────────┬─────────┘
         │                                         │                                         │
         └─────────────────────────────────────────┼─────────────────────────────────────────┘
                                                   │
                                                   ▼
                                       ┌───────────────────────┐
                                       │ Non-CS Socratic Tutor │
                                       │ (Intuitive Analogies) │
                                       └───────────────────────┘
```

---

## 📋 taskList / Development Roadmap

### Phase 1: Foundation & Non-CS Bridge Strategy 🌉
- [x] **1.1 Non-CS Intuitive Analogy Engine**
  - Translate abstract CS concepts into clear analogies (e.g., Pointers = Library Cross-References; State Machines = Historical Treaty Stages; Memory Heap/Stack = Workspace Desks vs Filing Cabinets; Graph Traversal = International Trade Routes).
- [x] **1.2 Math & Greek Notation Rosetta Stone 🔣**
  - Interactive decoder for AI & Robotics math equations ($\nabla L(\theta)$, $\sum_{i=1}^n$, $\mathbf{J} \in \mathbb{R}^{m \times n}$, $\mathbb{E}_{x \sim p}[f(x)]$).
  - Plain-English breakdown of Greek variables ($\alpha, \beta, \theta, \lambda, \sigma, \nabla, \Sigma, \Pi$) and step-by-step LaTeX derivation cards.
- [x] **1.3 Zero-Jargon to MSc Rigor Path**
  - Progressive 5-tier level structure per module:
    - **Tier 1 (Foundation):** Plain-English conceptual introduction & analogies.
    - **Tier 2 (Syntax & Basics):** Core language constructs, functions, typing.
    - **Tier 3 (Intermediate Code):** OOP, Data Structures, Error Handling.
    - **Tier 4 (Advanced MSc Level):** Math proofs, PyTorch/ROS 2 internals, memory & pointers.
    - **Tier 5 (Exam Distinction):** Edge-case analysis, optimization proofs, critical evaluation.

---

### Phase 2: Documentation Ingestion Engine (RAG) 📄
- [x] **2.1 Multi-Format Doc Parser**
  - Support parsing documentation files in PDF (`pypdf`), Markdown, HTML, and Text/Code formats (`MultiFormatParser`).
- [x] **2.2 Auto-Curriculum Level Generator**
  - Automatically chunk uploaded documentation files into progressive 5-tier learning modules and practice questions (`AutoCurriculumGenerator`).

---

### Phase 3: Active Syntax Memory & Anti-Copilot Drills ⚡
- [x] **3.1 Anti-Copilot Syntax Drills (Muscle Memory Builder)**
  - Zero autocomplete allowed. Force typing out full syntaxes from memory (`AntiCopilotEngine`).
  - Immediate visual feedback on character mismatches, indentations, and line diffs.
- [x] **3.2 Paper-and-Pen / No-Compiler Exam Mode 📝**
  - Simulates UK university written exam environments: no IDE squiggles, no auto-formatting, and no compiler error hints (`NoCompilerExamMode`).
  - Evaluates raw code submissions against AST syntax validation and sandboxed test cases.
- [x] **3.3 Fill-in-the-Blank Code Completion**
  - Omit crucial keywords, type hints, or function signatures from snippet templates.
- [x] **3.4 Code Tracing & Output Prediction**
  - Present code snippets with subtle edge cases (scope, mutation, closures, reference passing) and force user to manually trace and predict output.

---

### Phase 4: Flashcards & Spaced Repetition System (SRS) 🎴
- [x] **4.1 SuperMemo SM-2 Algorithm Implementation**
  - Calculate review intervals based on user confidence ratings (0 = Complete Blackout to 5 = Perfect Recall) (`SM2Engine`).
  - Prioritize weak syntax, forgotten functions, and difficult UK exam definitions.
- [x] **4.2 Categorized Flashcard Decks**
  - **Deck 1:** Python Syntax & Memory Models.
  - **Deck 2:** C++ Pointers, Memory Management & STL.
  - **Deck 3:** Data Structures & Algorithms Patterns.
  - **Deck 4:** Math for AI (Linear Algebra, Calculus, Probability Formulas).
  - **Deck 5:** Robotics & ROS 2 Architecture (Nodes, Topics, Actions, Transformation Matrices).
  - **Deck 6:** UK MSc Exam Essay Key Definitions & Theory.

---

### Phase 5: Gated Quizzes & UK Pass-Mark Threshold System 🎯
- [x] **5.1 Cumulative End-of-Module Q&A & Pass-Mark Gate (50% Pass / 70% Distinction)**
  - End-of-lecture Q&A tests Module $N$ plus cumulative review questions from all previous modules ($M_1 \dots M_N$).
  - Enforces **50% Pass / 70% Distinction** degree threshold scoring.
- [x] **5.2 Dynamic Quiz Generator & Retake Variation**
  - Quiz retakes randomize question variations and code parameter inputs so users must demonstrate true understanding rather than memorizing answer choices (`DynamicQuizGenerator`).
- [x] **5.3 Question Types**
  - Multiple Choice Theory, Code Output Prediction, Syntax Correction, Complexity Identification ($O(1), O(N), O(N^2), O(\log N)$), Short Conceptual Explanations.

---

### Phase 6: Data Structures & Algorithms (DSA) Mastery Track 🧩
- [x] **6.1 Pattern Recognition Drills**
  - Categorized learning tracks for key DSA patterns (`DSARepository`):
    - **Array & Strings:** Two Pointers, Sliding Window, Prefix Sum.
    - **LinkedLists & Stacks/Queues:** Fast & Slow Pointers, Monotonic Stack.
    - **Trees & Graphs:** BFS, DFS, Dijkstra's, A* Search, Topological Sort.
    - **Dynamic Programming & Recursion:** Memoization, Tabulation, Backtracking.
    - **Heaps & Hash Tables:** Top K elements, Hash Map frequency.
- [x] **6.2 Step-by-Step UK Whiteboard Mode**
  - Enforces mandatory 5-step presentation (I/O Examples, Edge Cases, Plain-English Logic, Big-O Complexity, Code Execution) (`WhiteboardEvaluator`).

---

### Phase 7: MSc AI & Robotics Specialized Learning Modules 🤖 🎓
- [x] **7.1 Math for AI & Robotics**
  - **Linear Algebra:** Vectors, Matrices, Matrix Multiplication, $SE(2)/SE(3)$ Transformations (`MathAIEngine`).
  - **Calculus & Optimization:** Derivatives, Partial Derivatives, Gradients, Gradient Descent (`MathAIEngine`).
  - **Probability & Statistics:** Bayes' Theorem, Gaussian Distributions, Kalman Filters (`MathAIEngine`).
- [x] **7.2 Machine Learning & Neural Networks**
  - PyTorch tensor operations, autograd computation graphs, linear layers, MSE loss (`PyTorchSandbox`).
- [x] **7.3 Robotics Engineering & Virtual ROS 2 Sandbox**
  - **ROS 2 Architecture:** Nodes, Topics, Publishers, Subscribers, `ros2 topic echo` stream (`VirtualROS2Sandbox`).
  - **Virtual ROS 2 Node Visualizer:** Real-time visual graph of nodes publishing/subscribing to topics (`ros2 topic echo`).
  - **Kinematics & Dynamics:** 2-DOF Forward Kinematics, Transformation Matrices ($T \in SE(3)$).

---

### Phase 8: UK MSc Exam & Coursework Report Simulator 📝 🇬🇧
- [x] **8.1 2-Hour Timed UK Exam Simulator**
  - Formatted like authentic UK university exam papers across Parts A, B, C, and D totaling 100 marks (`UKExamEngine`).
- [x] **8.2 UK Coursework & Technical Report Writing Module 📄**
  - Guidance and LaTeX templates for writing UK Master's lab reports with Matplotlib benchmark plots (`CourseworkReportGenerator`).
- [x] **8.3 UK Marking Scheme Feedback Rubric**
  - Gives percentage score, UK classification (Distinction 70%+, Merit 60%+, Pass 50%+, Fail <50%), and feedback on upgrading Merit to Distinction (`UKExamEngine`).
- [x] **8.4 Non-CS Friendly Socratic AI Tutor**
  - Interactive Socratic AI tutor providing non-jargon guidance and guided questions (`SocraticTutor`).

---

### Phase 9: Web Studio UI, Grade Analytics & Daily Routine 💻
- [x] **9.1 UK Predicted Grade Heatmap & Analytics Dashboard**
  - Visual topic-by-topic grade heatmap (*Distinction 70%+, Merit 60%+, Pass 50%+, Fail <50%*) showing exact UK MSc readiness (`GradeAnalyticsEngine`).
- [x] **9.2 Daily 15-Minute Micro-Study Routine Generator**
  - Daily structured routine: 5 mins SRS Flashcards + 5 mins Anti-Copilot Syntax Drill + 5 mins UK Exam Question (`DailyRoutineGenerator`).
- [x] **9.3 Studio Web Interface & Code Sandbox**
  - Single-page glassmorphic dark-mode web dashboard featuring grade heatmaps, daily routines, and interactive study tools (`WebStudioServer`).

---

## 🗄️ Database Schemas & Data Model

### `users`
```json
{
  "id": 1,
  "name": "MSc Student",
  "background": "History & International Studies",
  "selectedTrack": "MSc AI & Robotics",
  "xp": 1450,
  "level": 3,
  "predictedGrade": "Distinction (72%)",
  "distinctionBadges": 5,
  "streakDays": 14
}
```

### `flashcards` (SRS SuperMemo SM-2)
```json
{
  "cardId": "fc_001",
  "deck": "Math for AI",
  "front": "What is the intuitive meaning of an Eigenvector in a Matrix Transformation?",
  "back": "An eigenvector is a vector whose direction does NOT change when a matrix transformation is applied—it only gets scaled by its eigenvalue.",
  "analogy": "Imagine a stretching sheet of rubber: lines along the stretch direction stay straight (eigenvectors), only growing longer (eigenvalue scale).",
  "easeFactor": 2.5,
  "interval": 6,
  "repetition": 3,
  "nextReviewDate": "2026-08-19"
}
```

### `module_quizzes` (Gated Progression)
```json
{
  "quizId": "quiz_ros2_01",
  "moduleTitle": "ROS 2 Nodes & Topics",
  "passMarkPercent": 50,
  "distinctionMarkPercent": 70,
  "userBestScore": 75,
  "unlockedNextLevel": true,
  "status": "Distinction Badge Earned"
}
```
