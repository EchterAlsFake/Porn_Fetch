# Updates the entire frontend

pyside6-uic form_android.ui -o ui_form_android.py
pyside6-uic form_android_startup.ui -o ui_form_android_startup.py
pyside6-uic form_desktop.ui -o ui_form_desktop.py
pyside6-uic form_install_dialog.ui -o ui_form_install_dialog.py
pyside6-uic form_license.ui -o ui_form_license.py
pyside6-uic form_range_selector.ui -o ui_form_range_selector.py

pyside6-rcc resources.qrc -o resources.py

# TODO: translations
