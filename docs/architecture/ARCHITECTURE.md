# Architecture

简体中文: [中文版本](ARCHITECTURE.zh-CN.md)

## Layers

```text
Windows/Tk adapters -> application controllers -> domain services/state -> pure models/policies
```

Domain and pure APIs must not import Tkinter or pystray. UI adapters render validated state and bind actions; transport adapters return normalized values without mutating UI. Background workers communicate with Tk through queues or scheduled main-thread callbacks.

Status presentation crosses the pure/UI boundary as five named rows. The pure snapshot owns order and compatibility text; the Tk adapter owns five persistent labels and updates them in place. The beta Signal HUD renders `progress`, `primary_5h`, `weekly`, and `reset_credit` in the expanded surface while Compact continues to render the battery alone.

The application, status-presentation, settings-persistence, and window-lifecycle controllers own coordination state but no widgets. `Pet` composes them and translates their decisions into Tk actions.

## Runtime boundaries

- Activity and Quota refresh channels are independent, single-flight, generation-safe, cancellable, and shutdown-aware.
- Tk calls stay on the Tk main thread; transport and filesystem work stay off it.
- The named mutex is acquired before UI creation. A second launch exits without killing another process.
- Shutdown is idempotent and prevents callbacks from scheduling new work.
- The local app-server is the quota transport boundary; no token or `auth.json` access is allowed.
- Windows Shell identity is normalized on the real root HWND after mapping, topmost/alpha transitions, Settings dialog creation, and delayed Settings close recovery so the overlay remains a tool window rather than an ordinary taskbar application.

Detailed public contracts are in [`API_SPEC.md`](API_SPEC.md); configuration transactions are in [`CONFIGURATION.md`](CONFIGURATION.md).
