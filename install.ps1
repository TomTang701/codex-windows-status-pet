[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [string]$ArtifactPath,
    [Parameter(Mandatory = $true)] [string]$Sha256,
    [Parameter(Mandatory = $true)] [ValidatePattern('^\d+\.\d+\.\d+$')] [string]$ExpectedVersion
)

$ErrorActionPreference = 'Stop'
$product = 'CodexStatusPet'
$installRoot = [IO.Path]::GetFullPath((Join-Path $env:LOCALAPPDATA 'Programs\CodexStatusPet'))
$artifact = Get-Item -LiteralPath $ArtifactPath -ErrorAction Stop
$stream = [IO.File]::OpenRead($artifact.FullName)
$hasher = [Security.Cryptography.SHA256]::Create()
try {
    $actual = ([BitConverter]::ToString($hasher.ComputeHash($stream))).Replace('-', '').ToLowerInvariant()
}
finally {
    $hasher.Dispose()
    $stream.Dispose()
}
if ($actual -ne $Sha256.Trim().ToLowerInvariant()) { throw 'Release checksum does not match.' }

$staging = Join-Path ([IO.Path]::GetTempPath()) "CodexStatusPet-stage-$([guid]::NewGuid())"
$backup = "$installRoot.backup-$([guid]::NewGuid())"
$settingsPath = Join-Path $env:USERPROFILE '.codex\codex-windows-status-pet.json'
$settingsSnapshot = Join-Path $staging 'settings-before-install.json'
$settingsExisted = $false
$success = $false

function Test-ProductInstanceRunning {
    try {
        $mutex = [Threading.Mutex]::OpenExisting('Local\CodexWindowsStatusPet')
        $mutex.Dispose()
        return $true
    }
    catch [Threading.WaitHandleCannotBeOpenedException] {
        return $false
    }
}

function Stop-InstalledProduct {
    $running = @(
        Get-CimInstance Win32_Process -Filter "Name = 'CodexStatusPet.exe'" |
            Where-Object { $_.ExecutablePath -and $_.ExecutablePath.StartsWith($installRoot, [StringComparison]::OrdinalIgnoreCase) }
    )
    foreach ($candidate in $running) {
        try {
            [void](Get-Process -Id $candidate.ProcessId -ErrorAction Stop).CloseMainWindow()
        }
        catch {
            # A tool window can lack a conventional main-window handle; use the
            # bounded fallback below only after this normal-close attempt.
        }
    }
    foreach ($candidate in $running) {
        try { Wait-Process -Id $candidate.ProcessId -Timeout 5 -ErrorAction Stop }
        catch { }
    }
    $remaining = @(
        Get-CimInstance Win32_Process -Filter "Name = 'CodexStatusPet.exe'" |
            Where-Object { $_.ExecutablePath -and $_.ExecutablePath.StartsWith($installRoot, [StringComparison]::OrdinalIgnoreCase) }
    )
    foreach ($candidate in $remaining) {
        Stop-Process -Id $candidate.ProcessId -Force -ErrorAction Stop
        Wait-Process -Id $candidate.ProcessId -Timeout 5 -ErrorAction SilentlyContinue
    }
}

try {
    Expand-Archive -LiteralPath $artifact.FullName -DestinationPath $staging -Force
    $runtime = Join-Path $staging $product
    $manifestPath = Join-Path $runtime 'release-manifest.json'
    if (!(Test-Path -LiteralPath $manifestPath)) { throw 'Release manifest is missing.' }
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    if ($manifest.schema_version -ne 1 -or $manifest.product -ne 'codex-windows-status-pet' -or $manifest.version -ne $ExpectedVersion -or $manifest.platform -ne 'windows' -or $manifest.arch -ne 'x64' -or $manifest.entrypoint -ne 'CodexStatusPet.exe') { throw 'Release manifest is invalid.' }
    $entrypoint = Join-Path $runtime $manifest.entrypoint
    if (!(Test-Path -LiteralPath $entrypoint)) { throw 'Release entry point is missing.' }

    if (Test-Path -LiteralPath $settingsPath) {
        Copy-Item -LiteralPath $settingsPath -Destination $settingsSnapshot -Force
        $settingsExisted = $true
    }
    Stop-InstalledProduct

    if (Test-ProductInstanceRunning) {
        throw 'Codex Windows Status Pet is still running. Close it from the tray before installing or upgrading.'
    }

    if (Test-Path -LiteralPath $installRoot) { Move-Item -LiteralPath $installRoot -Destination $backup }
    $installParent = Split-Path -Parent $installRoot
    New-Item -ItemType Directory -Force -Path $installParent | Out-Null
    Move-Item -LiteralPath $runtime -Destination $installRoot
    $installedExe = Join-Path $installRoot 'CodexStatusPet.exe'
    Start-Process -FilePath $installedExe
    Start-Sleep -Seconds 2
    if (!(Get-CimInstance Win32_Process -Filter "Name = 'CodexStatusPet.exe'" | Where-Object { $_.ExecutablePath -eq $installedExe })) { throw 'Installed executable did not remain running.' }

    $programs = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'
    New-Item -ItemType Directory -Force -Path $programs | Out-Null
    $shortcutPath = Join-Path $programs 'Codex Windows Status Pet.lnk'
    $shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $installedExe
    $shortcut.WorkingDirectory = $installRoot
    $shortcut.Save()
    $success = $true
}
finally {
    if (!$success -and (Test-Path -LiteralPath $backup)) {
        Remove-Item -LiteralPath $installRoot -Recurse -Force -ErrorAction SilentlyContinue
        Move-Item -LiteralPath $backup -Destination $installRoot
    }
    if ($success -and (Test-Path -LiteralPath $backup)) { Remove-Item -LiteralPath $backup -Recurse -Force }
    if ($settingsExisted -and (Test-Path -LiteralPath $settingsSnapshot)) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $settingsPath) | Out-Null
        Copy-Item -LiteralPath $settingsSnapshot -Destination $settingsPath -Force
    }
    Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue
}
