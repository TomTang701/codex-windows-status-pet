---
document_id: ADR-0002
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0002-tkinter-ui-framework.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0002: Tkinter UI framework

## Decision

Retain Tkinter for the overlay/settings/context menu and pystray for notification-area integration. Tk owns all UI state on its main thread.

## Consequences

Workers communicate through queues and `after` callbacks. Pure policies remain headless-testable. Replacing Tk requires a migration ADR, equivalent multi-monitor/tray behavior, and physical regression evidence.
