[CmdletBinding()]
param(
    [switch]$PurgeSettings,
    [string]$InstallRoot = "$env:LOCALAPPDATA\Programs\CodexStatusPet"
)

$ErrorActionPreference = 'Stop'
$resolvedRoot = [IO.Path]::GetFullPath($InstallRoot)
$expectedRoot = [IO.Path]::GetFullPath("$env:LOCALAPPDATA\Programs\CodexStatusPet")
if ($resolvedRoot -ne $expectedRoot) { throw 'Unexpected installation root.' }

Get-CimInstance Win32_Process -Filter "Name = 'CodexStatusPet.exe'" |
    Where-Object { $_.ExecutablePath -and $_.ExecutablePath.StartsWith($resolvedRoot, [StringComparison]::OrdinalIgnoreCase) } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

$shortcut = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Codex Windows Status Pet.lnk'
Remove-Item -LiteralPath $shortcut -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $resolvedRoot -Recurse -Force -ErrorAction SilentlyContinue

if ($PurgeSettings) {
    Remove-Item -LiteralPath (Join-Path $env:USERPROFILE '.codex\codex-windows-status-pet.json') -Force -ErrorAction SilentlyContinue
}
