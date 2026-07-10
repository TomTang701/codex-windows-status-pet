"""Check relative Markdown links across the maintained documentation tree."""

from __future__ import annotations

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _target_path(source: Path, target: str):
    target = target.strip().strip("<>").split("#", 1)[0].split("?", 1)[0]
    if not target or target.startswith("/"):
        return None
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc:
        return None
    return (source.parent / unquote(target)).resolve()


def check(root: Path = ROOT):
    errors = []
    for source in sorted(root.rglob("*.md")):
        if ".git" in source.parts or ".build" in source.parts:
            continue
        text = source.read_text(encoding="utf-8")
        in_fence = False
        links = []
        for line in text.splitlines():
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                links.extend(MARKDOWN_LINK.findall(line))
        for target in links:
            resolved = _target_path(source, target)
            if resolved is None:
                continue
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{source.relative_to(root)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{source.relative_to(root)}: missing link target: {target}")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("documentation links passed")
