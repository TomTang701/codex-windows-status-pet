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


WM_CLOSE = 0x0010
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


def _process_rows():
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
            rows.append((int(entry.th32ProcessID), int(entry.th32ParentProcessID)))
            if not kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                break
        return tuple(rows)
    finally:
        kernel32.CloseHandle(snapshot)


def _process_tree_ids(root_process_id):
    return process_tree_ids(root_process_id, _process_rows())


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


def _wait_until(predicate, *, seconds, message):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.1)
    raise RuntimeError(message)


def _request_normal_close(process_id):
    handles = _window_handles_for_processes(_process_tree_ids(process_id))
    if not handles:
        raise RuntimeError(f"no application window was found for process {process_id}")
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    for handle in handles:
        user32.PostMessageW(handle, WM_CLOSE, 0, 0)


def _close_test_process(process):
    if process.poll() is not None:
        return
    _request_normal_close(process.pid)
    _wait_until(lambda: process.poll() is not None, seconds=10, message="application did not close normally")


def packaged_runtime_smoke():
    """Verify one packaged GUI process starts, resists a duplicate, and exits cleanly."""
    if sys.platform != "win32":
        raise RuntimeError("packaged runtime smoke requires Windows")
    artifact = static_package_smoke()
    validate_release_archive(artifact, expected_version=artifact.name.split("-v", 1)[1].split("-win11", 1)[0])
    with tempfile.TemporaryDirectory(prefix="CodexStatusPet-runtime-") as directory:
        with zipfile.ZipFile(artifact) as archive:
            archive.extractall(directory)
        executable = Path(directory) / RELEASE_ROOT_NAME / "CodexStatusPet.exe"
        if pe_subsystem(executable) != WINDOWS_GUI_SUBSYSTEM:
            raise RuntimeError("packaged executable requires a console subsystem")
        first = subprocess.Popen([str(executable)])
        duplicate = None
        try:
            _wait_until(lambda: first.poll() is None, seconds=10, message="first packaged process exited during startup")
            duplicate = subprocess.Popen([str(executable)])
            _wait_until(
                lambda: bool(_window_handles_for_processes(_process_tree_ids(duplicate.pid))),
                seconds=10,
                message="duplicate launch did not show its existing-instance notice",
            )
            _close_test_process(duplicate)
            if first.poll() is not None:
                raise RuntimeError("duplicate launch displaced the first packaged process")
            _close_test_process(first)
        finally:
            for process in (duplicate, first):
                if process is not None and process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
    return artifact


def main():
    artifact = packaged_runtime_smoke()
    print(f"packaged runtime smoke passed: {artifact}")


if __name__ == "__main__":
    main()
