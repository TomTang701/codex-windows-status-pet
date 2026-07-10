# Codex Development Goal：Windows 11 当前版本修复与 v0.3.0 加固

> **Repository:** `TomTang701/codex-windows-status-pet`  
> **Baseline commit:** `477acc20e635e76a98fb3e4579bd796b264bd12e`  
> **Current application version:** `0.2.0`  
> **Target milestone:** `v0.3.0`  
> **Supported development environment:** Windows 11 x64  
> **Canonical documentation language:** English  
> **Required translation:** Simplified Chinese (`.zh-CN.md`)  
> **Goal type:** Bug fix, reliability hardening, release-governance cleanup  
> **Priority order:** P0 → P1 → P2  
> **Execution rule:** Use short-lived branches and focused commits. Do not combine unrelated phases into one commit.

---

# 1. Current repository baseline

The current repository already includes:

- 88 automated tests;
- 17 manifest-registered bilingual document pairs;
- a modular `scripts/ui/main_window.py`;
- UI modules for context menu, settings dialog, and tray integration;
- domain and transport modules under `scripts/api/`;
- independent Activity and Quota refresh channels;
- strict local quota parsing;
- last-good and stale quota state handling;
- configuration schema version `1`;
- atomic configuration writes and a validated `.bak` backup;
- Windows quality-gate workflow;
- document manifest, bilingual parity, link, version, dependency, and sensitive-file checks;
- Windows 11 dual-monitor physical evidence.

Do not rebuild these systems from scratch. Extend the existing APIs and preserve current behavior unless this Goal explicitly changes it.

---

# 2. Windows support scope

## 2.1 Current supported target

For the current development cycle and v0.3.0:

```text
Supported OS: Windows 11 x64
Supported Python baseline: Python 3.11 CI, Python 3.12.x local
Supported launcher: start_codex_status_pet.cmd
Supported UI: Tkinter desktop overlay and notification-area icon
```

## 2.2 Windows 10 policy

Windows 10 is **not part of the current development or release-validation scope**.

Requirements:

- Do not create Windows 10-specific code paths.
- Do not add Windows 10 CI jobs.
- Do not require Windows 10 physical evidence.
- Do not block v0.3.0 because Windows 10 has not been tested.
- Do not claim Windows 10 support in README, Installation, Release, Roadmap, or Compatibility Matrix.
- Preserve generally compatible code when this requires no extra complexity.
- Record Windows 10 only as a future, uncommitted compatibility investigation.

Recommended wording:

```text
Windows 11 x64 is the currently supported and physically tested platform.
Windows 10 is outside the current release scope and is not claimed as supported.
```

## 2.3 Windows 11 taskbar policy

Current Windows 11 support should assume the normal bottom taskbar.

- Bottom-taskbar behavior requires physical evidence.
- Top, left, and right taskbar geometry should remain covered by pure geometry tests.
- Alternate taskbar edges are not physical-release blockers while the product only claims normal Windows 11 configurations.
- Do not use unsupported registry modifications solely to create physical evidence.

---

# 3. Overall objective

Complete the following work in order:

1. Fix the bottom `重置 N 次` line so it displays both time and date.
2. Protect future configuration schemas from downgrade overwrite.
3. Update the official support scope to Windows 11 x64 only.
4. Separate normal quality checks from strict release-candidate checks.
5. Make release-readiness data structured and deterministic.
6. Complete compilation and regression coverage for all Python modules.
7. Activate and enforce the engineering documentation standard.
8. Reduce document drift and remove manually repeated test counts.
9. Further reduce responsibilities inside the main Tk window.
10. Complete practical Windows 11 physical evidence and assess v0.3.0 readiness.

---

# 4. Global safety and architecture constraints

The following rules are mandatory throughout all phases:

- Never read `auth.json`.
- Never extract, persist, transmit, or log access tokens.
- Never store account IDs unless a separately approved requirement exists.
- Never send prompts, responses, session text, project files, or raw quota responses to third parties.
- Never add telemetry without explicit opt-in and a separate security review.
- Never modify Codex core or built-in pet files.
- The local Codex app-server remains the quota boundary.
- Tk calls stay on the Tk main thread.
- Filesystem, subprocess, and app-server work stay off the Tk thread.
- Activity and Quota refresh channels remain independent.
- Shutdown remains idempotent.
- Single-instance behavior must never kill unrelated processes.
- Unknown provider fields must not reach the UI.
- Missing quota values must never be invented.
- English documentation remains canonical.
- Required Chinese files must be updated in the same commit.

---

# 5. Phase 1 — Fix Reset Credit time-and-date display

## 5.1 Required visible contract

The quota section should use the following contract:

```text
5h 80% / 18:30
周 65% / 09:00 7/15
重置 2 次 / 18:40 7/12
```

Rules:

- The `5h` row displays local `HH:MM` only.
- The weekly row keeps its existing local `HH:MM M/D` contract.
- The `重置 N 次` row must display local `HH:MM M/D` when a valid future expiry exists.
- Month and day have no leading zero.
- The reset-credit row displays no separator or fake date when no valid expiry exists.
- The date must not silently disappear because of parsing, formatting, stale state, or UI clipping.

## 5.2 Inspect the full data path

Review:

```text
scripts/api/quota_parse_api.py
scripts/api/quota_provider_api.py
scripts/api/quota_format_api.py
scripts/api/status_snapshot_api.py
scripts/ui/main_window.py
tests/test_quota_format_api.py
tests/test_quota_parse_api.py
tests/test_status_snapshot.py
```

Determine whether the failure occurs in:

```text
provider payload
→ strict parser
→ normalized snapshot
→ earliest future expiry selection
→ local formatting
→ presentation snapshot
→ Tk label layout
```

Do not assume that the formatter is the only cause.

## 5.3 Reset Credit parser contract

Support the approved aliases that may appear inside the Reset Credit container:

```text
availableCount
available_count

expiresAt
expires_at
resetsAt
resets_at
resetAt
reset_at
expirations
credits
```

Support controlled nested objects and lists inside the Reset Credit section.

Do not perform unrestricted recursive extraction across the full provider payload.

Recommended normalized shape:

```python
{
    "availableCount": 2,
    "expirations": [
        1893456000,
        "2030-01-01T00:00:00Z",
    ],
}
```

Choose one canonical internal expiration key and use it consistently.

## 5.4 Formatting contract

Use two explicit formatting functions:

```python
def local_time_only(value) -> str:
    """Return local HH:MM or --."""

def local_time_date(value) -> str:
    """Return local HH:MM M/D or --."""
```

Requirements:

- `5h` uses `local_time_only()`.
- Reset Credit uses `local_time_date()`.
- Do not derive time-only output through arbitrary string slicing.
- Avoid platform-dependent `%-m` and `%-d`.
- Produce the same result on Windows and CI.

Recommended implementation:

```python
current = datetime.fromtimestamp(timestamp).astimezone()
return f"{current.hour:02d}:{current.minute:02d} {current.month}/{current.day}"
```

## 5.5 UI layout contract

Expanded mode must show the complete Reset Credit line.

Review:

```text
window minimum width
Label wraplength
font-size range
text padding
compact/expanded transitions
```

Requirements:

- Do not fix parsing defects only by widening the window.
- Do not silently truncate the date.
- Compact mode may hide detailed text.
- Expanded mode must preserve the complete presentation string.
- Prefer separate status-row labels or a layout API if one large label remains fragile.
- If keeping one label, calculate an appropriate wrap length from current window width.

## 5.6 Required tests

Add deterministic tests for:

```text
Reset Credit epoch expiry
Reset Credit ISO expiry
nested expiresAt
snake_case aliases
multiple expiries
past and future mixed expiries
invalid expiry values
missing expiry
no raw-field leakage
5h time-only contract
Reset Credit time-and-date contract
```

Required presentation assertion:

```python
assert re.fullmatch(
    r"重置 2 次 / \d{2}:\d{2} \d{1,2}/\d{1,2}",
    reset_line,
)
```

Also verify:

```python
assert not re.search(r"\d{1,2}/\d{1,2}", primary_5h_line)
```

## 5.7 Documentation

Update both languages for:

```text
CHANGELOG
API_SPEC
ROADMAP
COMPATIBILITY_MATRIX
```

Document:

```text
Primary 5h reset: local HH:MM.
Weekly reset: local HH:MM M/D.
Reset Credit expiry: local HH:MM M/D.
Missing provider dates are never invented.
```

## 5.8 Phase acceptance

```text
[ ] Reset Credit shows HH:MM M/D
[ ] 5h still shows HH:MM only
[ ] parsing supports the actual approved payload shape
[ ] invalid/missing expiry is safe
[ ] full line is visible in expanded mode
[ ] automated regression tests pass
[ ] Windows 11 manual verification passes
[ ] English and Chinese documents are synchronized
```

Recommended commits:

```text
Fix reset-credit expiry date display
Add reset-credit parser and presentation regressions
```

---

# 6. Phase 2 — Protect future configuration schemas

## 6.1 Existing risk

The current schema-v1 loader can safely reject an unknown schema, but the application may later save default values during:

```text
normal close
drag completion
hide action
topmost toggle
lock toggle
window recovery
settings actions
```

This may overwrite a configuration created by a future application version.

## 6.2 Introduce an explicit load result

Replace ambiguous tuple-only state with a typed result:

```python
@dataclass(frozen=True)
class ConfigLoadResult:
    settings: SettingsSnapshot
    warnings: tuple[str, ...]
    schema_status: ConfigSchemaStatus
    writable: bool
```

Suggested enum:

```text
CURRENT
LEGACY
UNSUPPORTED_FUTURE
MALFORMED
MISSING
```

## 6.3 Required behavior

### CURRENT

- load normally;
- writable;
- backup allowed.

### LEGACY

- normalize in memory;
- writable;
- save current schema when explicitly or normally persisted.

### UNSUPPORTED_FUTURE

- do not overwrite the existing file;
- automatic saves are disabled;
- log a sanitized warning;
- show a user-visible diagnostic;
- allow an explicit user-confirmed reset to current schema.

### MALFORMED

- preserve the malformed file;
- do not silently replace it during normal shutdown;
- optionally save a dated `.corrupt-*` copy;
- provide a recovery or reset action.

### MISSING

- use defaults;
- writable.

## 6.4 All persistence entry points must respect writability

Audit every call to `save_settings_atomic()`.

Do not fix only `close()`.

## 6.5 Required tests

```text
future schema sets writable=False
close does not overwrite future schema
drag does not overwrite future schema
hide does not overwrite future schema
toggle does not overwrite future schema
legacy schema migrates
current schema saves and backs up
explicit reset enables a current-schema save
malformed file remains preserved
```

Recommended commit:

```text
Protect future settings schemas from downgrade overwrite
```

---

# 7. Phase 3 — Normalize Windows 11 support documentation

Update both English and Chinese versions of:

```text
README.md
README.zh-CN.md
docs/product/ROADMAP.md
docs/product/ROADMAP.zh-CN.md
docs/governance/RELEASE.md
docs/governance/RELEASE.zh-CN.md
docs/operations/INSTALLATION.md
docs/operations/INSTALLATION.zh-CN.md
docs/quality/COMPATIBILITY_MATRIX.md
docs/quality/COMPATIBILITY_MATRIX.zh-CN.md
docs/quality/TESTING.md
docs/quality/TESTING.zh-CN.md
```

Required changes:

- Windows 11 x64 becomes the only currently supported OS.
- Remove Windows 10 from current release blockers.
- Replace Windows 10 `Pending` with one of:

```text
Deferred
Outside current scope
Not claimed
```

- The Windows 10 row may remain for transparency, but it must be explicitly non-blocking.
- Remove `Test Windows 10/11` wording from the active Roadmap.
- Do not claim ARM64 or 32-bit support.
- Keep Python 3.11 CI and Python 3.12.x local baselines.
- Document that the current binary/package may be unsigned.

Recommended commit:

```text
Define Windows 11 x64 as the current support target
```

---

# 8. Phase 4 — Separate quality gates from release-candidate gates

## 8.1 Current problem

The current release-check runner includes a non-strict physical-readiness report. This is useful for everyday CI but can be confused with a complete release approval.

## 8.2 Required scripts

Create or clearly separate:

```text
scripts/run_quality_checks.py
scripts/run_release_candidate_checks.py
```

### Quality checks

Run on every push and pull request:

```text
document manifest
document links
document parity
document metadata
version sources
sensitive-file scan
dependencies
compileall
unit and integration tests
startup audit
package smoke
non-strict physical-readiness report
```

### Release-candidate checks

Run manually and for release tags:

```text
all quality checks
strict physical-readiness gate
version/tag consistency
release changelog heading
known-issues review
rollback instructions
artifact generation
artifact checksum
```

## 8.3 GitHub Actions

Recommended workflows:

```text
.github/workflows/quality.yml
.github/workflows/release-candidate.yml
```

Triggers:

```text
quality:
  push main
  pull_request main

release candidate:
  workflow_dispatch
  tags v*
```

## 8.4 Compile all Python modules

Replace partial explicit compilation with:

```powershell
python -m compileall -q scripts
```

This must cover:

```text
scripts/*.py
scripts/api/*.py
scripts/ui/*.py
future nested Python modules
```

Recommended commits:

```text
Separate quality and release-candidate gates
Compile the complete Python source tree
```

---

# 9. Phase 5 — Make compatibility evidence structured

## 9.1 Add stable IDs and explicit blocking state

Replace the current free-form matrix with:

| ID | Area | Coverage | Status | Blocking | Evidence / next action |
|---|---|---|---|---|---|

Allowed status values:

```text
Pending
Automated pass
Physical pass
Partial
Deferred
Approved limitation
Not applicable
Blocked
```

Allowed blocking values:

```text
Yes
No
```

Examples:

```text
WIN11-X64        Physical pass   Yes
WIN10-DEFERRED   Deferred        No
TASKBAR-BOTTOM   Physical pass   Yes
TASKBAR-ALT      Automated pass  No
DPI-MIXED        Partial         depends on claimed scope
```

## 9.2 Release-readiness parser

Do not infer blockers from arbitrary words such as `partial`.

The script must parse the explicit Blocking column.

Release is blocked only when:

```text
Blocking == Yes
and Status not in {Automated pass, Physical pass, Approved limitation, Not applicable}
```

## 9.3 Windows 11 physical scope

Required physical evidence for v0.3.0:

```text
Windows 11 x64 startup
normal bottom taskbar
single-instance repeated launch
tray hide and show
settings open/apply/save/close
Reset Credit complete date display
one-monitor mode
two-monitor mode when available
monitor disconnect/reconnect when practical
compact idle shrink and hover expansion
normal shutdown and repeated shutdown
configuration backup restore
```

Physical evidence not required for v0.3.0:

```text
Windows 10
ARM64
32-bit Windows
top/left/right Windows taskbars
unsupported registry-modified taskbars
```

## 9.4 Clean environment policy

A separate Windows PC is not mandatory.

Accept one of:

```text
fresh local venv on Windows 11
fresh Windows Sandbox session when available
fresh Windows VM when available
separate Windows 11 machine
```

The evidence must state which environment was used.

Recommended commit:

```text
Structure Windows 11 compatibility evidence
```

---

# 10. Phase 6 — Activate document governance

## 10.1 Engineering Standard

Review and change:

```json
"status": "active",
"required_for_release": true
```

for `ENGINEERING-STANDARD`.

Reference it from:

```text
README
docs/README
CONTRIBUTING
RELEASE
```

## 10.2 Document metadata

Add front matter to active maintained documents:

```yaml
---
document_id: API-SPEC
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: API_SPEC.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
```

Chinese files must reference the canonical English file.

## 10.3 Enforce manifest fields

Add checks for:

```text
manifest ID matches front matter
document versions match
translation pair exists
required release documents exist
active normative files are registered
archived files do not act as active rules
review age produces warnings or release blockers
orphan active documents are rejected
```

## 10.4 Strengthen bilingual checks

Keep structural checks and add comparison of:

```text
document ID
document version
API names
test IDs
compatibility IDs
semantic versions
configuration schema versions
table first-column keys
code-fence language tags
```

Do not require literal English/Chinese line equality.

Recommended commits:

```text
Activate the engineering documentation standard
Enforce document metadata and review policy
Strengthen bilingual semantic checks
```

---

# 11. Phase 7 — Simplify the Roadmap

The current Roadmap repeats completed P0/P1 work and manually maintained test counts.

Replace it with:

```text
Current baseline
Now
Next
Later
Blocked
Deferred
Out of scope
```

Rules:

- Completed implementation details move to Changelog or release notes.
- Do not manually repeat the automated test count in multiple documents.
- Windows 10 belongs under `Deferred`, not `Blocked`.
- Current supported platform is Windows 11 x64.
- Each active item should have an exit criterion.
- Each blocked item should name its blocker.
- Keep API catalog details in API_SPEC, not Roadmap.

Recommended commit:

```text
Refocus the roadmap on active future work
```

---

# 12. Phase 8 — Continue application modularization

The main window has been extracted, but it still coordinates many responsibilities.

## 12.1 Target boundaries

Introduce or strengthen:

```text
ApplicationController
StatusPresentationController
SettingsPersistenceController
WindowLifecycleController
```

The Tk window should primarily:

```text
create widgets
bind events
render presentation state
schedule main-thread callbacks
```

It should not directly own:

```text
provider parsing
configuration schema decisions
retry/backoff policy
release diagnostics
raw refresh-generation logic
```

## 12.2 Status-row UI

Consider replacing the single multiline text label with separate rows:

```text
activity row
progress row
5h quota row
weekly quota row
reset-credit row
```

Benefits:

- Reset Credit dates cannot be silently clipped.
- Each row has an explicit format contract.
- Long diagnostics can wrap independently.
- Quota rows can remain single-line.
- Tests can target stable row IDs.

Do not perform this refactor before the Reset Credit bug has a focused regression test.

## 12.3 Required tests

```text
controller state transitions
no Tk calls from workers
stale generation ignored
shutdown prevents new scheduling
status rows preserve text
compact-to-expanded restoration
tray restart remains single-scheduled
```

Recommended commits:

```text
Extract application coordination from the Tk window
Split quota presentation into stable status rows
```

---

# 13. Phase 9 — Windows 11 physical validation

Create dated records under:

```text
docs/quality/test-records/
```

Each record must include:

```text
date
commit
app version
Windows 11 edition/build
Python/runtime
monitor topology
DPI/scaling
taskbar state
steps
expected
actual
result
limitations
safe evidence
```

Minimum practical records:

```text
Reset Credit date display
single-monitor mode
dual-monitor mode
hide/show through tray
settings transaction behavior
configuration backup restore
compact idle and hover
normal close and repeated close
fresh environment installation
```

Do not record simulated results as physical passes.

Do not include credentials, account identifiers, prompt text, response text, session content, or project files.

---

# 14. Test and validation commands

Before every substantial commit:

```powershell
python -m compileall -q scripts
python -m unittest discover -s tests -q
python scripts/check_doc_manifest.py
python scripts/check_doc_links.py
python scripts/check_doc_parity.py
python scripts/check_version_sources.py
python scripts/check_sensitive_files.py
python scripts/check_dependencies.py
python scripts/run_release_checks.py
python scripts/package_smoke_test.py
git diff --check
```

After gate separation:

```powershell
python scripts/run_quality_checks.py
```

For a release candidate:

```powershell
python scripts/run_release_candidate_checks.py
```

The release-candidate command must fail when a required Windows 11 blocking row is incomplete.

---

# 15. Recommended commit sequence

```text
1. Fix reset-credit expiry date display
2. Add reset-credit parser and presentation regressions
3. Protect future settings schemas from downgrade overwrite
4. Define Windows 11 x64 as the current support target
5. Structure Windows 11 compatibility evidence
6. Separate quality and release-candidate gates
7. Compile the complete Python source tree
8. Activate the engineering documentation standard
9. Enforce document metadata and review policy
10. Strengthen bilingual semantic checks
11. Refocus the roadmap on active future work
12. Extract application coordination from the Tk window
13. Split quota presentation into stable status rows
14. Record remaining Windows 11 physical evidence
15. Prepare the v0.3.0 release candidate
```

Each commit must:

- contain one coherent change;
- include relevant tests;
- update English and Chinese documents when applicable;
- pass the quality gate;
- avoid unrelated formatting churn.

---

# 16. Definition of Done

## Reset Credit

```text
[ ] Reset Credit displays HH:MM M/D
[ ] 5h remains HH:MM only
[ ] approved provider aliases are parsed
[ ] missing dates are not invented
[ ] expanded UI shows the full line
[ ] regressions are covered by automated tests
[ ] Windows 11 physical evidence exists
```

## Configuration safety

```text
[ ] future schemas are read-only
[ ] automatic saves cannot overwrite future schemas
[ ] all save entry points respect writability
[ ] malformed files are preserved
[ ] legacy migration remains supported
```

## Platform scope

```text
[ ] Windows 11 x64 is the only claimed current platform
[ ] Windows 10 is marked deferred/non-blocking
[ ] Windows 10 is removed from active test requirements
[ ] ARM64 and 32-bit Windows remain unclaimed
[ ] normal bottom taskbar is the physical target
```

## Quality and release

```text
[ ] all Python source files compile
[ ] quality and release-candidate gates are distinct
[ ] release candidate uses strict structured blockers
[ ] package smoke passes
[ ] version sources agree
[ ] sensitive-file and dependency checks pass
```

## Documentation governance

```text
[ ] Engineering Standard is active
[ ] required-for-release metadata is enforced
[ ] document metadata is validated
[ ] bilingual semantic identifiers are checked
[ ] Roadmap contains active future work rather than completed history
```

## Architecture

```text
[ ] Tk window responsibilities are reduced
[ ] workers do not call Tk
[ ] Activity and Quota remain independent
[ ] shutdown remains idempotent
[ ] status rows preserve complete quota text
```

## Windows 11 evidence

```text
[ ] required Windows 11 blocking rows are complete
[ ] each physical pass has a dated record
[ ] no Windows 10 evidence is required
[ ] unavailable configurations are transparently marked Deferred or Approved limitation
```

---

# 17. Stop conditions

Stop and report rather than guess when:

- the real Reset Credit payload shape is uncertain;
- timestamps may be milliseconds rather than seconds;
- the running executable comes from a different repository copy;
- a stale `pythonw.exe` process is serving old code;
- configuration behavior could overwrite user data;
- a change would require token or authentication access;
- a physical result cannot be reproduced;
- a compatibility claim exceeds the tested Windows 11 environment.

When stopped:

1. preserve the safe behavior;
2. add a minimal sanitized fixture;
3. record the unknown field or condition;
4. do not mark the requirement as passed;
5. provide the exact next verification step.

---

# 18. Required final Codex report

At the end of execution, report:

1. baseline and final commit;
2. root cause of the Reset Credit date issue;
3. changed files;
4. tests added or changed;
5. quality-gate output;
6. Windows 11 physical evidence;
7. configuration migration behavior;
8. documentation changes;
9. remaining non-blocking deferred items;
10. remaining release blockers;
11. whether v0.3.0 is a Release Candidate;
12. commit SHA for every completed phase.

Do not report only “fixed” or “tests passed.” Provide verifiable evidence.
