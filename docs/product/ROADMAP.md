# Codex Windows Status Pet Renewal Roadmap

简体中文: [中文版本](ROADMAP.zh-CN.md)

**Status:** `v0.9.2-beta.1` candidate on the isolated UI branch
**Latest stable product:** `v0.9.1`
**Active implementation scope:** Signal HUD beta validation; `main` remains unchanged

## Current state

- **Released:** v0.3.2 through v0.9.1 are merged, tagged, and published. v0.9.1 remains the latest stable product release.
- **Beta candidate:** v0.9.2-beta.1 contains the isolated Signal HUD redesign, four-row expanded layout, quota progress bars, compact percentage display, unified quota text color, and Windows Shell identity hardening. It is not a formal release yet.
- **Released v0.9.1 direction:** public REST Release bootstrap with exact product ZIP, checksum sidecar, and existing installer delegation; ordinary installation does not require GitHub CLI credentials.
- **Repository hygiene:** merged-head branch auto-deletion is enabled. The final audit removed only branches proven merged, duplicate, or superseded by later merged delivery lineage; the remote now retains only `main`.
- **Released v0.8.0 direction:** Windows productization and menu unification ship a checksum-verified PyInstaller onedir ZIP, safe per-user install/uninstall, Start Menu entry, unified localized tray/overlay menus, real packaged bilingual evidence, and clean-runner installed lifecycle CI. The ZIP and SHA-256 sidecar are published in the v0.8.0 GitHub Release.
- **Historical verification:** v0.5.3 has real root-HWND RED/GREEN, full lifecycle identity coverage, exact-head Windows CI, and merged-main RC. v0.5.2 remains a closed stale-process investigation without a product release.
- **Product architecture:** the external companion uses local official Codex app-server data, local approved session metadata, five stable status rows, a notification-area adapter, and one canonical 80–200% Window Size scale.
- **Released direction:** v0.5.4 remains a closed no-release investigation. v0.5.5 is the released mixed-DPI startup recovery patch. v0.6.0 is the released 5H Battery Indicator and Layout Tightening: it replaces the paw with a truthful 2×5 ten-cell battery while preserving five rows, compact battery-only behavior, mixed-DPI recovery, and Shell identity.
- **Released quota identity:** v0.6.1 classifies official quota windows by safe duration metadata, retains absent windows as unavailable, and keeps the default battery on the classified weekly source without fallback.
- **Released row visibility:** v0.6.2 adds optional 5-hour, weekly, and reset-credit text-row visibility with equal dynamic distribution in the unchanged text region.
- **Released battery source selector:** v0.6.3 adds a persisted two-state 5-hour/weekly battery source selector. Weekly remains the default, selected-source unavailability remains unavailable, and there is no fallback; it is independent of row visibility.
- **Released bilingual and Compact direction:** v0.7.0 enforces documentation path privacy and manifest-managed bilingual navigation, adds English/Simplified Chinese runtime UI, and replaces automatic compaction with persisted manual Compact.
- **Released v0.7.1 direction:** session metadata remains semantic until the presentation localization boundary; every manual-Compact settings re-application retains a Compact root; and Compact drag validates visible-square geometry before persisting canonical expanded-window coordinates.
- **Released v0.7.1 correction:** English activity rows now localize semantic session state at the presentation boundary, Compact remains square through settings re-application, and Compact drag persists canonical expanded-window coordinates after visible-square validation.
- **Environment limitations:** alternate physical taskbar edges and a separate clean Windows machine are not available and are not claimed as physical evidence. The 125% primary / 100% secondary mixed-DPI topology is now covered by production-equivalent Windows automation for v0.5.5.
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
