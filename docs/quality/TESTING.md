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

The release-validation target is Windows 11 x64 with the normal bottom taskbar. Windows 10, ARM64, 32-bit Windows, and physical alternate-edge taskbars are deferred and non-blocking.

## Commands

```powershell
$py = "<bundled-python>"
& $py scripts/check_doc_parity.py
& $py -m unittest discover -s tests -q
& $py scripts/run_release_checks.py
```

UI changes require deterministic adapter tests plus Windows manual evidence. Display/DPI changes require geometry tests plus the physical compatibility matrix. Security-boundary changes require negative and redaction tests.

Physical records must include date, commit, Windows build, monitor topology, DPI, taskbar position, result, and safe evidence. Tests must not depend on a live Codex account unless explicitly marked manual.

## Minimum matrix

| Change | Minimum evidence |
|---|---|
| Pure policy or parser | Unit and contract fixtures, including malformed input |
| Cross-module state flow | Integration test with injected transport/time/filesystem |
| Tk or tray adapter | UI-contract test plus targeted physical interaction |
| Claimed Windows 11 display/taskbar | Geometry tests plus dated Windows physical record |
| Packaging or launcher | Package smoke, repeated-launch check, clean-machine record |
| Security boundary | Negative, redaction, injection, and sensitive-file checks |

Fixtures must be synthetic, minimal, and credential-free. Real-account execution is disabled in automation; a manual account test requires explicit scope and may record only safe derived state.

## Concurrency, shutdown, and soak

Race tests cover duplicate refresh, stale generation, file-stat changes, tray restart, repeated close, and callbacks arriving during shutdown. An eight-hour soak records memory/process stability, refresh continuity, app-server recovery, tray actions, hide/show, compact transitions, settings edits, and clean final shutdown. A simulated run is labeled automated or platform evidence, never Physical pass.

## Physical record template

Each scenario creates a new `docs/quality/test-records/YYYY-MM-DD-<scenario>.md` with Date, Commit, App version, Windows version/build, monitor topology, DPI, taskbar, steps, expected, actual, result, limitations, and safe evidence. Existing records are append-only evidence and are never overwritten.
