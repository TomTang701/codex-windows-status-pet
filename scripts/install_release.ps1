[CmdletBinding()]
param(
    [string]$Tag
)

$ErrorActionPreference = 'Stop'
$repository = 'TomTang701/codex-windows-status-pet'
$staging = Join-Path ([IO.Path]::GetTempPath()) "CodexStatusPet-release-$([guid]::NewGuid())"

function Fail-ReleaseBootstrap {
    param([string]$Category, [string]$Detail)
    throw "$Category failure: $Detail"
}

try {
    & gh auth status | Out-Null
    if ($LASTEXITCODE -ne 0) { Fail-ReleaseBootstrap 'Authentication' 'run gh auth login with access to the private repository' }

    if ($Tag) {
        $releaseArguments = @('release', 'view', $Tag, '--repo', $repository, '--json', 'tagName,isDraft,isPrerelease,assets')
    }
    else {
        $releaseArguments = @('release', 'view', '--repo', $repository, '--json', 'tagName,isDraft,isPrerelease,assets')
    }
    $releaseText = & gh @releaseArguments
    if ($LASTEXITCODE -ne 0) { Fail-ReleaseBootstrap 'Release resolution' 'unable to resolve the requested published Release' }
    $release = $releaseText | ConvertFrom-Json
    if ($release.isDraft -or $release.isPrerelease) { Fail-ReleaseBootstrap 'Release resolution' 'Release must be published and stable' }
    if ($release.tagName -notmatch '^v(\d+\.\d+\.\d+)$') { Fail-ReleaseBootstrap 'Release resolution' 'Release tag must be vMAJOR.MINOR.PATCH' }

    $expectedVersion = $Matches[1]
    $zipName = "CodexStatusPet-v$expectedVersion-win11-x64.zip"
    $checksumName = "$zipName.sha256"
    $required = @($zipName, $checksumName, 'install.ps1')
    $assetNames = @($release.assets | ForEach-Object { $_.name })
    foreach ($name in $required) {
        if ($assetNames -notcontains $name) { Fail-ReleaseBootstrap 'Release resolution' "required asset is missing: $name" }
    }

    New-Item -ItemType Directory -Force -Path $staging | Out-Null
    & gh release download $release.tagName --repo $repository --dir $staging --pattern $zipName --pattern $checksumName --pattern 'install.ps1'
    if ($LASTEXITCODE -ne 0) { Fail-ReleaseBootstrap 'Release acquisition' 'authenticated GitHub download failed' }

    $artifact = Join-Path $staging $zipName
    $sidecar = Join-Path $staging $checksumName
    $installer = Join-Path $staging 'install.ps1'
    if (!(Test-Path -LiteralPath $artifact) -or !(Test-Path -LiteralPath $sidecar) -or !(Test-Path -LiteralPath $installer)) { Fail-ReleaseBootstrap 'Release acquisition' 'download did not produce the required assets' }
    $checksumRecord = (Get-Content -LiteralPath $sidecar -Raw).Trim()
    if ($checksumRecord -notmatch '^([0-9a-fA-F]{64})  .+$') { Fail-ReleaseBootstrap 'Checksum' 'release SHA-256 sidecar is invalid' }

    $expectedChecksum = $Matches[1]
    & $installer -ArtifactPath $artifact -Sha256 $expectedChecksum -ExpectedVersion $expectedVersion
    if ($LASTEXITCODE -ne 0) { Fail-ReleaseBootstrap 'Installation' 'install.ps1 did not complete successfully' }
}
finally {
    Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue
}
