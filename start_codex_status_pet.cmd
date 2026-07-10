@echo off
setlocal
set "ROOT=%~dp0"
set "PY=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\pythonw.exe"
set "SCRIPT=%ROOT%scripts\codex_status_pet.py"
if not exist "%SCRIPT%" exit /b 1
if exist "%PY%" (
    start "Codex Status Pet" "%PY%" "%SCRIPT%"
    exit /b 0
)
where pythonw.exe >nul 2>&1 || exit /b 1
start "Codex Status Pet" pythonw.exe "%SCRIPT%"
