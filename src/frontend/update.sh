## Updates the entire frontend

pyside6-uic UI/form_main_window.ui -o UI/ui_form_main_window.py
pyside6-uic UI/form_android.ui -o UI/ui_form_android.py

# Translations
pyside6-lupdate ../../main.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/ts/en.ts -no-obsolete
pyside6-lupdate ../../main.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/ts/de_DE.ts -no-obsolete
pyside6-lupdate ../../main.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/ts/fr.ts -no-obsolete
pyside6-lupdate ../../main.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/ts/zh_CN.ts -no-obsolete
pyside6-lrelease translations/ts/de_DE.ts -qm translations/qm/de_DE.qm
pyside6-lrelease translations/ts/zh_CN.ts -qm translations/qm/zh_CN.qm
pyside6-lrelease translations/ts/fr.ts -qm translations/qm/fr.qm

# Resource file
pyside6-rcc resources.qrc -o UI/resources.py
