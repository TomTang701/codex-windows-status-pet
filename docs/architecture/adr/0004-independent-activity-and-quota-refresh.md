---
document_id: ADR-0004
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0004-independent-activity-and-quota-refresh.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0004: Independent Activity and Quota refresh

## Decision

Activity and Quota use independent single-flight channels, generations, clocks, workers, and failure state. Neither waits for or cancels the other.

## Consequences

Slow app-server I/O cannot freeze Activity or Tk. Stale callbacks are discarded and shutdown cancels both channels. Cross-channel coupling requires explicit architecture review and race tests.
