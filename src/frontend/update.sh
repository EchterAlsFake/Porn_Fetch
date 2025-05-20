## Updates the entire frontend

pyside6-uic form_android.ui -o ui_form_android.py
pyside6-uic form_android_startup.ui -o ui_form_android_startup.py
pyside6-uic form_desktop.ui -o ui_form_desktop.py
pyside6-uic form_install_dialog.ui -o ui_form_install_dialog.py
pyside6-uic form_license.ui -o ui_form_license.py
pyside6-uic form_range_selector.ui -o ui_form_range_selector.py
pyside6-uic form_keyboard_shortcuts.ui -o ui_form_keyboard_shortcuts.py
pyside6-uic form_main_window.ui -o ui_form_main_window.py

# Resource file
pyside6-rcc resources.qrc -o resources.py

# Translations
pyside6-lupdate ../../main.py ../backend/class_help.py ui_form_desktop.py ui_form_install_dialog.py ui_form_license.py ui_form_range_selector.py form_keyboard_shortcuts.ui ui_form_keyboard_shortcuts.py form_desktop.ui form_install_dialog.ui form_license.ui form_range_selector.ui -ts translations/en.ts -no-obsolete
pyside6-lupdate ../../main.py ../backend/class_help.py ui_form_desktop.py ui_form_install_dialog.py ui_form_license.py ui_form_range_selector.py form_keyboard_shortcuts.ui ui_form_keyboard_shortcuts.py form_desktop.ui form_install_dialog.ui form_license.ui form_range_selector.ui -ts translations/de_DE.ts -no-obsolete
pyside6-lupdate ../../main.py ../backend/class_help.py ui_form_desktop.py ui_form_install_dialog.py ui_form_license.py ui_form_range_selector.py form_keyboard_shortcuts.ui ui_form_keyboard_shortcuts.py form_desktop.ui form_install_dialog.ui form_license.ui form_range_selector.ui -ts translations/zh_CN.ts -no-obsolete
pyside6-lupdate ../../main.py ../backend/class_help.py ui_form_desktop.py ui_form_install_dialog.py ui_form_license.py ui_form_range_selector.py form_keyboard_shortcuts.ui ui_form_keyboard_shortcuts.py form_desktop.ui form_install_dialog.ui form_license.ui form_range_selector.ui -ts translations/fr.ts -no-obsolete
pyside6-lrelease translations/de_DE.ts -qm translations/de_DE.qm
pyside6-lrelease translations/zh_CN.ts -qm translations/zh_CN.qm
pyside6-lrelease translations/fr.ts -qm translations/fr.qm

