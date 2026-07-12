# ACTIVE VERSION BRIEF — v0.6.1 Quota Window Identity Correctness

## Released baseline

- `v0.6.0` is the verified released segmented-battery baseline at `b7915d86a5007d76a62a7870ad248b9230fe0f4a`.
- `v0.5.5` remains the released mixed-DPI startup-position recovery patch.
- `v0.5.4` remains a closed position-persistence investigation with no product release.

## Active outcome

Investigate and correct quota-window identity only from safe official local app-server evidence. The companion must keep real 5-hour and weekly quota values on their truthful rows; a missing enabled 5-hour window must render as `5h -- / --`.

The v0.6.n default battery source is the truthfully classified weekly window. If weekly is unavailable, the battery is unavailable; it must not fall back to 5-hour data. The user-selectable source control is deferred to v0.6.3.

## Protected contracts

- Official local `codex app-server --stdio` remains the sole quota authority.
- No `auth.json`, access-token, third-party endpoint, or arbitrary unknown-field propagation.
- Five persistent row identities, the v0.6.0 ten-cell battery, mixed-DPI recovery, and Shell identity remain protected.
- No positional, dictionary-order, `primary`, or `secondary` naming assumption may determine window identity without exact safe official evidence.

## Current phase

`PROGRAM ACTIVE / v0.6.1 ROOT-CAUSE INVESTIGATION / NO PRODUCTION CORRECTION YET`
