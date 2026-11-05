[CmdletBinding()]
param(
    [string]$Msys2Root = "C:\msys64",
    [switch]$WithoutFFmpeg,
    [switch]$NoPause
)
$ErrorActionPreference = "Stop"
if ($VerbosePreference -eq 'Continue') { $env:PORN_FETCH_BUILD_VERBOSE = '1' }

function Run {
    param([string]$Exe, [Parameter(ValueFromRemainingArguments=$true)]$Arguments)
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Exe failed with exit code $LASTEXITCODE" }
}

function Refresh-Path {
    # Keep this session's additions and import paths registered by installers.
    $paths = @($env:PATH,
        [Environment]::GetEnvironmentVariable('Path', 'Machine'),
        [Environment]::GetEnvironmentVariable('Path', 'User'))
    $env:PATH = ($paths | Where-Object { $_ }) -join [IO.Path]::PathSeparator
}

function Ensure-Git {
    if (Get-Command git -ErrorAction SilentlyContinue) { return }
    Refresh-Path
    if (Get-Command git -ErrorAction SilentlyContinue) { return }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw 'Git and winget are unavailable. Install App Installer from the Microsoft Store, or install Git for Windows, then rerun this script.'
    }
    Write-Host 'Installing Git for Windows with winget...'
    Run winget install --id Git.Git --exact --source winget --accept-package-agreements --accept-source-agreements
    Refresh-Path
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'Git installation completed, but git.exe is not on PATH. Reopen PowerShell and rerun this script.'
    }
    Run git --version
}

function Ensure-Msys2 {
    param([string]$Architecture)
    switch ($Architecture.ToLowerInvariant()) {
        { $_ -in @('amd64', 'x86_64', 'x64') } {
            $msystem = 'CLANG64'
            $msysArchitecture = 'x64'
            $prefix = 'mingw-w64-clang-x86_64'
            break
        }
        { $_ -in @('arm64', 'aarch64') } {
            $msystem = 'CLANGARM64'
            $msysArchitecture = 'arm64'
            $prefix = 'mingw-w64-clang-aarch64'
            break
        }
        default { throw "Unsupported Python architecture for FFmpeg: $Architecture" }
    }
    $bash = Join-Path $Msys2Root 'usr\bin\bash.exe'
    $pacman = Join-Path $Msys2Root 'usr\bin\pacman.exe'
    if (-not (Test-Path -LiteralPath $bash)) {
        if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
            throw 'MSYS2 and winget are unavailable. Install App Installer from the Microsoft Store, or install MSYS2, then rerun this script.'
        }
        Write-Host "Installing MSYS2 into $Msys2Root..."
        Run winget install --id MSYS2.MSYS2 --exact --source winget --silent --location $Msys2Root --architecture $msysArchitecture --accept-package-agreements --accept-source-agreements
        if (-not (Test-Path -LiteralPath $bash)) {
            throw "MSYS2 installation did not create $bash. Check -Msys2Root and the installer output above."
        }
    }
    $previousMsystem = $env:MSYSTEM
    $previousChereInvoking = $env:CHERE_INVOKING
    $previousPath = $env:PATH
    try {
        $env:MSYSTEM = $msystem
        $env:CHERE_INVOKING = 'yes'
        $env:PATH = (Join-Path $Msys2Root 'usr\bin') + [IO.Path]::PathSeparator + $env:PATH
        Write-Host "Preparing MSYS2 $msystem for FFmpeg..."
        Run $bash -lc 'true'
        # Run pacman directly, without a parent MSYS shell that a core update
        # would close. The second process finishes updating with the new core.
        try { Run $pacman --noconfirm -Syu } catch {
            Write-Host "Initial MSYS2 update interrupted: $_. Retrying in a fresh process..."
        }
        Run $pacman --noconfirm -Syu
        Run $pacman --noconfirm -S --needed make diffutils pkgconf "$prefix-toolchain" "$prefix-zlib"
        Run $bash -lc 'command -v make && command -v clang && command -v llvm-strip && pkg-config --exists zlib && clang --version'
    } finally {
        $env:MSYSTEM = $previousMsystem
        $env:CHERE_INVOKING = $previousChereInvoking
        $env:PATH = $previousPath
    }
}

function Main {
    Ensure-Git
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        # The upstream installer calls exit on failure. Keep that exit inside
        # a child process when this script is invoked through irm ... | iex.
        $uvInstaller = Join-Path ([IO.Path]::GetTempPath()) ("pornfetch-uv-" + [guid]::NewGuid().ToString('N') + '.ps1')
        try {
            Invoke-WebRequest https://astral.sh/uv/install.ps1 -UseBasicParsing -OutFile $uvInstaller
            $shell = (Get-Process -Id $PID).Path
            Run $shell -NoLogo -NoProfile -ExecutionPolicy Bypass -File $uvInstaller
        } finally {
            Remove-Item -LiteralPath $uvInstaller -Force -ErrorAction SilentlyContinue
        }
        $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
    }
    if (Test-Path "scripts\build_desktop.py") {
        $projectDir = (Get-Location).Path
    } elseif ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "build_desktop.py"))) {
        $projectDir = Split-Path $PSScriptRoot -Parent
    } else {
        if (-not (Test-Path Porn_Fetch)) {
            Run git clone https://github.com/EchterAlsFake/Porn_Fetch.git Porn_Fetch
        }
        $projectDir = (Resolve-Path Porn_Fetch).Path
    }
    $previousNoSync = $env:UV_NO_SYNC
    Push-Location $projectDir
    try {
        if (-not (Test-Path scripts/build_desktop.py)) { throw "Use the build instructions from this checkout's release tag." }
        Run uv python install 3.15
        Run uv sync --upgrade --extra gui --extra build --extra desktop-build
        $env:UV_NO_SYNC = '1'
        if (-not $WithoutFFmpeg) {
            $buildArch = Run uv run --no-sync python -c 'import platform; print(platform.machine().lower())'
            Ensure-Msys2 -Architecture $buildArch.Trim()
        }
        $buildArguments = @('run', '--no-sync', 'python', 'scripts/build_desktop.py')
        if ($WithoutFFmpeg) { $buildArguments += '--without-ffmpeg' }
        else { $buildArguments += @('--msys2-root', $Msys2Root) }
        Run uv @buildArguments
    } finally {
        $env:UV_NO_SYNC = $previousNoSync
        Pop-Location
    }
}

$logDirectory = Join-Path ([IO.Path]::GetTempPath()) 'porn-fetch-build-logs'
$logPath = Join-Path $logDirectory ("install-windows-" + [guid]::NewGuid().ToString('N') + '.log')
$transcriptStarted = $false
try {
    New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
    Start-Transcript -Path $logPath | Out-Null
    $transcriptStarted = $true
    Write-Host "Installation log: $logPath"
    Main
} catch {
    Write-Host "`nPorn Fetch build failed:" -ForegroundColor Red
    Write-Host $_.ToString() -ForegroundColor Red
    Write-Host $_.InvocationInfo.PositionMessage
    Write-Host $_.ScriptStackTrace
    if ($transcriptStarted) { Write-Host "Full log: $logPath" }
    if (-not $NoPause -and [Environment]::UserInteractive -and -not [Console]::IsInputRedirected) {
        try { Read-Host 'Press Enter to return to PowerShell' | Out-Null } catch { }
    }
    throw
} finally {
    if ($transcriptStarted) { Stop-Transcript | Out-Null }
}
