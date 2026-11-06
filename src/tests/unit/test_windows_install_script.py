"""Exercise installer failures in a real PowerShell without downloading or building."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

POWERSHELL = shutil.which("pwsh") or shutil.which("powershell")
SCRIPT = Path(__file__).resolve().parents[3] / "scripts/install_windows.ps1"


@unittest.skipUnless(POWERSHELL, "PowerShell is required")
class WindowsInstallScriptTests(unittest.TestCase):
    def run_failure(self, mock_commands: str, invocation: str, *, checkout: bool = True):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            if checkout:
                (root / "scripts").mkdir()
                (root / "scripts/build_desktop.py").touch()
            harness = root / "test.ps1"
            harness.write_text(mock_commands + "\n" + r"""
$source = Get-Content -LiteralPath $env:PORN_FETCH_INSTALL_SCRIPT -Raw
try {
""" + invocation + r"""
} catch {
    Write-Output "Caller caught: $_"
}
Write-Output 'CALLING_SHELL_SURVIVED'
""", encoding="utf-8")
            result = subprocess.run(
                [POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(harness)],
                cwd=root, input="", capture_output=True, text=True, timeout=30,
                env=dict(os.environ, TEMP=temporary, TMP=temporary, TMPDIR=temporary,
                         PORN_FETCH_INSTALL_SCRIPT=str(SCRIPT)),
            )
            output = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, output)
            self.assertIn("CALLING_SHELL_SURVIVED", output)
            self.assertIn("Porn Fetch build failed:", output)
            logs = list((root / "porn-fetch-build-logs").glob("*.log"))
            self.assertEqual(len(logs), 1, output)
            return output, logs[0].read_text(encoding="utf-8-sig")

    def test_bootstrap_exit_keeps_iex_caller_alive_and_saves_diagnostics(self):
        output, log = self.run_failure(r"""
function Get-Command {
    param($Name)
    if ($Name -eq 'git') { return @{ Name = 'git' } }
    return $null
}
function Invoke-WebRequest {
    param($Uri, [switch]$UseBasicParsing, $OutFile)
    Set-Content -LiteralPath $OutFile -Value "Write-Output 'UV_BOOTSTRAP_FAILED'; exit 23"
}
""", "Invoke-Expression $source")
        self.assertIn("exit code 23", output)
        self.assertIn("UV_BOOTSTRAP_FAILED", log)
        self.assertIn("exit code 23", log)

    def test_native_command_failure_is_logged_with_no_pause(self):
        output, log = self.run_failure(r"""
function uv {
    Write-Output 'UV_COMMAND_FAILED'
    $global:LASTEXITCODE = 12
}
""", "& ([scriptblock]::Create($source)) -WithoutFFmpeg -NoPause")
        self.assertIn("uv failed with exit code 12", output)
        self.assertIn("UV_COMMAND_FAILED", log)
        self.assertIn("uv failed with exit code 12", log)

    def test_missing_git_is_installed_before_build_commands(self):
        output, log = self.run_failure(r"""
$global:GitInstalled = $false
function Get-Command {
    param($Name)
    if ($Name -eq 'git' -and -not $global:GitInstalled) { return $null }
    return @{ Name = $Name }
}
function winget {
    if (($args -join ' ') -ne 'install --id Git.Git --exact --source winget --accept-package-agreements --accept-source-agreements') {
        throw 'Unexpected Git installation arguments'
    }
    Write-Output 'WINGET_GIT_INSTALLED'
    $global:GitInstalled = $true
    $global:LASTEXITCODE = 0
}
function git {
    Write-Output 'GIT_READY'
    $global:LASTEXITCODE = 0
}
function uv {
    if (-not $global:GitInstalled) { throw 'Build started without Git' }
    Write-Output 'BUILD_STARTED_AFTER_GIT'
    $global:LASTEXITCODE = 12
}
""", "& ([scriptblock]::Create($source)) -WithoutFFmpeg -NoPause")
        self.assertIn("uv failed with exit code 12", output)
        self.assertLess(log.index("WINGET_GIT_INSTALLED"), log.index("GIT_READY"))
        self.assertLess(log.index("GIT_READY"), log.index("BUILD_STARTED_AFTER_GIT"))

    def test_failed_git_install_stops_before_build(self):
        output, log = self.run_failure(r"""
function Get-Command {
    param($Name)
    if ($Name -eq 'git') { return $null }
    return @{ Name = $Name }
}
function winget {
    Write-Output 'GIT_INSTALL_FAILED'
    $global:LASTEXITCODE = 42
}
function uv { throw 'BUILD_MUST_NOT_START' }
""", "& ([scriptblock]::Create($source)) -WithoutFFmpeg -NoPause")
        self.assertIn("winget failed with exit code 42", output)
        self.assertIn("GIT_INSTALL_FAILED", log)
        self.assertNotIn("BUILD_MUST_NOT_START", output)

    def test_fresh_clone_uses_user_profile_instead_of_the_calling_directory(self):
        output, _ = self.run_failure(r"""
function uv { }
function Test-Path {
    param($Path, $LiteralPath)
    if ($LiteralPath -and $LiteralPath.EndsWith('Porn_Fetch')) { return $false }
    if ($LiteralPath) { return Microsoft.PowerShell.Management\Test-Path -LiteralPath $LiteralPath }
    return Microsoft.PowerShell.Management\Test-Path $Path
}
function git {
    Write-Host ('CLONE_TARGET: ' + $args[-1])
    throw 'STOP_BEFORE_ACTUAL_CLONE'
}
""", "& ([scriptblock]::Create($source)) -WithoutFFmpeg -NoPause", checkout=False)
        self.assertIn(f"CLONE_TARGET: {Path.home() / 'Porn_Fetch'}", output)
        self.assertIn("STOP_BEFORE_ACTUAL_CLONE", output)

    def run_msys2_setup(self, architecture: str, fail_update: bool = False):
        with tempfile.TemporaryDirectory() as temporary:
            harness = Path(temporary) / "test.ps1"
            harness.write_text(r"""
$ErrorActionPreference = 'Stop'
$source = Get-Content -LiteralPath $env:PORN_FETCH_INSTALL_SCRIPT -Raw
$ast = [Management.Automation.Language.Parser]::ParseInput($source, [ref]$null, [ref]$null)
foreach ($statement in $ast.EndBlock.Statements) {
    if ($statement -is [Management.Automation.Language.FunctionDefinitionAst]) {
        Invoke-Expression $statement.Extent.Text
    }
}
$Msys2Root = Join-Path $env:TEMP 'custom-msys'
$env:MSYSTEM = 'ORIGINAL_SYSTEM'
$env:CHERE_INVOKING = 'ORIGINAL_CHERE'
$originalPath = $env:PATH
$global:updates = 0
function winget { }
function Run {
    param([string]$Exe, [Parameter(ValueFromRemainingArguments=$true)]$Arguments)
    if ($Exe -eq 'winget') {
        if ($Arguments[2] -ne 'MSYS2.MSYS2' -or $Arguments[[Array]::IndexOf($Arguments, '--location') + 1] -ne $Msys2Root) {
            throw 'Wrong MSYS2 package or custom installation path'
        }
        $expectedArch = if ($env:PORN_FETCH_TEST_ARCH -eq 'amd64') { 'x64' } else { 'arm64' }
        if ($Arguments[[Array]::IndexOf($Arguments, '--architecture') + 1] -ne $expectedArch) {
            throw 'MSYS2 installer architecture does not match Python'
        }
        Write-Output 'MSYS2_INSTALLED'
        New-Item -ItemType Directory (Join-Path $Msys2Root 'usr/bin') -Force | Out-Null
        New-Item (Join-Path $Msys2Root 'usr/bin/bash.exe') | Out-Null
    } elseif ($Exe.EndsWith('pacman.exe')) {
        if ($Arguments -contains '-Syu') {
            $global:updates++
            if ($global:updates -eq 1 -or $env:PORN_FETCH_FAIL_UPDATE -eq '1') {
                throw 'SIMULATED_CORE_UPDATE_EXIT'
            }
            Write-Output 'UPDATE_FINISHED'
        } else {
            Write-Output ('PACKAGES: ' + ($Arguments -join ' '))
        }
    } elseif ($Exe.EndsWith('bash.exe')) {
        if ($Arguments[1] -ne 'true') {
            Write-Output ('TOOLS_READY: ' + $env:MSYSTEM)
        }
    } else { throw "Unexpected tool: $Exe" }
}
try {
    Ensure-Msys2 -Architecture $env:PORN_FETCH_TEST_ARCH
    Write-Output 'MSYS2_SETUP_COMPLETE'
} catch { Write-Output "SETUP_FAILED: $_" }
if ($env:MSYSTEM -ne 'ORIGINAL_SYSTEM' -or $env:CHERE_INVOKING -ne 'ORIGINAL_CHERE') {
    throw 'MSYS2 environment was not restored'
}
if ($env:PATH -ne $originalPath) { throw 'MSYS2 PATH was not restored' }
""", encoding="utf-8")
            result = subprocess.run(
                [POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(harness)],
                capture_output=True, text=True, timeout=30,
                env=dict(os.environ, TEMP=temporary, TMP=temporary, TMPDIR=temporary,
                         PORN_FETCH_INSTALL_SCRIPT=str(SCRIPT), PORN_FETCH_TEST_ARCH=architecture,
                         PORN_FETCH_FAIL_UPDATE="1" if fail_update else "0"),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return result.stdout

    def test_msys2_bootstrap_finishes_core_update_and_selects_python_architecture(self):
        for arch, system, prefix in (("amd64", "CLANG64", "x86_64"), ("arm64", "CLANGARM64", "aarch64")):
            with self.subTest(arch=arch):
                output = self.run_msys2_setup(arch)
                self.assertIn("MSYS2_INSTALLED", output)
                self.assertIn("UPDATE_FINISHED", output)
                self.assertIn(f"mingw-w64-clang-{prefix}-toolchain", output)
                self.assertIn(f"mingw-w64-clang-{prefix}-zlib", output)
                self.assertIn("make diffutils pkgconf", output)
                self.assertIn(f"TOOLS_READY: {system}", output)
                self.assertIn("MSYS2_SETUP_COMPLETE", output)

    def test_failed_final_msys2_update_stops_toolchain_installation(self):
        output = self.run_msys2_setup("amd64", fail_update=True)
        self.assertIn("SETUP_FAILED: SIMULATED_CORE_UPDATE_EXIT", output)
        self.assertNotIn("PACKAGES:", output)
        self.assertNotIn("MSYS2_SETUP_COMPLETE", output)

    def test_without_ffmpeg_skips_msys2_bootstrap(self):
        output = self.run_msvc_setup("missing", invoke_main=True)
        self.assertIn("BUILD_REACHED_WITHOUT_MSYS2", output)
        self.assertIn("MSVC_READY_BEFORE_SYNC", output)
        self.assertNotIn("DEPENDENCIES_STARTED_WITHOUT_MSVC", output)

    def run_msvc_setup(self, state: str, architecture: str = "amd64", repair_exit: int = 0, invoke_main: bool = False):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            (root / "scripts/build_desktop.py").touch()
            harness = Path(temporary) / "test.ps1"
            harness.write_text(r"""
$ErrorActionPreference = 'Stop'
$source = Get-Content -LiteralPath $env:PORN_FETCH_INSTALL_SCRIPT -Raw
$ast = [Management.Automation.Language.Parser]::ParseInput($source, [ref]$null, [ref]$null)
foreach ($statement in $ast.EndBlock.Statements) {
    if ($statement -is [Management.Automation.Language.FunctionDefinitionAst]) {
        Invoke-Expression $statement.Extent.Text
    }
}
$global:MsvcReady = $env:PORN_FETCH_MSVC_STATE -eq 'ready'
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio/Installer/vswhere.exe'
New-Item -ItemType Directory (Split-Path $vswhere) -Force | Out-Null
New-Item $vswhere | Out-Null
function winget { }
function uv { }
function Run {
    param([string]$Exe, [Parameter(ValueFromRemainingArguments=$true)]$Arguments)
    if ($Exe -eq 'winget') {
        if ($Arguments[2] -ne 'Microsoft.VisualStudio.2022.BuildTools') { throw 'Wrong MSVC package' }
        $options = $Arguments[-1]
        foreach ($required in @('--wait', '--norestart', '--includeRecommended', 'Microsoft.VisualStudio.Workload.VCTools')) {
            if (-not $options.Contains($required)) { throw "Missing installer option: $required" }
        }
        Write-Host "INSTALL_MSVC: $options"
        $global:MsvcReady = $true
    } elseif ($Exe -eq 'uv') {
        if ($Arguments[0] -eq 'python' -and $Arguments[1] -eq 'find') { Write-Output 'fake-python' }
        if ($Arguments[0] -eq 'sync') {
            if (-not $global:MsvcReady) { throw 'DEPENDENCIES_STARTED_WITHOUT_MSVC' }
            Write-Host 'MSVC_READY_BEFORE_SYNC'
        }
        if ($Arguments -contains 'scripts/build_desktop.py') { throw 'BUILD_REACHED_WITHOUT_MSYS2' }
    } elseif ($Exe -eq 'fake-python') {
        Write-Output $env:PORN_FETCH_TEST_ARCH
    } elseif ($Arguments -contains '-find') {
        if ($Arguments -notcontains 'Microsoft.VisualStudio.Component.Windows*SDK.*') { throw 'Windows SDK was not checked' }
        if ($Arguments -notcontains 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64') { throw 'C++ tools were not checked' }
        if ($env:PORN_FETCH_TEST_ARCH -eq 'arm64') {
            if ($Arguments -notcontains 'Microsoft.VisualStudio.Component.VC.Tools.ARM64') { throw 'ARM64 compiler was not checked' }
            if (-not $Arguments[-1].Contains('\arm64\cl.exe')) { throw 'Wrong compiler target' }
        }
        if ($global:MsvcReady) { Write-Output 'C:\VisualStudio\VC\Tools\MSVC\14.44\bin\Hostx64\cl.exe' }
    } elseif ($env:PORN_FETCH_MSVC_STATE -eq 'incomplete') {
        Write-Output 'C:\Existing BuildTools'
    }
}
function Start-Process {
    param($FilePath, $ArgumentList, [switch]$Wait, [switch]$PassThru)
    if (-not $ArgumentList.Contains('modify --installPath "C:\Existing BuildTools"')) { throw 'Wrong repair target' }
    if ($ArgumentList.Contains('--wait')) { throw 'setup.exe does not support --wait' }
    if (-not $Wait) { throw 'Installer was not awaited' }
    Write-Host 'REPAIR_MSVC'
    $global:MsvcReady = $true
    return @{ ExitCode = [int]$env:PORN_FETCH_REPAIR_EXIT }
}
try {
    if ($env:PORN_FETCH_TEST_MAIN -eq '1') { $WithoutFFmpeg = $true; Main }
    else { Ensure-Msvc -Architecture $env:PORN_FETCH_TEST_ARCH }
    Write-Output 'MSVC_SETUP_COMPLETE'
}
catch { Write-Output "SETUP_FAILED: $_" }
""", encoding="utf-8")
            result = subprocess.run(
                [POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(harness)],
                cwd=root, capture_output=True, text=True, timeout=30,
                env=dict(os.environ, **{"ProgramFiles(x86)": temporary},
                         PORN_FETCH_INSTALL_SCRIPT=str(SCRIPT), PORN_FETCH_MSVC_STATE=state,
                         PORN_FETCH_TEST_ARCH=architecture, PORN_FETCH_REPAIR_EXIT=str(repair_exit),
                         PORN_FETCH_TEST_MAIN="1" if invoke_main else "0"),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return result.stdout

    def test_existing_msvc_and_sdk_are_kept(self):
        output = self.run_msvc_setup("ready")
        self.assertIn("MSVC_SETUP_COMPLETE", output)
        self.assertNotIn("INSTALL_MSVC:", output)
        self.assertNotIn("REPAIR_MSVC", output)

    def test_msvc_installation_includes_cpp_workload_and_arm64_when_needed(self):
        for arch in ("amd64", "arm64"):
            with self.subTest(arch=arch):
                output = self.run_msvc_setup("missing", arch)
                self.assertIn("INSTALL_MSVC:", output)
                self.assertIn("MSVC_SETUP_COMPLETE", output)
                if arch == "arm64":
                    self.assertIn("Microsoft.VisualStudio.Component.VC.Tools.ARM64", output)

    def test_incomplete_build_tools_are_modified_and_reboot_is_reported(self):
        for exit_code in (0, 3010):
            with self.subTest(exit_code=exit_code):
                output = self.run_msvc_setup("incomplete", repair_exit=exit_code)
                self.assertIn("REPAIR_MSVC", output)
                self.assertNotIn("INSTALL_MSVC:", output)
                if exit_code == 0:
                    self.assertIn("MSVC_SETUP_COMPLETE", output)
                else:
                    self.assertIn("Restart Windows", output)
                    self.assertNotIn("MSVC_SETUP_COMPLETE", output)


if __name__ == "__main__":
    unittest.main()
