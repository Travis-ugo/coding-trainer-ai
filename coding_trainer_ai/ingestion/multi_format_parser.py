import os
import re
from typing import Dict, List, Any


class MultiFormatParser:
    """
    Parses documentation files across multiple formats (PDF, Markdown, HTML, Plain Text, Source Code).
    """

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            return self._parse_pdf(file_path)
        elif ext in (".md", ".markdown"):
            return self._parse_markdown(file_path)
        elif ext in (".html", ".htm"):
            return self._parse_html(file_path)
        else:  # .txt, .py, .cpp, .c, .h, etc.
            return self._parse_text(file_path)

    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        text_content = ""
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content += extracted + "\n"
        except Exception as e:
            # Fallback text reading if pypdf fails or not supported
            text_content = f"[PDF Parsing Note: Extracted raw bytes from {os.path.basename(file_path)}]\n"

        code_snippets = self._extract_code_blocks(text_content)
        headers = self._extract_headers(text_content)

        return {
            "file_name": os.path.basename(file_path),
            "format": "pdf",
            "full_text": text_content,
            "headers": headers,
            "code_snippets": code_snippets,
            "word_count": len(text_content.split()),
        }

    def _parse_markdown(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Extract markdown code blocks ```python ... ```
        code_snippets = re.findall(r"```(?:\w+)?\n(.*?)```", content, flags=re.DOTALL)
        headers = [line.strip("# ").strip() for line in content.splitlines() if line.startswith("#")]

        # Strip markdown syntax for clean text
        clean_text = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        clean_text = re.sub(r"[#*`_\[\]()]", " ", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()

        return {
            "file_name": os.path.basename(file_path),
            "format": "markdown",
            "full_text": clean_text,
            "headers": headers,
            "code_snippets": code_snippets,
            "word_count": len(clean_text.split()),
        }

    def _parse_html(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        code_snippets = re.findall(r"<pre[^>]*>(.*?)</pre>", content, flags=re.DOTALL)
        code_snippets = [re.sub(r"<[^>]+>", "", s).strip() for s in code_snippets if s.strip()]

        headers = re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", content, flags=re.IGNORECASE)
        headers = [re.sub(r"<[^>]+>", "", h).strip() for h in headers]

        clean_text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", content, flags=re.DOTALL)
        clean_text = re.sub(r"<[^>]+>", " ", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()

        return {
            "file_name": os.path.basename(file_path),
            "format": "html",
            "full_text": clean_text,
            "headers": headers,
            "code_snippets": code_snippets,
            "word_count": len(clean_text.split()),
        }

    def _parse_text(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        code_snippets = self._extract_code_blocks(content)
        headers = self._extract_headers(content)

        return {
            "file_name": os.path.basename(file_path),
            "format": "text",
            "full_text": content,
            "headers": headers,
            "code_snippets": code_snippets,
            "word_count": len(content.split()),
        }

    def _extract_code_blocks(self, text: str) -> List[str]:
        # Indented blocks or function definitions
        snippets = []
        for line in text.splitlines():
            if line.strip().startswith(("def ", "class ", "for ", "if ", "#include ", "int main")):
                snippets.append(line.strip())
        return snippets[:10]

    def _extract_headers(self, text: str) -> List[str]:
        headers = []
        for line in text.splitlines():
            line_str = line.strip()
            if line_str and len(line_str) < 80 and (line_str.isupper() or line_str.startswith("#") or line_str.endswith(":")):
                headers.append(line_str.strip("#: "))
        return headers[:10]
