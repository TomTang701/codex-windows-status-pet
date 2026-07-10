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

## Threat model and sensitive data

Threats include malicious or malformed settings/JSONL/provider data, command or argument injection, executable-path replacement, credential leakage through logs/diagnostics, unsafe third-party endpoints, and tampered release artifacts. Sensitive data includes tokens, account identifiers, prompts, responses, project/session content, raw quota payloads, private filesystem content, and screenshots or logs containing any of them.

All parsers use allowlisted fields, bounded traversal, size/time limits where applicable, and safe fallback. Subprocesses use argument arrays and approved executable discovery; no untrusted value is interpolated into a shell command. Executable-path changes and new providers require a dedicated security review, contract fixtures, and maintainer approval.

## Logging, reports, and artifacts

Operational logs contain only sanitized state, error type, and safe paths. Diagnostics never include raw payloads or content. Vulnerabilities are reported privately through the repository owner's private contact or a private GitHub security advisory; public issues must contain no exploit secret or personal data.

Release candidates pass sensitive-file/dependency checks, strict evidence gates, package inspection, and checksum generation. Unsigned artifacts are labeled as such; a checksum proves integrity of the published bytes but is not a code signature.
