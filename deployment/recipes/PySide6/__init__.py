# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
# Qt-Security score:critical reason:handling-untrusted-data
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from pythonforandroid.logger import info
from pythonforandroid.recipe import PythonRecipe

def safe_extractall(zip_ref: zipfile.ZipFile, target_path: Path) -> None:
    """
    Extract all members of zip_ref into target_path, checking that each entry
    resolves inside target_path to prevent path traversal attacks.
    """
    resolved_target = target_path.resolve()
    for member in zip_ref.infolist():
        member_path = (target_path / member.filename).resolve()
        if not member_path.is_relative_to(resolved_target):
            raise RuntimeError(
                f"Refusing to extract '{member.filename}': "
                f"path resolves outside the extraction directory"
            )
        zip_ref.extract(member, target_path)


class PySideRecipe(PythonRecipe):
    version = '6.12.0'
    wheel_path = '/home/asuna/PycharmProjects/Porn_Fetch/pyside6-6.12.0-6.12.0-cp314-cp314-android_aarch64.whl'
    depends = ["shiboken6"]
    call_hostpython_via_targetpython = False
    install_in_hostpython = False

    def build_arch(self, arch):
        """Unzip the wheel and copy into site-packages of target"""

        info("Copying libc++_shared.so from SDK to be loaded on startup")
        libcpp_path = f"{self.ctx.ndk.sysroot_lib_dir}/{arch.command_prefix}/libc++_shared.so"
        shutil.copyfile(libcpp_path, Path(self.ctx.get_libs_dir(arch.arch)) / "libc++_shared.so")

        info(f"Installing {self.name} into site-packages")
        with zipfile.ZipFile(self.wheel_path, "r") as zip_ref:
            info("Unzip wheels and copy into {}".format(self.ctx.get_python_install_dir(arch.arch)))
            safe_extractall(zip_ref, Path(self.ctx.get_python_install_dir(arch.arch)))

        lib_dir = Path(f"{self.ctx.get_python_install_dir(arch.arch)}/PySide6/Qt/lib")

        info("Copying Qt libraries to be loaded on startup")
        shutil.copytree(lib_dir, self.ctx.get_libs_dir(arch.arch), dirs_exist_ok=True)
        shutil.copyfile(lib_dir.parent.parent / "libpyside6.abi3.so",
                        Path(self.ctx.get_libs_dir(arch.arch)) / "libpyside6.abi3.so")

        # porn-fetch-all-abi3-v1
        info("Copying PySide6 and Qt Python abi3 libraries")
        for so_file in (lib_dir.parent.parent).glob("*.abi3.so"):
            shutil.copyfile(so_file, Path(self.ctx.get_libs_dir(arch.arch)) / so_file.name)

          # noqa: E999

          # noqa: E999
        plugin_path = (lib_dir.parent / "plugins" / "platforms" /
                      f"libplugins_platforms_qtforandroid_{arch.arch}.so")
        if plugin_path.exists():
            shutil.copyfile(plugin_path,
                            (Path(self.ctx.get_libs_dir(arch.arch)) /
                             f"libplugins_platforms_qtforandroid_{arch.arch}.so"))
          # noqa: E999


recipe = PySideRecipe()