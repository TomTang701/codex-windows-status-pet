---
document_id: ADR-0005
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0005-schema-versioned-settings.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0005: Schema-versioned settings

## Decision

Persist `schema_version` and classify loads as current, legacy, missing, malformed, or unsupported future. Malformed and future files are read-only until explicit reset.

## Consequences

Legacy settings migrate safely while old applications cannot silently downgrade newer data. Every automatic save uses the shared writable guard; schema changes require migration, fallback, and overwrite-regression tests.
