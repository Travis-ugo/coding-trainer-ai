from typing import Dict, Any, List
from coding_trainer_ai.ai_engine import GeminiAIEngine


class SocraticTutor:
    """
    Non-CS Friendly Socratic AI Tutor powered by Gemini AI:
    Provides intuitive Non-CS analogy mappings and guided questions
    to lead learners to solve coding/math problems without giving away raw code.
    """

    def __init__(self):
        self.ai_engine = GeminiAIEngine()

    def generate_socratic_guidance(self, user_query: str) -> Dict[str, Any]:
        if self.ai_engine.config.is_active:
            ai_res = self.ai_engine.generate_socratic_guidance(user_query)
            return {
                "query": user_query,
                "non_cs_analogy": ai_res.non_cs_analogy,
                "conceptual_hint": ai_res.conceptual_hint,
                "socratic_questions": ai_res.socratic_questions,
            }

        # Offline fallback
        query_lower = user_query.lower()

        if "pointer" in query_lower or "memory" in query_lower or "c++" in query_lower:
            analogy = "🏛️ Non-CS Analogy: Think of a pointer as a Library Call Number on an index card, while the object itself is the book on the shelf."
            hint = "A variable holds the book value itself. A pointer holds the call number telling you where the book is stored."
            socratic_questions = [
                "1. If you copy the call number on a piece of paper, does that duplicate the physical book on the shelf?",
                "2. What happens if you change the text inside the book at that call number location?",
            ]
        elif "recursion" in query_lower or "stack" in query_lower or "overflow" in query_lower:
            analogy = "🏛️ Non-CS Analogy: Think of recursion as Russian Matryoshka dolls nesting inside each other."
            hint = "Each function call opens a smaller doll until you reach the smallest solid doll (the Base Case)."
            socratic_questions = [
                "1. What stops the process of nesting smaller dolls from going on infinitely?",
                "2. Is your function calling itself with a strictly smaller or simpler input state on every step?",
            ]
        elif "kalman" in query_lower or "sensor" in query_lower or "filter" in query_lower:
            analogy = "🏛️ Non-CS Analogy: Think of a GPS navigation app balancing its noisy satellite signal against your car's speedometer reading."
            hint = "Kalman filtering computes a weighted average of two uncertain estimations based on their noise variances."
            socratic_questions = [
                "1. If sensor A is extremely noisy and sensor B is highly precise, which one should receive higher weight (Kalman Gain)?",
                "2. How does the covariance (uncertainty) change after combining two independent measurements?",
            ]
        else:
            analogy = "🏛️ Non-CS Analogy: Break the problem down into everyday steps before writing any code."
            hint = "Identify the inputs coming in, the transformations required, and the expected final output format."
            socratic_questions = [
                "1. Can you write out one manual example step-by-step using pen and paper first?",
                "2. What boundary edge case could cause this logic to fail (e.g. empty inputs, zero, negative numbers)?",
            ]

        return {
            "query": user_query,
            "non_cs_analogy": analogy,
            "conceptual_hint": hint,
            "socratic_questions": socratic_questions,
        }
