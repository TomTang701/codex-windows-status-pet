import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from check_release_readiness import assess


class ReleaseReadinessTests(unittest.TestCase):
    def test_repository_matrix_keeps_required_physical_ids(self):
        matrix = Path(__file__).parents[1] / "docs" / "quality" / "COMPATIBILITY_MATRIX.md"
        text = matrix.read_text(encoding="utf-8")
        required = {
            "WIN-10", "DISPLAY-1", "DPI-MIXED", "TASKBAR-TOP", "TASKBAR-LEFT",
            "TASKBAR-RIGHT", "COMPACT-HOVER", "CLEAN-MACHINE", "INPUT-PASTE",
            "QUOTA-DISPLAY", "DISPLAY-RECONNECT", "WORKAREA-RUNTIME", "SOAK-8H",
        }
        present = {line.strip("|").split("|", 1)[0].strip() for line in text.splitlines() if line.startswith("|")}
        self.assertEqual(required - present, set())

    def test_partial_physical_rows_block_release(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| ID | Area | Coverage | Status | Evidence / next action | Blocking |\n"
                "|---|---|---|---|---|---|\n"
                "| WIN-10 | Windows | Windows 10 | Pending | needs a machine | Yes |\n"
                "| UNIT | Tests | Unit | Automated pass | green | No |\n",
                encoding="utf-8",
            )
            result = assess(matrix)
            self.assertFalse(result["ready"])
            self.assertEqual(result["blockers"][0]["coverage"], "Windows 10")

    def test_all_pass_rows_are_release_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| ID | Area | Coverage | Status | Evidence / next action | Blocking |\n"
                "|---|---|---|---|---|---|\n"
                "| WIN-11 | Windows | Windows 11 | Physical pass | verified | Yes |\n"
                "| UNIT | Tests | Unit | Automated pass | green | No |\n",
                encoding="utf-8",
            )
            self.assertEqual(assess(matrix), {"ready": True, "blockers": []})

    def test_invalid_status_is_always_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| ID | Area | Coverage | Status | Evidence | Blocking |\n"
                "|---|---|---|---|---|---|\n"
                "| BAD | Tests | Unit | Mostly done | vague | No |\n",
                encoding="utf-8",
            )
            result = assess(matrix)
            self.assertFalse(result["ready"])
            self.assertEqual(result["blockers"][0]["status"], "Invalid")
