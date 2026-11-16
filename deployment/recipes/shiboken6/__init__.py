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


class ShibokenRecipe(PythonRecipe):
    version = '6.12.0'
    wheel_path = '/home/asuna/PycharmProjects/Porn_Fetch/shiboken6-6.12.0-6.12.0-cp314-cp314-android_aarch64.whl'

    call_hostpython_via_targetpython = False
    install_in_hostpython = False

    def build_arch(self, arch):
        ''' Unzip the wheel and copy into site-packages of target'''
        info('Installing {} into site-packages'.format(self.name))
        with zipfile.ZipFile(self.wheel_path, 'r') as zip_ref:
            info('Unzip wheels and copy into {}'.format(self.ctx.get_python_install_dir(arch.arch)))
            safe_extractall(zip_ref, Path(self.ctx.get_python_install_dir(arch.arch)))

        lib_dir = Path(f"{self.ctx.get_python_install_dir(arch.arch)}/shiboken6")
        shutil.copyfile(lib_dir / "libshiboken6.abi3.so",
                        Path(self.ctx.get_libs_dir(arch.arch)) / "libshiboken6.abi3.so")


recipe = ShibokenRecipe()