"""Check structural parity between canonical English and Chinese documents."""

from __future__ import annotations

from pathlib import Path
import sys


PAIRS = ("README", "API_SPEC", "FILE_SPEC", "CHANGELOG", "PRODUCT_REVIEW", "DEVELOPMENT_PLAN", "COMPATIBILITY_MATRIX")


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


def check(root: Path):
    errors = []
    for base in PAIRS:
        english = root / f"{base}.md"
        chinese = root / f"{base}.zh-CN.md"
        if not english.exists() or not chinese.exists():
            errors.append(f"missing pair: {base}")
            continue
        left, right = structure(english), structure(chinese)
        for key in ("headings", "fences", "table_rows"):
            if left[key] != right[key]:
                errors.append(f"{base}: {key} differs ({left[key]} != {right[key]})")
    return errors


if __name__ == "__main__":
    problems = check(Path(__file__).resolve().parents[1])
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print(f"document parity passed for {len(PAIRS)} pairs")
