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
    def test_gate_returns_timeout_code_when_a_child_never_exits(self):
        timeout = subprocess.TimeoutExpired(["python", "-m", "unittest"], 120)
        with patch.object(run_ui_redesign_checks.subprocess, "run", side_effect=timeout):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(run_ui_redesign_checks.main(), 124)


if __name__ == "__main__":
    unittest.main()
