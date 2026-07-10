"""Enforce manifest-to-front-matter identity and translation metadata."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from doc_metadata_api import read_front_matter


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"document_id", "status", "document_version", "canonical_language", "translation_pair", "owner", "last_reviewed", "review_cycle_days"}


def check(root=ROOT):
    manifest = json.loads((root / "docs" / "document_manifest.json").read_text(encoding="utf-8"))
    errors = []
    for document in manifest["documents"]:
        canonical = document["canonical"]
        translation = document["translations"]["zh-CN"]
        pair_metadata = []
        for relative, pair in ((canonical, translation), (translation, canonical)):
            metadata = read_front_matter(root / relative)
            missing = sorted(REQUIRED - metadata.keys())
            if missing:
                errors.append(f"{relative}: missing metadata: {', '.join(missing)}")
                continue
            if metadata["document_id"] != document["id"]:
                errors.append(f"{relative}: document_id differs from manifest")
            if metadata["status"] != document["status"]:
                errors.append(f"{relative}: status differs from manifest")
            if metadata["translation_pair"] != pair:
                errors.append(f"{relative}: translation_pair differs from manifest")
            if metadata["owner"] != document["owner"]:
                errors.append(f"{relative}: owner differs from manifest")
            if metadata["review_cycle_days"] != str(document["review_cycle_days"]):
                errors.append(f"{relative}: review_cycle_days differs from manifest")
            pair_metadata.append(metadata)
        if len(pair_metadata) == 2 and pair_metadata[0].get("document_version") != pair_metadata[1].get("document_version"):
            errors.append(f"{document['id']}: document_version differs between languages")
        if document.get("required_for_release") and document.get("status") != "active":
            errors.append(f"{document['id']}: required_for_release document must be active")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("document metadata passed")
