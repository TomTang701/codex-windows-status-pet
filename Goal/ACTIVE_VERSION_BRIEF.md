# ACTIVE VERSION BRIEF — v0.6.2 Quota Row Visibility and Dynamic Distribution

## Released baseline

- `v0.6.1` is the released quota-window identity correction at `40d59c8b7d9f9f536299aacc67686ed7a70467eb`.
- `v0.6.0` is the verified released segmented-battery baseline at `b7915d86a5007d76a62a7870ad248b9230fe0f4a`.
- `v0.5.5` remains the released mixed-DPI startup-position recovery patch.
- `v0.5.4` remains a closed position-persistence investigation with no product release.

## Active outcome

Add independent visibility settings for 5-hour, weekly, and reset-credit rows. Activity and progress remain visible; enabled rows retain truthful unavailable text, while disabled persistent labels leave the layout and all visible rows evenly share the unchanged text region.

The v0.6.n default battery source is the truthfully classified weekly window. If weekly is unavailable, the battery is unavailable; it must not fall back to 5-hour data. The user-selectable source control is deferred to v0.6.3.

## Protected contracts

- Official local `codex app-server --stdio` remains the sole quota authority.
- No `auth.json`, access-token, third-party endpoint, or arbitrary unknown-field propagation.
- Five persistent row identities, the v0.6.0 ten-cell battery, mixed-DPI recovery, and Shell identity remain protected.
- No positional, dictionary-order, `primary`, or `secondary` naming assumption may determine window identity without exact safe official evidence.

## Current phase

`PROGRAM ACTIVE / v0.6.2 RELEASE CANDIDATE VERIFICATION`
