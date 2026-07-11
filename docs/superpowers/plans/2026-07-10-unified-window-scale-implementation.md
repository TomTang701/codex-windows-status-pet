# Unified Window Scale Implementation Plan

> **For the current Codex run:** Execute this plan directly and sequentially under `Goal/ACTIVE_GOAL.md`. Use `superpowers:test-driven-development` for every production behavior task, `superpowers:systematic-debugging` for any unexpected failure, and `superpowers:verification-before-completion` before each commit/readiness claim. The Goal explicitly selects inline execution and does not require an additional execution-mode skill.

**Goal:** Replace independent font and free-form geometry controls with one 80–200% proportional Window Size slider that coherently scales expanded geometry, typography, wrapping, and required spacing while preserving schema-1 downgrade compatibility.

**Architecture:** A new pure `window_scale_api.py` owns all scale constants, normalization, migration inference, and immutable metrics. Configuration translates legacy schema-1 width/height into the canonical percentage and persists derived compatibility fields; the settings dialog edits only the percentage; the main window derives one metrics object and reuses it for expanded, Compact, Hide/Show, and recovery paths.

**Tech Stack:** Python 3.11/3.12, standard-library dataclasses/math/json/tkinter, existing unittest suite, Tk/Win32 Windows 11 host probes, GitHub Actions Windows Quality.

## Global Constraints

- Supported platform remains Windows 11 x64; Windows 10 is not claimed.
- Keep `CONFIG_SCHEMA_VERSION = 1` unless a focused failing compatibility test proves schema 1 unsafe.
- Canonical base metrics: 330x138 geometry, text font 10, face font 28, 100% default.
- Final range: 80–200%, step 5%; Windows Tk measurement already shows representative five-row content fits every step.
- Exactly two normal-dialog Tk `Scale` widgets: `透明度` and `窗口大小`.
- Persist `window_scale_percent` plus derived `font_size`, `window_width`, `window_height`, and `scale_mode = "proportional"`.
- Preserve Apply/Save/Close/Restore Defaults, config protection, position, colors, refresh, topmost, lock, Compact, Hide/Show, menu, restart, and one-instance behavior.
- New network, IPC, worker, subprocess, timer, polling, telemetry, dependency, external service, credential path, and quota consumption: none.
- English normative documents are canonical; update Chinese pairs in the same documentation commit.
- Do not implement v0.4.1+, unrelated cleanup, new controls, or new menu actions.
- Commit and push every independently verified task.

## File responsibility map

| File | Responsibility in v0.4.0 |
|---|---|
| `scripts/api/window_scale_api.py` | Pure constants, scale clamp/quantization, immutable `WindowMetrics`, metric derivation, legacy area inference. |
| `tests/test_window_scale_api.py` | Pure API contract, malformed values, bounds, monotonicity, ratio, migration. |
| `scripts/api/config_api.py` | Schema-1 canonical scale normalization, legacy migration, derived downgrade fields, existing protected-write behavior. |
| `tests/test_api.py` | Config normalization/migration/persistence/protection coverage. |
| `scripts/ui/settings_dialog.py` | Exact two-slider dialog and scale draft synchronization; no metric formulas. |
| `tests/test_ui_menu.py` | Real Tk control inventory and transaction behavior. |
| `scripts/ui/main_window.py` | Derive/apply one metrics object; reuse it for expanded layout, recovery, Compact, and Hide/Show. |
| `tests/test_ui_status_rows.py`, `tests/test_ui_menu.py`, `tests/test_window_recovery.py` | Style propagation, integrated scale retention, and derived-geometry recovery. |
| `docs/architecture/API_SPEC*.md`, `CONFIGURATION*.md` | Canonical API/config contracts and schema-1 downgrade behavior. |
| `docs/product/PRODUCT_OVERVIEW*.md`, `ROADMAP*.md` | Current product controls, completed outcome, and honest limitations. |
| `docs/quality/test-records/2026-07-10-v0.4.0-window-scale-validation.md` | Windows 11 80/100/150/200 host evidence. |
| `.codex-plugin/plugin.json`, `scripts/ui/main_window.py`, `scripts/api/codex_transport_api.py`, `tests/test_codex_transport_api.py`, `CHANGELOG*.md` | Final v0.4.0 release identity and bilingual history. |

---

### Task 1: Pure Window Scale API

**Files:**

- Create: `tests/test_window_scale_api.py`
- Create: `scripts/api/window_scale_api.py`
- Modify: `Goal/EXECUTION_STATE.md`

**Interfaces:**

- Consumes: only Python standard library `dataclasses` and `math`.
- Produces:

```python
@dataclass(frozen=True)
class WindowMetrics:
    scale_percent: int
    width: int
    height: int
    text_font_size: int
    face_font_size: int
    horizontal_padding: int
    vertical_padding: int
    face_text_gap: int
    wraplength: int

def clamp_scale_percent(value) -> float: ...
def quantize_scale_percent(value) -> int: ...
def derive_window_metrics(value) -> WindowMetrics: ...
def infer_scale_percent(width, height) -> int: ...
```

- Constants: `BASE_WINDOW_WIDTH`, `BASE_WINDOW_HEIGHT`, `BASE_TEXT_FONT_SIZE`, `BASE_FACE_FONT_SIZE`, `BASE_HORIZONTAL_PADDING`, `BASE_VERTICAL_PADDING`, `BASE_FACE_TEXT_GAP`, `BASE_WRAPLENGTH`, `MIN_WINDOW_SCALE_PERCENT`, `MAX_WINDOW_SCALE_PERCENT`, `WINDOW_SCALE_STEP`, `DEFAULT_WINDOW_SCALE_PERCENT`.

- [ ] **Step 1: Write the pure-contract tests**

Create `tests/test_window_scale_api.py` with these concrete cases:

```python
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.window_scale_api import (
    DEFAULT_WINDOW_SCALE_PERCENT,
    MAX_WINDOW_SCALE_PERCENT,
    MIN_WINDOW_SCALE_PERCENT,
    derive_window_metrics,
    infer_scale_percent,
    quantize_scale_percent,
)


class WindowScaleApiTests(unittest.TestCase):
    def test_100_percent_returns_canonical_metrics(self):
        metrics = derive_window_metrics(100)
        self.assertEqual((metrics.width, metrics.height), (330, 138))
        self.assertEqual((metrics.text_font_size, metrics.face_font_size), (10, 28))
        self.assertEqual(metrics.wraplength, 260)

    def test_bounds_and_half_up_quantization_are_deterministic(self):
        self.assertEqual(quantize_scale_percent(79), MIN_WINDOW_SCALE_PERCENT)
        self.assertEqual(quantize_scale_percent(82.5), 85)
        self.assertEqual(quantize_scale_percent(198), 200)
        self.assertEqual(quantize_scale_percent(999), MAX_WINDOW_SCALE_PERCENT)
        self.assertEqual(quantize_scale_percent("bad"), DEFAULT_WINDOW_SCALE_PERCENT)

    def test_supported_steps_preserve_ratio_and_monotonic_visual_metrics(self):
        previous = None
        for percent in range(80, 201, 5):
            metrics = derive_window_metrics(percent)
            self.assertLessEqual(abs(metrics.width / metrics.height - 330 / 138), 0.01)
            if previous is not None:
                self.assertGreaterEqual(metrics.width, previous.width)
                self.assertGreaterEqual(metrics.height, previous.height)
                self.assertGreaterEqual(metrics.text_font_size, previous.text_font_size)
                self.assertGreaterEqual(metrics.face_font_size, previous.face_font_size)
                self.assertGreaterEqual(metrics.wraplength, previous.wraplength)
            self.assertEqual(metrics, derive_window_metrics(percent))
            previous = metrics

    def test_legacy_geometry_inference_uses_area_and_clamps(self):
        self.assertEqual(infer_scale_percent(330, 138), 100)
        self.assertEqual(infer_scale_percent(660, 276), 200)
        self.assertEqual(infer_scale_percent(264, 110), 80)
        self.assertEqual(infer_scale_percent(660, 138), 140)
        self.assertEqual(infer_scale_percent(1, 1), 80)
        self.assertEqual(infer_scale_percent("bad", 138), 100)
        self.assertEqual(infer_scale_percent(-1, 138), 100)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the exact test and observe RED**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest tests.test_window_scale_api -v
```

Expected: import failure for missing `api.window_scale_api`; no unrelated syntax/import failure.

- [ ] **Step 3: Implement the complete pure API**

Create `scripts/api/window_scale_api.py`:

```python
"""Pure proportional window and typography scale calculations."""

from __future__ import annotations

import math
from dataclasses import dataclass

BASE_WINDOW_WIDTH = 330
BASE_WINDOW_HEIGHT = 138
BASE_TEXT_FONT_SIZE = 10
BASE_FACE_FONT_SIZE = 28
BASE_HORIZONTAL_PADDING = 12
BASE_VERTICAL_PADDING = 10
BASE_FACE_TEXT_GAP = 5
BASE_WRAPLENGTH = 260
MIN_WINDOW_SCALE_PERCENT = 80
MAX_WINDOW_SCALE_PERCENT = 200
WINDOW_SCALE_STEP = 5
DEFAULT_WINDOW_SCALE_PERCENT = 100


@dataclass(frozen=True)
class WindowMetrics:
    """One coherent expanded-window metric set derived from one percentage."""

    scale_percent: int
    width: int
    height: int
    text_font_size: int
    face_font_size: int
    horizontal_padding: int
    vertical_padding: int
    face_text_gap: int
    wraplength: int


def _finite_number(value, default):
    if isinstance(value, bool):
        return float(default)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return float(default)
    return number if math.isfinite(number) else float(default)


def clamp_scale_percent(value) -> float:
    """Return a finite percentage inside the supported range."""
    number = _finite_number(value, DEFAULT_WINDOW_SCALE_PERCENT)
    return min(MAX_WINDOW_SCALE_PERCENT, max(MIN_WINDOW_SCALE_PERCENT, number))


def quantize_scale_percent(value) -> int:
    """Clamp and select the nearest supported step with half-up ties."""
    clamped = clamp_scale_percent(value)
    stepped = math.floor((clamped + WINDOW_SCALE_STEP / 2) / WINDOW_SCALE_STEP) * WINDOW_SCALE_STEP
    return int(min(MAX_WINDOW_SCALE_PERCENT, max(MIN_WINDOW_SCALE_PERCENT, stepped)))


def derive_window_metrics(value) -> WindowMetrics:
    """Derive expanded geometry, typography, wrapping, and spacing once."""
    percent = quantize_scale_percent(value)
    scale = percent / 100
    return WindowMetrics(
        scale_percent=percent,
        width=round(BASE_WINDOW_WIDTH * scale),
        height=round(BASE_WINDOW_HEIGHT * scale),
        text_font_size=round(BASE_TEXT_FONT_SIZE * scale),
        face_font_size=round(BASE_FACE_FONT_SIZE * scale),
        horizontal_padding=round(BASE_HORIZONTAL_PADDING * scale),
        vertical_padding=round(BASE_VERTICAL_PADDING * scale),
        face_text_gap=round(BASE_FACE_TEXT_GAP * scale),
        wraplength=round(BASE_WRAPLENGTH * scale),
    )


def infer_scale_percent(width, height) -> int:
    """Infer one deterministic scale from legacy visual area."""
    width_value = _finite_number(width, -1)
    height_value = _finite_number(height, -1)
    if width_value <= 0 or height_value <= 0:
        return DEFAULT_WINDOW_SCALE_PERCENT
    area_ratio = (width_value * height_value) / (BASE_WINDOW_WIDTH * BASE_WINDOW_HEIGHT)
    return quantize_scale_percent(math.sqrt(area_ratio) * 100)
```

- [ ] **Step 4: Run focused GREEN and pure regressions**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest tests.test_window_scale_api tests.test_window_size_api tests.test_resize_session_api -v
```

Expected: all tests pass; no existing compatibility API regression.

- [ ] **Step 5: Verify, update execution evidence, commit, and push**

Record the RED command/error and GREEN command/count in `Goal/EXECUTION_STATE.md`, then run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_sensitive_files.py
git diff --check
git add scripts/api/window_scale_api.py tests/test_window_scale_api.py Goal/EXECUTION_STATE.md
git commit -m "Add the pure unified window scale API"
git push origin release/v0.4.0-unified-window-scale
```

Expected: checks exit 0, focused commit created and pushed.

---

### Task 2: Schema-1 Configuration Migration and Downgrade Fields

**Files:**

- Modify: `scripts/api/config_api.py`
- Modify: `tests/test_api.py`
- Modify: `Goal/EXECUTION_STATE.md`

**Interfaces:**

- Consumes: `derive_window_metrics(value) -> WindowMetrics`, `infer_scale_percent(width, height) -> int`, `DEFAULT_WINDOW_SCALE_PERCENT`.
- Produces: normalized dictionaries containing canonical `window_scale_percent` and derived legacy fields while retaining `ConfigLoadResult` and schema 1.

- [ ] **Step 1: Add focused migration and protection tests**

Add these methods to `ConfigApiTests` in `tests/test_api.py`:

```python
    def test_legacy_geometry_migrates_to_canonical_scale_and_derived_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({
                "window_width": 660,
                "window_height": 138,
                "font_size": 19,
                "scale_mode": "free",
                "x": 4151,
            }), encoding="utf-8")
            result = load_settings(path)
            self.assertEqual(result.settings["window_scale_percent"], 140)
            self.assertEqual((result.settings["window_width"], result.settings["window_height"]), (462, 193))
            self.assertEqual(result.settings["font_size"], 14)
            self.assertEqual(result.settings["scale_mode"], "proportional")
            self.assertEqual(result.settings["x"], 4151)
            self.assertTrue(result.writable)

    def test_new_scale_overrides_conflicting_legacy_fields_and_round_trips(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_settings_atomic(path, {
                **DEFAULT_SETTINGS,
                "window_scale_percent": 150,
                "window_width": 180,
                "window_height": 800,
                "font_size": 8,
                "scale_mode": "free",
            })
            result = load_settings(path)
            self.assertEqual(result.settings["window_scale_percent"], 150)
            self.assertEqual((result.settings["window_width"], result.settings["window_height"]), (495, 207))
            self.assertEqual(result.settings["font_size"], 15)
            self.assertEqual(result.settings["scale_mode"], "proportional")
            raw = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(raw["schema_version"], 1)

    def test_invalid_new_scale_is_protected_and_uses_safe_default(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            original = json.dumps({"schema_version": 1, "window_scale_percent": "bad"})
            path.write_text(original, encoding="utf-8")
            result = load_settings(path)
            self.assertEqual(result.settings["window_scale_percent"], 100)
            self.assertFalse(result.writable)
            with self.assertRaises(ConfigWriteProtectedError):
                save_settings_atomic(path, result.settings)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_future_schema_scale_remains_protected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            original = json.dumps({"schema_version": 99, "window_scale_percent": 150})
            path.write_text(original, encoding="utf-8")
            result = load_settings(path)
            self.assertEqual(result.settings, DEFAULT_SETTINGS)
            self.assertFalse(result.writable)
            with self.assertRaises(ConfigWriteProtectedError):
                save_settings_atomic(path, result.settings)
            self.assertEqual(path.read_text(encoding="utf-8"), original)
```

- [ ] **Step 2: Run focused tests and observe RED**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest tests.test_api.ConfigApiTests -v
```

Expected: failures for absent `window_scale_percent` and old independent compatibility values.

- [ ] **Step 3: Add canonical defaults and one compatibility helper**

Import the pure API in `config_api.py`, derive `DEFAULT_WINDOW_METRICS`, and define defaults from it:

```python
from .window_scale_api import (
    DEFAULT_WINDOW_SCALE_PERCENT,
    derive_window_metrics,
    infer_scale_percent,
)

DEFAULT_WINDOW_METRICS = derive_window_metrics(DEFAULT_WINDOW_SCALE_PERCENT)

DEFAULT_SETTINGS = {
    "schema_version": CONFIG_SCHEMA_VERSION,
    "alpha": 0.95,
    "font_color": "#e5e7eb",
    "font_size": DEFAULT_WINDOW_METRICS.text_font_size,
    "background_color": "#111827",
    "topmost": True,
    "locked": False,
    "x": 30,
    "y": 120,
    "window_width": DEFAULT_WINDOW_METRICS.width,
    "window_height": DEFAULT_WINDOW_METRICS.height,
    "scale_mode": "proportional",
    "window_scale_percent": DEFAULT_WINDOW_METRICS.scale_percent,
    "refresh_interval_seconds": 5,
    "compact_when_idle": False,
}
```

Add private helpers:

```python
def _valid_numeric_scale(value):
    if isinstance(value, bool):
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _apply_scale_compatibility(settings, scale_percent):
    metrics = derive_window_metrics(scale_percent)
    settings["window_scale_percent"] = metrics.scale_percent
    settings["font_size"] = metrics.text_font_size
    settings["window_width"] = metrics.width
    settings["window_height"] = metrics.height
    settings["scale_mode"] = "proportional"
    return metrics
```

Import `math`. Keep the existing legacy width/height normalization before calling the helper. Replace independent font/mode ownership at the end of `normalize_settings` with:

```python
    if "window_scale_percent" in raw:
        candidate = raw.get("window_scale_percent")
        if _valid_numeric_scale(candidate):
            scale_percent = candidate
        else:
            scale_percent = DEFAULT_WINDOW_SCALE_PERCENT
            warnings.append("window_scale_percent is invalid; default retained")
    else:
        scale_percent = infer_scale_percent(settings["window_width"], settings["window_height"])
    _apply_scale_compatibility(settings, scale_percent)
```

Remove the old font-size and scale-mode branches as independent final sources; keep width/height validation only as migration input.

- [ ] **Step 4: Run GREEN, config regressions, and schema checker**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest tests.test_api.ConfigApiTests tests.test_settings_session tests.test_application_controllers -v
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_version_sources.py
```

Expected: all selected tests pass; schema remains 1; version checker exits 0.

- [ ] **Step 5: Verify, record RED/GREEN, commit, and push**

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_sensitive_files.py
git diff --check
git add scripts/api/config_api.py tests/test_api.py Goal/EXECUTION_STATE.md
git commit -m "Migrate settings to the unified scale source"
git push origin release/v0.4.0-unified-window-scale
```

Expected: focused configuration commit pushed with no runtime UI change yet.

---

### Task 3: Exact Two-Slider Transactional Settings Dialog

**Files:**

- Modify: `scripts/ui/settings_dialog.py`
- Modify: `tests/test_ui_menu.py`
- Modify: `Goal/EXECUTION_STATE.md`

**Interfaces:**

- Consumes: scale constants and `derive_window_metrics(value) -> WindowMetrics`; generic `SettingsSession` unchanged.
- Produces: exactly two Tk `Scale` widgets; `sync_draft()` writes canonical and derived fields only on Apply/Save.

- [ ] **Step 1: Add real Tk control-inventory and transaction tests**

Add reusable traversal to `MenuInteractionTests`:

```python
    @staticmethod
    def descendants(widget):
        result = []
        for child in widget.winfo_children():
            result.append(child)
            result.extend(MenuInteractionTests.descendants(child))
        return result
```

Add these methods:

```python
    def test_settings_dialog_has_exactly_two_scales_and_no_legacy_size_controls(self):
        app = self.module["Pet"]()
        try:
            app.show_settings()
            app.update_idletasks()
            widgets = self.descendants(app.settings_dialog)
            scales = [widget for widget in widgets if widget.winfo_class() == "Scale"]
            texts = [widget.cget("text") for widget in widgets if "text" in widget.keys()]
            self.assertEqual(len(scales), 2)
            self.assertIn("透明度", texts)
            self.assertIn("窗口大小", texts)
            for removed in ("字体大小", "窗口大小 (宽, 高)", "−", "+", "等比例缩放"):
                self.assertNotIn(removed, texts)
            self.assertIn("默认位置 (X, Y)", texts)
            self.assertIn("刷新间隔 (秒)", texts)
            for retained in ("置顶", "锁定位置", "空闲时收缩", "字体颜色...", "背景颜色...", "保存", "应用", "恢复默认值", "关闭"):
                self.assertIn(retained, texts)
        finally:
            self.destroy_app(app)

    def test_scale_slider_is_draft_only_until_apply_and_defaults_to_100(self):
        app = self.module["Pet"]()
        apply_calls = []
        original_apply = app.apply_settings
        app.apply_settings = lambda settings: (apply_calls.append(dict(settings)), original_apply(settings))[1]
        try:
            app.show_settings()
            app.update_idletasks()
            widgets = self.descendants(app.settings_dialog)
            scales = [widget for widget in widgets if widget.winfo_class() == "Scale"]
            scale = next(widget for widget in scales if float(widget.cget("to")) == 200.0)
            scale.set(150)
            app.update_idletasks()
            self.assertEqual(app.settings["window_scale_percent"], 100)
            self.assertEqual(apply_calls, [])
            buttons = {widget.cget("text"): widget for widget in widgets if widget.winfo_class() == "Button"}
            buttons["应用"].invoke()
            self.assertEqual(app.settings["window_scale_percent"], 150)
            self.assertEqual((app.settings["window_width"], app.settings["window_height"]), (495, 207))
            buttons["恢复默认值"].invoke()
            self.assertEqual(int(scale.get()), 100)
        finally:
            self.destroy_app(app)
```

- [ ] **Step 2: Run the exact UI tests and observe RED**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest tests.test_ui_menu.MenuInteractionTests.test_settings_dialog_has_exactly_two_scales_and_no_legacy_size_controls tests.test_ui_menu.MenuInteractionTests.test_scale_slider_is_draft_only_until_apply_and_defaults_to_100 -v
```

Expected: inventory reports old controls/more than two required size semantics, or canonical key is absent.

- [ ] **Step 3: Replace old settings controls with the canonical slider**

In `settings_dialog.py`:

```python
from api.window_scale_api import (
    MAX_WINDOW_SCALE_PERCENT,
    MIN_WINDOW_SCALE_PERCENT,
    WINDOW_SCALE_STEP,
    derive_window_metrics,
)
```

Use `window_scale = tk.IntVar(value=draft["window_scale_percent"])`. Keep opacity at row 0 and add:

```python
tk.Label(body, text="窗口大小").grid(row=1, column=0, sticky="w")
tk.Scale(
    body,
    from_=MIN_WINDOW_SCALE_PERCENT,
    to=MAX_WINDOW_SCALE_PERCENT,
    resolution=WINDOW_SCALE_STEP,
    orient="horizontal",
    length=230,
    variable=window_scale,
    label="%",
).grid(row=1, column=1)
```

Move position to row 2, refresh to row 3, topmost/lock to row 4, Compact to row 5, colors to row 6, and buttons to row 7. Delete `size`, `window_width`, `window_height`, `scale_mode`, `ResizeSession`, `resize_by`, and all related widgets/imports.

In `sync_draft()` derive once:

```python
metrics = derive_window_metrics(window_scale.get())
draft["window_scale_percent"] = metrics.scale_percent
draft["font_size"] = metrics.text_font_size
draft["window_width"] = metrics.width
draft["window_height"] = metrics.height
draft["scale_mode"] = "proportional"
```

Preserve existing coordinate, refresh, booleans, colors, and error behavior. In `restore_defaults()`, replace old size/dimension/mode setters with:

```python
window_scale.set(draft["window_scale_percent"])
```

- [ ] **Step 4: Run GREEN and all Tk integration tests**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest tests.test_ui_menu tests.test_ui_status_rows -v
```

Expected: all Tk tests pass; exactly two Scale widgets; no disk write or Apply during slider movement.

- [ ] **Step 5: Verify, record RED/GREEN, commit, and push**

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_sensitive_files.py
git diff --check
git add scripts/ui/settings_dialog.py tests/test_ui_menu.py Goal/EXECUTION_STATE.md
git commit -m "Replace size controls with one scale slider"
git push origin release/v0.4.0-unified-window-scale
```

Expected: focused user-visible settings commit pushed.

---

### Task 4: Main Window, Recovery, Hide/Show, and Compact Integration

**Files:**

- Modify: `scripts/ui/main_window.py`
- Modify: `tests/test_ui_menu.py`
- Modify: `tests/test_window_recovery.py` only if the existing pure recovery contract needs a new derived-size fixture
- Modify: `Goal/EXECUTION_STATE.md`

**Interfaces:**

- Consumes: `derive_window_metrics(value) -> WindowMetrics` and canonical normalized settings.
- Produces: `Pet.window_metrics: WindowMetrics`; coherent expanded layout; current metrics reused by recovery and Compact.

- [ ] **Step 1: Add integrated Tk behavior tests**

Add to `MenuInteractionTests`:

```python
    def test_apply_scale_updates_geometry_fonts_wrap_and_padding_together(self):
        import tkinter.font as tkfont
        app = self.module["Pet"]()
        try:
            app.apply_settings({**app.settings, "window_scale_percent": 150})
            app.update_idletasks()
            self.assertEqual(app.window_metrics.scale_percent, 150)
            self.assertTrue(app.geometry().startswith("495x207"))
            text_font = tkfont.Font(root=app, font=next(iter(app.text.labels.values())).cget("font"))
            face_font = tkfont.Font(root=app, font=app.face.cget("font"))
            self.assertEqual(text_font.cget("size"), 15)
            self.assertEqual(face_font.cget("size"), 42)
            for label in app.text.labels.values():
                self.assertEqual(int(label.cget("wraplength")), 390)
            self.assertEqual(app.face.pack_info()["padx"], (18, 8))
            self.assertEqual(app.face.pack_info()["pady"], 15)
        finally:
            self.destroy_app(app)

    def test_hide_show_and_compact_expand_preserve_current_scale(self):
        app = self.module["Pet"]()
        app.save_settings = lambda **_kwargs: True
        try:
            app.apply_settings({**app.settings, "window_scale_percent": 150})
            app.hide_window()
            self.assertTrue(app.hidden)
            self.assertEqual(float(app.attributes("-alpha")), 0.0)
            app.show_window()
            app.update_idletasks()
            self.assertFalse(app.hidden)
            self.assertTrue(app.geometry().startswith("495x207"))
            app.set_compact(True)
            self.assertFalse(app.geometry().startswith("495x207"))
            app.set_compact(False)
            app.update_idletasks()
            self.assertTrue(app.geometry().startswith("495x207"))
            self.assertEqual(app.window_metrics.scale_percent, 150)
        finally:
            self.destroy_app(app)

    def test_scale_application_keeps_five_row_identities(self):
        app = self.module["Pet"]()
        try:
            identities = {key: str(value) for key, value in app.text.labels.items()}
            app.apply_settings({**app.settings, "window_scale_percent": 80})
            app.apply_settings({**app.settings, "window_scale_percent": 200})
            self.assertEqual({key: str(value) for key, value in app.text.labels.items()}, identities)
            self.assertEqual(len(app.text.labels), 5)
        finally:
            self.destroy_app(app)
```

If tuple-valued Tk `pack_info()` is stringified on the host, normalize with `app.tk.splitlist(...)` while preserving the exact expected numeric values.

- [ ] **Step 2: Run integrated tests and observe RED**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest tests.test_ui_menu.MenuInteractionTests.test_apply_scale_updates_geometry_fonts_wrap_and_padding_together tests.test_ui_menu.MenuInteractionTests.test_hide_show_and_compact_expand_preserve_current_scale tests.test_ui_menu.MenuInteractionTests.test_scale_application_keeps_five_row_identities -v
```

Expected: absent `window_metrics`, unchanged paw font/wrap/padding, or geometry still using independent fields.

- [ ] **Step 3: Derive and apply one metrics object**

Import `derive_window_metrics`. In `Pet.__init__`, derive `self.window_metrics` immediately after configuration load and use it to create initial face/text fonts and spacing.

Add helpers:

```python
    def _sync_compatibility_metrics(self, settings):
        metrics = derive_window_metrics(settings.get("window_scale_percent"))
        settings["window_scale_percent"] = metrics.scale_percent
        settings["font_size"] = metrics.text_font_size
        settings["window_width"] = metrics.width
        settings["window_height"] = metrics.height
        settings["scale_mode"] = "proportional"
        self.window_metrics = metrics
        return metrics

    def _pack_expanded_content(self):
        metrics = self.window_metrics
        self.face.pack_forget()
        self.face.pack(
            side="left",
            padx=(metrics.horizontal_padding, metrics.face_text_gap),
            pady=metrics.vertical_padding,
        )
        self.text.pack(
            side="left",
            fill="both",
            expand=True,
            pady=metrics.vertical_padding,
        )
```

In `apply_settings`:

```python
self.settings = dict(settings)
metrics = self._sync_compatibility_metrics(self.settings)
self.settings["x"], self.settings["y"] = self.safe_position(...)
self.geometry(f"{metrics.width}x{metrics.height}+{x}+{y}")
self.face.configure(font=("Segoe UI Emoji", metrics.face_font_size), ...)
self.text.configure_rows(
    font=("Segoe UI", metrics.text_font_size),
    wraplength=metrics.wraplength,
    ...,
)
if not self.compact:
    self._pack_expanded_content()
```

Use `self.window_metrics.width/height` in `safe_position`, `recover_window_if_needed`, `set_compact`, and expanded geometry. In `set_compact(False)`, call `_pack_expanded_content()` and restore `metrics.width x metrics.height`. In Compact mode keep existing `compact_size` and `compact_geometry` policies but pass the current metrics.

- [ ] **Step 4: Run GREEN and lifecycle/recovery regressions**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest tests.test_ui_menu tests.test_ui_status_rows tests.test_window_recovery tests.test_display_mode_api tests.test_application_controllers -v
```

Expected: all selected tests pass; five row identities and existing lifecycle behavior remain.

- [ ] **Step 5: Verify, record RED/GREEN, commit, and push**

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_sensitive_files.py
git diff --check
git add scripts/ui/main_window.py tests/test_ui_menu.py tests/test_window_recovery.py Goal/EXECUTION_STATE.md
git commit -m "Apply unified metrics across the overlay lifecycle"
git push origin release/v0.4.0-unified-window-scale
```

Stage `tests/test_window_recovery.py` only if it actually changed.

---

### Task 5: Canonical Documentation and Windows 11 Host Validation

**Files:**

- Modify: `docs/architecture/API_SPEC.md`
- Modify: `docs/architecture/API_SPEC.zh-CN.md`
- Modify: `docs/architecture/CONFIGURATION.md`
- Modify: `docs/architecture/CONFIGURATION.zh-CN.md`
- Modify: `docs/product/PRODUCT_OVERVIEW.md`
- Modify: `docs/product/PRODUCT_OVERVIEW.zh-CN.md`
- Modify: `docs/product/ROADMAP.md`
- Modify: `docs/product/ROADMAP.zh-CN.md`
- Modify: `docs/quality/COMPATIBILITY_MATRIX.md` only for new scale evidence
- Modify: `docs/quality/COMPATIBILITY_MATRIX.zh-CN.md` in the same commit if the matrix changes
- Create: `docs/quality/test-records/2026-07-10-v0.4.0-window-scale-validation.md`
- Modify: `Goal/EXECUTION_STATE.md`

**Interfaces:**

- Consumes: implemented API names, final constants/range, schema behavior, exact UI inventory, and current build.
- Produces: synchronized normative contract and dated Windows 11 evidence; no runtime behavior.

- [ ] **Step 1: Update English canonical documents with exact implemented facts**

Document:

- Window Scale API row, symbols, side effects (`None`), errors (safe fallback), and tests;
- schema-1 JSON including `window_scale_percent` and derived compatibility fields;
- geometric-mean migration and v0.3.2 downgrade behavior;
- exactly two sliders and removed old controls;
- 80–200%, 5%, 100% base metrics;
- legacy `WindowSizeAPI`/`ResizeSessionAPI` retained only as compatibility utilities with no normal UI consumer;
- completed roadmap outcome and remaining honest mixed-DPI/clean-machine limitations.

Do not copy stale test counts or v0.3.0 release wording.

- [ ] **Step 2: Translate the same changes to Chinese pairs**

Preserve headings, API names, constants, JSON, versions, tables, and code examples. Add no Chinese-only requirement.

- [ ] **Step 3: Run full automated gates before host mutation**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' -m compileall -q scripts
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest discover -s tests -q
& '.build\v032-clean-venv\Scripts\python.exe' scripts\run_quality_checks.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\package_smoke_test.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_release_readiness.py --strict
git diff --check
```

Expected: compilation succeeds, all tests pass, Quality/package/strict readiness exit 0, document parity passes.

- [ ] **Step 4: Validate the running Windows build at four scales without consuming Codex quota**

Use a temporary copy of the current valid settings file or a temporary `SettingsPersistenceController` path so the user's original configuration can be restored exactly. For each 80, 100, 150, and 200:

1. derive expected metrics through `derive_window_metrics`;
2. apply the normalized settings to a current-build `Pet` instance with dummy transport/tray adapters;
3. inspect real Tk geometry, five stable label identities, text and face font sizes, wraplength, and pack padding;
4. invoke menu placement at a monitor edge and confirm work-area containment;
5. test unlocked drag movement and locked no-movement with synthetic Tk events;
6. call Hide then Show and verify geometry/percentage retention;
7. call Compact then Expand and verify current expanded geometry/percentage retention;
8. save to the temporary schema-1 file, reload, and verify restart persistence.

Then perform one actual app-local exit/relaunch from the branch root and verify one process, no persistent CMD, current CommandLine, valid HWND, and live two-monitor probe. Reuse existing Compact physical evidence only for behavior unchanged by this feature; the four-scale Compact geometry must be inspected in current Tk.

Record exact measured results and limitations in `2026-07-10-v0.4.0-window-scale-validation.md`. Never record simulation as mixed-DPI physical evidence.

- [ ] **Step 5: Verify docs/evidence, commit, and push**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_doc_manifest.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_doc_governance.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_doc_links.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_doc_parity.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_sensitive_files.py
git diff --check
git add docs/architecture docs/product docs/quality Goal/EXECUTION_STATE.md
git commit -m "Document and validate unified window scaling"
git push origin release/v0.4.0-unified-window-scale
```

Expected: all documentation gates pass and the evidence contains no sensitive content.

---

### Task 6: v0.4.0 Version, Final RC, PR, Merge, Tag, and Final Audit

**Files:**

- Modify: `.codex-plugin/plugin.json`
- Modify: `scripts/ui/main_window.py`
- Modify: `scripts/api/codex_transport_api.py`
- Modify: `tests/test_codex_transport_api.py`
- Modify: `CHANGELOG.md`
- Modify: `CHANGELOG.zh-CN.md`
- Modify: `Goal/EXECUTION_STATE.md` while the branch is active
- External: PR #, GitHub Release report, tag `v0.4.0`

**Interfaces:**

- Consumes: fully verified implementation/evidence at current branch head.
- Produces: consistent version 0.4.0, one exact-title PR, squash-merged verified main, annotated remote tag, release report, deleted branch, final goal completion evidence.

- [ ] **Step 1: Update all authoritative version sources and bilingual Changelog**

Set application/plugin/client/test versions to `0.4.0`. Use plugin build metadata `0.4.0+codex.<current YYYYMMDDHHMMSS>`.

Add `## 0.4.0 - 2026-07-10` to both Changelogs describing only:

- one Window Size slider replacing font/width/height/button/mode controls;
- fixed-ratio geometry and adaptive typography/layout metrics;
- deterministic legacy migration and schema-1 downgrade fields;
- transaction/lifecycle/Windows validation;
- no new resource/privacy boundary.

Do not rewrite the historical `Unreleased` backlog and do not mention v0.4.1+.

- [ ] **Step 2: Run the complete final branch verification**

Run:

```powershell
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_version_sources.py
& '.build\v032-clean-venv\Scripts\python.exe' -m compileall -q scripts
& '.build\v032-clean-venv\Scripts\python.exe' -m unittest discover -s tests -q
& '.build\v032-clean-venv\Scripts\python.exe' scripts\run_quality_checks.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\package_smoke_test.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_release_readiness.py --strict
git diff --check
& '.build\v032-clean-venv\Scripts\python.exe' scripts\run_release_candidate_checks.py
```

Expected: version sources 0.4.0, zero test failures, Quality/package/strict readiness/RC approved, whitespace clean.

- [ ] **Step 3: Commit, push, and open the exact-title PR**

```powershell
git add .codex-plugin/plugin.json scripts/ui/main_window.py scripts/api/codex_transport_api.py tests/test_codex_transport_api.py CHANGELOG.md CHANGELOG.zh-CN.md Goal/EXECUTION_STATE.md
git commit -m "Release v0.4.0 unified window scaling"
git push origin release/v0.4.0-unified-window-scale
$testOutput = & '.build\v032-clean-venv\Scripts\python.exe' -m unittest discover -s tests -q 2>&1
if ($LASTEXITCODE) { $testOutput; throw 'Final test recount failed' }
$testLine = ($testOutput | Select-String '^Ran \d+ tests').Line
$body = @"
## Outcome
Unifies window and typography scaling behind one proportional Window Size slider.

## Controls removed
Font Size, free Width/Height, minus/plus size buttons, and Proportional Scaling are absent from the normal settings dialog.

## Contract and compatibility
Expanded geometry keeps 330:138; typography, wrapping, and spacing derive from `window_scale_percent`. Legacy geometry migrates by geometric-mean area inference. Schema 1 and derived compatibility fields preserve v0.3.2 downgrade behavior.

## Verification
- Full unittest: $testLine, zero failures.
- Quality, package smoke, strict readiness, and Release Candidate: approved in the final branch verification.
- Windows 11 host: 80/100/150/200 geometry, typography, five rows, menu, drag/lock, Hide/Show, Compact/Expand, and restart persistence validated in the dated record.

## Resource and privacy
No new network, IPC, worker, subprocess, polling, telemetry, dependency, provider, credential path, or Codex quota consumption.

## Rollback
Return to v0.3.2; its schema-1 reader consumes the derived compatibility fields.

No v0.4.1 or later work was included.
"@
$prUrl = gh pr create --base main --head release/v0.4.0-unified-window-scale --title '[v0.4.0] Unify window and typography scaling' --body $body
```

The PR body must include outcome, removed controls, fixed ratio, adaptive metrics, migration/schema compatibility, exact tests, Windows evidence, resource/privacy impact, rollback, main-protection limitation, and `No v0.4.1 or later work was included`.

- [ ] **Step 4: Monitor exact-head CI and squash merge**

Verify the PR head SHA equals the pushed branch. Wait for `Windows Quality / quality` success with bounded polling. If it fails, invoke Systematic Debugging before any fix. When successful:

```powershell
$prNumber = gh pr view --json number --jq .number
gh pr merge $prNumber --squash --subject "Release v0.4.0 unified window scaling (#$prNumber)"
```

Do not delete the branch until main/tag/report checks finish.

- [ ] **Step 5: Retest merged main and run post-release Windows smoke**

```powershell
git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
& '.build\v032-clean-venv\Scripts\python.exe' scripts\run_quality_checks.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\package_smoke_test.py
& '.build\v032-clean-venv\Scripts\python.exe' scripts\check_release_readiness.py --strict
& '.build\v032-clean-venv\Scripts\python.exe' scripts\run_release_candidate_checks.py
```

Repeat app-local exit/relaunch and the 80/100/150/200 Tk host smoke on merged main. Expected: one process, current main CommandLine, valid HWND, exactly two settings sliders, five rows, scale persistence, menu/drag/lock/Hide/Show/Compact behavior, no persistent CMD.

- [ ] **Step 6: Tag verified main, publish report, delete branch**

```powershell
$verifiedMain = git rev-parse HEAD
git tag -a v0.4.0 $verifiedMain -m 'Release v0.4.0'
git push origin v0.4.0
git fetch origin --tags
git merge-base --is-ancestor 'v0.4.0^{}' origin/main
```

Create a GitHub Release report containing the final slider range, base metrics, removed controls, migration/schema decision, test and Windows evidence, resource impact, PR/CI/merge/tag SHAs, rollback, design/plan paths, material debugging conclusions, representative RED/GREEN evidence, and `No v0.4.1 or later work was included`.

After the report exists:

```powershell
git push origin --delete release/v0.4.0-unified-window-scale
git branch -D release/v0.4.0-unified-window-scale
```

Force-delete the local branch only after verifying its exact head was the merged PR head; squash merge intentionally breaks ordinary ancestor-based `-d` detection.

- [ ] **Step 7: Perform the Final Definition of Done audit**

Read every v0.3.2 and v0.4.0 checkbox in `Goal/ACTIVE_GOAL.md` and map it to current evidence: commit, test output, PR metadata, CI, main SHA, tag SHA, runtime/Windows evidence, or release report. Verify working tree clean, no interrupted Git operation, tags reachable, branches deleted, and no v0.4.1+ work.

Only if every item is proven, mark the persistent goal complete. Otherwise keep the goal active and continue the missing requirement.

## Plan self-review result

- Spec coverage: every design section maps to Tasks 1–6, including pure metrics, migration, UI inventory, transaction flow, main/Compact integration, resource/privacy, docs, Windows host validation, and release lifecycle.
- Placeholder scan: every code-changing step includes concrete code or an exact bounded procedure; no unfinished placeholder language remains.
- Type consistency: `WindowMetrics` fields and four public function names are identical across API, configuration, UI, main integration, tests, and docs.
- Ordering: pure API precedes migration; migration precedes UI; UI precedes lifecycle integration; implementation precedes docs/host evidence; release metadata and final RC occur last.
- Scope: one canonical scale source, schema 1, no dependency/resource boundary, no v0.4.1+ work, frequent focused commits.
