---
document_id: SECURITY
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: SECURITY.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# Security

The default product is local-only: it uses the local Codex app-server boundary and never reads `auth.json`, stores access tokens/account IDs, sends prompts/responses/project files to third parties, logs raw quota responses, or adds telemetry without explicit opt-in and review.

Report suspected vulnerabilities privately to the maintainer before public disclosure. Do not commit credentials, session text, logs, screenshots containing sensitive data, or unreviewed provider endpoints.
