"""Run routine automated quality checks without making a release decision."""

from __future__ import annotations

import json
import os
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
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    return completed.returncode, completed.stdout + completed.stderr


def quality_commands(python=sys.executable):
    api_files = [str(path) for path in (ROOT / "scripts" / "api").glob("*.py")]
    all_test_modules = [
        f"tests.{path.stem}"
        for path in sorted((ROOT / "tests").glob("test_*.py"))
    ]
    test_modules = [module for module in all_test_modules if not module.rsplit(".", 1)[-1].startswith("test_ui_")]
    ui_test_modules = [module for module in all_test_modules if module.rsplit(".", 1)[-1].startswith("test_ui_")]
    return {
        "document_manifest": [python, str(ROOT / "scripts" / "check_doc_manifest.py")],
        "document_governance": [python, str(ROOT / "scripts" / "check_doc_governance.py")],
        "document_links": [python, str(ROOT / "scripts" / "check_doc_links.py")],
        "document_privacy": [python, str(ROOT / "scripts" / "check_doc_privacy.py")],
        "document_navigation": [python, str(ROOT / "scripts" / "check_doc_navigation.py")],
        "version_sources": [python, str(ROOT / "scripts" / "check_version_sources.py")],
        "sensitive_files": [python, str(ROOT / "scripts" / "check_sensitive_files.py")],
        "dependencies": [python, str(ROOT / "scripts" / "check_dependencies.py")],
        "document_parity": [python, str(ROOT / "scripts" / "check_doc_parity.py")],
        "verification_inventory": [python, str(ROOT / "scripts" / "check_verification_inventory.py")],
        "compile": [
            python,
            "-m",
            "py_compile",
            str(ROOT / "scripts" / "codex_status_pet.py"),
            str(ROOT / "scripts" / "ui" / "main_window.py"),
            *api_files,
        ],
        "tests_core": [python, "-m", "unittest", *test_modules, "-q"],
        "tests_ui": [python, "-m", "unittest", *ui_test_modules, "-q"],
        "startup_audit": [python, str(ROOT / "scripts" / "startup_audit.py")],
    }


def main():
    results = {}
    for name, command in quality_commands().items():
        code, output = run(command)
        results[name] = {"passed": code == 0, "output": output.strip()}
    approved = all(item["passed"] for item in results.values())
    print(json.dumps({"quality_approved": approved, "checks": results}, ensure_ascii=True, indent=2))
    return 0 if approved else 1


if __name__ == "__main__":
    raise SystemExit(main())
