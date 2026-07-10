---
document_id: TESTING
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/quality/TESTING.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# Testing

## Required layers

Use Unit, Contract, Integration, UI-contract, Platform, Physical, Packaging, and Soak tests as appropriate. Simulation must never be recorded as physical evidence.

## Commands

```powershell
$py = "<bundled-python>"
& $py scripts/check_doc_parity.py
& $py -m unittest discover -s tests -q
& $py scripts/run_release_checks.py
```

UI changes require deterministic adapter tests plus Windows manual evidence. Display/DPI changes require geometry tests plus the physical compatibility matrix. Security-boundary changes require negative and redaction tests.

Physical records must include date, commit, Windows build, monitor topology, DPI, taskbar position, result, and safe evidence. Tests must not depend on a live Codex account unless explicitly marked manual.
