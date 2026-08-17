import re
from typing import List, Dict


class DocParser:
    """
    Parses downloaded official Python documentation HTML/Markdown into clean summary snippets.
    """

    @staticmethod
    def strip_html_tags(html_content: str) -> str:
        # Remove script and style elements
        clean = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_content, flags=re.DOTALL)
        # Remove HTML tags
        clean = re.sub(r"<[^>]+>", " ", clean)
        # Collapse multiple whitespaces
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean

    @staticmethod
    def extract_code_examples(html_content: str) -> List[str]:
        # Extract content inside <pre> tags or <code> blocks
        matches = re.findall(r"<pre[^>]*>(.*?)</pre>", html_content, flags=re.DOTALL)
        snippets = []
        for match in matches:
            clean_snippet = re.sub(r"<[^>]+>", "", match).strip()
            if clean_snippet and ("def " in clean_snippet or "for " in clean_snippet or "if " in clean_snippet or "class " in clean_snippet):
                snippets.append(clean_snippet)
        return snippets

    def parse_doc(self, raw_content: str) -> Dict[str, str]:
        text_summary = self.strip_html_tags(raw_content)
        code_examples = self.extract_code_examples(raw_content)
        return {
            "summary": text_summary[:1000] + "..." if len(text_summary) > 1000 else text_summary,
            "snippet_count": str(len(code_examples)),
            "first_example": code_examples[0] if code_examples else "No code example found.",
        }
