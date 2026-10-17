from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class ChompjsRecipe(CompiledComponentsPythonRecipe):
    name = "chompjs"
    version = "1.4.1"

    url = (
        "https://files.pythonhosted.org/packages/source/"
        "c/chompjs/chompjs-{version}.tar.gz"
    )

    site_packages_name = "chompjs"

    depends = ["setuptools", "python3"]

    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        python_recipe = self.ctx.python_recipe
        link_version = python_recipe.link_version
        link_dir = python_recipe.link_root(arch.arch)
        libs_dir = self.ctx.get_libs_dir(arch.arch)
        include_dir = python_recipe.include_root(arch.arch)

        env["CFLAGS"] = f"{env.get('CFLAGS', '')} -I{include_dir}"
        env["LDFLAGS"] = (
            f"{env.get('LDFLAGS', '')} "
            f"-L{link_dir} -L{libs_dir} "
            f"-lpython{link_version}"
        )
        return env


recipe = ChompjsRecipe()
