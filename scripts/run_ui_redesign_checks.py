"""Run the fast branch-local gate for the UI redesign worktree."""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    commands = [
        [sys.executable, "-m", "py_compile", "scripts/codex_status_pet.py"],
        [sys.executable, "-m", "unittest", "tests.test_ui_redesign"],
    ]
    for command in commands:
        completed = subprocess.run(command, check=False)
        if completed.returncode:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
