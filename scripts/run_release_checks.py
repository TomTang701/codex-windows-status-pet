"""Run the reproducible automated release gate.

Physical monitor, tray, and clean-machine checks remain separate gates in
docs/quality/COMPATIBILITY_MATRIX.md and are intentionally not inferred here.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return completed.returncode, completed.stdout + completed.stderr


def main():
    python = sys.executable
    api_files = [str(path) for path in (ROOT / "scripts" / "api").glob("*.py")]
    checks = {
        "document_manifest": [python, str(ROOT / "scripts" / "check_doc_manifest.py")],
        "document_parity": [python, str(ROOT / "scripts" / "check_doc_parity.py")],
        "compile": [python, "-m", "py_compile", str(ROOT / "scripts" / "codex_status_pet.py"), *api_files],
        "tests": [python, "-m", "unittest", "discover", "-s", "tests", "-q"],
        "release_readiness_report": [python, str(ROOT / "scripts" / "check_release_readiness.py")],
        "startup_audit": [python, str(ROOT / "scripts" / "startup_audit.py")],
    }
    results = {}
    for name, command in checks.items():
        code, output = run(command)
        results[name] = {"passed": code == 0, "output": output.strip()}
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(item["passed"] for item in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
