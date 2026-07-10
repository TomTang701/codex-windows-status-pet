"""Reject active governed documents that are absent from the manifest."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from doc_metadata_api import read_front_matter


ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT):
    manifest = json.loads((root / "docs" / "document_manifest.json").read_text(encoding="utf-8"))
    registered = {item["canonical"] for item in manifest["documents"]}
    registered.update(item["translations"]["zh-CN"] for item in manifest["documents"])
    errors = []
    for path in root.rglob("*.md"):
        relative = path.relative_to(root).as_posix()
        metadata = read_front_matter(path)
        if metadata.get("status") == "active" and relative not in registered:
            errors.append(f"orphan active document: {relative}")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("orphan document check passed")
