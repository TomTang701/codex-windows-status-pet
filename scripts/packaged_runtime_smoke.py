"""Exercise the actual Windows EXE lifecycle without a source fallback."""

from __future__ import annotations

import ctypes
import struct
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

from package_smoke_test import static_package_smoke
from api.release_artifact_api import RELEASE_ROOT_NAME, validate_release_archive
from api.runtime_api import SINGLE_INSTANCE_MUTEX_NAME


WM_CLOSE = 0x0010
BM_CLICK = 0x00F5
WM_NULL = 0x0000
WINDOWS_GUI_SUBSYSTEM = 2
TH32CS_SNAPPROCESS = 0x00000002


class _ProcessEntry(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_ulong),
        ("cntUsage", ctypes.c_ulong),
        ("th32ProcessID", ctypes.c_ulong),
        ("th32DefaultHeapID", ctypes.c_size_t),
        ("th32ModuleID", ctypes.c_ulong),
        ("cntThreads", ctypes.c_ulong),
        ("th32ParentProcessID", ctypes.c_ulong),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", ctypes.c_ulong),
        ("szExeFile", ctypes.c_wchar * 260),
    ]


def pe_subsystem(executable):
    """Return the PE subsystem field or fail visibly for a malformed binary."""
    data = Path(executable).read_bytes()
    if len(data) < 0x40 or data[:2] != b"MZ":
        raise ValueError("executable is not a PE file")
    header = struct.unpack_from("<I", data, 0x3C)[0]
    subsystem_offset = header + 24 + 68
    if data[header:header + 4] != b"PE\0\0" or len(data) < subsystem_offset + 2:
        raise ValueError("executable is not a PE file")
    return struct.unpack_from("<H", data, subsystem_offset)[0]


def process_tree_ids(root_process_id, processes):
    """Return one process and every descendant from (pid, parent_pid) rows."""
    descendants = {int(root_process_id)}
    changed = True
    while changed:
        changed = False
        for process_id, parent_process_id in processes:
            if parent_process_id in descendants and process_id not in descendants:
                descendants.add(process_id)
                changed = True
    return frozenset(descendants)


def live_process_tree_ids(root_process_id, processes):
    """Return only extant descendants when a PyInstaller parent already exited."""
    rows = tuple(processes)
    existing = {process_id for process_id, _parent_process_id in rows}
    return process_tree_ids(root_process_id, rows) & existing


def _process_snapshot():
    if sys.platform != "win32":
        raise RuntimeError("packaged runtime smoke requires Windows")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    invalid = ctypes.c_void_p(-1).value
    if snapshot == invalid:
        raise OSError(ctypes.get_last_error(), "CreateToolhelp32Snapshot failed")
    try:
        entry = _ProcessEntry()
        entry.dwSize = ctypes.sizeof(entry)
        rows = []
        if not kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
            raise OSError(ctypes.get_last_error(), "Process32FirstW failed")
        while True:
            rows.append((
                int(entry.th32ProcessID),
                int(entry.th32ParentProcessID),
                str(entry.szExeFile),
            ))
            if not kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                break
        return tuple(rows)
    finally:
        kernel32.CloseHandle(snapshot)


def _process_rows():
    return tuple((process_id, parent_process_id) for process_id, parent_process_id, _name in _process_snapshot())


def _process_tree_ids(root_process_id):
    return process_tree_ids(root_process_id, _process_rows())


def _live_process_tree_ids(root_process_id):
    return live_process_tree_ids(root_process_id, _process_rows())


def _named_mutex_exists():
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenMutexW.restype = ctypes.c_void_p
    handle = kernel32.OpenMutexW(0x00100000, False, SINGLE_INSTANCE_MUTEX_NAME)
    if not handle:
        return False
    kernel32.CloseHandle(ctypes.c_void_p(handle))
    return True


def _window_handles_for_processes(process_ids):
    """Return top-level Windows owned by one test process."""
    if sys.platform != "win32":
        raise RuntimeError("packaged runtime smoke requires Windows")
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    handles = []

    @callback_type
    def collect(handle, _parameter):
        owner = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(handle, ctypes.byref(owner))
        if owner.value in process_ids:
            handles.append(handle)
        return True

    user32.EnumWindows(collect, None)
    return handles


def _window_class_name(handle):
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    class_name = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(handle, class_name, len(class_name))
    return class_name.value


def _duplicate_dialog_handles(process_id):
    return [
        handle
        for handle in _window_handles_for_processes(_live_process_tree_ids(process_id))
        if _window_class_name(handle) == "#32770"
    ]


def _child_window_handles(parent_handle):
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    handles = []

    @callback_type
    def collect(handle, _parameter):
        handles.append(handle)
        return True

    user32.EnumChildWindows(parent_handle, collect, None)
    return handles


def _duplicate_dialog_button_handles(process_id):
    return [
        child_handle
        for dialog_handle in _duplicate_dialog_handles(process_id)
        for child_handle in _child_window_handles(dialog_handle)
        if _window_class_name(child_handle) == "Button"
    ]


def _window_is_responsive(handle):
    """Require the native duplicate-instance notice to enter its message loop."""
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    result = ctypes.c_size_t()
    return bool(user32.SendMessageTimeoutW(
        handle, WM_NULL, 0, 0, 0x0002, 1000, ctypes.byref(result)
    ))


def duplicate_notice_ready(root_process_id):
    handles = _duplicate_dialog_handles(root_process_id)
    return bool(handles) and all(_window_is_responsive(handle) for handle in handles)


def first_instance_ready(root_process_id):
    return (
        _named_mutex_exists()
        and bool(_window_handles_for_processes(_live_process_tree_ids(root_process_id)))
    )


def _wait_until(predicate, *, seconds, message):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.1)
    raise RuntimeError(message)


def _request_normal_close(process_id):
    handles = _window_handles_for_processes(_live_process_tree_ids(process_id))
    if not handles:
        raise RuntimeError(f"no application window was found for process {process_id}")
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    for handle in handles:
        user32.PostMessageW(handle, WM_CLOSE, 0, 0)


def _confirm_duplicate_notice(process_id):
    """Acknowledge the native duplicate-instance MessageBox as a user would."""
    button_handles = _duplicate_dialog_button_handles(process_id)
    if not button_handles:
        raise RuntimeError(f"no duplicate-instance notice was found for process {process_id}")
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    for button_handle in button_handles:
        user32.SendMessageW(button_handle, BM_CLICK, 0, 0)


def _close_test_process(process):
    if not _live_process_tree_ids(process.pid):
        return
    _request_normal_close(process.pid)
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        live = _live_process_tree_ids(process.pid)
        if not live:
            return
        time.sleep(0.1)
    snapshot = _process_snapshot()
    rows = tuple((process_id, parent_process_id) for process_id, parent_process_id, _name in snapshot)
    live = live_process_tree_ids(process.pid, rows)
    relation = [
        f"{process_id}->{parent_process_id} ({name})"
        for process_id, parent_process_id, name in snapshot
        if process_id in live
    ]
    raise RuntimeError(
        "application did not close normally; live test process tree: "
        + ", ".join(sorted(relation))
    )


def _force_terminate_test_tree(process):
    """Last-resort cleanup for a test-owned extracted runtime tree."""
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    for process_id in sorted(_live_process_tree_ids(process.pid), reverse=True):
        handle = kernel32.OpenProcess(0x0001, False, process_id)
        if handle:
            try:
                kernel32.TerminateProcess(handle, 1)
            finally:
                kernel32.CloseHandle(handle)
    _wait_until(
        lambda: not _live_process_tree_ids(process.pid),
        seconds=5,
        message="test process tree could not be terminated",
    )


def packaged_runtime_smoke():
    """Verify one packaged GUI process starts, resists a duplicate, and exits cleanly."""
    if sys.platform != "win32":
        raise RuntimeError("packaged runtime smoke requires Windows")
    artifact = static_package_smoke()
    validate_release_archive(artifact, expected_version=artifact.name.split("-v", 1)[1].split("-win11", 1)[0])
    if _named_mutex_exists():
        raise RuntimeError("an existing Codex Windows Status Pet instance prevents runtime smoke")
    with tempfile.TemporaryDirectory(prefix="CodexStatusPet-runtime-") as directory:
        with zipfile.ZipFile(artifact) as archive:
            archive.extractall(directory)
        executable = Path(directory) / RELEASE_ROOT_NAME / "CodexStatusPet.exe"
        if pe_subsystem(executable) != WINDOWS_GUI_SUBSYSTEM:
            raise RuntimeError("packaged executable requires a console subsystem")
        first = subprocess.Popen([str(executable)])
        duplicate = None
        try:
            _wait_until(
                lambda: first_instance_ready(first.pid),
                seconds=10,
                message="first packaged process did not acquire its mutex and show a window",
            )
            duplicate = subprocess.Popen([str(executable)])
            _wait_until(
                lambda: duplicate_notice_ready(duplicate.pid),
                seconds=10,
                message="duplicate launch did not show its existing-instance notice",
            )
            _confirm_duplicate_notice(duplicate.pid)
            _wait_until(
                lambda: not _live_process_tree_ids(duplicate.pid),
                seconds=10,
                message="duplicate packaged process did not close after its existing-instance notice was confirmed",
            )
            if not _live_process_tree_ids(first.pid):
                raise RuntimeError("duplicate launch displaced the first packaged process")
            _close_test_process(first)
        finally:
            for process in (duplicate, first):
                if process is not None and _live_process_tree_ids(process.pid):
                    _force_terminate_test_tree(process)
    return artifact


def main():
    artifact = packaged_runtime_smoke()
    print(f"packaged runtime smoke passed: {artifact}")


if __name__ == "__main__":
    main()
