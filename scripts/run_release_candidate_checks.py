"""Run strict Release Candidate gates; success is formal automated approval only."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
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
    passes = []
    blockers = []
    limitations = []
    for name, command in release_candidate_commands().items():
        code, output = run(command)
        results[name] = {"passed": code == 0, "output": output.strip()}
        if code == 0:
            passes.append(name)
        else:
            blockers.append({"check": name, "output": output.strip()})
        if name == "compatibility_strict":
            try:
                readiness = json.loads(output)
            except json.JSONDecodeError:
                readiness = {}
            limitations.extend(readiness.get("limitations", []))
    approved = not blockers
    print(
        json.dumps(
            {
                "release_candidate_approved": approved,
                "passes": passes,
                "blockers": blockers,
                "limitations": limitations,
                "checks": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if approved else 1


if __name__ == "__main__":
    raise SystemExit(main())
