"""Windows Codex status overlay and notification-area companion."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import colorchooser
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw
import pystray


DEFAULT_SETTINGS = {
    "alpha": 0.95,
    "font_color": "#e5e7eb",
    "font_size": 10,
    "background_color": "#111827",
    "topmost": True,
    "locked": False,
    "x": 30,
    "y": 120,
}

_single_instance_mutex = None


def ensure_single_instance():
    """Terminate stale launcher instances, then keep one live process."""
    global _single_instance_mutex
    kernel32 = ctypes.windll.kernel32
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    for image in ("python.exe", "pythonw.exe"):
        try:
            subprocess.run(
                ["taskkill", "/F", "/FI", f"IMAGENAME eq {image}", "/FI", "WINDOWTITLE eq Codex Windows Status Pet"],
                startupinfo=startup,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except OSError:
            pass
    for _ in range(3):
        _single_instance_mutex = kernel32.CreateMutexW(None, True, "Local\\CodexWindowsStatusPet")
        if _single_instance_mutex and kernel32.GetLastError() != 183:
            return True
        time.sleep(0.25)
    return False


def find_codex() -> str:
    candidates = []
    configured = os.environ.get("CODEX_CLI_PATH")
    if configured:
        candidates.append(configured)
    config = Path.home() / ".codex" / "config.toml"
    if config.exists():
        for line in config.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "CODEX_CLI_PATH" in line and "=" in line:
                candidates.append(line.split("=", 1)[1].strip().strip("'\""))
    candidates.extend(["codex.exe", "codex"])
    for candidate in candidates:
        if Path(candidate).exists() or candidate in ("codex.exe", "codex"):
            return candidate
    raise FileNotFoundError("Codex CLI was not found")


class AppServer:
    def __init__(self, updates: queue.Queue):
        self.updates = updates
        self.proc = None
        self.next_id = 1
        self.pending = {}
        self.lock = threading.Lock()

    def start(self):
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = subprocess.SW_HIDE
        self.proc = subprocess.Popen(
            [find_codex(), "app-server", "--stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            startupinfo=startup,
        )
        threading.Thread(target=self._reader, daemon=True).start()
        self._send({"method": "initialize", "params": {"clientInfo": {
            "name": "codex-windows-status-pet", "title": "Codex Windows Status Pet", "version": "0.2.0"
        }, "capabilities": {"experimentalApi": True}}})
        self._send({"method": "initialized", "params": {}}, wait=False)

    def _reader(self):
        try:
            for line in self.proc.stdout:
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ident = message.get("id")
                if ident in self.pending:
                    self.pending.pop(ident)(message)
        finally:
            self.updates.put({"error": "Codex app-server stopped"})

    def _send(self, message, wait=True):
        if not self.proc or self.proc.poll() is not None:
            raise RuntimeError("Codex app-server is not running")
        ident = None
        if wait:
            with self.lock:
                ident = self.next_id
                self.next_id += 1
                message["id"] = ident
                event = threading.Event()
                result = []
                self.pending[ident] = lambda value: (result.append(value), event.set())
        self.proc.stdin.write(json.dumps(message) + "\n")
        self.proc.stdin.flush()
        if not wait:
            return None
        if not event.wait(5):
            self.pending.pop(ident, None)
            raise TimeoutError("Codex app-server request timed out")
        return result[0]

    def read_limits(self):
        response = self._send({"method": "account/rateLimits/read", "params": {}})
        if "error" in response:
            raise RuntimeError(response["error"].get("message", "rate limit request failed"))
        return response.get("result", {})

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()


def percent_left(window):
    if not isinstance(window, dict):
        return "--"
    return f"{max(0, 100 - int(window.get('usedPercent', 0)))}%"


def short_time(epoch):
    if not epoch:
        return "--"
    return datetime.fromtimestamp(epoch, tz=timezone.utc).astimezone().strftime("%H:%M")


def parse_plan(payload):
    """Return (completed, total) for JSON or JSON-like update_plan payloads."""
    raw = payload.get("input") or payload.get("arguments") or ""
    if isinstance(raw, dict):
        data = raw
    else:
        try:
            data = json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            data = None
    plan = data.get("plan") if isinstance(data, dict) else None
    if isinstance(plan, list) and plan:
        total = len(plan)
        done = sum(1 for item in plan if isinstance(item, dict) and item.get("status") == "completed")
        return done, total
    if isinstance(raw, str):
        statuses = re.findall(
            r"(?:[\"']?status[\"']?)\s*:\s*[\"'](completed|in_progress|pending)[\"']",
            raw,
        )
        if statuses:
            return statuses.count("completed"), len(statuses)
    return None


class ActivityMonitor:
    """Infer active turns and latest plan completion from Codex session JSONL."""

    def __init__(self):
        self.sessions = Path.home() / ".codex" / "sessions"
        self.stale_seconds = 600

    def snapshot(self):
        now = time.time()
        active = []
        recently_completed = []
        latest_plan = None
        latest_plan_time = -1
        if not self.sessions.exists():
            return {"active": 0, "detail": "\u7a7a\u95f2", "progress": ""}

        files = [p for p in self.sessions.rglob("*.jsonl")
                 if now - p.stat().st_mtime <= self.stale_seconds]
        for path in files:
            started = None
            completed = None
            last_phase = "\u601d\u8003\u4e2d"
            last_event_time = 0
            try:
                with path.open("r", encoding="utf-8", errors="ignore") as stream:
                    for line in stream:
                        try:
                            record = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        stamp = record.get("timestamp", "")
                        try:
                            event_time = datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()
                        except (ValueError, TypeError):
                            event_time = now
                        last_event_time = event_time
                        if record.get("type") == "event_msg":
                            event = record.get("payload", {}).get("type")
                            if event == "task_started":
                                started = event_time
                                completed = None
                                last_phase = "\u601d\u8003\u4e2d"
                            elif event == "task_complete":
                                completed = event_time
                                last_phase = "\u5df2\u5b8c\u6210"
                        elif record.get("type") == "response_item":
                            payload = record.get("payload", {})
                            item_type = payload.get("type")
                            plan = parse_plan(payload) if (
                                payload.get("name") in ("update_plan", "plan")
                                or item_type in ("function_call", "custom_tool_call")
                            ) else None
                            if plan and event_time >= latest_plan_time:
                                latest_plan = plan
                                latest_plan_time = event_time
                            if started and not completed:
                                if item_type in ("function_call", "custom_tool_call"):
                                    last_phase = "\u8c03\u7528\u5de5\u5177"
                                elif item_type in ("function_call_output", "custom_tool_call_output"):
                                    last_phase = "\u6267\u884c\u547d\u4ee4"
                                elif item_type == "message":
                                    last_phase = "\u8f93\u51fa\u4e2d"
                                elif item_type == "reasoning":
                                    last_phase = "\u601d\u8003\u4e2d"
            except OSError:
                continue

            if started and not completed and now - started <= self.stale_seconds:
                active.append((last_event_time, last_phase))
            elif completed and now - completed <= 12:
                recently_completed.append(completed)

        if active:
            active.sort(reverse=True)
            _, phase = active[0]
            if latest_plan:
                completed, total = latest_plan
                current = min(total, completed + 1)
                progress = f"\u6d3b\u52a8\u5bf9\u8bdd {len(active)} \u4e2a\uff08\u7b2c {current}/{total} \u6b65\uff09"
            else:
                progress = f"\u6d3b\u52a8\u5bf9\u8bdd {len(active)} \u4e2a"
            return {"active": len(active), "detail": phase, "progress": progress}
        if recently_completed:
            if latest_plan:
                completed, total = latest_plan
                progress = f"\u6d3b\u52a8\u5bf9\u8bdd 0 \u4e2a\uff08\u7b2c {min(total, completed + 1)}/{total} \u6b65\uff09"
            else:
                progress = "\u6700\u8fd1\u5bf9\u8bdd\u5df2\u5b8c\u6210"
            return {"active": 0, "detail": "\u5df2\u5b8c\u6210", "progress": progress}
        return {"active": 0, "detail": "\u7a7a\u95f2", "progress": "\u6ca1\u6709\u6d3b\u52a8\u4e2d\u7684\u5bf9\u8bdd"}


class TrayIcon:
    """Minimal Win32 notification-area icon with a thread-safe action queue."""

    WM_APP = 0x8000
    WM_COMMAND = 0x0111
    WM_DESTROY = 0x0002
    WM_RBUTTONUP = 0x0205
    WM_LBUTTONUP = 0x0202
    NIM_ADD = 0
    NIM_DELETE = 2
    NIF_MESSAGE = 1
    NIF_ICON = 2
    NIF_TIP = 4

    def __init__(self, actions: queue.Queue):
        self.actions = actions
        self.hwnd = None
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _debug(self, message):
        try:
            path = Path.home() / ".codex" / "codex-windows-status-pet-tray.log"
            with path.open("a", encoding="utf-8") as stream:
                stream.write(f"{datetime.now().isoformat()} {message}\n")
        except OSError:
            pass

    def _run(self):
        user32 = ctypes.windll.user32
        shell32 = ctypes.windll.shell32
        kernel32 = ctypes.windll.kernel32
        kernel32.GetModuleHandleW.restype = ctypes.c_void_p
        kernel32.GetLastError.restype = wintypes.DWORD
        user32.LoadIconW.restype = ctypes.c_void_p
        user32.CreateWindowExW.restype = ctypes.c_void_p
        user32.GetMessageW.restype = ctypes.c_int
        shell32.Shell_NotifyIconW.restype = ctypes.c_int
        WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
        class WNDCLASS(ctypes.Structure):
            _fields_ = [("style", wintypes.UINT), ("lpfnWndProc", WNDPROC), ("cbClsExtra", ctypes.c_int),
                        ("cbWndExtra", ctypes.c_int), ("hInstance", wintypes.HINSTANCE), ("hIcon", wintypes.HICON),
                        ("hCursor", wintypes.HANDLE), ("hbrBackground", wintypes.HANDLE),
                        ("lpszMenuName", wintypes.LPCWSTR), ("lpszClassName", wintypes.LPCWSTR)]
        class NOTIFYICONDATA(ctypes.Structure):
            _fields_ = [("cbSize", wintypes.DWORD), ("hWnd", wintypes.HWND), ("uID", wintypes.UINT),
                        ("uFlags", wintypes.UINT), ("uCallbackMessage", wintypes.UINT), ("hIcon", wintypes.HICON),
                        ("szTip", wintypes.WCHAR * 128), ("dwState", wintypes.DWORD), ("dwStateMask", wintypes.DWORD),
                        ("szInfo", wintypes.WCHAR * 256), ("uTimeoutOrVersion", wintypes.UINT),
                        ("szInfoTitle", wintypes.WCHAR * 64), ("dwInfoFlags", wintypes.DWORD),
                        ("guidItem", ctypes.c_byte * 16), ("hBalloonIcon", wintypes.HICON)]
        message = self.WM_APP + 11
        class_name = "CodexStatusPetTray"
        user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASS)]
        user32.CreateWindowExW.argtypes = [wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD,
                                           ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                           ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        user32.SetForegroundWindow.argtypes = [ctypes.c_void_p]
        user32.DestroyWindow.argtypes = [ctypes.c_void_p]
        user32.TrackPopupMenu.argtypes = [ctypes.c_void_p, wintypes.UINT, ctypes.c_int, ctypes.c_int,
                                          ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
        user32.PostMessageW.argtypes = [ctypes.c_void_p, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]

        @WNDPROC
        def wndproc(hwnd, msg, wparam, lparam):
            if msg == message:
                if lparam == self.WM_RBUTTONUP:
                    self._show_menu(hwnd, user32)
                elif lparam == self.WM_LBUTTONUP:
                    self.actions.put("show")
                return 0
            if msg == self.WM_COMMAND:
                command = wparam & 0xFFFF
                self.actions.put({1001: "show", 1002: "settings", 1003: "exit"}.get(command, ""))
                return 0
            if msg == self.WM_DESTROY:
                user32.PostQuitMessage(0)
                return 0
            return 0

        self._wndproc = wndproc
        kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        instance = kernel32.GetModuleHandleW(None)
        wc = WNDCLASS(0, self._wndproc, 0, 0, instance, user32.LoadIconW(None, 32512), 0, 0, None, class_name)
        registered = user32.RegisterClassW(ctypes.byref(wc))
        self._debug(f"register_class={registered} instance={bool(instance)}")
        hwnd = user32.CreateWindowExW(0, class_name, class_name, 0, 0, 0, 0, 0, 0, 0, instance, None)
        self._debug(f"create_window={bool(hwnd)} error={kernel32.GetLastError()}")
        if not hwnd:
            return
        self.hwnd = hwnd
        nid = NOTIFYICONDATA()
        nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        nid.hWnd = hwnd
        nid.uID = 1
        nid.uFlags = self.NIF_MESSAGE | self.NIF_ICON | self.NIF_TIP
        nid.uCallbackMessage = message
        nid.hIcon = user32.LoadIconW(None, 32512)
        nid.szTip = "Codex Status Pet"
        added = shell32.Shell_NotifyIconW(self.NIM_ADD, ctypes.byref(nid))
        self._debug(f"shell_notify_add={bool(added)}")
        if not added:
            user32.DestroyWindow(hwnd)
            self.hwnd = None
            return
        nid.uTimeoutOrVersion = 4
        shell32.Shell_NotifyIconW(4, ctypes.byref(nid))
        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
        shell32.Shell_NotifyIconW(self.NIM_DELETE, ctypes.byref(nid))

    def _show_menu(self, hwnd, user32):
        menu = user32.CreatePopupMenu()
        user32.AppendMenuW(menu, 0, 1001, "\u663e\u793a\uff0f\u9690\u85cf\u7a97\u53e3")
        user32.AppendMenuW(menu, 0, 1002, "\u6253\u5f00\u8bbe\u7f6e")
        user32.AppendMenuW(menu, 0x800, 0, None)
        user32.AppendMenuW(menu, 0, 1003, "\u9000\u51fa")
        point = wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(point))
        user32.SetForegroundWindow(hwnd)
        user32.TrackPopupMenu(menu, 0x0008, point.x, point.y, 0, hwnd, None)
        user32.DestroyMenu(menu)

    def stop(self):
        if self.hwnd:
            ctypes.windll.user32.PostMessageW(self.hwnd, self.WM_DESTROY, 0, 0)


class TrayIcon2:
    """Use the Tk window itself as the notification-area callback window."""

    NIM_ADD = 0
    NIM_DELETE = 2
    NIM_SETVERSION = 4
    NIF_MESSAGE = 1
    NIF_ICON = 2
    NIF_TIP = 4
    TRAY_MESSAGE = 0x8000 + 21

    def __init__(self, root, actions):
        self.root = root
        self.actions = actions
        self.debug_path = Path.home() / ".codex" / "codex-windows-status-pet-tray.log"
        self.window = tk.Toplevel(root)
        self.window.withdraw()
        self.window.title("CodexStatusPetTray")
        self.window.update_idletasks()
        self.hwnd = ctypes.c_void_p(self.window.winfo_id())
        self.user32 = ctypes.windll.user32
        self.shell32 = ctypes.windll.shell32
        self.user32.GetWindowLongPtrW.restype = ctypes.c_void_p
        self.user32.SetWindowLongPtrW.restype = ctypes.c_void_p
        self.user32.CallWindowProcW.restype = ctypes.c_ssize_t
        self.user32.GetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
        self.user32.SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_void_p]
        self.user32.CallWindowProcW.argtypes = [ctypes.c_void_p, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
        self.shell32.Shell_NotifyIconW.restype = ctypes.c_int
        self.WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

        class NOTIFYICONDATA(ctypes.Structure):
            _fields_ = [("cbSize", wintypes.DWORD), ("hWnd", wintypes.HWND), ("uID", wintypes.UINT),
                        ("uFlags", wintypes.UINT), ("uCallbackMessage", wintypes.UINT), ("hIcon", wintypes.HICON),
                        ("szTip", wintypes.WCHAR * 128), ("dwState", wintypes.DWORD), ("dwStateMask", wintypes.DWORD),
                        ("szInfo", wintypes.WCHAR * 256), ("uTimeoutOrVersion", wintypes.UINT),
                        ("szInfoTitle", wintypes.WCHAR * 64), ("dwInfoFlags", wintypes.DWORD),
                        ("guidItem", ctypes.c_byte * 16), ("hBalloonIcon", wintypes.HICON)]
        self.NOTIFYICONDATA = NOTIFYICONDATA

        @self.WNDPROC
        def callback(hwnd, msg, wparam, lparam):
            if msg == self.TRAY_MESSAGE:
                mouse_message = int(lparam) & 0xFFFF
                self._log(f"callback={mouse_message}")
                if mouse_message in (0x0201, 0x0202, 0x0203):
                    self.actions.put("show")
                elif mouse_message in (0x007B, 0x0204, 0x0205, 0x0206):
                    self.actions.put("tray_menu")
                return 0
            return self.user32.CallWindowProcW(self.old_proc, hwnd, msg, wparam, lparam)

        self.callback = callback
        self.old_proc = self.user32.GetWindowLongPtrW(self.hwnd, -4)
        self.callback_ptr = ctypes.cast(self.callback, ctypes.c_void_p)
        replaced = self.user32.SetWindowLongPtrW(self.hwnd, -4, self.callback_ptr)
        self._log(f"old_proc={bool(self.old_proc)} replaced={bool(replaced)}")
        self.nid = NOTIFYICONDATA()
        self.nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        self.nid.hWnd = self.hwnd
        self.nid.uID = 1
        self.nid.uFlags = self.NIF_MESSAGE | self.NIF_ICON | self.NIF_TIP
        self.nid.uCallbackMessage = self.TRAY_MESSAGE
        self.nid.hIcon = self.user32.LoadIconW(None, 32512)
        self.nid.szTip = "Codex Status Pet"
        self.added = bool(self.shell32.Shell_NotifyIconW(self.NIM_ADD, ctypes.byref(self.nid)))
        self._log(f"added={self.added}")
        if self.added:
            self.nid.uTimeoutOrVersion = 4
            self.shell32.Shell_NotifyIconW(self.NIM_SETVERSION, ctypes.byref(self.nid))

    def _log(self, message):
        try:
            with self.debug_path.open("a", encoding="utf-8") as stream:
                stream.write(f"{datetime.now().isoformat()} {message}\n")
        except OSError:
            pass

    def stop(self):
        if self.added:
            self.shell32.Shell_NotifyIconW(self.NIM_DELETE, ctypes.byref(self.nid))
        if self.old_proc:
            self.user32.SetWindowLongPtrW(self.hwnd, -4, self.old_proc)
        if self.window.winfo_exists():
            self.window.destroy()


class TrayIcon3:
    """Stable notification-area integration backed by pystray."""

    def __init__(self, actions):
        self.actions = actions
        image = Image.new("RGBA", (64, 64), (17, 24, 39, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((12, 12, 52, 52), fill=(147, 197, 253, 255))
        draw.ellipse((22, 18, 30, 26), fill=(17, 24, 39, 255))
        draw.ellipse((34, 18, 42, 26), fill=(17, 24, 39, 255))
        menu = pystray.Menu(
            pystray.MenuItem("\u663e\u793a\u7a97\u53e3", lambda icon, item: actions.put("show")),
            pystray.MenuItem("\u9690\u85cf\u7a97\u53e3", lambda icon, item: actions.put("hide")),
            pystray.MenuItem("\u6253\u5f00\u8bbe\u7f6e", lambda icon, item: actions.put("settings")),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("\u9000\u51fa", lambda icon, item: actions.put("exit")),
        )
        self.icon = pystray.Icon("codex-windows-status-pet", image, "Codex Status Pet", menu)
        self.thread = threading.Thread(target=self.icon.run, daemon=True)
        self.thread.start()

    def stop(self):
        self.icon.stop()


class Pet(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Codex Windows Status Pet")
        self.overrideredirect(True)
        self.settings_path = Path.home() / ".codex" / "codex-windows-status-pet.json"
        self.closing = False
        self.settings = self.load_settings()
        self.settings["x"], self.settings["y"] = self.safe_position(self.settings["x"], self.settings["y"])
        self.configure(bg=self.settings["background_color"])
        self.geometry(f"330x138+{self.settings['x']}+{self.settings['y']}")
        self.hidden = False
        self.hidden_position = (self.settings["x"], self.settings["y"])
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.queue = queue.Queue()
        self.tray_actions = queue.Queue()
        self.settings_dialog = None
        self.server = AppServer(self.queue)
        self.activity = ActivityMonitor()
        self.refresh_inflight = False
        self.topmost_var = tk.BooleanVar(value=self.settings["topmost"])
        self.locked_var = tk.BooleanVar(value=self.settings["locked"])
        self.face = tk.Label(self, text="\U0001f43e", font=("Segoe UI Emoji", 28), fg=self.settings["font_color"], bg=self.settings["background_color"])
        self.face.pack(side="left", padx=(12, 5), pady=10)
        self.text = tk.Label(self, text="Codex\n\u8fde\u63a5\u4e2d...", justify="left", anchor="w", font=("Segoe UI", self.settings["font_size"]), fg=self.settings["font_color"], bg=self.settings["background_color"])
        self.text.pack(side="left", fill="both", expand=True, pady=10)
        self.bind("<Button-3>", self.menu)
        for widget in (self.face, self.text):
            widget.bind("<Button-3>", self.menu)
            widget.bind("<B1-Motion>", self.drag)
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<ButtonRelease-1>", self.finish_drag)
        self._drag = (0, 0)
        self.apply_settings(self.settings)
        self.tray = TrayIcon3(self.tray_actions)
        self.after(100, self.process_tray_actions)
        self.after(250, self.poll)
        self.after(1000, self.refresh)

    def load_settings(self):
        settings = dict(DEFAULT_SETTINGS)
        try:
            loaded = json.loads(self.settings_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                settings.update({key: loaded[key] for key in DEFAULT_SETTINGS if key in loaded})
        except (OSError, json.JSONDecodeError):
            pass
        settings["alpha"] = min(1.0, max(0.25, float(settings["alpha"])))
        settings["font_size"] = min(20, max(8, int(settings["font_size"])))
        settings["topmost"] = bool(settings["topmost"])
        settings["locked"] = bool(settings["locked"])
        settings["x"] = int(settings["x"])
        settings["y"] = int(settings["y"])
        return settings

    def safe_position(self, x, y):
        """Preserve user-supplied virtual-desktop coordinates, including monitor 2."""
        try:
            return int(x), int(y)
        except (TypeError, ValueError):
            return 30, 120

    def save_settings(self):
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings_path.write_text(json.dumps(self.settings, ensure_ascii=False, indent=2), encoding="utf-8")

    def apply_settings(self, settings):
        self.settings = dict(settings)
        self.settings["x"], self.settings["y"] = self.safe_position(self.settings["x"], self.settings["y"])
        self.geometry(f"+{self.settings['x']}+{self.settings['y']}")
        self.attributes("-alpha", self.settings["alpha"])
        self.attributes("-topmost", self.settings["topmost"])
        bg, fg = self.settings["background_color"], self.settings["font_color"]
        self.configure(bg=bg)
        self.face.configure(bg=bg, fg=fg)
        self.text.configure(bg=bg, fg=fg, font=("Segoe UI", self.settings["font_size"]))
        self.topmost_var.set(self.settings["topmost"])
        self.locked_var.set(self.settings["locked"])

    def show_window(self):
        x, y = self.hidden_position if self.hidden else (self.settings["x"], self.settings["y"])
        x, y = self.safe_position(x, y)
        self.settings["x"], self.settings["y"] = x, y
        self.hidden_position = (x, y)
        self.geometry(f"+{x}+{y}")
        self.hidden = False
        self.state("normal")
        self.deiconify()
        self.update_idletasks()
        self.attributes("-alpha", self.settings["alpha"])
        self.attributes("-topmost", True)
        self.lift()
        self.focus_force()
        self.after(150, lambda: self.attributes("-topmost", self.settings["topmost"]))

    def ensure_visible(self):
        """Restore the overlay after any settings-dialog focus/state transition."""
        if not self.closing:
            self.show_window()

    def hide_window(self):
        if not self.hidden:
            self.hidden_position = (self.settings["x"], self.settings["y"])
            self.settings["x"], self.settings["y"] = self.hidden_position
            self.save_settings()
        self.hidden = True
        self.attributes("-alpha", 0.0)

    def start_drag(self, event):
        if not self.settings["locked"]:
            self._drag = (event.x_root - self.winfo_rootx(), event.y_root - self.winfo_rooty())

    def drag(self, event):
        if not self.settings["locked"]:
            x = event.x_root - self._drag[0]
            y = event.y_root - self._drag[1]
            x, y = self.safe_position(x, y)
            self.geometry(f"+{x}+{y}")
            self.settings["x"], self.settings["y"] = x, y

    def finish_drag(self, _event):
        if not self.settings["locked"]:
            self.save_settings()

    def menu(self, event):
        if getattr(self, "context_menu", None) is not None:
            try:
                self.context_menu.destroy()
            except tk.TclError:
                pass
        menu = tk.Menu(self, tearoff=0)
        self.context_menu = menu

        def close_menu():
            if getattr(self, "context_menu", None) is menu:
                self.context_menu = None
            try:
                menu.grab_release()
                menu.unpost()
                menu.destroy()
            except tk.TclError:
                pass

        def run_and_close(command):
            command()
            close_menu()

        menu.add_command(label="\u7acb\u5373\u5237\u65b0", command=lambda: run_and_close(self.refresh))
        menu.add_command(label="\u663e\u793a\u8bbe\u7f6e", command=lambda: run_and_close(self.show_settings))
        menu.add_checkbutton(label="\u7f6e\u9876", variable=self.topmost_var, command=lambda: run_and_close(self.toggle_topmost))
        menu.add_checkbutton(label="\u9501\u5b9a\u4f4d\u7f6e", variable=self.locked_var, command=lambda: run_and_close(self.toggle_locked))
        menu.add_separator()
        menu.add_command(label="\u9690\u85cf\u7a97\u53e3", command=lambda: run_and_close(self.hide_window))
        menu.add_command(label="\u9000\u51fa", command=lambda: run_and_close(self.close))

        # Some Windows Tk builds consume the first mouse release while the
        # posted menu is acquiring focus. Handle the release at widget level
        # so the first click always invokes the selected entry exactly once.
        def invoke_first_click(click_event):
            try:
                index = menu.index(f"@{click_event.y}")
                if index is not None and menu.type(index) not in ("separator", None):
                    menu.invoke(index)
                    return "break"
            except tk.TclError:
                pass
            return None

        menu.bind("<ButtonRelease-1>", invoke_first_click, add="+")
        menu.post(event.x_root, event.y_root)
        menu.grab_set()

    def toggle_topmost(self):
        self.settings["topmost"] = bool(self.topmost_var.get())
        self.apply_settings(self.settings)
        self.save_settings()

    def toggle_locked(self):
        self.settings["locked"] = bool(self.locked_var.get())
        self.apply_settings(self.settings)
        self.save_settings()

    def show_settings(self):
        if self.settings_dialog is not None and self.settings_dialog.winfo_exists():
            self.show_window()
            self.settings_dialog.deiconify()
            self.settings_dialog.lift()
            self.settings_dialog.focus_force()
            return
        self.show_window()
        dialog = tk.Toplevel(self)
        self.settings_dialog = dialog
        dialog.title("Codex \u5ba0\u7269\u8bbe\u7f6e")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        draft = dict(self.settings)
        body = tk.Frame(dialog, padx=14, pady=12)
        body.pack(fill="both", expand=True)
        alpha = tk.DoubleVar(value=draft["alpha"])
        size = tk.IntVar(value=draft["font_size"])
        position_x = tk.IntVar(value=draft["x"])
        position_y = tk.IntVar(value=draft["y"])
        topmost = tk.BooleanVar(value=draft["topmost"])
        locked = tk.BooleanVar(value=draft["locked"])

        tk.Label(body, text="\u900f\u660e\u5ea6").grid(row=0, column=0, sticky="w")
        tk.Scale(body, from_=0.25, to=1.0, resolution=0.05, orient="horizontal", length=230, variable=alpha).grid(row=0, column=1)
        tk.Label(body, text="\u5b57\u4f53\u5927\u5c0f").grid(row=1, column=0, sticky="w")
        tk.Scale(body, from_=8, to=20, resolution=1, orient="horizontal", length=230, variable=size).grid(row=1, column=1)
        tk.Label(body, text="\u9ed8\u8ba4\u4f4d\u7f6e (X, Y)").grid(row=2, column=0, sticky="w")
        position = tk.Frame(body)
        position.grid(row=2, column=1, sticky="w")
        tk.Entry(position, textvariable=position_x, width=8).pack(side="left")
        tk.Label(position, text=", ").pack(side="left")
        tk.Entry(position, textvariable=position_y, width=8).pack(side="left")
        tk.Checkbutton(body, text="\u7f6e\u9876", variable=topmost).grid(row=3, column=0, sticky="w")
        tk.Checkbutton(body, text="\u9501\u5b9a\u4f4d\u7f6e", variable=locked).grid(row=3, column=1, sticky="w")

        def choose_font():
            chosen = colorchooser.askcolor(color=draft["font_color"], parent=dialog)[1]
            if chosen:
                draft["font_color"] = chosen

        def choose_background():
            chosen = colorchooser.askcolor(color=draft["background_color"], parent=dialog)[1]
            if chosen:
                draft["background_color"] = chosen

        tk.Button(body, text="\u5b57\u4f53\u989c\u8272...", command=choose_font).grid(row=4, column=0, pady=(8, 0), sticky="w")
        tk.Button(body, text="\u80cc\u666f\u989c\u8272...", command=choose_background).grid(row=4, column=1, pady=(8, 0), sticky="w")

        def sync_draft():
            draft["alpha"] = float(alpha.get())
            draft["font_size"] = int(size.get())
            draft["x"] = int(position_x.get())
            draft["y"] = int(position_y.get())
            draft["topmost"] = bool(topmost.get())
            draft["locked"] = bool(locked.get())

        def apply_draft():
            sync_draft()
            self.apply_settings(draft)

        def save_and_close():
            apply_draft()
            self.save_settings()
            self.close_settings(dialog)

        def restore_defaults():
            draft.clear()
            draft.update(DEFAULT_SETTINGS)
            alpha.set(draft["alpha"])
            size.set(draft["font_size"])
            position_x.set(draft["x"])
            position_y.set(draft["y"])
            topmost.set(draft["topmost"])
            locked.set(draft["locked"])

        buttons = tk.Frame(body)
        buttons.grid(row=5, column=0, columnspan=2, pady=(14, 0))
        tk.Button(buttons, text="\u4fdd\u5b58", width=8, command=save_and_close).pack(side="left", padx=3)
        tk.Button(buttons, text="\u5e94\u7528", width=8, command=apply_draft).pack(side="left", padx=3)
        tk.Button(buttons, text="\u6062\u590d\u9ed8\u8ba4\u503c", width=12, command=restore_defaults).pack(side="left", padx=3)
        tk.Button(buttons, text="\u5173\u95ed", width=8, command=lambda: self.close_settings(dialog)).pack(side="left", padx=3)
        dialog.protocol("WM_DELETE_WINDOW", lambda: self.close_settings(dialog))
        dialog.update_idletasks()
        dialog.deiconify()
        dialog.lift()
        dialog.focus_force()
        self.after_idle(self.ensure_visible)

    def close_settings(self, dialog):
        if dialog is not None and dialog.winfo_exists():
            dialog.destroy()
        if self.settings_dialog is dialog:
            self.settings_dialog = None
        self.after_idle(self.ensure_visible)

    def process_tray_actions(self):
        if self.closing:
            return
        try:
            while True:
                action = self.tray_actions.get_nowait()
                if action == "show":
                    self.show_window()
                elif action == "hide":
                    self.hide_window()
                elif action == "tray_menu":
                    event = type("TrayEvent", (), {
                        "x_root": self.winfo_pointerx(),
                        "y_root": self.winfo_pointery(),
                    })()
                    self.menu(event)
                elif action == "settings":
                    self.show_window()
                    self.show_settings()
                elif action == "exit":
                    self.close()
        except queue.Empty:
            pass
        self.after(100, self.process_tray_actions)

    def refresh(self):
        if self.closing or self.refresh_inflight:
            return
        self.refresh_inflight = True
        def worker():
            try:
                if not self.server.proc or self.server.proc.poll() is not None:
                    self.server.start()
                payload = self.server.read_limits()
                payload["_activity"] = self.activity.snapshot()
                self.queue.put(payload)
            except Exception as exc:
                self.queue.put({"error": str(exc)})
            finally:
                self.queue.put({"_refresh_done": True})
        threading.Thread(target=worker, daemon=True).start()

    def poll(self):
        if self.closing:
            return
        try:
            while True:
                payload = self.queue.get_nowait()
                if payload.get("_refresh_done"):
                    self.refresh_inflight = False
                    if not self.closing:
                        self.after(5000, self.refresh)
                    continue
                if "error" in payload:
                    self.text.config(text="Codex\n" + payload["error"][:30], fg="#fca5a5")
                    continue
                limits = payload.get("rateLimits", {})
                primary, secondary = limits.get("primary", {}), limits.get("secondary", {})
                credits = payload.get("rateLimitResetCredits", {})
                activity = payload.get("_activity", {"detail": "\u7a7a\u95f2", "progress": ""})
                self.text.config(text=(
                    f"Codex {activity.get('detail', '\u7a7a\u95f2')}\n"
                    f"{activity.get('progress', '')}\n"
                    f"5h {percent_left(primary)} / {short_time(primary.get('resetsAt'))}\n"
                    f"\u5468 {percent_left(secondary)} / {short_time(secondary.get('resetsAt'))}\n"
                    f"\u91cd\u7f6e {credits.get('availableCount', '--')} \u6b21"
                ), fg=self.settings["font_color"])
        except queue.Empty:
            pass
        self.after(250, self.poll)

    def close(self):
        if self.closing:
            return
        self.closing = True
        self.save_settings()
        if hasattr(self, "tray"):
            self.tray.stop()
        self.server.stop()
        self.destroy()


if __name__ == "__main__":
    if sys.platform != "win32":
        raise SystemExit("This tool is for Windows.")
    if not ensure_single_instance():
        raise SystemExit(0)
    app = Pet()
    app.mainloop()
