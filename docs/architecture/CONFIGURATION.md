# Configuration

简体中文: [中文版本](CONFIGURATION.zh-CN.md)

## Location and schema

Settings are stored at `%USERPROFILE%\.codex\codex-windows-status-pet.json` and use schema version `1`. A legacy file without `schema_version` is read as the pre-version format and normalized in memory; a save writes the current schema.

The last valid file is retained at `%USERPROFILE%\.codex\codex-windows-status-pet.json.bak`. The configuration API can validate this sidecar before atomically restoring it; missing or malformed backups are ignored. Restoration is not exposed in the context menu.

Future-schema, unreadable, malformed, non-object, and field-invalid source files are read-only during routine operation. Drag, hide, toggles, recovery, shutdown, and an ordinary Save cannot overwrite them. To intentionally replace a protected source, choose **Restore Defaults** and then **Save** in the settings dialog.

```json
{
  "schema_version": 1,
  "alpha": 0.35,
  "font_color": "#e5e7eb",
  "font_size": 10,
  "background_color": "#000000",
  "topmost": true,
  "locked": true,
  "x": 4151,
  "y": 1248,
  "window_scale_percent": 100,
  "window_width": 330,
  "window_height": 138,
  "scale_mode": "proportional",
  "refresh_interval_seconds": 5,
  "compact_when_idle": false
}
```

`window_scale_percent` is the canonical expanded-size source. It is clamped to 80–200%, quantized to 5% steps, and defaults to 100%. Window width/height, text font size, paw font size, wrapping, and required spacing derive from the same pure Window Scale API result.

For schema-1 downgrade compatibility, Save also persists derived `font_size`, `window_width`, `window_height`, and `scale_mode: "proportional"`. v0.3.2 ignores the unknown canonical field and reads those usable derived values.

A valid legacy file without `window_scale_percent` is migrated in memory by geometric-mean area inference: `sqrt((old_width * old_height) / (330 * 138))`, followed by clamp and quantization. Legacy font size and scale mode do not remain independent sources. Migration preserves position, opacity, colors, refresh interval, topmost, lock, and Compact preference, and does not write disk until the user saves.

`x` and `y` are virtual-desktop coordinates and may be negative or beyond the primary display. Coordinates, opacity, colors, booleans, refresh interval, canonical scale, and legacy migration inputs are normalized before use.

## Settings transaction

The settings UI keeps persisted, active-runtime, draft, and opening-snapshot values separate:

- **Apply** previews a valid draft without persistence or closing the dialog.
- **Save** applies and persists the valid draft.
- **Restore Defaults** replaces the draft and explicitly authorizes the following Save to replace a protected source.
- **Close** restores the opening snapshot for changes that were not saved.
- A failed save preserves the previous valid settings file.

Opening or closing settings restores the main overlay to visible state. Hiding changes opacity to zero without overwriting the saved position.

The settings dialog exposes one Window Size slider. Moving it changes only the draft; Apply derives and previews the complete metric set, Save persists canonical and compatibility fields, Close restores the opening scale, and Restore Defaults resets the scale to 100%.

## Validation and recovery

Editable values require candidate, submission, and load-time validation. Invalid configuration falls back field-by-field. Coordinates must preserve valid secondary-monitor and negative positions; off-screen windows recover to a visible work area.
