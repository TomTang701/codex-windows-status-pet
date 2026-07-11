import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from check_release_readiness import assess


class ReleaseReadinessTests(unittest.TestCase):
    def test_partial_physical_rows_block_release(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| Area | Coverage | Status | Evidence / next action |\n"
                "|---|---|---|---|\n"
                "| Display | Mixed DPI | Automated partial | needs a machine |\n"
                "| Tests | Unit | Pass | green |\n",
                encoding="utf-8",
            )
            result = assess(matrix)
            self.assertFalse(result["ready"])
            self.assertEqual(result["blockers"][0]["coverage"], "Mixed DPI")

    def test_deferred_not_claimed_non_blocking_row_is_reported_but_not_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| Area | Coverage | Status | Evidence / next action |\n"
                "|---|---|---|---|\n"
                "| Windows | Windows 10 | Deferred / Not claimed / Non-blocking | outside support |\n"
                "| Tests | Unit | Pass | green |\n",
                encoding="utf-8",
            )
            result = assess(matrix)
            self.assertTrue(result["ready"])
            self.assertEqual(result["blockers"], [])
            self.assertEqual(result["limitations"][0]["coverage"], "Windows 10")
            self.assertEqual(result["passes"][0]["coverage"], "Unit")

    def test_all_pass_rows_are_release_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| Area | Coverage | Status | Evidence / next action |\n"
                "|---|---|---|---|\n"
                "| Windows | Windows 11 | Physical pass | verified |\n"
                "| Tests | Unit | Pass | green |\n",
                encoding="utf-8",
            )
            self.assertEqual(
                assess(matrix),
                {
                    "ready": True,
                    "passes": [
                        {
                            "area": "Windows",
                            "coverage": "Windows 11",
                            "status": "Physical pass",
                            "evidence": "verified",
                        },
                        {
                            "area": "Tests",
                            "coverage": "Unit",
                            "status": "Pass",
                            "evidence": "green",
                        },
                    ],
                    "blockers": [],
                    "limitations": [],
                },
            )
