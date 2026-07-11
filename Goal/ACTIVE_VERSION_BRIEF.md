# ACTIVE VERSION BRIEF — v0.4.0 Unified Window Scale

## Identity

- Version: `0.4.0`
- Branch: `release/v0.4.0-unified-window-scale`
- Base: `main` at tagged v0.3.2 commit `f75b7a57b0557f5daacc1f643a53d8d18a43ef9f`
- PR: `[v0.4.0] Unify window and typography scaling`
- Tag: `v0.4.0`

## Product

- Outcome: Replace independent font-size and free-form width/height controls with one proportional Window Size percentage slider that scales expanded geometry and typography coherently.
- Product decision: `GO`
- Target user: A Windows 11 x64 Codex user who wants predictable readable overlay sizing without understanding coupled low-level controls.
- User-visible controls: exactly two Tk Scale widgets — `透明度` and `窗口大小`; position, refresh, topmost, lock, Compact, colors, Save, Apply, Restore Defaults, and Close remain.
- Removed controls: font-size slider, width input, height input, minus/plus size buttons, and proportional-scaling checkbox.

## Contract

- `window_scale_percent` is the only canonical expanded-size source.
- Base metrics are 330x138 geometry, text font 10, and face font 28 at 100%.
- Geometry keeps the fixed 330:138 ratio and typography/layout metrics derive from the same pure result.
- Initial range candidate is 80–200% in 5% steps; physical/Tk measurement determines the final safe range.
- Configuration schema remains version 1 unless implementation evidence proves it unsafe.
- Legacy width/height migrate deterministically by geometric-mean area inference, then clamp and quantize.
- Derived `font_size`, `window_width`, `window_height`, and proportional `scale_mode` remain persisted for downgrade compatibility.
- Apply/Save/Close/Restore Defaults semantics remain transactional.
- Hide/Show, Compact/Expand, restart, drag/lock, position recovery, menu, and topmost preserve scale.

## Scope lock

- Preferred production files: pure scale API, config normalization, settings dialog, main window, and only directly required settings/compact boundaries.
- Required tests: pure metrics, migration, config protection, transaction semantics, exact two-slider inventory, main integration, recovery and persistence.
- Explicit non-goals: theme presets, font family, manual resize, width/height/font controls, aspect toggle, quota/refresh feature, new menu action, provider, network, IPC, subprocess, worker, polling, telemetry, installer, updater, Windows 10, v0.4.1+ work, or unrelated cleanup.

## Quality, compatibility, and release

- Use Brainstorming → validated design spec → Writing Plans → sequential TDD implementation.
- Run focused RED/GREEN cycles, full Quality, package smoke, strict readiness, strict RC, and Windows 11 host checks at minimum/100/middle-large/maximum scale.
- English normative documents remain canonical and Chinese pairs update in the same commit.
- Release through one PR, successful `Windows Quality / quality`, squash merge, verified main, tag `v0.4.0`, post-release smoke, and branch deletion.

## Resource, security, and rollback

- New network/IPC/worker/subprocess/polling/telemetry/dependency/quota consumption: `No`.
- Scale derivation is pure, bounded, deterministic, and constant time; slider movement changes draft only.
- Keep schema v1 and derived legacy fields so rollback to v0.3.2 loads usable geometry and font settings.
