"""Validate manifest-managed reciprocal language switches and link routing."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("docs") / "document_manifest.json"
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _links(path: Path):
    in_fence = False
    links = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            links.extend(MARKDOWN_LINK.findall(line))
    return links


def _resolved(source: Path, target: str, root: Path):
    value = target.strip().strip("<>").split("#", 1)[0].split("?", 1)[0]
    if not value or value.startswith("/") or "://" in value:
        return None
    return (source.parent / value).resolve()


def _load_pairs(root: Path):
    data = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    pairs = {}
    for document in data.get("documents", []):
        english = document.get("canonical")
        chinese = document.get("translations", {}).get("zh-CN")
        if isinstance(english, str) and isinstance(chinese, str):
            pairs[english] = chinese
    return pairs


def check(root: Path = ROOT):
    """Return manifest-aware language-navigation errors."""
    root = root.resolve()
    pairs = _load_pairs(root)
    reverse = {value: key for key, value in pairs.items()}
    managed = set(pairs) | set(reverse)
    errors = []
    for source_relative, counterpart_relative in {**pairs, **reverse}.items():
        source = root / source_relative
        counterpart = root / counterpart_relative
        if not source.exists() or not counterpart.exists():
            continue
        links = _links(source)
        targets = []
        language_switch_found = False
        for label, link in links:
            resolved = _resolved(source, link, root)
            if resolved is None:
                continue
            try:
                target = resolved.relative_to(root).as_posix()
                targets.append(target)
                if target == counterpart_relative:
                    if source_relative in pairs and any(marker in label for marker in ("简体中文", "中文版本")):
                        language_switch_found = True
                    if source_relative in reverse and "English" in label:
                        language_switch_found = True
            except ValueError:
                errors.append(f"{source_relative}: link escapes repository: {link}")
        if not language_switch_found:
            direction = "English-to-Chinese" if source_relative in pairs else "Chinese-to-English"
            errors.append(f"{source_relative}: missing {direction} switch")
        for target in targets:
            if source_relative in pairs and target in reverse and target != counterpart_relative:
                errors.append(f"{source_relative}: wrong-language managed link: {target}")
            if source_relative in reverse and target in pairs and target != counterpart_relative:
                errors.append(f"{source_relative}: wrong-language managed link: {target}")
            if target == counterpart_relative and not language_switch_found:
                errors.append(f"{source_relative}: wrong-language managed link: {target}")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("document navigation passed")
