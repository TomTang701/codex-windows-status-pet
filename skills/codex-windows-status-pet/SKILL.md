---
name: codex-windows-status-pet
description: Run the local Windows Codex status pet that shows 5-hour and weekly rate limits plus reset credits.
---

# Codex Windows Status Pet

Run `scripts/codex_status_pet.py` with the bundled Python runtime or a normal Windows Python installation. The pet talks only to the local `codex app-server --stdio`; it does not read `auth.json`, call a third-party endpoint, or upload project data.

Use the right-click menu to refresh or exit. Drag the pet with the left mouse button.
