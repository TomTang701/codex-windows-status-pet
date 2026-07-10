# Codex Windows Status Pet Documentation

This directory is the development documentation home. English is canonical; a `.zh-CN.md` file beside an English document is its Chinese translation.

The active [Engineering Standard](governance/ENGINEERING_STANDARD.md) has highest precedence for repository engineering and release decisions.

## Start here

| Reader | First document |
|---|---|
| User | [Root README](../README.md) |
| Contributor | [Engineering Standard](governance/ENGINEERING_STANDARD.md), [Roadmap](product/ROADMAP.md) |
| API or UI developer | [API Specification](architecture/API_SPEC.md), [Repository Structure](architecture/REPOSITORY_STRUCTURE.md), [Configuration](architecture/CONFIGURATION.md) |
| Tester or release maintainer | [Compatibility Matrix](quality/COMPATIBILITY_MATRIX.md), [Test Error Report](archive/audits/2026-07-09-test-error-report.md) |

Architecture, testing, release, security, installation, troubleshooting, and contribution rules are indexed in [`document_manifest.json`](document_manifest.json) and linked by their category directory.

## Document classes

- **Normative:** defines required behavior or process.
- **Descriptive:** explains the current design or product.
- **Evidence:** records automated or physical test results.
- **Historical:** preserves a completed audit or superseded plan.

The repository is migrating from a flat root-level layout to the layered structure described in [the documentation structure plan](../Goal/codex-status-pet-documentation-structure-plan-zh.md). The manifest records the active source path and links remain compatible with the current layout.

## Source of truth

The English document is authoritative. Chinese translations must preserve headings, identifiers, tables, code examples, versions, and requirements, and must be updated in the same commit as substantive English changes.

The machine-readable inventory is [`document_manifest.json`](document_manifest.json). Run the repository release checks after documentation changes.
