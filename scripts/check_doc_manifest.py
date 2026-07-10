"""Validate the document inventory without checking bilingual text structure."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "document_manifest.json"
ALLOWED_CLASSES = {"normative", "descriptive", "evidence", "generated", "historical"}
ALLOWED_STATUSES = {"draft", "proposed", "active", "deprecated", "archived", "generated"}


def check(root: Path = ROOT):
    errors = []
    path = root / "docs" / "document_manifest.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"missing manifest: {path}"]
    except json.JSONDecodeError as exc:
        return [f"invalid manifest JSON: {exc}"]

    if data.get("schema_version") != 1:
        errors.append("manifest schema_version must be 1")
    documents = data.get("documents")
    if not isinstance(documents, list) or not documents:
        return errors + ["manifest documents must be a non-empty list"]

    ids = set()
    paths = set()
    for index, document in enumerate(documents):
        prefix = f"documents[{index}]"
        if not isinstance(document, dict):
            errors.append(f"{prefix} must be an object")
            continue
        doc_id = document.get("id")
        if not isinstance(doc_id, str) or not doc_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
        elif doc_id in ids:
            errors.append(f"duplicate document id: {doc_id}")
        else:
            ids.add(doc_id)
        if document.get("class") not in ALLOWED_CLASSES:
            errors.append(f"{prefix}.class is invalid")
        if document.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{prefix}.status is invalid")
        canonical = document.get("canonical")
        if not isinstance(canonical, str) or not canonical:
            errors.append(f"{prefix}.canonical must be a path")
        elif canonical in paths:
            errors.append(f"duplicate document path: {canonical}")
        else:
            paths.add(canonical)
            if not (root / canonical).is_file():
                errors.append(f"{doc_id}: missing canonical file: {canonical}")
        translations = document.get("translations")
        if not isinstance(translations, dict) or not isinstance(translations.get("zh-CN"), str):
            errors.append(f"{doc_id}: zh-CN translation path is required")
        else:
            translation = translations["zh-CN"]
            if translation in paths:
                errors.append(f"duplicate document path: {translation}")
            paths.add(translation)
            if not (root / translation).is_file():
                errors.append(f"{doc_id}: missing translation file: {translation}")
        if not isinstance(document.get("owner"), str) or not document["owner"].strip():
            errors.append(f"{doc_id}: owner is required")
        if not isinstance(document.get("review_cycle_days"), int) or document["review_cycle_days"] <= 0:
            errors.append(f"{doc_id}: review_cycle_days must be positive")
        if not isinstance(document.get("required_for_release"), bool):
            errors.append(f"{doc_id}: required_for_release must be boolean")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("document manifest passed")
