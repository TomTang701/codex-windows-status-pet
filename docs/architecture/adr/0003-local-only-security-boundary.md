---
document_id: ADR-0003
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0003-local-only-security-boundary.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0003: Local-only security boundary

## Decision

Do not read `auth.json`, tokens, account IDs, prompt/response/project/session content, or send telemetry. Logs and diagnostics contain only sanitized derived state.

## Consequences

Some data unavailable from approved local interfaces remains unavailable rather than inferred. Any boundary expansion requires explicit user scope, threat review, negative tests, documentation, and a new ADR.
