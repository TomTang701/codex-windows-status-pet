"""Run the fast branch-local gate for the UI redesign worktree."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHILD_TIMEOUT_SECONDS = 120


def main() -> int:
    commands = [
        [
            sys.executable,
            "-m",
            "py_compile",
            str(ROOT / "scripts" / "codex_status_pet.py"),
            *[str(path) for path in (ROOT / "scripts" / "ui").glob("*.py")],
            *[str(path) for path in (ROOT / "scripts" / "api").glob("*.py")],
        ],
        [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_ui_redesign",
            "tests.test_ui_gate_runner",
        ],
    ]
    for command in commands:
        try:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                check=False,
                timeout=CHILD_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            print(
                f"UI redesign gate timed out after {CHILD_TIMEOUT_SECONDS} seconds: {command[0]}"
            )
            return 124
        if completed.returncode:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
