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
            "WIN10-DEFERRED", "WIN11-X64", "DISPLAY-1", "DISPLAY-2", "TASKBAR-BOTTOM",
            "TASKBAR-ALT", "COMPACT-HOVER", "CLEAN-ENV", "QUOTA-DISPLAY",
            "DISPLAY-RECONNECT", "SINGLE-INSTANCE", "TRAY-RESTORE",
        }
        present = {line.strip("|").split("|", 1)[0].strip() for line in text.splitlines() if line.startswith("|")}
        self.assertEqual(required - present, set())

    def test_partial_physical_rows_block_release(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| ID | Area | Coverage | Status | Blocking | Evidence / next action |\n"
                "|---|---|---|---|---|---|\n"
                "| WIN-10 | Windows | Windows 10 | Pending | Yes | needs a machine |\n"
                "| UNIT | Tests | Unit | Automated pass | No | green |\n",
                encoding="utf-8",
            )
            result = assess(matrix)
            self.assertFalse(result["ready"])
            self.assertEqual(result["blockers"][0]["coverage"], "Windows 10")

    def test_all_pass_rows_are_release_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| ID | Area | Coverage | Status | Blocking | Evidence / next action |\n"
                "|---|---|---|---|---|---|\n"
                "| WIN-11 | Windows | Windows 11 | Physical pass | Yes | verified |\n"
                "| UNIT | Tests | Unit | Automated pass | No | green |\n",
                encoding="utf-8",
            )
            self.assertEqual(assess(matrix), {"ready": True, "blockers": []})

    def test_invalid_status_is_always_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| ID | Area | Coverage | Status | Blocking | Evidence |\n"
                "|---|---|---|---|---|---|\n"
                "| BAD | Tests | Unit | Mostly done | No | vague |\n",
                encoding="utf-8",
            )
            result = assess(matrix)
            self.assertFalse(result["ready"])
            self.assertEqual(result["blockers"][0]["status"], "Invalid")

    def test_automated_pass_can_satisfy_an_explicit_blocking_row(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.md"
            matrix.write_text(
                "| ID | Area | Coverage | Status | Blocking | Evidence |\n"
                "|---|---|---|---|---|---|\n"
                "| CLEAN | Environment | Fresh venv | Automated pass | Yes | verified |\n",
                encoding="utf-8",
            )
            self.assertEqual(assess(matrix), {"ready": True, "blockers": []})
