[CmdletBinding()]
param(
    [string]$ArtifactPath,
    [string]$Sha256,
    [ValidatePattern('^\d+\.\d+\.\d+$')] [string]$ExpectedVersion,
    [string]$SourceRoot,
    [switch]$TestFailAfterBackup
)

$ErrorActionPreference = 'Stop'
$product = 'CodexStatusPet'
$installRoot = [IO.Path]::GetFullPath((Join-Path $env:LOCALAPPDATA 'Programs\CodexStatusPet'))
$usingSource = ![string]::IsNullOrWhiteSpace($SourceRoot)
$usingArtifact = ![string]::IsNullOrWhiteSpace($ArtifactPath) -or ![string]::IsNullOrWhiteSpace($Sha256) -or ![string]::IsNullOrWhiteSpace($ExpectedVersion)
if ($usingSource -and $usingArtifact) { throw 'Specify either extracted SourceRoot or the verified artifact parameters, not both.' }
if (!$usingSource -and !($ArtifactPath -and $Sha256 -and $ExpectedVersion)) { throw 'Verified artifact installation requires ArtifactPath, Sha256, and ExpectedVersion.' }

if ($usingSource) {
    $sourceItem = Get-Item -LiteralPath $SourceRoot -ErrorAction Stop
    if (!$sourceItem.PSIsContainer -or !(Test-Path -LiteralPath (Join-Path $sourceItem.FullName 'release-manifest.json'))) {
        throw 'SourceRoot requires a directory containing release-manifest.json.'
    }
    $SourceRoot = [IO.Path]::GetFullPath($sourceItem.FullName).TrimEnd('\', '/')
    if ($SourceRoot.Equals($installRoot, [StringComparison]::OrdinalIgnoreCase) -or $SourceRoot.StartsWith($installRoot.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'SourceRoot cannot be the installed product directory or one of its descendants.'
    }
    $sourceManifest = Get-Content -LiteralPath (Join-Path $SourceRoot 'release-manifest.json') -Raw | ConvertFrom-Json
    $ExpectedVersion = [string]$sourceManifest.version
    if ($ExpectedVersion -notmatch '^\d+\.\d+\.\d+$') { throw 'Extracted source manifest version must be MAJOR.MINOR.PATCH.' }
} else {
    $artifact = Get-Item -LiteralPath $ArtifactPath -ErrorAction Stop
    $stream = [IO.File]::OpenRead($artifact.FullName)
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { $actual = ([BitConverter]::ToString($hasher.ComputeHash($stream))).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose(); $stream.Dispose() }
    if ($actual -ne $Sha256.Trim().ToLowerInvariant()) { throw 'Release checksum does not match.' }
}

$staging = Join-Path ([IO.Path]::GetTempPath()) "CodexStatusPet-stage-$([guid]::NewGuid())"
$backup = "$installRoot.backup-$([guid]::NewGuid())"
$success = $false

function Stop-InstalledProduct {
    $candidates = @(
        Get-CimInstance Win32_Process | Where-Object {
            $_.ProcessId -ne $PID -and (
                ($_.ExecutablePath -and $_.ExecutablePath.StartsWith($installRoot, [StringComparison]::OrdinalIgnoreCase)) -or
                ($_.CommandLine -and $_.CommandLine.IndexOf($installRoot, [StringComparison]::OrdinalIgnoreCase) -ge 0)
            )
        }
    )
    foreach ($candidate in $candidates) {
        try { [void](Get-Process -Id $candidate.ProcessId -ErrorAction Stop).CloseMainWindow() } catch { }
    }
    foreach ($candidate in $candidates) {
        try { Wait-Process -Id $candidate.ProcessId -Timeout 5 -ErrorAction Stop } catch { }
    }
    Get-CimInstance Win32_Process | Where-Object {
        $_.ProcessId -ne $PID -and (
            ($_.ExecutablePath -and $_.ExecutablePath.StartsWith($installRoot, [StringComparison]::OrdinalIgnoreCase)) -or
            ($_.CommandLine -and $_.CommandLine.IndexOf($installRoot, [StringComparison]::OrdinalIgnoreCase) -ge 0)
        )
    } | ForEach-Object {
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }
    foreach ($candidate in $candidates) {
        try { Wait-Process -Id $candidate.ProcessId -Timeout 10 -ErrorAction Stop } catch { }
    }
}

function Get-PythonProbe {
    param([string[]]$Command)
    $probe = @'
import json, struct, sys
p = {
    'path': sys.executable,
    'version': [sys.version_info.major, sys.version_info.minor],
    'bits': struct.calcsize('P') * 8,
}
try:
    import tkinter
    p['tkinter'] = True
except Exception:
    p['tkinter'] = False
try:
    import pip
    p['pip'] = True
except Exception:
    p['pip'] = False
print(json.dumps(p))
'@
    try {
        $arguments = @()
        if ($Command.Length -gt 1) { $arguments = $Command[1..($Command.Length - 1)] }
        $output = & $Command[0] @arguments -c $probe 2>$null
        if ($LASTEXITCODE -ne 0) { return $null }
        return ($output -join '') | ConvertFrom-Json
    }
    catch { return $null }
}

function Find-CompatiblePython {
    $candidates = @()
    $bundled = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $bundled) { $candidates += ,@('codex', @($bundled)) }
    $py = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($py) { $candidates += ,@('py', @($py.Source, '-3')) }
    $pathPython = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pathPython) { $candidates += ,@('path', @($pathPython.Source)) }
    foreach ($candidate in $candidates) {
        $probe = Get-PythonProbe $candidate[1]
        if ($probe -and $probe.version[0] -ge 3 -and (($probe.version[0] -gt 3) -or $probe.version[1] -ge 10) -and $probe.bits -eq 64 -and $probe.tkinter -and $probe.pip) {
            $python = [IO.Path]::GetFullPath([string]$probe.path)
            $pythonw = Join-Path (Split-Path -Parent $python) 'pythonw.exe'
            if (Test-Path -LiteralPath $pythonw) {
                return [pscustomobject]@{ Path = $python; Pythonw = $pythonw; Source = $candidate[0]; Version = "$($probe.version[0]).$($probe.version[1])" }
            }
        }
    }
    throw 'No compatible Python 3.10+ x64 runtime with Tkinter, pip, and pythonw.exe was found.'
}

function New-Shortcut {
    param([string]$Path, [string]$Root, [string]$Icon, [switch]$Legacy)
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($Path)
    if ($Legacy) {
        $shortcut.TargetPath = Join-Path $Root 'CodexStatusPet.exe'
        $shortcut.Arguments = ''
    } else {
        $shortcut.TargetPath = Join-Path $env:WINDIR 'System32\wscript.exe'
        $shortcut.Arguments = "//B //Nologo `"$(Join-Path $Root 'launch.vbs')`""
    }
    $shortcut.WorkingDirectory = $Root
    $shortcut.Description = 'Codex Windows Status Pet'
    if (Test-Path -LiteralPath $Icon) { $shortcut.IconLocation = "$Icon,0" }
    $shortcut.Save()
}

function Copy-ReleaseSource {
    param([string]$Root, [string]$Destination)
    $excluded = @('runtime.json', 'runtime-packages')
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -LiteralPath $Root -Force | Where-Object { $_.Name -notin $excluded } | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $Destination -Recurse -Force
    }
}

try {
    $runtime = Join-Path $staging $product
    if ($usingSource) {
        Copy-ReleaseSource -Root $SourceRoot -Destination $runtime
    } else {
        Expand-Archive -LiteralPath $artifact.FullName -DestinationPath $staging -Force
    }
    $manifestPath = Join-Path $runtime 'release-manifest.json'
    if (!(Test-Path -LiteralPath $manifestPath)) { throw 'Release manifest is missing.' }
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    $legacy = $manifest.schema_version -eq 1 -and $manifest.product -eq 'codex-windows-status-pet' -and $manifest.version -eq $ExpectedVersion -and $manifest.platform -eq 'windows' -and $manifest.arch -eq 'x64' -and $manifest.entrypoint -eq 'CodexStatusPet.exe'
    $source = $manifest.schema_version -eq 2 -and $manifest.product -eq 'codex-windows-status-pet' -and $manifest.version -eq $ExpectedVersion -and $manifest.platform -eq 'windows' -and $manifest.arch -eq 'x64' -and $manifest.runtime -eq 'python' -and $manifest.entrypoint -eq 'scripts/codex_status_pet.py' -and $manifest.launcher -eq 'launch.vbs' -and $manifest.icon -eq 'assets/CodexStatusPet.ico'
    if (!$legacy -and !$source) { throw 'Release manifest is invalid.' }
    if (!(Test-Path -LiteralPath (Join-Path $runtime $manifest.entrypoint))) { throw 'Release entry point is missing.' }
    if ($source -and !(Test-Path -LiteralPath (Join-Path $runtime 'launch.cmd'))) { throw 'CMD fallback launcher is missing.' }
    if ($source -and (Get-ChildItem -LiteralPath $runtime -Recurse -File | Where-Object { $_.Extension -in @('.exe', '.pyc', '.pyo') -or $_.Name -eq '_internal' })) { throw 'Source package contains prohibited executable runtime material.' }

    if ($source) {
        $python = Find-CompatiblePython
        $runtimePackages = Join-Path $runtime 'runtime-packages'
        New-Item -ItemType Directory -Force -Path $runtimePackages | Out-Null
        & $python.Path -m pip install --disable-pip-version-check --no-warn-script-location --upgrade --target $runtimePackages -r (Join-Path $runtime 'requirements-runtime.txt')
        if ($LASTEXITCODE -ne 0) { throw 'Application-private runtime dependency installation failed.' }
        (@{ python_path = $python.Path; source = $python.Source; version = $python.Version } | ConvertTo-Json) | Set-Content -LiteralPath (Join-Path $runtime 'runtime.json') -Encoding utf8
    }

    Stop-InstalledProduct
    if (Test-Path -LiteralPath $installRoot) { Move-Item -LiteralPath $installRoot -Destination $backup }
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $installRoot) | Out-Null
    Move-Item -LiteralPath $runtime -Destination $installRoot
    if ($TestFailAfterBackup) { throw 'Test failure after backup creation.' }

    $icon = Join-Path $installRoot 'assets\CodexStatusPet.ico'
    $desktop = [Environment]::GetFolderPath('Desktop')
    $programs = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'
    New-Item -ItemType Directory -Force -Path $desktop, $programs | Out-Null
    New-Shortcut (Join-Path $desktop 'Codex Windows Status Pet.lnk') $installRoot $icon -Legacy:$legacy
    New-Shortcut (Join-Path $programs 'Codex Windows Status Pet.lnk') $installRoot $icon -Legacy:$legacy
    if ($legacy) {
        Start-Process -FilePath (Join-Path $installRoot 'CodexStatusPet.exe') -WorkingDirectory $installRoot -WindowStyle Hidden
    } else {
        Start-Process -FilePath (Join-Path $installRoot 'launch.vbs') -WorkingDirectory $installRoot -WindowStyle Hidden
    }
    $success = $true
}
finally {
    if (!$success -and (Test-Path -LiteralPath $backup)) {
        Remove-Item -LiteralPath $installRoot -Recurse -Force -ErrorAction SilentlyContinue
        Move-Item -LiteralPath $backup -Destination $installRoot
    }
    if ($success -and (Test-Path -LiteralPath $backup)) { Remove-Item -LiteralPath $backup -Recurse -Force }
    Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue
}
