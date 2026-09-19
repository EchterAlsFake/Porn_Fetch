# update_ui.ps1
$ErrorActionPreference = "Stop"
Write-Output "Updating UI components, resource files, and translations..."

# Change to the script's directory
Set-Location -Path $PSScriptRoot

# Update translations
Write-Output "Updating translations..."
# Translations
$qmlFiles = Get-ChildItem -Path UI -Filter *.qml | ForEach-Object { $_.FullName }
uv run pyside6-lupdate ../backend/application.py $qmlFiles -ts translations/ts/en.ts -no-obsolete
uv run pyside6-lupdate ../backend/application.py $qmlFiles -ts translations/ts/de_DE.ts -no-obsolete
uv run pyside6-lupdate ../backend/application.py $qmlFiles -ts translations/ts/fr.ts -no-obsolete
uv run pyside6-lupdate ../backend/application.py $qmlFiles -ts translations/ts/zh_CN.ts -no-obsolete
uv run pyside6-lrelease translations/ts/de_DE.ts -qm translations/qm/de_DE.qm
uv run pyside6-lrelease translations/ts/zh_CN.ts -qm translations/qm/zh_CN.qm
uv run pyside6-lrelease translations/ts/fr.ts -qm translations/qm/fr.qm


# Process resource file
Write-Output "Processing resource file..."
uv run pyside6-rcc resources.qrc -o UI/resources.py

Write-Output "UI update completed successfully!"
