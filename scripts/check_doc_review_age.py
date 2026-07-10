"""Report stale document reviews; strict mode blocks required release documents."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys

from doc_metadata_api import parsed_date, read_front_matter


ROOT = Path(__file__).resolve().parents[1]


def stale_documents(root=ROOT, today=None):
    today = today or date.today()
    manifest = json.loads((root / "docs" / "document_manifest.json").read_text(encoding="utf-8"))
    stale = []
    for document in manifest["documents"]:
        if document["status"] in {"archived", "deprecated"}:
            continue
        metadata = read_front_matter(root / document["canonical"])
        reviewed = parsed_date(metadata.get("last_reviewed"))
        if reviewed is None or (today - reviewed).days > document["review_cycle_days"]:
            stale.append({"id": document["id"], "required_for_release": document["required_for_release"], "last_reviewed": metadata.get("last_reviewed", "invalid")})
    return stale


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    stale = stale_documents()
    for item in stale:
        print(f"stale document: {item['id']} last_reviewed={item['last_reviewed']}")
    blocked = args.strict and any(item["required_for_release"] for item in stale)
    if not stale:
        print("document review age passed")
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
