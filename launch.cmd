@echo off
setlocal
set "ROOT=%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%launch.ps1" %*
exit /b %ERRORLEVEL%
