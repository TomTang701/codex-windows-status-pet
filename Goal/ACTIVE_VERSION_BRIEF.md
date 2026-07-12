# ACTIVE VERSION BRIEF — v0.5.2 Rendered Content Visibility Contract Correction

## Historical truth

- v0.5.1 remains released from commit `10de01410126a1877ac9406fc02e3bc583659df3` through PR #17.
- PR #18 reconciled main at `71c2719fca0ac4cfe3fa9ce1ffb6d675fe074fa8`.
- The then-current Quality, Tk, DPI/scale, lifecycle, and RC contracts passed.
- New production screenshot evidence invalidates only the v0.5.1 rendered-visibility completion claim; it does not rewrite release history.

## Active incident

The released application can visibly clip the fifth `reset_credit` row at the expanded client bottom even though the previous authority reported 50 DPI/scale combinations and 15 lifecycle transitions fitted.

Incident root cause: the supplied screenshot came from a process started before the v0.5.1 fix; current disk version/HEAD was incorrectly used as proof of the already-running process's loaded code. A released-v0.5.1 rendered defect is not reproduced.

## Required outcome

Identify the exact false-positive mechanism, reproduce released v0.5.1 through the real production presentation route with a rendered-boundary RED, correct one root cause, replace the insufficient authority, and release v0.5.2.

## Status

`v0.5.2 INVESTIGATION ACTIVE / DESIGN VERIFICATION FAILED / v0.6.0 BLOCKED`

No production geometry, DPI-order, font, padding, or height modification is permitted. The required released-v0.5.1 RED is unavailable: after an evidence-backed restart, the released code renders the fifth row completely.
