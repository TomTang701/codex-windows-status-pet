# Unified Window Scale Design

- Date: 2026-07-10
- Target: v0.4.0
- Branch: `release/v0.4.0-unified-window-scale`
- Base: tagged v0.3.2 main commit `f75b7a57b0557f5daacc1f643a53d8d18a43ef9f`
- Product decision: GO
- Change class: C2 compatible behavior with configuration migration and Windows UI validation

## Goal

Replace the independent font-size slider, free width/height entries, plus/minus buttons, and proportional-mode checkbox with one Window Size percentage slider. One canonical percentage must derive expanded geometry, typography, wrapping, and the small set of spacing metrics needed for visual balance.

The settings dialog must contain exactly two Tk `Scale` widgets: opacity and Window Size. Existing position, refresh, topmost, lock, Compact, color, Apply, Save, Restore Defaults, and Close behavior remains.

## Non-goals

- No manual width, height, font-size, aspect-ratio, or resize-handle control.
- No theme, font-family, animation, quota, refresh, menu, provider, installer, updater, or Windows 10 feature.
- No new network, IPC, subprocess, worker, timer, polling, telemetry, dependency, or quota-consuming path.
- No configuration schema bump unless implementation evidence proves schema 1 unsafe.
- No unrelated refactor and no v0.4.1 or later work.

## Current architecture observations

### Configuration

`scripts/api/config_api.py` currently treats `font_size`, `window_width`, `window_height`, and `scale_mode` as independent validated sources. Schema 1 already ignores unknown fields, protects malformed/future configuration from routine writes, and atomically persists normalized dictionaries.

### Settings transaction

`SettingsSession` already separates persisted, runtime, draft, and opening snapshots. This generic transaction boundary does not need new scale-specific behavior. The Tk dialog currently owns the old font slider, width/height entries, resize buttons, and scale-mode checkbox, then copies all values into the draft on Apply or Save.

### Main window and Compact

`Pet` consumes width and height during startup, Apply, position recovery, and Compact geometry. Text font and wraplength are applied separately; paw font and padding are partly hard-coded. Compact expansion already returns to settings width/height, so replacing those compatibility fields with values derived from one percentage preserves the existing state machine while removing independent sources.

### Tests and documentation

Existing tests cover configuration protection, settings transactions, Tk menu/dialog behavior, five stable rows, Compact restoration, position recovery, and legacy free/proportional helper APIs. The new behavior needs a new pure scale contract plus focused migration, exact-control inventory, and integration assertions. Existing free-resize APIs can remain as documented compatibility utilities but must have no production UI consumer.

## Windows Tk range measurement

The supported range is 80–200% in 5% steps, default 100%.

The range was measured on the supported Windows 11 host with Tk's real `Segoe UI` and `Segoe UI Emoji` font metrics. The fixture used representative longest rows including `周 100% / 23:59 12/31` and `重置 999 次 / 23:59 12/31`, five text lines, scaled wraplength, and scaled outer/gap/vertical spacing.

Key results:

| Scale | Geometry | Text / face font | Required content box | Result |
|---:|---:|---:|---:|---|
| 80% | 264x110 | 8 / 22 | 179x81 | Fits |
| 100% | 330x138 | 10 / 28 | 217x105 | Fits |
| 150% | 495x207 | 15 / 42 | 329x170 | Fits |
| 200% | 660x276 | 20 / 56 | 446x225 | Fits |

Every 5% step from 80 through 200 fit the measured representative content. Final physical host validation still checks actual widgets, all five row identities, menu placement, drag/lock, Hide/Show, Compact/Hover, and restart persistence at 80, 100, 150, and 200%.

## Alternatives considered

### A. New pure Window Scale API — selected

Add `scripts/api/window_scale_api.py` as the only calculation boundary. Configuration performs legacy migration and writes derived compatibility fields. The settings dialog edits only the percentage. The main window derives one immutable metrics object and applies it coherently.

Benefits:

- one source of truth and one formula location;
- pure deterministic tests without Tk;
- migration and downgrade responsibilities stay explicit;
- main-window and Compact code consume the same metrics;
- follows the existing inward dependency direction.

Cost: one new module and corresponding canonical documentation.

### B. Extend Window Size API and ResizeSession — rejected

The existing APIs could be repurposed to return scaled fonts and geometry. This reduces file count, but their contracts are explicitly free/proportional width-height transformations around a session base. Reusing them would mix obsolete user-controlled geometry with canonical product metrics and make legacy inference ownership unclear.

### C. Persist every metric with schema 2 — rejected

Persisting width, height, fonts, padding, and wraplength as first-class fields makes reload straightforward, but creates multiple persisted truths, requires conflict resolution and migration, weakens v0.3.2 downgrade behavior, and has no evidence-based need for a schema bump.

## Selected component boundaries

### Pure Window Scale API

Create `scripts/api/window_scale_api.py` with no Tk, filesystem, platform, or configuration side effects.

Constants:

```python
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
```

Immutable result:

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
```

Public functions:

```python
clamp_scale_percent(value) -> float
quantize_scale_percent(value) -> int
derive_window_metrics(value) -> WindowMetrics
infer_scale_percent(width, height) -> int
```

Contracts:

- Boolean and nonnumeric values use the safe default.
- Clamp occurs before quantization.
- Quantization selects the nearest 5% step with deterministic half-up ties.
- Geometry and visual metrics use the quantized scale.
- Width and height use `round(base * scale)` and preserve 330:138 within integer-rounding tolerance.
- Text, face, padding, gap, and wraplength are monotonic over the supported steps.
- Legacy inference uses `sqrt((width * height) / (330 * 138)) * 100`, then clamp and quantize.
- Invalid or nonpositive legacy geometry returns 100%.

### Configuration API

Keep `CONFIG_SCHEMA_VERSION = 1` and add `window_scale_percent` to defaults.

Normalization order:

1. Preserve existing schema/source protection classification.
2. Normalize legacy width and height using their existing safe bounds.
3. If `window_scale_percent` is absent, infer it from normalized legacy geometry.
4. If present and numeric, clamp and quantize it.
5. If present but invalid, use 100% and emit a field warning.
6. Derive one `WindowMetrics` result.
7. Replace compatibility fields with derived values:
   - `font_size = metrics.text_font_size`
   - `window_width = metrics.width`
   - `window_height = metrics.height`
   - `scale_mode = "proportional"`
8. Preserve all unrelated normalized values.

Valid legacy files remain writable and are migrated in memory without an automatic disk write. Malformed, invalid-current, non-object, and future-schema files remain protected exactly as before. Saving writes the canonical percentage and derived compatibility fields atomically.

Downgrade to v0.3.2 remains usable because schema 1 is unchanged, the unknown canonical field is ignored by the old reader, and the old reader consumes the derived font/width/height/mode fields.

### Settings dialog

The normal dialog contains exactly these two `Scale` widgets:

```text
透明度
窗口大小
```

The Window Size slider uses 80–200, resolution 5, default/current canonical percentage, and a visible percentage cue. The two slider rows align. Removed controls leave no empty row.

Moving either slider changes only Tk variables. `sync_draft` writes the canonical percentage and derived compatibility fields only when Apply or Save occurs. It does not refresh quota, write disk, create work, or apply during slider movement.

Restore Defaults resets the canonical percentage to 100 and refreshes every existing draft control. Apply derives and previews the complete settings dictionary. Save applies, atomically persists, and closes. Close reapplies the opening snapshot and discards unsaved draft/session changes. Repeated Apply at the same scale is idempotent.

### Main window

At startup and every Apply:

```text
settings.window_scale_percent
→ derive WindowMetrics once
→ synchronize in-memory compatibility fields
→ recover position using metrics width/height
→ apply geometry, text font, face font, wraplength, and scaled padding/gap
```

No formula is duplicated in UI code. `Pet` may retain the latest immutable metrics as `self.window_metrics` for Compact and recovery consumers.

`safe_position`, `recover_window_if_needed`, drag, and hidden-position recovery use the current derived width/height. Apply changes dimensions without changing x/y unless the larger window no longer fits a work area, in which case the existing recovery policy makes it visible.

### Compact and expanded restoration

Compact size and edge anchoring receive `self.window_metrics.width` and `.height`. Entering Compact hides the five-row container and uses the current scaled paw/font configuration. Exiting Compact repacks the face and text with the current scaled padding/gap and restores the current derived expanded geometry. Hide/Show forces expansion through the existing path and therefore restores the same scale.

Changing scale while settings are open starts from an expanded overlay, so no separate compact draft state is needed.

## Data flow

```text
disk schema-1 JSON
  → Config API validation
  → canonical percentage or legacy inference
  → WindowMetrics
  → normalized settings plus derived compatibility fields
  → SettingsSession snapshots
  → Tk draft percentage
  → Apply/Save sync
  → Main window derives WindowMetrics once
  → geometry + typography + wrapping + spacing + Compact recovery
```

## Error behavior

- Invalid canonical scale in a readable current file falls back to 100%, emits a sanitized warning, and preserves the existing write-protection rule for field-invalid source files.
- Out-of-range numeric scales clamp and quantize without crashing.
- Invalid legacy width/height use existing defaults before inference.
- Future schema and malformed files remain byte-for-byte protected from routine writes.
- Pure metric functions never raise for user-originated scalar input; programmer contract violations are avoided by normalization.
- No broad exception handling is added around scale application.

## Compatibility and removal behavior

- Configuration schema remains 1.
- Legacy settings migrate deterministically and idempotently.
- v0.3.2 can read the persisted derived compatibility fields.
- Existing free resize helper modules remain as compatibility APIs for this release but are removed from all production UI paths and marked legacy in API documentation. Their future removal requires separate deprecation governance.
- The user-visible control removal and migration are documented in the bilingual Changelog and configuration/product/API documentation pairs.

## Resource and privacy analysis

Scale derivation is fixed-size arithmetic and effectively constant time. Slider movement updates only in-memory Tk variables. Apply derives one metrics object; Save performs the existing single atomic configuration write.

Resource boundary:

```text
new network: No
new IPC: No
new worker: No
new subprocess: No
new polling: No
new timer: No
new dependency: No
new telemetry: No
new paid service: No
Codex quota consumption: No
```

No prompt, response, session text, raw quota, token, account identifier, or credential enters the scale API, configuration additions, logs, tests, or evidence.

## Test strategy

### Pure API

- canonical metrics at 100%; safe metrics at 80%; bounded metrics at 200%;
- clamp and half-up quantization, including malformed input;
- fixed ratio within rounding tolerance;
- monotonic text/face/padding/wrap metrics;
- deterministic repeated derivation;
- geometric-mean migration, defaults, extreme clamp, and invalid geometry.

### Configuration

- new valid scale reloads identically;
- legacy 330x138 maps to 100%; arbitrary geometry maps deterministically;
- legacy font size is not independent after migration;
- new scale overrides conflicting legacy fields;
- save persists canonical and derived compatibility fields with schema 1;
- malformed/future/invalid-current protection remains;
- unrelated fields remain unchanged.

### Settings and Tk contract

- exactly two `Scale` widgets;
- opacity and Window Size labels exist;
- old font/width/height/minus/plus/proportional controls are absent;
- position and refresh entries, ordinary checkboxes, colors, and four transaction buttons remain;
- Apply/Save/Close/Restore Defaults and repeated Apply semantics;
- slider movement alone performs no owner Apply, Save, refresh, worker, or disk action.

### Main integration

- one percentage updates geometry, text font, face font, wraplength, and padding coherently;
- five stable row widgets remain;
- position recovery receives derived geometry;
- Hide/Show, Compact/Expand, and restart preserve scale;
- minimum, 100, middle-large, and maximum scales remain readable.

Every production behavior change follows an observed focused RED, minimum GREEN implementation, focused rerun, and relevant regression suite.

## Windows 11 host validation

Validate the actual running build at 80, 100, 150, and 200% on the current two-monitor Windows 11 host. Use Tk/Win32/widget/geometry inspection to record:

- canonical percentage and derived geometry;
- text and face font sizes, wraplength, and padding;
- exactly five row widgets and Reset Credit date visibility;
- fixed ratio within rounding tolerance;
- menu placement and first dispatch;
- drag when unlocked and no drag when locked;
- Hide/Show scale retention;
- Compact/Hover scale restoration;
- restart persistence and one-process/no-console behavior.

Where both connected displays remain 96 DPI, retain the existing truthful mixed-DPI non-blocking limitation; do not label simulation as physical mixed-DPI evidence.

## Documentation and release impact

Update paired canonical documents in the same commits:

- `docs/architecture/API_SPEC.md` and `.zh-CN.md`;
- `docs/architecture/CONFIGURATION.md` and `.zh-CN.md`;
- `docs/product/PRODUCT_OVERVIEW.md` and `.zh-CN.md`;
- `docs/product/ROADMAP.md` and `.zh-CN.md` where current controls/status are stale;
- `CHANGELOG.md` and `CHANGELOG.zh-CN.md` for 0.4.0;
- Windows 11 v0.4.0 test evidence.

Release through `[v0.4.0] Unify window and typography scaling`, successful Windows Quality, squash merge, main retest, tag `v0.4.0`, post-release smoke, release report, and branch deletion.

## Rollback

Return to `v0.3.2`. The old version ignores `window_scale_percent` and uses the persisted derived schema-1 `font_size`, `window_width`, `window_height`, and proportional `scale_mode`, preserving a usable last-selected size. Existing configuration backup and protected-write behavior remain available.

## Self-review result

- Placeholder scan: no unfinished placeholder language.
- Internal consistency: one canonical percentage, schema 1, 80–200/5, metric formulas, migration, UI, and Compact flow agree.
- Scope: one v0.4.0 feature with directly required compatibility and documentation work.
- Ambiguity: quantization ties, invalid input, compatibility-field ownership, legacy API retention, final range, and Compact behavior are explicit.
- Authority check: no conflict found with `ENGINEERING_STANDARD.md`, `Goal/ACTIVE_GOAL.md`, or `Goal/ACTIVE_VERSION_BRIEF.md`.
