# Changelog

## 0.2.0 - 2026-07-10

- Removed plan-step text from the overlay; the second line now always shows only the active conversation count.
- Added stale-process cleanup plus a named mutex so repeated launches leave at most one overlay and tray icon.
- Reworked the overlay context menu to execute on the first click and close immediately.
- Added a Windows notification-area integration with show, hide, settings, and exit actions.
- Switched the launcher and Startup shortcut to `pythonw.exe` to avoid a persistent console window.
- Added persistent opacity, colors, font size, topmost, lock, and multi-monitor X/Y settings.
- Added plan completion display instead of tool-call counts.
- Fixed hidden-window state recovery and preserved virtual-desktop coordinates.
- Fixed context-menu command dispatch and main-thread Tk scheduling.
- Added bilingual README, file specification, and changelog documents.

## 0.1.0 - 2026-07-09

- Initial Windows external companion implementation.
- Added local Codex app-server rate-limit polling and session activity inference.
- Added a draggable desktop overlay and basic settings menu.
