"""Small dependency-free helpers for document front matter."""

from __future__ import annotations

from datetime import date
from pathlib import Path


def read_front_matter(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return result
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return {}


def parsed_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None
