"""Run the repeatable daily quality gate without claiming release readiness."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return completed.returncode, completed.stdout + completed.stderr


def quality_commands(python=None):
    python = python or sys.executable
    return {
        "document_manifest": [python, str(ROOT / "scripts" / "check_doc_manifest.py")],
        "document_metadata": [python, str(ROOT / "scripts" / "check_doc_metadata.py")],
        "document_review_age": [python, str(ROOT / "scripts" / "check_doc_review_age.py")],
        "orphan_documents": [python, str(ROOT / "scripts" / "check_orphan_documents.py")],
        "document_links": [python, str(ROOT / "scripts" / "check_doc_links.py")],
        "version_sources": [python, str(ROOT / "scripts" / "check_version_sources.py")],
        "sensitive_files": [python, str(ROOT / "scripts" / "check_sensitive_files.py")],
        "dependencies": [python, str(ROOT / "scripts" / "check_dependencies.py")],
        "document_parity": [python, str(ROOT / "scripts" / "check_doc_parity.py")],
        "compile": [python, "-m", "compileall", "-q", str(ROOT / "scripts")],
        "tests": [python, "-m", "unittest", "discover", "-s", "tests", "-q"],
        "startup_audit": [python, str(ROOT / "scripts" / "startup_audit.py")],
        "release_readiness_report": [python, str(ROOT / "scripts" / "check_release_readiness.py")],
        "package_smoke": [python, str(ROOT / "scripts" / "package_smoke_test.py")],
    }


def main():
    results = {}
    for name, command in quality_commands().items():
        code, output = run(command)
        results[name] = {"passed": code == 0, "output": output.strip()}
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(item["passed"] for item in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
