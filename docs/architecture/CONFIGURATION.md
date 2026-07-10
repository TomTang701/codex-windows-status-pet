# Configuration

## Location and schema

Settings are stored at `%USERPROFILE%\.codex\codex-windows-status-pet.json`. The current file predates schema-versioned migration; adding a schema version is a required follow-up before a breaking configuration change.

The last valid file is retained at `%USERPROFILE%\.codex\codex-windows-status-pet.json.bak`. The context menu action **Restore Previous Settings** validates this sidecar before atomically restoring it; missing or malformed backups are ignored.

```json
{
  "alpha": 0.35,
  "font_color": "#e5e7eb",
  "font_size": 10,
  "background_color": "#000000",
  "topmost": true,
  "locked": true,
  "x": 4151,
  "y": 1248,
  "window_width": 330,
  "window_height": 138,
  "scale_mode": "free",
  "refresh_interval_seconds": 5,
  "compact_when_idle": false
}
```

`x` and `y` are virtual-desktop coordinates and may be negative or beyond the primary display. Width, height, opacity, font size, colors, booleans, scale mode, and refresh interval are normalized through the input-validation API before use.

## Settings transaction

The settings UI keeps persisted, active-runtime, draft, and opening-snapshot values separate:

- **Apply** previews a valid draft without persistence or closing the dialog.
- **Save** applies and persists the valid draft.
- **Restore Defaults** replaces the draft first.
- **Close** restores the opening snapshot for changes that were not saved.
- A failed save preserves the previous valid settings file.

Opening or closing settings restores the main overlay to visible state. Hiding changes opacity to zero without overwriting the saved position.

## Validation and recovery

Editable values require candidate, submission, and load-time validation. Invalid configuration falls back field-by-field. Coordinates must preserve valid secondary-monitor and negative positions; off-screen windows recover to a visible work area.
