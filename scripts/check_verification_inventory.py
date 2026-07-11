"""Validate the canonical release-verification classification inventory."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "docs" / "quality" / "verification-inventory.json"
CLASSIFICATIONS = {"AUTOMATED", "AUTOMATABLE", "PHYSICAL-ONLY", "OBSOLETE", "DUPLICATE"}
DISPOSITIONS = {"pass", "blocker", "limitation", "excluded"}


def validate_inventory(data):
    errors = []
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return ["schema_version must equal 1"]
    items = data.get("items")
    if not isinstance(items, list):
        return ["items must be a list"]

    ids = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"item {index}: must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            errors.append(f"item {index}: id must be a non-empty string")
            continue
        ids.append(item_id)
        classification = item.get("classification")
        disposition = item.get("disposition")
        if classification not in CLASSIFICATIONS:
            errors.append(f"{item_id}: invalid classification: {classification}")
        if disposition not in DISPOSITIONS:
            errors.append(f"{item_id}: invalid disposition: {disposition}")
        if not isinstance(item.get("fact"), str) or not item["fact"].strip():
            errors.append(f"{item_id}: fact must be a non-empty string")
        if not isinstance(item.get("authority"), str) or not item["authority"].strip():
            errors.append(f"{item_id}: authority must be a non-empty string")
        if classification == "PHYSICAL-ONLY" and disposition not in {"limitation", "blocker"}:
            errors.append(f"{item_id}: PHYSICAL-ONLY disposition must be limitation or blocker")

    counts = Counter(ids)
    errors.extend(f"duplicate id: {item_id}" for item_id, count in counts.items() if count > 1)
    known_ids = set(ids)
    for item in items:
        if not isinstance(item, dict) or item.get("classification") != "DUPLICATE":
            continue
        item_id = item.get("id", "item")
        replacement = item.get("replacement")
        if not isinstance(replacement, str) or not replacement.strip():
            errors.append(f"{item_id}: DUPLICATE requires replacement")
        elif replacement not in known_ids:
            errors.append(f"{item_id}: replacement does not exist: {replacement}")
    return errors


def main():
    try:
        data = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = {"valid": False, "errors": [str(exc)], "counts": {}}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    errors = validate_inventory(data)
    counts = Counter(item.get("classification") for item in data.get("items", []) if isinstance(item, dict))
    print(json.dumps({"valid": not errors, "errors": errors, "counts": dict(sorted(counts.items()))}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
