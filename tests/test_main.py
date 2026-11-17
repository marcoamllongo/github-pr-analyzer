import unittest
from main import analyze


class PullRequestAnalysisTests(unittest.TestCase):
    def test_missing_description_is_flagged(self):
        self.assertIn("Missing PR description", analyze({"body": ""}, []))

    def test_valid_description_has_no_warning(self):
        self.assertEqual([], analyze({"body": "Explains implementation", "draft": False}, []))

    def test_draft_is_flagged(self):
        self.assertIn("PR is still a draft", analyze({"body": "Ready soon", "draft": True}, []))

    def test_large_pr_is_flagged(self):
        self.assertTrue(analyze({"body": "Refactor", "changed_files": 11}, []))


if __name__ == "__main__":
    unittest.main()
