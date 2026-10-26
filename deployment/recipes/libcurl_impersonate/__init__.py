"""Verified upstream Android curl-impersonate libraries for each application ABI."""

import tarfile
from pathlib import Path

from pythonforandroid.recipe import Recipe

ASSETS = {
    "arm64-v8a": ("aarch64", "fd8a9ba3386d10f8519fcff3b50f655a41fd38e5e5a2fb8eabcac6085587bcbf"),
    "armeabi-v7a": ("armv7", "a3ca8c80d74fcc6ba4dd92bedb0c9a82bb2246806e5116294196351cfd8fbede"),
    "x86": ("x86", "22bc873b2ba2eae98367a34155107df6c6b221b707e5b8be0bc4746db25ea389"),
    "x86_64": ("x86_64", "d7f7d00b3bd0eae23eb7440e374ffbbbf978be782f8ebddccf888a1677282513"),
}


class CurlImpersonateRecipe(Recipe):
    version = "2.3.1"

    @property
    def url(self):
        architecture, digest = ASSETS[self.ctx.archs[0].arch]
        return ("https://github.com/lexiforest/curl-impersonate/releases/download/"
                f"v{self.version}/libcurl-impersonate-v{self.version}.{architecture}-linux-android.tar.gz"
                f"#sha256={digest}")

    def unpack(self, arch):
        # These release archives contain files at the archive root, unlike
        # source archives for which p4a moves a single top-level directory.
        filename = self.url.rsplit("/", 1)[1].split("#", 1)[0]
        archive = Path(self.ctx.packages_path) / self.name / filename
        destination = Path(self.get_build_dir(arch))
        destination.mkdir(parents=True, exist_ok=True)
        with tarfile.open(archive) as bundle:
            bundle.extractall(destination, filter="data")


recipe = CurlImpersonateRecipe()
