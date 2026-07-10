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
