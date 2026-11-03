# update_ui.ps1
[CmdletBinding()]
param()
if ($VerbosePreference -eq 'Continue') { $env:PORN_FETCH_BUILD_VERBOSE = '1' }
$ErrorActionPreference = "Stop"
Write-Output "Updating UI components, resource files, and translations..."

# Change to the script's directory
Set-Location -Path $PSScriptRoot

# Use the same registry and validation as Unix and CI.
uv run python ../../scripts/translations.py extract
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv run python ../../scripts/translations.py build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# QML Bytecode compilation
Write-Output "Compiling QML to bytecode..."
uv run python ../../scripts/compile_qml.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "UI update completed successfully!"
