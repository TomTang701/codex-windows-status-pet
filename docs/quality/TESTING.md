# Testing

## Required layers

Use Unit, Contract, Integration, UI-contract, Platform, Physical, Packaging, and Soak tests as appropriate. Simulation must never be recorded as physical evidence.

## Commands

```powershell
$py = "<bundled-python>"
& $py scripts/check_doc_parity.py
& $py -m unittest discover -s tests -q
& $py scripts/run_quality_checks.py
# The only formal automated release candidate command.
& $py scripts/run_release_candidate_checks.py
```

Machine-observable UI facts require deterministic adapter, Tk, Win32, process, filesystem, or GitHub evidence. Human visual confirmation is not a routine gate. Physical evidence is reserved for unavailable hardware/topology or genuinely subjective appearance. Display/DPI changes require geometry tests plus an honest physical compatibility classification; security-boundary changes require negative and redaction tests.

`verification-inventory.json` classifies every release fact and names its one authority. `AUTOMATABLE` work must be converted when it enters release scope; `PHYSICAL-ONLY` limitations are recorded once and are not failed tests. `DUPLICATE` and `OBSOLETE` items are excluded from independent release procedure.

Physical records must include date, commit, Windows build, monitor topology, DPI, taskbar position, result, and safe evidence. Tests must not depend on a live Codex account unless explicitly marked manual.
