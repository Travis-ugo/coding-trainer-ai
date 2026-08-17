import os
import urllib.request
import urllib.error
from typing import Dict, Optional

PYTHON_DOCS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "resources",
    "python_docs",
)

# Official Python 3 Tutorial URLs from docs.python.org
DOC_URLS = {
    "informal_intro": "https://docs.python.org/3/tutorial/introduction.html",
    "control_flow": "https://docs.python.org/3/tutorial/controlflow.html",
    "data_structures": "https://docs.python.org/3/tutorial/datastructures.html",
    "modules": "https://docs.python.org/3/tutorial/modules.html",
    "errors_exceptions": "https://docs.python.org/3/tutorial/errors.html",
    "classes": "https://docs.python.org/3/tutorial/classes.html",
    "stdlib": "https://docs.python.org/3/tutorial/stdlib.html",
}

DEFAULT_FALLBACK_DOCS = {
    "control_flow": (
        "# Python Control Flow Documentation\n\n"
        "Python uses standard if, elif, and else statements for conditional execution. "
        "The for statement in Python iterates over the items of any sequence (a list or a string), "
        "in the order that they appear in the sequence. Range() generates arithmetic progressions.\n"
    ),
    "data_structures": (
        "# Python Data Structures Documentation\n\n"
        "Data structures in Python include Lists (mutable ordered sequences), Tuples (immutable ordered sequences), "
        "Dictionaries (key-value hash maps), and Sets (unordered collections of unique elements).\n"
    ),
    "classes": (
        "# Python Classes Documentation\n\n"
        "Classes provide a means of bundling data and functionality together. Creating a new class creates a new "
        "type of object, allowing new instances of that type to be made. Each class instance can have attributes "
        "attached to it for maintaining its state.\n"
    ),
}


class DocDownloader:
    """
    Downloads and manages official Python documentation files locally.
    """

    def __init__(self, target_dir: str = PYTHON_DOCS_DIR):
        self.target_dir = target_dir
        os.makedirs(self.target_dir, exist_ok=True)

    def download_all(self) -> Dict[str, str]:
        downloaded = {}
        for key, url in DOC_URLS.items():
            file_path = os.path.join(self.target_dir, f"{key}.html")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    downloaded[key] = f.read()
                continue

            content = self._fetch_url(url)
            if not content:
                # Use bundled fallback content if network is unreachable
                content = DEFAULT_FALLBACK_DOCS.get(key, f"# Python {key} Documentation\n\nOfficial tutorial reference.")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            downloaded[key] = content
        return downloaded

    def _fetch_url(self, url: str) -> Optional[str]:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "CodingTrainerAI/1.0 (Python Documentation Downloader)"},
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.read().decode("utf-8", errors="ignore")
        except Exception:
            return None

    def get_cached_docs(self) -> Dict[str, str]:
        docs = {}
        if not os.path.exists(self.target_dir):
            return self.download_all()
        
        for filename in os.listdir(self.target_dir):
            if filename.endswith(".html") or filename.endswith(".txt"):
                key = os.path.splitext(filename)[0]
                with open(os.path.join(self.target_dir, filename), "r", encoding="utf-8", errors="ignore") as f:
                    docs[key] = f.read()
        if not docs:
            return self.download_all()
        return docs


if __name__ == "__main__":
    downloader = DocDownloader()
    res = downloader.download_all()
    print(f"Downloaded/Cached {len(res)} Python documentation files to {PYTHON_DOCS_DIR}")
