@echo off
setlocal
set "ROOT=%~dp0"
if exist "%ROOT%runtime.json" goto launch

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%install.ps1" -SourceRoot "%ROOT%"
set "RESULT=%ERRORLEVEL%"
if "%RESULT%"=="0" exit /b 0
echo.
echo CodexStatusPet installation failed. Review the error above, then run launch.cmd again.
if not "%CODEX_STATUS_PET_NO_PAUSE%"=="1" pause
exit /b %RESULT%

:launch
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%launch.ps1" %*
set "RESULT=%ERRORLEVEL%"
exit /b %RESULT%
