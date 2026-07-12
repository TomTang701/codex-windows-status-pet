# Installation

简体中文: [中文版本](INSTALLATION.zh-CN.md)

The recommended entry point is `start_codex_status_pet.cmd`. It uses the bundled `pythonw.exe` when available and does not create a command prompt window or install a Startup-folder entry. A fallback Python environment must install `requirements.txt`.

The tested fallback versions are Python 3.11 on CI and Python 3.12.13 locally. The supported path is Windows 11 x64. Windows 10 is Deferred, Not claimed, and Non-blocking; ARM64 and 32-bit Windows are also not claimed.

The application is an external companion and does not modify Codex core or built-in pet files. To stop it, use the tray Exit action or the documented process owner; do not kill unrelated processes by name.
