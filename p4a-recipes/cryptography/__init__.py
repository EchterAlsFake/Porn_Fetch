"""Use maintained cryptography with the target Python installation for cross builds."""

from pathlib import Path

from pythonforandroid.recipe import RustCompiledComponentsRecipe


class CryptographyRecipe(RustCompiledComponentsRecipe):
    version = "50.0.2"
    url = "https://files.pythonhosted.org/packages/source/c/cryptography/cryptography-{version}.tar.gz"
    sha256sum = "7b46165bb56eb4704e2eaaf86f3c940d19154535d9b0ca7d6d590b04060e00d5"
    depends = ["openssl", "cffi"]

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)
        openssl = Path(self.get_recipe("openssl", self.ctx).get_build_dir(arch.arch))
        target = self.RUST_ARCH_CODES[arch.arch].upper().replace("-", "_")
        env[f"{target}_OPENSSL_INCLUDE_DIR"] = str(openssl / "include")
        env[f"{target}_OPENSSL_LIB_DIR"] = str(openssl)
        # cryptography derives include/pythonX.Y from this installed target
        # prefix. p4a's default points at android-build/build/lib.*, which
        # causes the CFFI helper to use host headers or a nonexistent path.
        python = self.ctx.python_recipe
        env["PYO3_CROSS_LIB_DIR"] = str(Path(python.get_python_root(arch)) / "lib"
                                         / f"python{self.python_major_minor_version}")
        return env


recipe = CryptographyRecipe()
