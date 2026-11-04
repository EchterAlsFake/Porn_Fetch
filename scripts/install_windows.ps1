[CmdletBinding()]
param(
    [string]$Msys2Root = "C:\msys64",
    [switch]$WithoutFFmpeg
)
$ErrorActionPreference = "Stop"
if ($VerbosePreference -eq 'Continue') { $env:PORN_FETCH_BUILD_VERBOSE = '1' }

function Run {
    param([string]$Exe, [Parameter(ValueFromRemainingArguments=$true)]$Arguments)
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Exe failed with exit code $LASTEXITCODE" }
}

function Main {
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
        $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
    }
    if (Test-Path "scripts\build_desktop.py") {
        $projectDir = (Get-Location).Path
    } elseif ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "build_desktop.py"))) {
        $projectDir = Split-Path $PSScriptRoot -Parent
    } else {
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
            throw "Install Git for Windows, reopen PowerShell, and run this script again."
        }
        if (-not (Test-Path Porn_Fetch)) {
            Run git clone https://github.com/EchterAlsFake/Porn_Fetch.git Porn_Fetch
        }
        $projectDir = (Resolve-Path Porn_Fetch).Path
    }
    $previousNoSync = $env:UV_NO_SYNC
    Push-Location $projectDir
    try {
        if (-not (Test-Path scripts/build_desktop.py)) { throw "Use the build instructions from this checkout's release tag." }
        if (-not $WithoutFFmpeg -and -not (Test-Path "$Msys2Root\usr\bin\make.exe")) {
            throw "Install MSYS2 and its CLANG64/CLANGARM64 build tools first (docs/INSTALLATION.md), or use -WithoutFFmpeg with FFmpeg on PATH."
        }
        Run uv python install 3.15
        Run uv sync --upgrade --extra gui --extra build --extra desktop-build
        $env:UV_NO_SYNC = '1'
        $buildArguments = @('run', '--no-sync', 'python', 'scripts/build_desktop.py')
        if ($WithoutFFmpeg) { $buildArguments += '--without-ffmpeg' }
        else { $buildArguments += @('--msys2-root', $Msys2Root) }
        Run uv @buildArguments
    } finally {
        $env:UV_NO_SYNC = $previousNoSync
        Pop-Location
    }
}

Main
