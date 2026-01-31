"""
This file is a patch for the GitHub actions that will replace the 'IS_SOURCE_RUN = True' to False
in the config.py file. This is needed to restrict the license features in the binary builds
and additionally ensure that users who run from source get a warning that source builds may be
unsafe due to random code changes that haven't been tested.
"""
import sys
from pathlib import Path
file_path = "../backend/config.py"

SEARCH = "IS_SOURCE_RUN = True"
REPLACE = "IS_SOURCE_RUN = False"

file = Path(file_path)

if not file.exists() or not file.is_file():
    print(f"Error: '{file_path}' is not a valid file path.", file=sys.stderr)

original = file.read_text(encoding="utf-8")

if SEARCH not in original:
    print("No match found. File unchanged.")

updated = original.replace(SEARCH, REPLACE)

# Write back only if something actually changed
if updated != original:
    file.write_text(updated, encoding="utf-8")
    count = original.count(SEARCH)
    print(f"Replaced {count} occurrence(s).")
else:
    print("Nothing changed.")

