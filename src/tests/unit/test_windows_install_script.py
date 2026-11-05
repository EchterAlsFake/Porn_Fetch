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
    def run_failure(self, mock_commands: str, invocation: str):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
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


if __name__ == "__main__":
    unittest.main()
