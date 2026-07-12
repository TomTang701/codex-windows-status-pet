"""Reject local-machine leakage from tracked repository Markdown."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
DRIVE_PATH = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]")
FILE_URI = re.compile(r"file://", re.IGNORECASE)
UNC_PATH = re.compile(r"\\\\[^\\/\s]+[\\/]")
RETIRED_LAUNCHER = "启动Codex状态宠物.cmd"
DEFAULT_REAL_USER_FRAGMENTS = ("tangz",)


def _markdown_files(root: Path):
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "*.md"],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return sorted(root.rglob("*.md"))
    return [root / line for line in completed.stdout.splitlines() if line]


def _links(text):
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield from MARKDOWN_LINK.findall(line)


def check(root: Path = ROOT, *, real_user_fragments=DEFAULT_REAL_USER_FRAGMENTS):
    """Return privacy-boundary errors for tracked Markdown below *root*."""
    root = root.resolve()
    errors = []
    fragments = tuple(fragment.lower() for fragment in real_user_fragments if fragment)
    for source in _markdown_files(root):
        if not source.is_file():
            continue
        relative = source.relative_to(root).as_posix()
        text = source.read_text(encoding="utf-8")
        if DRIVE_PATH.search(text):
            errors.append(f"{relative}: drive-letter absolute local path")
        if FILE_URI.search(text):
            errors.append(f"{relative}: local file URI")
        if UNC_PATH.search(text):
            errors.append(f"{relative}: UNC local/network path")
        if RETIRED_LAUNCHER in text and relative in {"README.md", "README.zh-CN.md"}:
            errors.append(f"{relative}: retired launcher reference")
        if any(fragment in text.lower() for fragment in fragments):
            errors.append(f"{relative}: configured real-user fragment")
        for target in _links(text):
            target = target.strip().strip("<>").split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith("/") or "://" in target:
                continue
            try:
                (source.parent / target).resolve().relative_to(root)
            except ValueError:
                errors.append(f"{relative}: Markdown link escapes repository: {target}")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("document privacy passed")
