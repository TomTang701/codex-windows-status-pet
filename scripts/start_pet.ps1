$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$python = 'C:\Users\tangz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    $python = (Get-Command python.exe -ErrorAction Stop).Source
}
$running = Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -like '*codex_status_pet.py*' }
if (-not $running) {
    Start-Process -FilePath $python -ArgumentList @((Join-Path $root 'scripts\codex_status_pet.py')) `
        -WorkingDirectory $root -WindowStyle Hidden
}
