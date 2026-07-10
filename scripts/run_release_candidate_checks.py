"""Run strict release-candidate checks after the daily quality suite."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from run_quality_checks import ROOT, run


def _version():
    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    return str(manifest["version"]).split("+", 1)[0]


def _artifact_check():
    artifact = ROOT / ".build" / "codex-windows-status-pet-smoke.zip"
    if not artifact.is_file() or artifact.stat().st_size == 0:
        return 1, "package artifact is missing or empty"
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    checksum = artifact.with_suffix(artifact.suffix + ".sha256")
    checksum.write_text(f"{digest}  {artifact.name}\n", encoding="ascii")
    return 0, f"artifact={artifact.name} sha256={digest}"


def _release_metadata_check():
    version = _version()
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    release_guide = (ROOT / "docs" / "governance" / "RELEASE.md").read_text(encoding="utf-8")
    failures = []
    if f"## {version} -" not in changelog:
        failures.append(f"CHANGELOG has no formal {version} section")
    if "rollback" not in release_guide.lower():
        failures.append("release guide has no rollback procedure")
    ref_type = os.environ.get("GITHUB_REF_TYPE")
    ref_name = os.environ.get("GITHUB_REF_NAME")
    if ref_type == "tag" and ref_name != f"v{version}":
        failures.append(f"tag {ref_name!r} does not match v{version}")
    return (1, "; ".join(failures)) if failures else (0, f"release metadata matches {version}")


def main():
    results = {}
    code, output = run([sys.executable, str(ROOT / "scripts" / "run_quality_checks.py")])
    results["quality"] = {"passed": code == 0, "output": output.strip()}
    code, output = run([sys.executable, str(ROOT / "scripts" / "check_release_readiness.py"), "--strict"])
    results["physical_readiness_strict"] = {"passed": code == 0, "output": output.strip()}
    code, output = run([sys.executable, str(ROOT / "scripts" / "check_doc_review_age.py"), "--strict"])
    results["document_review_age_strict"] = {"passed": code == 0, "output": output.strip()}
    for name, check in (("release_metadata", _release_metadata_check), ("artifact_checksum", _artifact_check)):
        code, output = check()
        results[name] = {"passed": code == 0, "output": output}
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(item["passed"] for item in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
