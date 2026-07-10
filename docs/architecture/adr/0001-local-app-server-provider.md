---
document_id: ADR-0001
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0001-local-app-server-provider.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0001: Local app-server quota provider

## Decision

Use `codex app-server --stdio` as the only quota transport. Normalize approved fields behind QuotaProviderAPI; no UI code owns transport.

## Consequences

The app reuses the official local Codex boundary and needs no token reader or backend. Provider shape changes require sanitized fixtures and parser updates. Third-party endpoints require a new ADR and security review.
