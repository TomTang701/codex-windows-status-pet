"""Check structural parity between canonical English and Chinese documents."""

from __future__ import annotations

import json
from pathlib import Path
import sys


MANIFEST = Path("docs") / "document_manifest.json"


def structure(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    in_fence = False
    headings = fences = table_rows = 0
    for line in lines:
        if line.strip().startswith("```"):
            fences += 1
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        headings += line.startswith("#")
        table_rows += line.strip().startswith("|")
    return {
        "headings": headings,
        "fences": fences,
        "table_rows": table_rows,
    }


def load_manifest(root: Path):
    path = root / MANIFEST
    if not path.exists():
        return None, [f"missing manifest: {MANIFEST.as_posix()}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"invalid manifest: {exc}"]
    if data.get("schema_version") != 1:
        return None, ["unsupported manifest schema_version"]
    documents = data.get("documents")
    if not isinstance(documents, list):
        return None, ["manifest documents must be a list"]
    ids = [item.get("id") for item in documents if isinstance(item, dict)]
    errors = []
    if len(ids) != len(set(ids)):
        errors.append("manifest document IDs must be unique")
    return documents, errors


def check(root: Path):
    documents, errors = load_manifest(root)
    if documents is None:
        return errors
    for document in documents:
        if not isinstance(document, dict):
            errors.append("manifest document entries must be objects")
            continue
        doc_id = document.get("id", "<missing-id>")
        canonical_value = document.get("canonical")
        if not isinstance(canonical_value, str):
            errors.append(f"{doc_id}: missing canonical path")
            continue
        english = root / canonical_value
        if not english.exists():
            errors.append(f"{doc_id}: missing canonical: {canonical_value}")
            continue
        translations = document.get("translations", {})
        if not isinstance(translations, dict):
            errors.append(f"{doc_id}: translations must be an object")
            continue
        chinese_value = translations.get("zh-CN")
        if not isinstance(chinese_value, str):
            errors.append(f"{doc_id}: missing zh-CN translation path")
            continue
        chinese = root / chinese_value
        if not chinese.exists():
            errors.append(f"{doc_id}: missing translation: {chinese_value}")
            continue
        left, right = structure(english), structure(chinese)
        for key in ("headings", "fences", "table_rows"):
            if left[key] != right[key]:
                errors.append(f"{doc_id}: {key} differs ({left[key]} != {right[key]})")
    return errors


if __name__ == "__main__":
    problems = check(Path(__file__).resolve().parents[1])
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    documents, _ = load_manifest(Path(__file__).resolve().parents[1])
    print(f"document parity passed for {len(documents)} manifest documents")
