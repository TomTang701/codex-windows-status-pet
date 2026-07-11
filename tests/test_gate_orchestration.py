import sys
import unittest
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

import run_quality_checks
import run_release_candidate_checks


class GateOrchestrationTests(unittest.TestCase):
    def test_quality_has_no_release_readiness_decision(self):
        commands = run_quality_checks.quality_commands("python")
        flattened = repr(commands)
        self.assertNotIn("check_release_readiness", flattened)
        self.assertNotIn("--strict", flattened)

    def test_release_candidate_requires_strict_compatibility(self):
        commands = run_release_candidate_checks.release_candidate_commands("python")
        self.assertEqual(commands["compatibility_strict"][-1], "--strict")
        self.assertIn("run_quality_checks.py", commands["quality"][1])

    def test_release_candidate_fails_when_any_child_gate_fails(self):
        with mock.patch.object(
            run_release_candidate_checks,
            "run",
            side_effect=[(0, "quality ok"), (0, "package ok"), (1, "blocking evidence"), (0, "clean")],
        ):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(run_release_candidate_checks.main(), 1)

    def test_release_candidate_succeeds_when_every_child_gate_passes(self):
        with mock.patch.object(run_release_candidate_checks, "run", return_value=(0, "ok")):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(run_release_candidate_checks.main(), 0)


if __name__ == "__main__":
    unittest.main()
