# Troubleshooting

简体中文: [中文版本](TROUBLESHOOTING.zh-CN.md)

- **No window:** use the tray Show action; settings also provide recovery for off-screen coordinates.
- **Duplicate tray icons:** close the existing instance through the tray before launching again; the named mutex rejects a second instance.
- **No quota:** Activity remains independent; inspect the sanitized log and app-server status without exposing credentials.
- **Popup clipped:** move the pointer to the target monitor and reopen the menu; placement is constrained to the monitor work area and taskbar reservation.
- **Startup problems:** run `scripts/startup_audit.py` in report-only mode and inspect the launcher target. It must not silently install legacy startup entries.
