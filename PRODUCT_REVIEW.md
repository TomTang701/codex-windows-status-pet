# Codex Windows Status Pet — Product Review

## Current positioning

This is a low-distraction external status companion for heavy Codex users. It provides active
conversation state, rate-limit windows, reset credits, settings, and a tray recovery path without
modifying Codex core files or injecting text into the built-in pet.

## Current product contract

- The overlay shows only the active conversation count; it does not show plan-step `N/M` text.
- Settings support opacity, colors, font size, topmost, lock, and virtual-desktop X/Y coordinates.
- The tray is the recovery path when the overlay is hidden or off-screen.
- API boundaries and headless regression tests are defined in `API_SPEC.md`.

## Strengths

- Local-only data boundary and no third-party backend.
- External architecture limits risk to Codex core behavior.
- Explicit configuration persistence and multi-monitor coordinate support.
- API split makes configuration and activity behavior testable without Tk.

## Current risks

- Windows Tk and notification-area behavior still require physical multi-monitor and DPI testing.
- The tray needs failure-injection tests and automatic recreation before it can be treated as a
  guaranteed recovery path.
- The fixed-size overlay can clip long diagnostics or localized text.
- A clean virtual environment now passes dependency import and regression tests; physical mixed-DPI coverage remains.

## Recommended product priorities

1. Make the tray and off-screen recovery observable and self-healing.
2. Finish DPI/mixed-scale and multi-monitor test coverage.
3. Add a diagnostics view or a clear “open log” action.
4. Keep the default overlay compact and status-focused; avoid bringing plan-step detail back into
   the primary line unless it is explicitly user-configurable.
