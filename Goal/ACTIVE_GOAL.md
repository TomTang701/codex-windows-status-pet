# CLOSED GOAL — v0.5.4 Position Persistence Investigation Closure

> **Status:** CLOSURE REQUIRED / NO PRODUCT RELEASE
> **Released baseline:** `v0.5.3`
> **Investigation evidence commit:** `5d3e453 test: trace position persistence round trip`
> **Scope:** close the position-persistence investigation after the reported symptom is no longer reproducible
> **Production code changes:** FORBIDDEN unless new reproducible evidence establishes a defect
> **Product release:** NO `v0.5.4` tag or GitHub Release
> **Next feature:** `v0.6.0 5H Battery Indicator and Layout Tightening` remains NOT STARTED
> **Execution:** evidence reconciliation → documentation closure → verification-before-completion → authorized GitHub workflow → STOP

---

## 0. Mission

Close the v0.5.4 position-persistence investigation truthfully.

Tom has now confirmed:

> Restarting the software no longer loses the saved window position.

The investigation already established that the complete tested persistence path preserves the same coordinate:

```text
drag
→ unlock
→ wait for resumed polling
→ tray Exit
→ restart
→ persisted JSON
→ shutdown state
→ load
→ safe_position
→ final window
```

Observed coordinate:

```text
(4143, 1182)
```

The coordinate remained consistent through the tested path.

No first coordinate divergence was found.

The required production-equivalent RED was not established.

Design Verification was correctly marked FAILED because there was no demonstrated defect against which a root-cause fix could be validated.

The original user-visible symptom is now no longer reproducible.

Therefore:

> **Do not manufacture a RED, do not invent a root cause, do not modify production persistence logic, and do not release v0.5.4.**

The correct outcome is investigation closure.

---

## 1. Historical truth

Preserve these facts:

- `v0.5.3` remains the released product baseline.
- The v0.5.4 position-persistence investigation was started because Tom reported restart position loss.
- The running instance provenance was verified as the intended repository/runtime path and v0.5.3 baseline.
- The complete tested A-path preserved coordinate `(4143, 1182)`.
- No first coordinate divergence was identified.
- The required RED was not established.
- Design Verification therefore failed correctly.
- No production code was modified for the alleged persistence defect.
- Tom subsequently confirmed that restarting the software no longer loses the window position.
- Commit `5d3e453` contains investigation and round-trip tracing evidence.

Do not rewrite this investigation as a successful bug fix.

Do not claim that production code corrected position persistence.

Use the truthful classification:

```text
v0.5.4 position persistence
= CLOSED INVESTIGATION
= REPORTED SYMPTOM NO LONGER REPRODUCIBLE
= NO PROVEN PRODUCTION DEFECT
= NO PRODUCTION FIX
= NO PRODUCT RELEASE
```

---

## 2. Required conclusion

The investigation conclusion must state:

> The reported restart position-loss symptom is no longer reproducible. Production-equivalent tracing preserved the same virtual-desktop coordinate through persistence, shutdown, loading, safe-position validation, and final window placement. No first divergence or valid RED was established, so no production correction is justified.

Do not state:

- fixed by v0.5.4;
- persistence bug repaired;
- root cause resolved;
- regression test proves a historical production defect;
- v0.5.4 is released.

There is insufficient evidence for those claims.

---

## 3. Preserve investigation evidence

Preserve commit:

```text
5d3e453 test: trace position persistence round trip
```

Review its diff before closure.

The investigation evidence may remain when it provides focused diagnostic or regression value and does not:

- alter production behavior;
- encode a false historical claim;
- depend on temporary machine-specific state;
- expose personal paths, secrets, tokens, or credentials;
- create brittle release authority for a defect that was never reproduced.

If part of the evidence is temporary diagnostic instrumentation unsuitable for the maintained repository, remove only that temporary portion with technical justification.

Do not discard valid investigation evidence merely because the incident closes without a product release.

---

## 4. Active-state reconciliation

Reconcile the authoritative state documents.

Inspect and update only the documents that currently claim v0.5.4 is active or release-bound, including as applicable:

```text
Goal/ACTIVE_GOAL.md
Goal/ACTIVE_VERSION_BRIEF.md
Goal/EXECUTION_STATE.md
docs/product/ROADMAP.md
paired Chinese roadmap/document when required
```

The final active state must communicate:

```text
released baseline = v0.5.3

v0.5.4 position-persistence investigation
= closed
= symptom no longer reproducible
= no proven production defect
= no production release

current implementation scope = none

v0.6.0 5H Battery Indicator and Layout Tightening
= not started
= requires Tom's next approved Goal
```

Do not start v0.6.0 inside this Goal.

Do not brainstorm or design v0.6.0 inside this Goal.

---

## 5. Version and release rules

Do not:

- change `APP_VERSION` to `0.5.4`;
- create a `v0.5.4` tag;
- create a v0.5.4 GitHub Release;
- publish binaries or packages as v0.5.4;
- describe the investigation commit as a product release;
- modify changelog/release history to imply v0.5.4 shipped.

`v0.5.3` remains the latest released product baseline.

The identifier `v0.5.4` may remain in investigation history where necessary to explain the closed incident.

---

## 6. Required verification

Before claiming closure:

1. Inspect `git status`.
2. Inspect the complete diff from the released/reconciled v0.5.3 main state through the investigation closure.
3. Confirm no production persistence fix was introduced.
4. Confirm `APP_VERSION` still represents `v0.5.3`.
5. Run the focused position-persistence tests retained by the investigation.
6. Run:

```powershell
python scripts/run_quality_checks.py
```

7. Run documentation/state consistency checks provided by the repository.
8. Search active authoritative documents for stale claims that:
   - v0.5.4 is ACTIVE;
   - v0.5.4 requires a production fix;
   - v0.5.4 is release-bound;
   - v0.6.0 has started.
9. Review changed files for unrelated changes.
10. Review changed files for secrets or credentials.

A formal v0.5.4 release candidate is not required because no product release is being made.

Do not run release machinery merely to simulate a release closure.

---

## 7. Git and GitHub closure

Follow repository `AGENTS.md` authorization and identity rules.

Before remote writes:

```text
git remote -v
gh auth status
git config user.name
git config user.email
```

Verify the intended Tom-owned GitHub account/repository is:

```text
TomTang701/codex-windows-status-pet
GitHub username = tomtang701
```

Preserve valid local investigation history.

Create the minimum focused documentation/state reconciliation commit required to close the investigation.

Use a commit message consistent with repository history, for example:

```text
docs: close v0.5.4 position persistence investigation
```

Use the repository's normal authorized GitHub workflow when permitted by `AGENTS.md`.

Do not create a v0.5.4 product Release.

---

## 8. Completion report

The final report must contain:

### Conclusion

State that v0.5.4 closed as an investigation without product release because the reported symptom is no longer reproducible and no RED/root-cause defect was established.

### Evidence

Report:

- the preserved `(4143, 1182)` round-trip evidence;
- the absence of a first coordinate divergence;
- Tom's confirmation that restart no longer loses position;
- focused test result;
- Quality result;
- state-consistency result;
- final diff review result.

### Repository state

Report:

```text
released baseline = v0.5.3
v0.5.4 investigation = closed without release
current implementation scope = none
v0.6.0 = not started
```

### Remote state

Report actual commit / PR / merge results only when those actions were really performed.

Do not claim release success.

---

## 9. STOP condition

After:

```text
investigation evidence reviewed
→ active state reconciled
→ required verification passed
→ authorized closure workflow completed
→ final evidence reported
```

STOP.

Do not start:

- v0.6.0 battery indicator;
- layout tightening;
- installer work;
- startup integration;
- unrelated refactoring;
- another position-persistence correction.

Wait for Tom's next approved Goal.
