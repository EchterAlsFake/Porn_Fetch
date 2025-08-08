# update_ui.ps1
Write-Output "Updating UI components, resource files, and translations..."

# Change to the script's directory
Set-Location -Path $PSScriptRoot

# Process UI files
pyside6-uic UI/form_main_window.ui -o UI/ui_form_main_window.py
pyside6-uic UI/form_android.ui -o UI/ui_form_android.py

# Update translations
Write-Output "Updating translations..."
# Translations
pyside6-lupdate ../../main.py ../backend/class_help.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/en.ts -no-obsolete
pyside6-lupdate ../../main.py ../backend/class_help.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/de_DE.ts -no-obsolete
pyside6-lupdate ../../main.py ../backend/class_help.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/fr.ts -no-obsolete
pyside6-lupdate ../../main.py ../backend/class_help.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/zh_CN.ts -no-obsolete
pyside6-lrelease translations/de_DE.ts -qm translations/de_DE.qm
pyside6-lrelease translations/zh_CN.ts -qm translations/zh_CN.qm
pyside6-lrelease translations/fr.ts -qm translations/fr.qm


# Process resource file
Write-Output "Processing resource file..."
pyside6-rcc resources.qrc -o UI/resources.py


Write-Output "UI update completed successfully!"
