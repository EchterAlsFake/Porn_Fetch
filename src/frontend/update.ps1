# update_ui.ps1
Write-Output "Updating UI components, resource files, and translations..."

# Change to the script's directory
Set-Location -Path $PSScriptRoot

# Process UI files
Write-Output "Processing UI files..."
pyside6-uic form_android.ui -o ui_form_android.py
pyside6-uic form_android_startup.ui -o ui_form_android_startup.py
pyside6-uic form_desktop.ui -o ui_form_desktop.py
pyside6-uic form_install_dialog.ui -o ui_form_install_dialog.py
pyside6-uic form_license.ui -o ui_form_license.py
pyside6-uic form_range_selector.ui -o ui_form_range_selector.py

# Process resource file
Write-Output "Processing resource file..."
pyside6-rcc resources.qrc -o resources.py

# Update translations
Write-Output "Updating translations..."
pyside6-lupdate `
    ../../main.py `
    ../backend/class_help.py `
    ui_form_desktop.py `
    ui_form_install_dialog.py `
    ui_form_license.py `
    ui_form_range_selector.py `
    form_desktop.ui `
    form_install_dialog.ui `
    form_license.ui `
    form_range_selector.ui `
    -ts translations/en.ts -no-obsolete

pyside6-lrelease translations/de_DE.ts -qm translations/de_DE.qm
pyside6-lrelease translations/zh_CN.ts -qm translations/zh_CN.qm
pyside6-lrelease translations/fr.ts -qm translations/fr.qm

Write-Output "UI update completed successfully!"