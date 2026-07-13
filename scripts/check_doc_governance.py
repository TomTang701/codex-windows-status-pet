"""Enforce the minimal active-Goal and archived-plan governance boundary."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_GOAL_FILES = {
    "ACTIVE_GOAL.md",
    "ACTIVE_VERSION_BRIEF.md",
    "EXECUTION_STATE.md",
    "V0.8.0_RELEASE_GATE_ADJUSTMENT_GOAL.md",
    "README.md",
}
REQUIRED_ARCHIVE_METADATA = {
    "status": "archived",
    "normative": "false",
}


def _front_matter(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    metadata = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return metadata
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return None


def check(root: Path = ROOT):
    errors = []
    goal = root / "Goal"
    if not (goal / "ACTIVE_GOAL.md").is_file():
        errors.append("Goal/ACTIVE_GOAL.md is required")
    if goal.exists():
        for path in sorted(goal.rglob("*")):
            if path.is_dir():
                continue
            relative = path.relative_to(goal).as_posix()
            if relative not in ALLOWED_GOAL_FILES:
                errors.append(f"unapproved Goal file: Goal/{relative}")

    archive = root / "docs" / "archive" / "plans"
    if archive.exists():
        for path in sorted(archive.glob("*.md")):
            metadata = _front_matter(path)
            label = path.relative_to(root).as_posix()
            if metadata is None:
                errors.append(f"{label}: archived plan requires YAML-like front matter")
                continue
            for key, expected in REQUIRED_ARCHIVE_METADATA.items():
                if metadata.get(key, "").lower() != expected:
                    errors.append(f"{label}: {key} must be {expected}")
            target = metadata.get("superseded_by")
            if not target:
                errors.append(f"{label}: superseded_by is required")
            elif not (path.parent / target).resolve().is_file():
                errors.append(f"{label}: superseded_by target is missing: {target}")

    manifest = root / "docs" / "document_manifest.json"
    try:
        documents = json.loads(manifest.read_text(encoding="utf-8")).get("documents", [])
    except (FileNotFoundError, json.JSONDecodeError):
        documents = []  # The dedicated manifest checker owns malformed/missing manifest errors.
    for document in documents:
        if not isinstance(document, dict):
            continue
        canonical = document.get("canonical", "")
        if canonical.startswith("docs/archive/") and document.get("required_for_release") is True:
            errors.append(f"archived document cannot be required for release: {canonical}")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("document governance passed")
