[CmdletBinding()]
param(
    [string]$Tag
)

$ErrorActionPreference = 'Stop'
$repository = 'TomTang701/codex-windows-status-pet'
$releasesApi = "https://api.github.com/repos/$repository/releases"
$headers = @{
    Accept = 'application/vnd.github+json'
    'User-Agent' = 'CodexStatusPet-public-bootstrap/1.0.0'
}
$staging = Join-Path ([IO.Path]::GetTempPath()) "CodexStatusPet-release-$([guid]::NewGuid())"

function Fail-ReleaseBootstrap {
    param([string]$Category, [string]$Detail)
    throw "$Category failure: $Detail"
}

try {
    if ($Tag -and $Tag -notmatch '^v\d+\.\d+\.\d+$') { Fail-ReleaseBootstrap 'Release resolution' 'requested release tag must be vMAJOR.MINOR.PATCH' }
    $metadataUri = if ($Tag) { "$releasesApi/tags/$Tag" } else { "$releasesApi/latest" }
    try {
        $release = Invoke-RestMethod -Uri $metadataUri -Headers $headers -Method Get -UseBasicParsing -ErrorAction Stop
    }
    catch {
        Fail-ReleaseBootstrap 'Public GitHub API request' "unable to resolve the requested published Release: $($_.Exception.Message)"
    }
    if ($release.draft -or $release.prerelease) { Fail-ReleaseBootstrap 'Release resolution' 'Release must be published and stable' }
    if ($release.tag_name -notmatch '^v(\d+\.\d+\.\d+)$') { Fail-ReleaseBootstrap 'Release resolution' 'Release tag must be vMAJOR.MINOR.PATCH' }
    if ($Tag -and $release.tag_name -cne $Tag) { Fail-ReleaseBootstrap 'Release resolution' 'pinned Release tag did not resolve exactly' }

    $expectedVersion = $Matches[1]
    $zipName = "CodexStatusPet-v$expectedVersion-win11-x64.zip"
    $checksumName = "$zipName.sha256"
    $required = @($zipName, $checksumName, 'install.ps1')
    $assetMap = @{}
    foreach ($asset in @($release.assets)) {
        if ($asset.name) { $assetMap[$asset.name] = $asset }
    }
    foreach ($name in $required) {
        if (!$assetMap.ContainsKey($name)) { Fail-ReleaseBootstrap 'Release resolution' "required asset is missing: $name" }
        if (!$assetMap[$name].browser_download_url) { Fail-ReleaseBootstrap 'Release resolution' "release asset download URL is missing: $name" }
    }

    New-Item -ItemType Directory -Force -Path $staging | Out-Null
    $artifact = Join-Path $staging $zipName
    $sidecar = Join-Path $staging $checksumName
    $installer = Join-Path $staging 'install.ps1'
    foreach ($download in @(
        @{ Url = $assetMap[$zipName].browser_download_url; Path = $artifact },
        @{ Url = $assetMap[$checksumName].browser_download_url; Path = $sidecar },
        @{ Url = $assetMap['install.ps1'].browser_download_url; Path = $installer }
    )) {
        try {
            Invoke-WebRequest -Uri $download.Url -Headers $headers -OutFile $download.Path -UseBasicParsing -ErrorAction Stop
        }
        catch {
            Fail-ReleaseBootstrap 'Public Release asset download' "unable to download $($download.Path): $($_.Exception.Message)"
        }
    }
    if (!(Test-Path -LiteralPath $artifact) -or !(Test-Path -LiteralPath $sidecar) -or !(Test-Path -LiteralPath $installer)) { Fail-ReleaseBootstrap 'Release acquisition' 'download did not produce the required assets' }
    $checksumRecord = (Get-Content -LiteralPath $sidecar -Raw).Trim()
    if ($checksumRecord -notmatch '^([0-9a-fA-F]{64})\s+(.+)$' -or $Matches[2] -ne $zipName) { Fail-ReleaseBootstrap 'Checksum' 'release SHA-256 sidecar is invalid' }

    $expectedChecksum = $Matches[1]
    & $installer -ArtifactPath $artifact -Sha256 $expectedChecksum -ExpectedVersion $expectedVersion
    if (-not $?) { Fail-ReleaseBootstrap 'Installation' 'install.ps1 did not complete successfully' }
}
finally {
    Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue
}
