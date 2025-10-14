#!/usr/bin/env bash
set -euo pipefail

# 1) (Re)generate the EN source catalog from your code/UI
pyside6-uic UI/form_main_window.ui -o UI/ui_form_main_window.py
pyside6-uic UI/form_android.ui      -o UI/ui_form_android.py

pyside6-lupdate ../../main.py translations/strings.py \
  UI/form_main_window.ui UI/ui_form_main_window.py \
  -ts translations/en.ts -no-obsolete

# 2) Build .qm files for every translated .ts except en.ts
for ts in translations/*.ts; do
  base="$(basename "$ts")"
  [[ "$base" == "en.ts" ]] && continue
  qm="translations/${base/.ts/.qm}"
  echo "Building $qm"
  pyside6-lrelease "$ts" -qm "$qm"
done

# Building resource file with the new translations
pyside6-rcc resources.qrc -o UI/resources.py
