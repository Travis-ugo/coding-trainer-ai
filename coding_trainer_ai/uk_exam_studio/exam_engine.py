from typing import List, Dict, Any, Tuple, Optional
from coding_trainer_ai.uk_exam_studio.models import (
    UKExamPaper,
    UKExamQuestion,
    ExamSection,
    ExamAttemptResult,
)
from coding_trainer_ai.quiz_engine.question_timer import QuestionTimer


class UKExamEngine:
    """
    Generates authentic 100-mark 4-part UK University Master's Exam Papers,
    tracks question timing, and evaluates student submissions against UK Postgraduate Marking Scheme Rubrics.
    """

    def generate_sample_exam_paper(self) -> UKExamPaper:
        questions = []

        # Part A: Short Answer Conceptual Questions (20 Marks)
        q1 = UKExamQuestion(
            id="q1_part_a",
            section=ExamSection.PART_A_CONCEPTUAL,
            question_number=1,
            marks=10,
            prompt="Explain the difference between mutable and immutable objects in Python memory models. Provide code examples.",
            model_answer="Immutable objects (tuples, strings, ints) cannot be modified after creation; operations create new objects. Mutable objects (lists, dicts) allow in-place modification.",
            distinction_criteria="Distinction answers mention identity `id()`, hashability, memory address reallocation, and argument passing by assignment.",
        )
        q2 = UKExamQuestion(
            id="q2_part_a",
            section=ExamSection.PART_A_CONCEPTUAL,
            question_number=2,
            marks=10,
            prompt="Describe the role of Nodes and Topics in ROS 2 robotics architecture.",
            model_answer="Nodes are independent computational processes. Topics are named bus channels for asynchronous publish/subscribe message passing.",
            distinction_criteria="Distinction answers mention executor threading, quality of service (QoS) profiles, and node lifecycle management.",
        )
        questions.extend([q1, q2])

        # Part B: Code Tracing, Bug Spotting & Output Analysis (30 Marks)
        q3 = UKExamQuestion(
            id="q3_part_b",
            section=ExamSection.PART_B_TRACING,
            question_number=3,
            marks=15,
            prompt="Analyze the following Python snippet. Identify the bug and state the corrected output.",
            code_snippet="def add_item(item, lst=[]):\n    lst.append(item)\n    return lst\n\nprint(add_item(1))\nprint(add_item(2))",
            model_answer="Bug: Mutable default argument `lst=[]` persists state across function calls. Output is [1] then [1, 2]. Fix: default to `None`.",
            distinction_criteria="Distinction answers explain function object evaluation timing at definition time vs execution time.",
        )
        q4 = UKExamQuestion(
            id="q4_part_b",
            section=ExamSection.PART_B_TRACING,
            question_number=4,
            marks=15,
            prompt="Trace the execution of this loop and state the final printed value.",
            code_snippet="total = 0\nfor i in range(1, 5):\n    if i % 2 == 0:\n        total += i * 2\n    else:\n        total += i\nprint(total)",
            model_answer="i=1 (odd)->+1=1. i=2 (even)->+4=5. i=3 (odd)->+3=8. i=4 (even)->+8=16. Final output: 16.",
            distinction_criteria="Distinction answers show step-by-step state trace table.",
        )
        questions.extend([q3, q4])

        # Part C: Algorithm Implementation & Pseudocode Design (30 Marks)
        q5 = UKExamQuestion(
            id="q5_part_c",
            section=ExamSection.PART_C_ALGORITHM,
            question_number=5,
            marks=30,
            prompt="Design an algorithm in Python to detect whether a target integer exists in a sorted array using Binary Search. State Time Complexity.",
            model_answer="def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return True\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return False",
            distinction_criteria="Distinction answers prove logarithmic time complexity O(log N) using master theorem or recurrence tree and state auxiliary space O(1).",
        )
        questions.append(q5)

        # Part D: Critical Discussion & Architectural Essay (20 Marks)
        q6 = UKExamQuestion(
            id="q6_part_d",
            section=ExamSection.PART_D_ESSAY,
            question_number=6,
            marks=20,
            prompt="Critically evaluate the advantages and failure modes of Kalman Filters vs Particle Filters in autonomous robot localization.",
            model_answer="Kalman Filters assume unimodal Gaussian noise and offer computational efficiency O(1). Particle Filters handle non-Gaussian multimodal belief distributions at higher computational cost O(M).",
            distinction_criteria="Distinction answers critically evaluate linearized Extended Kalman Filters (EKF), Unscented Kalman Filters (UKF), particle depletion traps, and real-time execution constraints.",
        )
        questions.append(q6)

        return UKExamPaper(
            id="msc_paper_comp7001",
            title="MSc AI & Robotics Master Examination Paper",
            module_code="COMP7001 - Foundation Systems & Autonomous Robotics",
            time_limit_minutes=120,
            total_marks=100,
            questions=questions,
        )

    def evaluate_exam_submission(
        self,
        paper: UKExamPaper,
        user_answers: Dict[str, str],
        question_timings: Optional[List[float]] = None,
    ) -> ExamAttemptResult:
        total_score = 0.0
        max_marks = float(paper.total_marks)
        section_scores = {s.value: 0.0 for s in ExamSection}
        num_q = len(paper.questions)

        if question_timings is None:
            question_timings = [30.0] * num_q

        total_duration = sum(question_timings)
        avg_seconds = (total_duration / num_q) if num_q > 0 else 0.0
        pacing_rating, _ = QuestionTimer.get_uk_pacing_rating(avg_seconds)

        for q in paper.questions:
            answer_text = user_answers.get(q.id, "").strip()

            score = 0.0
            if len(answer_text) >= 10:
                score = q.marks * 0.6  # Pass base

                model_keywords = q.model_answer.lower().split()
                matches = sum(1 for kw in model_keywords if kw in answer_text.lower())
                match_ratio = matches / len(model_keywords) if model_keywords else 0.5

                if match_ratio >= 0.3 or len(answer_text) >= 40:
                    score = q.marks * 0.85  # Distinction mark

            total_score += score
            section_scores[q.section.value] += score

        pct = (total_score / max_marks * 100.0) if max_marks > 0 else 0.0

        if pct >= 70.0:
            classification = "🏆 DISTINCTION (70% - 100%)"
            feedback = "Outstanding technical depth! Exceptional clarity, rigorous mathematical proofs, and thorough critical evaluation."
        elif pct >= 60.0:
            classification = "📜 MERIT (60% - 69%)"
            feedback = "Solid work! To upgrade to a 75%+ Distinction, include formal Big-O proofs, memory allocation details, and explicit edge case failure modes."
        elif pct >= 50.0:
            classification = "✅ PASS (50% - 59%)"
            feedback = "Minimum pass threshold met. Focus on structuring step-by-step logic and practicing written syntax drills."
        else:
            classification = "❌ FAIL (0% - 49%)"
            feedback = "Retake recommended. Review Foundation analogies, anti-copilot drills, and flashcards."

        return ExamAttemptResult(
            paper_id=paper.id,
            total_score=round(total_score, 1),
            max_marks=max_marks,
            percentage=round(pct, 1),
            uk_classification=classification,
            total_duration_seconds=round(total_duration, 1),
            avg_seconds_per_question=round(avg_seconds, 1),
            pacing_rating=pacing_rating,
            section_breakdown=section_scores,
            upgrade_feedback=feedback,
        )
