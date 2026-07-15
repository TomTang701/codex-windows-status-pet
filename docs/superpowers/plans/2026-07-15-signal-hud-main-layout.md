# Signal HUD Main Layout Implementation Plan

> **For agentic workers:** Execute this plan inline in the current isolated worktree.

**Goal:** Replace the expanded main window's legacy direct row layout with a clear two-card Signal HUD while preserving all existing status data, battery cells, compact mode, and pointer interactions.

**Architecture:** Keep `StatusRows` and `BatteryView` as the stable data-rendering widgets. Add presentation-only Tk frames in `Pet`: a top status rail, a left status card, and a right signal card. Bind the new containers to the existing drag/menu event surface and keep compact mode rendering the battery alone.

**Tech Stack:** Python 3, Tkinter, unittest, existing project theme tokens.

## Global Constraints

- Work only in `G:/Zixuan_Tang/Codex插件/codex-windows-status-pet-ui` on branch `feat/signal-hud-settings-ui-isolated`.
- Do not modify the original `main` worktree.
- Do not add keyboard-shortcut UI or new shortcut bindings.
- Preserve the five status row IDs and ten battery cells.
- Preserve the canonical expanded geometry and compact geometry contracts.
- Run Tk UI tests serially because concurrent Tk processes can steal desktop focus.

---

### Task 1: Remove the rejected shortcut expansion

**Files:**
- Modify: `scripts/api/localization_api.py`
- Modify: `scripts/ui/settings_dialog.py`
- Modify: `tests/test_ui_redesign.py`

- [ ] Remove only the uncommitted shortcut hint strings, hint label, Alt+R binding, and their assertions. Keep the already-existing Apply/Save/Escape behavior unchanged.
- [ ] Run `git diff --check` and confirm no shortcut expansion remains in the working diff.

### Task 2: Add a failing test for the expanded HUD composition

**Files:**
- Modify: `tests/test_ui_redesign.py`

- [ ] Assert that the expanded window exposes `hud_header`, `status_card`, and `signal_card` presentation containers, with `app.text` inside `status_card` and `app.battery` inside `signal_card`.
- [ ] Assert that the header contains a status label and that compact mode hides the expanded cards while keeping all ten battery cells mapped.
- [ ] Run the focused test and confirm it fails against the current direct-pack implementation.

### Task 3: Implement the two-card Signal HUD

**Files:**
- Modify: `scripts/ui/main_window.py`
- Modify: `scripts/ui/theme.py` only if an existing token is genuinely missing

- [ ] Create presentation-only frames using existing theme colors: a thin `hud_header`, a `status_card`, and a `signal_card`.
- [ ] Add a small title/status label to the header without changing the status row data contract.
- [ ] Pack the existing `StatusRows` and `BatteryView` into their cards; use card borders and restrained padding so all supported scales still fit.
- [ ] Include the new frames in right-click, hover, drag, and cursor synchronization event traversal.
- [ ] Update `apply_settings` and compact transitions so custom background/font colors still apply and compact mode hides the header/cards.

### Task 4: Run verification and review the diff

**Files:**
- Modify: none

- [ ] Run the branch-local UI gate: `scripts/run_ui_redesign_checks.py`.
- [ ] Run related legacy tests serially: `tests.test_ui_settings_dialog tests.test_ui_status_rows tests.test_ui_menu`.
- [ ] Run `tests.test_ui_content_fit` serially and inspect the actual Tk geometry assertions.
- [ ] Run `git diff --check`, inspect `git diff`, and confirm only the shortcut cleanup, main HUD layout, tests, and plan are changed.
