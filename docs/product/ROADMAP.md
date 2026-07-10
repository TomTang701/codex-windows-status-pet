---
document_id: DEVELOPMENT-PLAN
status: active
document_version: 1.2.0
canonical_language: en
translation_pair: docs/product/ROADMAP.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 30
---
# Codex Windows Status Pet Roadmap

Completed behavior belongs in `CHANGELOG.md`; evidence belongs in the compatibility matrix. Automated test counts are never maintained here.

## Current baseline

Windows 11 x64, Python 3.11 CI/Python 3.12.x local, the root CMD launcher, Tkinter overlay, notification-area icon, and normal bottom taskbar form the v0.3.0 support baseline. Exit: every claimed baseline has a structured compatibility row.

## Now

- Finish the Reset Credit visible record. Exit: dated Windows 11 evidence shows `HH:MM M/D`.
- Reduce Tk-window coordination and split quota presentation into stable rows. Exit: controller and row-contract tests pass.
- Keep Quality green and strict blockers deterministic. Exit: script output matches explicit matrix columns.

## Next

- Complete single-monitor and practical monitor reconnect records. Exit: dated Windows 11 evidence exists.
- Exercise compact idle shrink and hover expansion. Exit: a dated record shows both transitions.
- Complete settings transaction, backup/restore, and repeated shutdown evidence. Exit: claimed-scope rows pass.

## Later

- Evaluate signed packaging after reproducible artifacts and rollback are stable.
- Consider additional local-only presentation modes behind tested API boundaries.
- Review accessibility and optional eight-hour soak evidence.

## Blocked

- v0.3.0 approval is blocked only by incomplete Windows 11 rows explicitly marked `Blocking: Yes`; each row names its next action.

## Deferred

- Windows 10 compatibility investigation; support is not claimed and it does not block v0.3.0.
- ARM64, 32-bit Windows, mixed-DPI certification, alternate-edge physical taskbar tests, and eight-hour soak.

## Out of scope

- Reading `auth.json`, tokens, account IDs, prompt/response/project/session content, or raw quota responses.
- Third-party quota providers, telemetry, hosted backends, or modifying Codex core/built-in pets.
- Claiming physical compatibility from simulation or inferred evidence.
