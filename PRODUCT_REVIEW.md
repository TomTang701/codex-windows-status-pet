# Codex Windows Status Pet — Product Review

## Current positioning

This is a low-distraction external status companion for heavy Codex users. It provides active
conversation state, rate-limit windows, reset credits, settings, and a tray recovery path without
modifying Codex core files or injecting text into the built-in pet.

## Current product contract

- The overlay shows only the active conversation count; it does not show plan-step `N/M` text.
- Settings support opacity, colors, font size, topmost, lock, virtual-desktop X/Y coordinates, window dimensions, proportional scaling, and a 1–10 second refresh interval.
- The tray is the recovery path when the overlay is hidden or off-screen.
- API boundaries and headless regression tests are defined in `API_SPEC.md`.
- Popup placement and quota date formatting are independent, headless-testable API boundaries.

## Strengths

- Local-only data boundary and no third-party backend.
- The quota provider boundary is local-only and rejects credential propagation.
- External architecture limits risk to Codex core behavior.
- Explicit configuration persistence and multi-monitor coordinate support.
- API split makes configuration and activity behavior testable without Tk.

## Current risks

- Windows Tk and notification-area behavior still require Windows 10, mixed-DPI, taskbar-edge, and clean-machine evidence.
- Tray failure-injection and single-recovery policy are now covered by deterministic tests; direct tray interaction remains partly environment-limited.
- The fixed-size overlay can clip long diagnostics or localized text.
- A clean virtual environment and Windows CI runner pass dependency installation and regression tests; physical mixed-DPI coverage remains.
- The quota-float visual model is useful inspiration, but its token-based external quota boundary is not copied.

## Recommended product priorities

1. Finish Windows 10, DPI/mixed-scale, taskbar-edge, and clean-machine evidence.
2. Run a full idle desktop test for compact/hover behavior and publish the v0.3.0 reliability release.
3. Keep the diagnostic-summary action safe and add accessibility/keyboard interaction coverage.
4. Keep the default overlay compact and status-focused; avoid bringing plan-step detail back into
   the primary line unless it is explicitly user-configurable.
