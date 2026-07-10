---
document_id: ARCHITECTURE
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/ARCHITECTURE.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# Architecture

## Layers

```text
Windows/Tk adapters -> application controllers -> domain services/state -> pure models/policies
```

Domain and pure APIs must not import Tkinter or pystray. UI adapters render validated state and bind actions; transport adapters return normalized values without mutating UI. Background workers communicate with Tk through queues or scheduled main-thread callbacks.

## Runtime boundaries

- Activity and Quota refresh channels are independent, single-flight, generation-safe, cancellable, and shutdown-aware.
- Tk calls stay on the Tk main thread; transport and filesystem work stay off it.
- The named mutex is acquired before UI creation. A second launch exits without killing another process.
- Shutdown is idempotent and prevents callbacks from scheduling new work.
- The local app-server is the quota transport boundary; no token or `auth.json` access is allowed.

Detailed public contracts are in [`API_SPEC.md`](API_SPEC.md); configuration transactions are in [`CONFIGURATION.md`](CONFIGURATION.md).

## Components and dependency direction

```text
launcher -> runtime guard -> Tk main window
Tk main window -> UI adapters -> pure API policies
background Activity worker -> queue -> Tk poll/render
background Quota worker -> local app-server -> normalized snapshot -> queue -> Tk poll/render
tray thread -> action queue -> Tk action dispatcher
```

Dependencies point inward: UI and transport adapters may call API policies, but pure API modules never import Tk, pystray, or concrete window objects. Queue payloads are small normalized dictionaries containing a channel, generation, and approved activity/quota result or a sanitized error; raw provider objects never cross into presentation.

## Startup and shutdown sequence

Startup configures logging and DPI awareness, acquires the named mutex, loads and classifies settings, creates Tk state, starts the tray adapter, then schedules independent Activity and Quota refreshes. Quota starts the local app-server only from a background worker.

Shutdown first marks the application closing, cancels refresh generations, blocks new callbacks, conditionally persists writable settings, stops tray and app-server idempotently, destroys Tk, and releases the mutex. Repeated shutdown requests are harmless.

## State lifecycles and recovery

Settings move through persisted, opening snapshot, draft, and runtime states. Unsupported future or malformed configuration is read-only until an explicit reset. Activity and Quota retain separate generations and failure state; a Quota transport failure may use a recent last-good snapshot but must visibly become stale. Display topology is periodically re-evaluated, and only genuinely unreachable windows are moved. Tray failure schedules at most one restart; app-server failure is isolated to Quota and does not stop Activity.

## Decision records

Current architecture decisions are recorded in [`adr/`](adr/), including the local provider, Tkinter, local-only security boundary, independent refresh channels, and schema-versioned settings.
