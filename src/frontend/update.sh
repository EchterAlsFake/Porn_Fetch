## Updates the entire frontend

uv run pyside6-uic UI/form_main_window.ui -o UI/ui_form_main_window.py

# Translations
uv run pyside6-lupdate ../../main.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/ts/en.ts -no-obsolete
uv run pyside6-lupdate ../../main.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/ts/de_DE.ts -no-obsolete
uv run pyside6-lupdate ../../main.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/ts/fr.ts -no-obsolete
uv run pyside6-lupdate ../../main.py UI/form_main_window.ui UI/ui_form_main_window.py -ts translations/ts/zh_CN.ts -no-obsolete
uv run pyside6-lrelease translations/ts/de_DE.ts -qm translations/qm/de_DE.qm
uv run pyside6-lrelease translations/ts/zh_CN.ts -qm translations/qm/zh_CN.qm
uv run pyside6-lrelease translations/ts/fr.ts -qm translations/qm/fr.qm
uv run pyside6-lrelease translations/ts/it.ts -qm translations/qm/it.qm

# Resource file
uv run pyside6-rcc resources.qrc -o UI/resources.py
