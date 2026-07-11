# Codex Windows Status Pet — Product Review

## Current positioning

This is a low-distraction external status companion for heavy Codex users. It provides active
conversation state, rate-limit windows, reset credits, settings, and a tray recovery path without
modifying Codex core files or injecting text into the built-in pet.

## Current product contract

- The overlay shows only the active conversation count; it does not show plan-step `N/M` text.
- Settings expose exactly two sliders: opacity and proportional Window Size. The 80–200% size source scales fixed-ratio geometry, typography, wrapping, and spacing together; position, colors, topmost, lock, Compact, and the 1–10 second refresh interval remain.
- The tray is the recovery path when the overlay is hidden or off-screen.
- API boundaries and headless regression tests are defined in `docs/architecture/API_SPEC.md`.
- Popup placement and quota date formatting are independent, headless-testable API boundaries.

## Strengths

- Local-only data boundary and no third-party backend.
- The quota provider boundary is local-only and rejects credential propagation.
- External architecture limits risk to Codex core behavior.
- Explicit schema-1 configuration migration/downgrade compatibility and multi-monitor coordinate support.
- API split makes configuration and activity behavior testable without Tk.

## Current risks

- Windows 11 x64 Tk and notification-area behavior still require mixed-DPI, taskbar-edge, and clean-machine evidence; Windows 10 is deferred and not claimed.
- Tray failure-injection and single-recovery policy are now covered by deterministic tests; direct tray interaction remains partly environment-limited.
- The supported 80–200% scale range is measured against representative five-row Tk content; future longer localization still requires bounded-text review.
- A clean virtual environment and Windows CI runner pass dependency installation and regression tests; physical mixed-DPI coverage remains.
- The quota-float visual model is useful inspiration, but its token-based external quota boundary is not copied.

## Recommended product priorities

1. Validate unified scale at 80/100/150/200 on the Windows 11 host and publish v0.4.0.
2. Continue truthful mixed-DPI and separate-clean-machine evidence when hardware becomes available.
3. Add accessibility/keyboard coverage without expanding the menu or privacy boundary.
4. Keep the default overlay compact and status-focused; avoid bringing plan-step detail back into
   the primary line unless it is explicitly user-configurable.
