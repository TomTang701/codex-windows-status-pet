# ACTIVE VERSION BRIEF — No Active Implementation Version

## Released state

- Latest release: `v0.5.0` Lean-Core Simplification.
- Phase 1: `v0.4.1` correctness stabilization — complete.
- Phase 2: `v0.4.2` autonomous verification conversion — complete.
- Phase 3: `v0.5.0` lean-core simplification — complete.
- Phase 4: `PHASE 4 NOT NEEDED`.
- Phase 5: productization decision complete; implementation not authorized by this Goal.

## Phase 4 decision

The runtime has one coherent visible-state route:

```text
transport/activity result
→ normalized domain/coordination state
→ StatusPresentationController
→ five-row snapshot/color
→ StatusRows Tk adapter
```

`Pet` owns actual Tk geometry/visibility; `CompactState` owns delayed compact decisions. These are distinct responsibilities, not duplicate state ownership. Application refresh, settings persistence, lifecycle close state, and presentation each retain one owner. No direct emergency string/color renderer remains.

## Phase 5 decision

| Question | Decision | Evidence |
|---|---|---|
| Is the lean core stable? | Yes | v0.5.0 exact-head CI and merged-main RC passed; 159 tests, zero blockers. |
| Are supported-host routine checks automated? | Yes | v0.4.2 inventory and single RC path; no routine human visual gate for machine facts. |
| Are active docs truthful and small? | Yes | active normative LOC reduced to 953; release procedure has one formal command. |
| Is installation now the largest real usability problem? | Yes | the product still relies on a source checkout and root CMD launcher; there is no install/uninstall path, explicit startup choice, signed binary, or formal distributable. |
| Would productization add more value than another stabilization release? | Yes | no known blocking correctness issue remains; installation/startup friction is the clearest remaining user-facing gap. |

## Boundary

Do not automatically implement v0.6.0. A future productization Goal requires a separately approved design covering install/uninstall, explicit opt-in startup behavior, artifact format, clean-machine strategy, rollback, unsigned behavior, user documentation, and verification. Until then, remain on released v0.5.0.
