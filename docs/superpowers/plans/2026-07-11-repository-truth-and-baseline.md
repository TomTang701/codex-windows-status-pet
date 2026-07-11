# Repository Truth and Baseline Implementation Plan

> **For agentic workers:** Execute these tasks sequentially in the current session. Tom's allowed-skill policy does not authorize additional execution skills by default.

**Goal:** Reconcile the repository's active documents with the released v0.4.0 state, record a measured lean-core baseline and ranked backlog, and make v0.4.1 the only active implementation scope without changing runtime behavior.

**Architecture:** This is a documentation and evidence phase. Replace the obsolete active Goal with the supplied renewal Goal, preserve the former Goal as explicitly non-normative history, keep volatile execution facts only in `EXECUTION_STATE.md`, and store measured baseline evidence in one dated audit. Update only English/Chinese document pairs whose current product claims are false.

**Tech Stack:** Markdown, Git/GitHub CLI inspection, PowerShell, Python 3.12 repository checks.

## Global Constraints

- No production behavior changes in Phase 0.
- Windows 11 x64 remains the supported baseline.
- Do not read `auth.json`, tokens, prompt/response content, or add telemetry, providers, dependencies, or services.
- One active version only: v0.4.1 correctness stabilization.
- English manifest documents are canonical; update their Chinese translation pairs in the same change.
- No push, PR, merge, tag, release, or remote branch operation without Tom's explicit authorization.

---

### Task 1: Establish authoritative repository and complexity evidence

**Files:**
- Create: `docs/archive/audits/2026-07-11-renewal-baseline.md`

**Interfaces:**
- Consumes: local `main`, `origin/main`, GitHub PR/release/Actions state, `scripts/**/*.py`, `tests/**/*.py`, active documents, `requirements.txt`, and repository check output.
- Produces: one dated, non-normative baseline with explicit counting methods, current-state facts, consumer evidence, candidate classifications, and a ranked Phase 1+ backlog.

- [ ] **Step 1: Record reconciled release facts**

  Record branch/HEAD, remote main, application version, latest merged PR, latest release/tag, latest CI, and the observed stale active-document claims. Use exact values from current commands rather than copying old active documents.

- [ ] **Step 2: Record measured complexity**

  Record production/tool Python files and LOC, test files and LOC, active normative files and LOC, API/controller modules, two runtime dependencies, Quality duration, package result, and strict RC result. State whether QA scripts are included in each count.

- [ ] **Step 3: Classify evidence-backed candidates**

  Classify at least the known legacy resize APIs, unused typed model, status presentation/error paths, active-document duplication, facade compatibility, and Quality/RC duplication as `KEEP`, `MERGE`, `DELETE`, or `DEFER`. Do not delete code in Phase 0.

- [ ] **Step 4: Verify the evidence file**

  Run:

  ```powershell
  rg -n "Current repository truth|Counting method|Candidate classification|Ranked backlog|Phase 1" docs/archive/audits/2026-07-11-renewal-baseline.md
  ```

  Expected: every required section is present and contains no future behavior claim presented as complete.

### Task 2: Replace obsolete active governance state

**Files:**
- Replace: `Goal/ACTIVE_GOAL.md`
- Remove after replacement: `Goal/CODEX_PROJECT_RENEWAL_ACTIVE_GOAL.md`
- Create: `docs/archive/plans/2026-07-10-v0.3.2-v0.4.0-release-goal.md`
- Modify: `Goal/ACTIVE_VERSION_BRIEF.md`
- Modify: `Goal/EXECUTION_STATE.md`

**Interfaces:**
- Consumes: the supplied renewal Goal and Task 1 evidence.
- Produces: one normative Goal, one v0.4.1 brief below 180 lines, one execution state below 100 lines, and one explicitly non-normative historical record of the completed release Goal.

- [ ] **Step 1: Preserve and replace the Goal**

  Archive the prior `ACTIVE_GOAL.md` with front matter:

  ```yaml
  ---
  status: archived
  normative: false
  archived_on: 2026-07-11
  superseded_by: ../../../Goal/ACTIVE_GOAL.md
  reason: Historical v0.3.2 and v0.4.0 release goal; both releases are complete.
  ---
  ```

  Then make the supplied renewal file the exact `Goal/ACTIVE_GOAL.md` content and remove the extra Goal filename.

- [ ] **Step 2: Write the v0.4.1 Active Version Brief**

  Include outcome, clipping and legacy error-path scope, explicit non-goals, protected contracts, machine-checkable content-fit/error contracts, failure paths, regression surface, Design Verification status `PENDING`, evidence classes, and exit criteria. Do not claim implementation has started.

- [ ] **Step 3: Reconcile Execution State**

  Record Phase 1/v0.4.1 as active planning scope, local `main` at current HEAD, latest evidence, the failed baseline governance result and its diagnosed cause, no human fact required, no blocker, and the next exact action: Phase 1 investigation and design verification.

- [ ] **Step 4: Run Goal governance checks**

  Run:

  ```powershell
  & .build\v032-clean-venv\Scripts\python.exe scripts\check_doc_governance.py
  (Get-Content Goal\ACTIVE_VERSION_BRIEF.md).Count
  (Get-Content Goal\EXECUTION_STATE.md).Count
  ```

  Expected: governance passes; Brief is below 180 lines; Execution State is below 100 lines.

### Task 3: Correct released-product and installation claims

**Files:**
- Modify: `docs/product/ROADMAP.md`
- Modify: `docs/product/ROADMAP.zh-CN.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Inspect without changing unless false: `docs/operations/INSTALLATION.md`
- Inspect without changing unless false: `docs/operations/INSTALLATION.zh-CN.md`

**Interfaces:**
- Consumes: released v0.4.0 source, settings UI, launcher behavior, GitHub state, and Task 1 evidence.
- Produces: bilingual released-state documentation that describes the unified window-size slider, manual launcher behavior, current 141-test baseline, and renewal phase order without candidate-release drift.

- [ ] **Step 1: Rewrite the roadmap around the renewal phases**

  Keep the protected product objective and replace stale P0-P3 implementation history with released v0.4.0 facts plus Phase 0 through Phase 5 renewal direction. Mark only Phase 1/v0.4.1 active; later phases remain conditional direction.

- [ ] **Step 2: Correct README settings and startup claims**

  Replace independent font/width/height/proportional controls with opacity plus one Window Size slider and retained settings. State that the launcher does not install automatic startup; do not claim sign-in startup unless a Startup shortcut is separately installed.

- [ ] **Step 3: Synchronize Chinese translations**

  Preserve heading/table structure, API names, versions, and paths from each English canonical document while translating prose accurately.

- [ ] **Step 4: Verify documentation facts and parity**

  Run:

  ```powershell
  & .build\v032-clean-venv\Scripts\python.exe scripts\check_doc_parity.py
  & .build\v032-clean-venv\Scripts\python.exe scripts\check_doc_links.py
  rg -n "font size|width, height|Starts automatically|remains a candidate|Pending physical evidence" README.md docs/product/ROADMAP.md
  ```

  Expected: parity and links pass; the stale English claims return no matches.

### Task 4: Verify Phase 0 and review the complete change

**Files:**
- Review: all changed files from Tasks 1-3.

**Interfaces:**
- Consumes: completed Phase 0 documentation and evidence changes.
- Produces: fresh proof that Phase 0 changed no runtime behavior and leaves one truthful active scope.

- [ ] **Step 1: Run focused documentation checks**

  Run:

  ```powershell
  & .build\v032-clean-venv\Scripts\python.exe scripts\check_doc_manifest.py
  & .build\v032-clean-venv\Scripts\python.exe scripts\check_doc_governance.py
  & .build\v032-clean-venv\Scripts\python.exe scripts\check_doc_links.py
  & .build\v032-clean-venv\Scripts\python.exe scripts\check_doc_parity.py
  ```

  Expected: all pass.

- [ ] **Step 2: Run complete current gates**

  Run:

  ```powershell
  & .build\v032-clean-venv\Scripts\python.exe scripts\run_quality_checks.py
  & .build\v032-clean-venv\Scripts\python.exe scripts\package_smoke_test.py
  & .build\v032-clean-venv\Scripts\python.exe scripts\run_release_candidate_checks.py
  ```

  Expected: Quality approved, package smoke passes, and strict RC approved.

- [ ] **Step 3: Review scope and safety**

  Run:

  ```powershell
  git diff --check
  git status --short
  git diff --stat
  git diff -- scripts tests requirements.txt start_codex_status_pet.cmd
  ```

  Expected: no whitespace errors; only planned documentation/evidence files changed; no runtime, test, dependency, or launcher diff.

- [ ] **Step 4: Reconcile the execution checkpoint**

  Update `Goal/EXECUTION_STATE.md` with final Phase 0 verification, no human fact required, no blocker, and Phase 1 investigation/design as the next exact action. Do not create a commit or perform any remote action without separate authorization.

## Self-review

- Spec coverage: Tasks 1-4 cover Phase 0 truth reconciliation, Goal replacement/archive, active-document ownership, baseline, ranked backlog, Phase 1-only scope, bilingual factual corrections, and all required gates.
- Placeholder scan: every step names concrete files, evidence, commands, and expected results.
- Interface consistency: the baseline feeds all three active documents; the final checks consume exactly the files produced by prior tasks.
- Scope check: no production code, dependency, version, release, or remote state change is included.
