import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

import run_ui_redesign_checks


class UiGateRunnerTests(unittest.TestCase):
    def test_gate_commands_are_anchored_to_this_worktree(self):
        completed = subprocess.CompletedProcess(["python"], 0)
        with patch.object(run_ui_redesign_checks.subprocess, "run", return_value=completed) as run:
            run_ui_redesign_checks.main()
        self.assertEqual(run.call_count, 2)
        compile_command = run.call_args_list[0].args[0]
        self.assertIn(str(run_ui_redesign_checks.ROOT / "scripts" / "codex_status_pet.py"), compile_command)
        self.assertEqual(run.call_args_list[0].kwargs["cwd"], run_ui_redesign_checks.ROOT)

    def test_gate_returns_timeout_code_when_a_child_never_exits(self):
        timeout = subprocess.TimeoutExpired(["python", "-m", "unittest"], 120)
        with patch.object(run_ui_redesign_checks.subprocess, "run", side_effect=timeout):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(run_ui_redesign_checks.main(), 124)


if __name__ == "__main__":
    unittest.main()
