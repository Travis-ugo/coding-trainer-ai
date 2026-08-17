import unittest
from coding_trainer_ai.bridge import handle_bridge_request


class TestBridge(unittest.TestCase):

    def test_modules_endpoint(self):
        res = handle_bridge_request("modules", {})
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 9)
        self.assertIn("syntax_guide", res[0])

    def test_analytics_endpoint(self):
        res = handle_bridge_request("analytics", {})
        self.assertIn("user_name", res)
        self.assertIn("predicted_grade", res)
        self.assertTrue(len(res["topic_grades"]) > 0)

    def test_routine_endpoint(self):
        res = handle_bridge_request("routine", {})
        self.assertIn("date_str", res)
        self.assertIn("tasks", res)
        self.assertEqual(len(res["tasks"]), 3)

    def test_flashcards_endpoint(self):
        res = handle_bridge_request("flashcards", {})
        self.assertIsInstance(res, list)
        self.assertTrue(len(res) > 0)

    def test_flashcards_rate_endpoint(self):
        res = handle_bridge_request("flashcards/rate", {"card_id": "py_01", "rating": 5})
        self.assertEqual(res["card_id"], "py_01")
        self.assertIn("interval_days", res)

    def test_syntax_endpoint_safe_execution(self):
        # Test code containing potentially malicious quotes/syntax
        unsafe_code = "def foo():\n    return '''unsafe quote'''"
        res = handle_bridge_request("syntax", {"code": unsafe_code})
        self.assertIn("passed", res)
        self.assertTrue(res["ast_valid"])

    def test_ai_endpoint(self):
        res = handle_bridge_request("ai", {"prompt": "Explain Kalman Filter"})
        self.assertIn("analogy", res)
        self.assertIn("socratic_question", res)

    def test_ros2_endpoint(self):
        res = handle_bridge_request("ros2", {})
        self.assertIn("architecture", res)
        self.assertIn("kinematics", res)


if __name__ == "__main__":
    unittest.main()
