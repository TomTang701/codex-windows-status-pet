[CmdletBinding()]
param([string]$InstallRoot)

$ErrorActionPreference = 'Stop'
$InstallRoot = if ([string]::IsNullOrWhiteSpace($InstallRoot)) { $PSScriptRoot } else { $InstallRoot }
$InstallRoot = [IO.Path]::GetFullPath($InstallRoot)
$recordPath = Join-Path $InstallRoot 'runtime.json'
if (!(Test-Path -LiteralPath $recordPath)) { throw 'Python runtime is not configured. Run install.ps1 to repair the installation.' }
$record = Get-Content -LiteralPath $recordPath -Raw | ConvertFrom-Json
$python = [IO.Path]::GetFullPath([string]$record.python_path)
$pythonw = Join-Path (Split-Path -Parent $python) 'pythonw.exe'
if (!(Test-Path -LiteralPath $pythonw)) { throw 'The configured Python runtime is missing pythonw.exe. Run install.ps1 to repair it.' }
$env:PYTHONPATH = (Join-Path $InstallRoot 'runtime-packages') + ';' + (Join-Path $InstallRoot 'scripts')
$entrypoint = Join-Path $InstallRoot 'scripts\codex_status_pet.py'
$quotedEntrypoint = '"' + $entrypoint.Replace('"', '\\"') + '"'
Start-Process -FilePath $pythonw -ArgumentList @('-u', $quotedEntrypoint) -WorkingDirectory $InstallRoot -WindowStyle Hidden
