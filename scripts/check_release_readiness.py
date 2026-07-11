"""Report whether physical compatibility gates permit a v0.3.0 release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def assess(matrix_path=ROOT / "docs" / "quality" / "COMPATIBILITY_MATRIX.md"):
    passes = []
    blockers = []
    limitations = []
    for line in Path(matrix_path).read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4 or cells[0] == "Area":
            continue
        status = cells[2]
        item = {"area": cells[0], "coverage": cells[1], "status": status, "evidence": cells[3]}
        normalized = status.lower()
        if "non-blocking" in normalized:
            limitations.append(item)
        elif normalized == "pending" or "partial" in normalized:
            blockers.append(item)
        else:
            passes.append(item)
    return {"ready": not blockers, "passes": passes, "blockers": blockers, "limitations": limitations}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="return failure while any physical gate remains")
    args = parser.parse_args()
    result = assess()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.strict and not result["ready"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
