# ACTIVE VERSION BRIEF — v0.6.3 Battery Quota Source Selector

## Released baseline

- `v0.6.1` is the released quota-window identity correction at `40d59c8b7d9f9f536299aacc67686ed7a70467eb`.
- `v0.6.2` is the released quota-row visibility and dynamic-distribution correction at `8b7c7fec2a864fa94601ed8235d04cb5cb716a03`.
- `v0.6.0` is the verified released segmented-battery baseline at `b7915d86a5007d76a62a7870ad248b9230fe0f4a`.
- `v0.5.5` remains the released mixed-DPI startup-position recovery patch.
- `v0.5.4` remains a closed position-persistence investigation with no product release.

## Active outcome

Add a two-state persisted battery source selector. It selects either the real 5-hour or real weekly quota for the existing ten-cell battery while keeping weekly as the default and never falling back. The three v0.6.2 row-visibility settings remain layout-only and independent.

The v0.6.n default battery source is the truthfully classified weekly window. If the selected source is unavailable, the battery is unavailable; it must not fall back to the other quota window.

## Protected contracts

- Official local `codex app-server --stdio` remains the sole quota authority.
- No `auth.json`, access-token, third-party endpoint, or arbitrary unknown-field propagation.
- Five persistent row identities, the v0.6.0 ten-cell battery, mixed-DPI recovery, and Shell identity remain protected.
- No positional, dictionary-order, `primary`, or `secondary` naming assumption may determine window identity without exact safe official evidence.

## Current phase

`PROGRAM ACTIVE / v0.6.3 DESIGN VERIFIED / IMPLEMENTATION PLAN NEXT`
