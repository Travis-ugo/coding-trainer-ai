import unittest
import os
import tempfile
from coding_trainer_ai.ingestion import MultiFormatParser, AutoCurriculumGenerator
from coding_trainer_ai.foundation.models import TierLevel


class TestMultiFormatDocIngestion(unittest.TestCase):

    def setUp(self):
        self.parser = MultiFormatParser()
        self.generator = AutoCurriculumGenerator()
        self.temp_dir = tempfile.mkdtemp()

    def test_markdown_parsing(self):
        md_file = os.path.join(self.temp_dir, "test_doc.md")
        with open(md_file, "w", encoding="utf-8") as f:
            f.write("# ROS 2 Architecture Overview\n\nROS 2 uses nodes and topics for communication.\n\n```python\nimport rclpy\n```")

        res = self.parser.parse_file(md_file)
        self.assertEqual(res["format"], "markdown")
        self.assertIn("ROS 2 Architecture Overview", res["headers"])
        self.assertGreaterEqual(len(res["code_snippets"]), 1)
        self.assertIn("import rclpy", res["code_snippets"][0])

    def test_html_parsing(self):
        html_file = os.path.join(self.temp_dir, "test_doc.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write("<html><body><h1>PyTorch Tensors</h1><pre>import torch\nx = torch.tensor([1, 2])</pre></body></html>")

        res = self.parser.parse_file(html_file)
        self.assertEqual(res["format"], "html")
        self.assertIn("PyTorch Tensors", res["headers"])
        self.assertIn("import torch", res["code_snippets"][0])

    def test_text_parsing(self):
        txt_file = os.path.join(self.temp_dir, "notes.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("KEY CONCEPTS:\nLine 1: Pointers in C++\ndef process_pointers():\n    pass")

        res = self.parser.parse_file(txt_file)
        self.assertEqual(res["format"], "text")
        self.assertGreaterEqual(res["word_count"], 5)

    def test_auto_curriculum_generation(self):
        doc_data = {
            "file_name": "pytorch_guide.md",
            "format": "markdown",
            "full_text": "PyTorch provides dynamic computational graphs for deep learning models. Autograd calculates gradients efficiently.",
            "headers": ["PyTorch Fundamentals", "Autograd"],
            "code_snippets": ["import torch\nloss.backward()"],
            "word_count": 150,
        }

        mod = self.generator.generate_module_from_doc(doc_data)
        self.assertIsNotNone(mod)
        self.assertIn("pytorch_guide", mod.id)

        # Check that all 5 tiers exist
        for tier_val in [1, 2, 3, 4, 5]:
            tier_enum = TierLevel(tier_val)
            self.assertIn(tier_enum, mod.tiers)
            t_obj = mod.tiers[tier_enum]
            self.assertTrue(len(t_obj.title) > 0)
            self.assertTrue(len(t_obj.explanation) > 0)

    def test_auto_practice_question_generation(self):
        doc_data = {
            "file_name": "ros2_topics.md",
            "format": "markdown",
            "full_text": "ROS 2 nodes publish messages to topics anonymously.",
            "headers": ["Nodes and Topics"],
            "code_snippets": [],
            "word_count": 50,
        }

        questions = self.generator.generate_practice_questions(doc_data, "mod_ros2")
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0].topic_id, "mod_ros2")
        self.assertIn("ros2_topics.md", questions[0].prompt)


if __name__ == "__main__":
    unittest.main()
