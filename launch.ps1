[CmdletBinding()]
param([string]$InstallRoot = $(Split-Path -Parent $MyInvocation.MyCommand.Path))

$ErrorActionPreference = 'Stop'
$InstallRoot = [IO.Path]::GetFullPath($InstallRoot)
$recordPath = Join-Path $InstallRoot 'runtime.json'
if (!(Test-Path -LiteralPath $recordPath)) { throw 'Python runtime is not configured. Run install.ps1 to repair the installation.' }
$record = Get-Content -LiteralPath $recordPath -Raw | ConvertFrom-Json
$python = [IO.Path]::GetFullPath([string]$record.python_path)
$pythonw = Join-Path (Split-Path -Parent $python) 'pythonw.exe'
if (!(Test-Path -LiteralPath $pythonw)) { throw 'The configured Python runtime is missing pythonw.exe. Run install.ps1 to repair it.' }
$env:PYTHONPATH = (Join-Path $InstallRoot 'runtime-packages') + ';' + (Join-Path $InstallRoot 'scripts')
$entrypoint = Join-Path $InstallRoot 'scripts\codex_status_pet.py'
Start-Process -FilePath $pythonw -ArgumentList @('-u', $entrypoint) -WorkingDirectory $InstallRoot -WindowStyle Hidden
