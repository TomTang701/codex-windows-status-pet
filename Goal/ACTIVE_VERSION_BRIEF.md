# FINAL VERSION BRIEF — v0.6.3 Battery Quota Source Selector

## Released product baseline

- `v0.6.3` is released at `7991c38ab19f05966025a46999c83852ea4c5b15`.
- `v0.6.2` is the released quota-row visibility and dynamic-distribution correction at `8b7c7fec2a864fa94601ed8235d04cb5cb716a03`.
- `v0.6.1` is the released quota-window identity correction at `40d59c8b7d9f9f536299aacc67686ed7a70467eb`.
- `v0.6.0` is the verified released segmented-battery baseline at `b7915d86a5007d76a62a7870ad248b9230fe0f4a`.
- `v0.5.5` remains the released mixed-DPI startup-position recovery patch; `v0.5.4` remains a closed investigation with no product release.

## Released outcome

v0.6.3 adds a persisted two-state battery quota-source selector. It selects either the truthfully classified 5-hour or weekly quota for the existing ten-cell battery; weekly is the default and no automatic fallback occurs. The v0.6.2 row-visibility settings remain layout-only and independent from source selection.

## Protected contracts retained

- Official local `codex app-server --stdio` remains the sole quota authority.
- No `auth.json`, access-token, third-party endpoint, or arbitrary unknown-field propagation.
- Five persistent row identities, the v0.6.0 ten-cell battery, mixed-DPI recovery, and Shell identity remain protected.
- No positional, dictionary-order, `primary`, or `secondary` naming assumption determines window identity.

## Final phase

`PROGRAM COMPLETE / NO ACTIVE IMPLEMENTATION SCOPE / STOPPED`
