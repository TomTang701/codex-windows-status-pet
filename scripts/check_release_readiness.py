"""Report whether physical compatibility gates permit a v0.3.0 release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_STATUSES = {"Pending", "Automated pass", "Physical pass", "Partial", "Deferred", "Not applicable", "Approved limitation", "Blocked"}
RELEASE_READY_STATUSES = {"Automated pass", "Physical pass", "Not applicable", "Approved limitation"}


def assess(matrix_path=ROOT / "docs" / "quality" / "COMPATIBILITY_MATRIX.md"):
    blockers = []
    for line in Path(matrix_path).read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 6 or cells[0] == "ID":
            continue
        test_id, area, coverage, status, blocking, evidence = cells[:6]
        if status not in ALLOWED_STATUSES:
            blockers.append({"id": test_id, "area": area, "coverage": coverage, "status": "Invalid", "evidence": f"unsupported status: {status}"})
        elif blocking == "Yes" and status not in RELEASE_READY_STATUSES:
            blockers.append({"id": test_id, "area": area, "coverage": coverage, "status": status, "evidence": evidence})
    return {"ready": not blockers, "blockers": blockers}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="return failure while any physical gate remains")
    args = parser.parse_args()
    result = assess()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.strict and not result["ready"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
