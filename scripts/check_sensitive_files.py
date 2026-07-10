"""Reject high-confidence credential files or secret material in the repository."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    "auth.json",
    "credentials.json",
    "secrets.json",
}
SENSITIVE_SUFFIXES = (".pem", ".key", ".pfx", ".p12", ".crt")
SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("github-token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
)


def _files(root: Path):
    ignored = {".git", ".build", "__pycache__"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in ignored for part in path.parts):
            continue
        if path.suffix.lower() in {".pyc", ".tmp", ".bak", ".log"}:
            continue
        yield path


def check(root: Path = ROOT):
    errors = []
    for path in _files(root):
        relative = path.relative_to(root).as_posix()
        if path.name.lower() in SENSITIVE_NAMES or path.suffix.lower() in SENSITIVE_SUFFIXES:
            errors.append(f"sensitive filename: {relative}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"possible {label} material: {relative}")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("sensitive-file scan passed")
