---
document_id: INSTALLATION
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/operations/INSTALLATION.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# Installation

The recommended entry point is `start_codex_status_pet.cmd`. It uses the bundled `pythonw.exe` when available and does not create a command prompt window or install a Startup-folder entry. A fallback Python environment must install `requirements.txt`.

The tested fallback versions are Python 3.11 on CI and Python 3.12.13 locally. Use x64 Windows for the verified path; Windows 10, ARM64, and 32-bit configurations remain unverified.

The application is an external companion and does not modify Codex core or built-in pet files. To stop it, use the tray Exit action or the documented process owner; do not kill unrelated processes by name.
