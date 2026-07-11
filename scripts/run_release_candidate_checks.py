"""Run strict Release Candidate gates; success is formal automated approval only."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return completed.returncode, completed.stdout + completed.stderr


def release_candidate_commands(python=sys.executable):
    return {
        "quality": [python, str(ROOT / "scripts" / "run_quality_checks.py")],
        "package_smoke": [python, str(ROOT / "scripts" / "package_smoke_test.py")],
        "compatibility_strict": [python, str(ROOT / "scripts" / "check_release_readiness.py"), "--strict"],
        "whitespace": ["git", "diff", "--check"],
    }


def main():
    results = {}
    for name, command in release_candidate_commands().items():
        code, output = run(command)
        results[name] = {"passed": code == 0, "output": output.strip()}
    approved = all(item["passed"] for item in results.values())
    print(json.dumps({"release_candidate_approved": approved, "checks": results}, ensure_ascii=False, indent=2))
    return 0 if approved else 1


if __name__ == "__main__":
    raise SystemExit(main())
