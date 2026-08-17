import re
from typing import Dict, Any, List
from coding_trainer_ai.foundation.models import TierLevel, ModuleTier, LearningModule
from coding_trainer_ai.python_trainer.models import PracticeQuestion, QuestionType


class AutoCurriculumGenerator:
    """
    Generates 5-Tier progressive learning modules and practice questions automatically
    from any parsed document (PDF, Markdown, HTML, Text).
    """

    def generate_module_from_doc(self, doc_data: Dict[str, Any]) -> LearningModule:
        file_name = doc_data.get("file_name", "Uploaded_Doc")
        title = f"Auto-Generated Module: {file_name}"
        full_text = doc_data.get("full_text", "")
        code_snippets = doc_data.get("code_snippets", [])
        headers = doc_data.get("headers", [])

        # Extract summary paragraphs
        paragraphs = [p.strip() for p in full_text.split("\n\n") if len(p.strip()) > 30]
        intro_text = paragraphs[0] if paragraphs else full_text[:400]
        second_text = paragraphs[1] if len(paragraphs) > 1 else full_text[400:800]
        sample_code = code_snippets[0] if code_snippets else "# Sample doc code snippet\npass"

        mod = LearningModule(
            id=f"auto_mod_{re.sub(r'[^a-zA-Z0-9_]', '_', file_name)}",
            title=title,
            track="Document-Driven RAG Ingestion Track",
            description=f"Auto-curated 5-tier progression generated from {file_name} ({doc_data.get('format', 'doc')}).",
        )

        # Tier 1: Plain-English Conceptual Overview & Analogy
        mod.tiers[TierLevel.TIER_1_FOUNDATION] = ModuleTier(
            tier_level=TierLevel.TIER_1_FOUNDATION,
            title=f"Tier 1: Conceptual Overview of {file_name}",
            summary=f"Plain-English introduction extracted from {file_name}.",
            explanation=(
                f"Core Concept Overview:\n{intro_text[:500]}\n\n"
                f"Analogy: Think of this document as an official diplomatic briefing document. "
                f"Key topics covered: {', '.join(headers[:5]) if headers else 'Core technical parameters'}."
            ),
            code_or_math_example="# Intuitive Concept Map\nDocument -> Core Definitions -> Operational Procedures",
            uk_distinction_key_takeaway=f"Foundation concept extracted from primary document source {file_name}.",
        )

        # Tier 2: Syntax & Language Basics
        mod.tiers[TierLevel.TIER_2_SYNTAX] = ModuleTier(
            tier_level=TierLevel.TIER_2_SYNTAX,
            title="Tier 2: Syntax Rules & Function Signatures",
            summary="Key syntax definitions and API structures found in doc.",
            explanation=f"Key Section Analysis:\n{second_text[:500]}",
            code_or_math_example=sample_code,
            uk_distinction_key_takeaway="Syntax structures must strictly conform to official documentation specifications.",
        )

        # Tier 3: Intermediate Systems
        mod.tiers[TierLevel.TIER_3_INTERMEDIATE] = ModuleTier(
            tier_level=TierLevel.TIER_3_INTERMEDIATE,
            title="Tier 3: Intermediate Implementation & Systems",
            summary="Applying document concepts in structured software routines.",
            explanation=f"Implementation Context:\n{intro_text[200:700]}",
            code_or_math_example=(
                code_snippets[1] if len(code_snippets) > 1 else sample_code
            ),
            uk_distinction_key_takeaway="Intermediate design requires defensive checks and standard library integration.",
        )

        # Tier 4: Advanced MSc Level
        mod.tiers[TierLevel.TIER_4_ADVANCED_MSC] = ModuleTier(
            tier_level=TierLevel.TIER_4_ADVANCED_MSC,
            title="Tier 4: Advanced MSc Architecture & Internals",
            summary="Technical internal mechanics and memory/algorithmic performance.",
            explanation=(
                f"Advanced Mechanics:\n"
                f"Analyzing internal execution flow and performance characteristics of {file_name}."
            ),
            code_or_math_example="Computational Complexity: O(N) space/time bounds based on document algorithms.",
            uk_distinction_key_takeaway="MSc answers demonstrate deep mechanical sympathy with internal memory layouts and algorithmic complexity.",
        )

        # Tier 5: Exam Distinction Analysis
        mod.tiers[TierLevel.TIER_5_EXAM_DISTINCTION] = ModuleTier(
            tier_level=TierLevel.TIER_5_EXAM_DISTINCTION,
            title="Tier 5: UK Exam Distinction & Critical Analysis",
            summary="Edge cases, potential security/performance traps, and critical evaluation.",
            explanation=(
                f"Critical Discussion & Failure Cases for {file_name}:\n"
                f"Evaluating trade-offs, potential memory leaks, concurrency issues, and edge-case exceptions."
            ),
            code_or_math_example="// Distinction Trap Analysis\nVerify boundary conditions and unexpected input types.",
            uk_distinction_key_takeaway="Distinction answers critically contrast alternative frameworks and analyze failure edge cases.",
        )

        return mod

    def generate_practice_questions(
        self, doc_data: Dict[str, Any], module_id: str
    ) -> List[PracticeQuestion]:
        file_name = doc_data.get("file_name", "Uploaded_Doc")
        headers = doc_data.get("headers", ["Core Concept", "API Usage"])
        
        q1 = PracticeQuestion(
            id=f"auto_q1_{re.sub(r'[^a-zA-Z0-9_]', '_', file_name)}",
            topic_id=module_id,
            question_type=QuestionType.MULTIPLE_CHOICE,
            prompt=f"According to the ingested document '{file_name}', what is a primary focus area?",
            options=[
                f"Implementation details surrounding {headers[0] if headers else 'the module'}.",
                "Graphics rendering pipelines in WebGL.",
                "Kernel device drivers for legacy printers.",
                "Database SQL table normalization rules.",
            ],
            correct_answer=f"Implementation details surrounding {headers[0] if headers else 'the module'}.",
            explanation=f"The document '{file_name}' heavily emphasizes topics such as {', '.join(headers[:3])}.",
            analogy_hint="Refers to the main topic header of the document.",
            uk_msc_distinction_tip="Primary documentation ingestion establishes ground truth API contracts.",
        )

        q2 = PracticeQuestion(
            id=f"auto_q2_{re.sub(r'[^a-zA-Z0-9_]', '_', file_name)}",
            topic_id=module_id,
            question_type=QuestionType.FILL_IN_BLANK,
            prompt=f"What document format was successfully parsed for '{file_name}'?",
            correct_answer=doc_data.get("format", "text"),
            explanation=f"The file format detected and parsed was {doc_data.get('format', 'text')}.",
            analogy_hint="The file extension format.",
            uk_msc_distinction_tip="Multi-format ingestion standardizes documentation into universal 5-tier learning models.",
        )

        return [q1, q2]
