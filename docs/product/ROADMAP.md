# Codex Windows Status Pet Renewal Roadmap

**Status:** Active roadmap
**Released baseline:** `v0.5.0`
**Active implementation scope:** `v0.5.1` runtime geometry reapplication stabilization

## Current state

- **Released:** v0.3.2 through v0.5.0 are merged, tagged, and published; v0.5.0 removed four unjustified production boundaries.
- **Verified baseline:** 137 core tests and 22 Tk UI tests pass on merged v0.5.0; exact-head Windows CI and merged-main RC passed with zero blockers and explicit limitations.
- **Product architecture:** the external companion uses local official Codex app-server data, local approved session metadata, five stable status rows, a notification-area adapter, and one canonical 80–200% Window Size scale.
- **Current direction:** New v0.5.0 production evidence reopened runtime geometry correctness as the only active patch scope. v0.6.0 Productization design is paused until v0.5.1 fully closes.
- **Environment limitations:** mixed-DPI physical hardware, alternate physical taskbar edges, and a separate clean Windows machine are not available and are not claimed as physical evidence.
- **Explicitly excluded:** token readers, third-party quota endpoints, telemetry, hosted services, and modifications to Codex core or built-in pet files.

## Product objective

Provide a reliable Windows companion that remains reachable on any monitor, reports Codex activity and quota data without inventing values, and exposes settings that are validated, persisted, recoverable, and machine-verifiable whenever practical.

## Delivery order

### Phase 0 — Repository truth and baseline

Reconcile released state, replace stale active governance, measure code/tests/documents/dependencies/gate duration, and rank correctness, automation, and simplification candidates. This phase changes no runtime behavior.

### Phase 1 — v0.4.1 Correctness Stabilization

Reproduce and resolve final-row clipping with an actual/requested Tk content-fit contract. Reproduce tray and quota transport failures through production paths and route their visible output through the authoritative five-row presentation boundary. No product feature or broad architecture cleanup is included.

### Phase 2 — v0.4.2 Autonomous Verification Conversion

Classify every Quality, RC, compatibility, and host check as automated, automatable, physical-only, obsolete, or duplicate. Convert machine-observable facts to one authoritative check each, consolidate duplicate gate logic, and record unavailable physical evidence once instead of asking for repeated manual confirmation.

### Phase 3 — v0.5.0 Lean-Core Simplification

Use measured consumer and compatibility evidence to delete dead code, remove compatibility APIs with no protected scenario, merge pass-through wrappers, consolidate duplicate presentation/state paths, and reduce duplicated active process prose. Preserve meaningful Tk/Windows, local transport, configuration, parsing, presentation, and refresh boundaries.

### Phase 4 — v0.5.1 Conditional State Unification

Proceed only if duplicate runtime or presentation ownership remains after Phase 3. Otherwise record `PHASE 4 NOT NEEDED`; do not invent work.

### Phase 5 — v0.6.0 Productization Decision

Paused pending v0.5.1 runtime geometry stabilization. After v0.5.1 fully closes, resume the existing decision that installer/startup productization requires a separately verified design and is not automatic.

## Protected direction

- Windows 11 x64 remains the supported baseline.
- Quota uses the local official Codex app-server; activity uses approved local session metadata.
- Five stable row identities, single instance, main-thread Tk ownership, bounded refresh, safe shutdown, tray reachability, transactional settings, proportional scaling, and configuration compatibility remain protected.
- One active version and one bounded outcome are allowed at a time.
- Do not perform a big-bang rewrite or preserve dead internals solely because implementation-detail tests import them.

## Documentation and verification rule

English manifest documents are canonical; Chinese pairs are synchronized translations in the same change. Prefer source, contract tests, Tk/Win32/process inspection, safe app-local interaction, and GitHub machine-readable state over human confirmation. Record measured evidence in dated quality/audit files and keep volatile SHAs or one-time release instructions out of long-lived roadmap prose.
