"""Check structural parity between canonical English and Chinese documents."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from doc_metadata_api import read_front_matter


MANIFEST = Path("docs") / "document_manifest.json"


def structure(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_fence = False
    headings = fences = table_rows = 0
    fence_languages = []
    stable_table_keys = set()
    for line in lines:
        if line.strip().startswith("```"):
            fences += 1
            if not in_fence:
                fence_languages.append(line.strip()[3:].strip())
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        headings += line.startswith("#")
        table_rows += line.strip().startswith("|")
        if line.strip().startswith("|") and not re.match(r"^\|?\s*:?-+", line.strip()):
            first = line.strip("|").split("|", 1)[0].strip()
            stable_table_keys.update(re.findall(r"`([^`]+)`|\b([A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+)\b", first))
    stable_table_keys = {left or right for left, right in stable_table_keys}
    metadata = read_front_matter(path)
    return {
        "headings": headings,
        "fences": fences,
        "table_rows": table_rows,
        "api_names": set(re.findall(r"\b[A-Z][A-Za-z0-9]*(?:[A-Z][A-Za-z0-9]*)+API\b", text)),
        "versions": set(re.findall(r"\b\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?\b", text)),
        "test_ids": {key for key in stable_table_keys if re.fullmatch(r"[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+", key)},
        "stable_table_keys": stable_table_keys,
        "fence_languages": fence_languages,
        "document_version": metadata.get("document_version"),
        "schema_versions": set(re.findall(r"(?i)schema(?:_version|\s*(?:版本|v(?:ersion)?))\s*[`: ]*(\d+)", text)),
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
        for key in (
            "headings", "fences", "table_rows", "api_names", "versions", "test_ids",
            "stable_table_keys", "fence_languages", "document_version", "schema_versions",
        ):
            if left[key] != right[key]:
                errors.append(f"{doc_id}: {key} differs ({left[key]!r} != {right[key]!r})")
    return errors


if __name__ == "__main__":
    problems = check(Path(__file__).resolve().parents[1])
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    documents, _ = load_manifest(Path(__file__).resolve().parents[1])
    print(f"document parity passed for {len(documents)} manifest documents")
