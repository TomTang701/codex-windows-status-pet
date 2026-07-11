# ACTIVE VERSION BRIEF — v0.3.2 Windows 11 Stabilization

## Identity

- Version: `0.3.2`
- Branch: `release/v0.3.2-windows11-stabilization`
- Base: `main` at `d4a69e9ce4a6adc7d519ff1a37b00617d548e8dd`
- PR: `[v0.3.2] Complete Windows 11 release stabilization`
- Tag: `v0.3.2`

## Product

- One-sentence outcome: The declared Windows 11 x64 scope has truthful physical evidence or explicit approved environment limitations, and strict Release Candidate passes.
- Target user: A Windows 11 x64 Codex user relying on the overlay continuously.
- Success criteria: Launch/relaunch, one-instance/no-console, five rows, Reset Credit date path, menu/settings, hide/show, tray recovery, secondary coordinates, compact interaction, and exit are verified; no blocking matrix row remains; strict RC exits 0.
- Explicit non-goals: New feature, any v0.4.0 work, Windows 10 claim, ARM64/32-bit claim, UI redesign, new setting, controller refactor, dependency change.
- Execution exclusions: No browser automation and no new network, IPC, worker, timer, or polling path.
- Decision: GO

## Applicability Matrix

| Role | Applicable | Decision |
|---|---:|---|
| Product | Yes | GO |
| Visual/UI/UX | Physical verification only | PASS pending evidence |
| Frontend | Yes | PASS pending evidence |
| Backend | Lifecycle/process verification only | PASS pending evidence |
| QA/Release | Yes | PASS pending evidence |
| Security/Resource | Yes | PASS pending evidence |
| Repository administration | Yes | PASS pending evidence |

## Physical Windows 11 Matrix

- Current host/build and architecture are recorded from authoritative OS probes.
- Current monitor topology, work areas, taskbar edge, DPI, overlay HWND/DPI, and secondary coordinates are recorded.
- Root launcher is run twice; one overlay/tray and no persistent CMD are verified.
- Main overlay visibly has five rows and Reset Credit uses truthful available data (date appears only when supplied).
- Right-click menu has exactly five items, first click works, settings remains visible, hide/show recovers, and exit/relaunch works.
- Compact shrink/hover-expand is tested through genuine existing application idle behavior; if the active Codex session prevents idle, the limitation is recorded without adding a debug path.
- Decision: PASS only with saved dated evidence.

## Environment Limitations

- Single-monitor hardware topology: unavailable on the connected dual-monitor host; automated geometry plus dual-monitor physical evidence is accepted for this release and recorded as an approved environment limitation.
- Alternate taskbar edges: stock supported Windows 11 exposes the bottom taskbar path; top/left/right are not applicable to the declared stock configuration, with geometry simulations retained.
- Mixed-DPI hardware: both connected displays report 96 DPI; simulated 96/120/144/192 paths plus current physical 96-DPI capture are accepted as an approved environment limitation, not claimed as physical mixed-DPI evidence.
- Separate clean machine: unavailable; isolated temporary environment, Windows CI, dependency import gate, package smoke, and launcher evidence are accepted as an approved environment limitation.
- Limitations must be explicit in the matrix and test record; they must never be mislabeled as physical passes.

## QA / Release

- Run routine Quality and package smoke.
- Save a dated v0.3.2 physical record and probe JSON.
- Inspect sanitized diagnostics for obvious new errors; do not include tokens/session content.
- Update matrix statuses to physical pass, not applicable, or approved environment limitation according to actual evidence.
- Run strict `run_release_candidate_checks.py`; it must exit 0.
- GitHub Quality must pass; post-merge main repeats Quality, strict RC, package smoke, launch/exit/relaunch.
- Decision: PASS pending completion.

## Security / Resource

- Verify one process/tray instance, no persistent console, bounded workers/timers, local-only transport, no startup mutation, and clean shutdown.
- No telemetry, cloud sync, external endpoint, token/auth reader, updater, or dependency is added.
- Decision: PASS pending evidence.

## Scope Lock

- Allowed product changes: only fixes for defects directly reproduced during v0.3.2 Windows 11 stabilization.
- Allowed release files: evidence records, compatibility/release/testing docs, tests for reproduced defects, canonical version sources, bilingual Changelog.
- Forbidden: new capabilities, Windows 10/ARM/32-bit claims, speculative refactors, new dependencies/settings/UI.
- Release shape: one focused stabilization/release commit, one PR, one tag.
- No v0.4.0 production work is included; v0.4.0 begins only after the v0.3.2 transition gate.
