# ACTIVE VERSION BRIEF — v0.7.0 Bilingual UI and Manual Compact

## Released baseline

- `v0.6.3` is released at `7991c38ab19f05966025a46999c83852ea4c5b15`.
- `v0.6.2` is the released quota-row visibility and dynamic-distribution correction at `8b7c7fec2a864fa94601ed8235d04cb5cb716a03`.
- `v0.6.1` is the released quota-window identity correction at `40d59c8b7d9f9f536299aacc67686ed7a70467eb`.
- `v0.6.0` is the verified released segmented-battery baseline at `b7915d86a5007d76a62a7870ad248b9230fe0f4a`.
- `v0.5.5` remains the released mixed-DPI startup-position recovery patch; `v0.5.4` remains a closed investigation with no product release.

## Approved v0.7.0 outcome

v0.7.0 adds English and Simplified Chinese runtime UI with English as the persisted default, then replaces automatic idle compaction with a persisted manual Compact setting. The existing selected battery source, weekly default, no-fallback behavior, and row-visibility independence remain unchanged.

## Protected contracts retained

- Official local `codex app-server --stdio` remains the sole quota authority.
- No `auth.json`, access-token, third-party endpoint, or arbitrary unknown-field propagation.
- Five persistent row identities, the v0.6.0 ten-cell battery, mixed-DPI recovery, and Shell identity remain protected.
- No positional, dictionary-order, `primary`, or `secondary` naming assumption determines window identity.

## Active phase

`Phase B/C implementation complete on the release-candidate branch; formal regression, package smoke, Quality, RC, and remote release gates remain.`
