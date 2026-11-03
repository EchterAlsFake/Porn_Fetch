"""Reuse p4a's Python recipe without patches already upstream in Python 3.15."""

import runpy
from pathlib import Path

import pythonforandroid

UPSTREAM_DIR = Path(pythonforandroid.__file__).resolve().parent / "recipes/python3"
UpstreamPython3Recipe = runpy.run_path(str(UPSTREAM_DIR / "__init__.py"))["Python3Recipe"]


class Python3Recipe(UpstreamPython3Recipe):
    version = "3.15.2"

    def get_recipe_dir(self):
        # Keep using upstream patch files and other recipe assets.
        return str(UPSTREAM_DIR)

    def apply_patch(self, filename, arch, build_dir=None):
        if self.major_minor_version_string == "3.15" and filename in {
            "patches/3.14_armv7l_fix.patch",
            "patches/3.14_fix_remote_debug.patch",
        }:
            return
        return super().apply_patch(filename, arch, build_dir)


recipe = Python3Recipe()
