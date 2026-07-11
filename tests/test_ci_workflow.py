import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class CiWorkflowTests(unittest.TestCase):
    def test_ci_runs_one_authoritative_release_candidate_gate(self):
        text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertEqual(text.count("python scripts/run_release_candidate_checks.py"), 1)
        self.assertNotIn("python scripts/run_quality_checks.py", text)
        self.assertNotIn("python scripts/package_smoke_test.py", text)
        self.assertNotIn("git diff --check", text)
        self.assertIn(".build/codex-windows-status-pet-smoke.zip", text)


if __name__ == "__main__":
    unittest.main()
