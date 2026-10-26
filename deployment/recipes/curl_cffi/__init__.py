"""Build the CFFI extension against Android Python and verified impersonation libraries."""

import shutil
from pathlib import Path

from pythonforandroid.recipe import PyProjectRecipe


class CurlCffiRecipe(PyProjectRecipe):
    version = "0.17.0"
    url = "https://files.pythonhosted.org/packages/source/c/curl_cffi/curl_cffi-{version}.tar.gz"
    sha256sum = "31ee8500d06d6502ce1ec0b7ded1c5aa8e8f3401bbe37ccd78d6153d859d8f3c"
    depends = ["python3", "cffi", "libcurl_impersonate", "certifi"]

    def lookup_prebuilt(self, arch):
        # Keep the same verified libcurl version on all four ABIs.
        return False

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)
        machine, bits = {
            "arm64-v8a": ("aarch64", "64"), "armeabi-v7a": ("armv7l", "32"),
            "x86_64": ("x86_64", "64"), "x86": ("i686", "32"),
        }[arch.arch]
        env.update({
            "CIBW_PLATFORM": "android",
            "CURL_CFFI_TARGET_MACHINE": machine,
            "CURL_CFFI_TARGET_POINTER_SIZE": bits,
            "IMPERSONATE_BUILD_DIR": self.get_recipe("libcurl_impersonate", self.ctx).get_build_dir(arch.arch),
            "IMPERSONATE_LINK_TYPE": "static",
        })
        include = self.ctx.python_recipe.include_root(arch.arch)
        env["CFLAGS"] = f"-I{include} {env.get('CFLAGS', '')}"
        env["LDFLAGS"] += (f" -L{self.ctx.python_recipe.link_root(arch.arch)}"
                           f" -lpython{self.ctx.python_recipe.link_version}")
        return env

    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)
        libraries = self.get_recipe("libcurl_impersonate", self.ctx)
        source = Path(libraries.get_build_dir(arch.arch))
        destination = Path(self.ctx.get_python_install_dir(arch.arch)) / "curl_cffi/third_party_licenses"
        destination.mkdir(parents=True, exist_ok=True)
        for notice in source.glob("LICENSE*"):
            shutil.copy2(notice, destination / notice.name)


recipe = CurlCffiRecipe()
