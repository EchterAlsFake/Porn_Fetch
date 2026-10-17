# Third-party notices and release inventory

Porn Fetch's [application license](LICENSE) covers only material for which its
licensor has the required rights. The components below keep their own licenses.
The exact components shipped in an executable must be checked against the
artifact and the pinned dependency versions for that platform. This document
is an inventory, not a substitute for those license texts.

| Component | Current license evidence | Distribution note |
| --- | --- | --- |
| `eaf_base_api` and the fifteen `unofficial-api-for-*` packages in `pyproject.toml` | Installed metadata: AGPL-3.0-or-later for `eaf_base_api`; AGPL-3.0-only for the providers | The [additional permission](LICENSES/Provider-permission.txt) applies only to portions Johannes Habel may license separately. Audit other contributions before distribution. |
| PySide6 and Qt 6 | PySide6 metadata: LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only; [Qt licensing](https://www.qt.io/development/open-source-lgpl-obligations) | Audit each bundled Qt module; preserve the LGPL notices and source availability, and verify that users can replace the LGPL libraries in the actual installer or one-file build. |
| `browser-cookie3`, `pydivert` | Installed metadata: LGPL; LGPL-3.0-or-later OR GPL-2.0-or-later | Include the exact distribution licenses and comply with the chosen LGPL/GPL terms. |
| PocketBase executable | [MIT](https://github.com/pocketbase/pocketbase/blob/master/LICENSE.md) | Installer and CI workflows download and bundle this executable; include its copyright and MIT text with each affected artifact. |
| FFmpeg executable | [LGPL-2.1-or-later](https://ffmpeg.org/legal.html), built from pinned FFmpeg 9.0.2 source | The minimal profile explicitly disables GPL, version-3, nonfree, and third-party codec features. FFmpeg runs as a separate executable. Its complete source archive, license texts, configure flags, configuration headers, and build hashes accompany it in `third_party/ffmpeg-legal` and release legal bundles. See [FFmpeg builds](docs/FFMPEG.md). |
| zlib | [zlib license](https://zlib.net/zlib_license.html) | Used for PNG cover probing. Linux/macOS use the system library; Windows statically links the MSYS2 library and includes its `zlib.h` copyright/license text in `ffmpeg-legal`. |
| Other Python packages | `uv.lock` and installed package metadata | Generate an artifact-specific list and include the packages' license and notice files; account for platform extras and transitive dependencies. |
| Application graphics | [Asset provenance](docs/ASSET_PROVENANCE.md) | Newly drawn SVGs are part of the application. Preserve the documented provenance of the PNG logo and splash assets; replace or clear any uncertain asset before release. |

The obsolete library list in `docs/CREDITS.md` is retained as historical
acknowledgment. It does not establish the shipped dependency list or license
obligations. Third-party notices and source availability must be present in the
delivered package, not only in this repository.
