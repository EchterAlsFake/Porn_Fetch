# Third-party notices and release inventory

Porn Fetch's [application license](LICENSE) covers only material for which its
licensor has the required rights. The components below keep their own licenses.
The exact components shipped in an executable must be checked against the
artifact and the pinned dependency versions for that platform. This document
is an inventory, not a substitute for those license texts.

| Component | Current license evidence | Distribution note |
| --- | --- | --- |
| `eaf_base_api` and the sixteen `unofficial-api-for-*` packages in `pyproject.toml` | Installed metadata: AGPL-3.0-or-later for `eaf_base_api`; AGPL-3.0-only for the providers | The [additional permission](LICENSES/Provider-permission.txt) applies only to portions Johannes Habel may license separately. Audit other contributions before distribution. |
| PySide6 and Qt 6 | PySide6 metadata: LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only; [Qt licensing](https://www.qt.io/development/open-source-lgpl-obligations) | Audit each bundled Qt module; preserve the LGPL notices and source availability, and verify that users can replace the LGPL libraries in the actual installer or one-file build. |
| `browser-cookie3`, `pydivert` | Installed metadata: LGPL; LGPL-3.0-or-later OR GPL-2.0-or-later | Include the exact distribution licenses and comply with the chosen LGPL/GPL terms. |
| PocketBase executable | [MIT](https://github.com/pocketbase/pocketbase/blob/master/LICENSE.md) | Installer and CI workflows download and bundle this executable; include its copyright and MIT text with each affected artifact. |
| FFmpeg | [LGPL-2.1-or-later](https://ffmpeg.org/legal.html), built from pinned FFmpeg 9.0.2 source | The minimal profile explicitly disables GPL, version-3, nonfree, and third-party codec features. Desktop and Android builds use a separate executable. iOS statically links the FFmpeg libraries into its replaceable `_ios_ffmpeg` extension. Release legal bundles include the complete source archive, license texts, configure flags, configuration headers and build hashes; the iOS bundle also includes bridge sources and `ffmpeg/0/REBUILD.md` for rebuilding and replacing the extension. Desktop build materials are also in `third_party/ffmpeg-legal`. |
| zlib | [zlib license](https://zlib.net/zlib_license.html) | Used for PNG cover probing. Linux/macOS use the system library; Windows statically links the MSYS2 library and includes its `zlib.h` copyright/license text in `ffmpeg-legal`. |
| LZ4 native compression library | [BSD-2-Clause](LICENSES/LZ4.txt) | macOS bundles the native library when required by the Python compression extensions; retain its copyright and license alongside the Python package's separate license. |
| Other Python packages | `pyproject.toml` and installed package metadata | Generate an artifact-specific list and include the packages' license and notice files; account for platform extras and transitive dependencies. |
| Application graphics | [Graphics source files](src/frontend/graphics/); Lucide settings-icon attribution below | Application-owned SVGs use the application license; Lucide icons retain their MIT notice. Preserve provenance records for the PNG logo and splash assets; replace or clear any uncertain asset before release. |
| Content-language flag images | [flag-icons](https://github.com/lipis/flag-icons), MIT | SVGs from revision `ac7e0eb3259eb62aa6100c435607e2fe03896a97`; copyright and license in [LICENSES/FlagIcons.txt](LICENSES/FlagIcons.txt). |

The obsolete library list in `docs/CREDITS.md` is retained as historical
acknowledgment. It does not establish the shipped dependency list or license
obligations. Third-party notices and source availability must be present in the
delivered package, not only in this repository.

## Settings icons

The video, gauge, settings, shield, palette and trash SVGs in
`src/frontend/graphics/settings/` are by Lucide Icons and Contributors, from
https://github.com/lucide-icons/lucide/tree/main/icons (downloaded 2026-10-26).
They are distributed under the ISC license, with the Feather-derived icons
covered by the MIT notice included in [LICENSES/Lucide.txt](LICENSES/Lucide.txt).
See https://lucide.dev/license. The SVG artwork is unmodified.

### Payment logos

The Bitcoin, Ethereum and Litecoin logo vectors in
`src/frontend/graphics/payments/` come from [Simple Icons](https://github.com/simple-icons/simple-icons)
under [CC0-1.0](LICENSES/SimpleIcons.txt). Display colours were added.

The Monero logo is by the Monero Project, from its
[press kit](https://www.getmonero.org/press-kit), obtained through Simple Icons.
It uses [CC BY-SA 4.0](LICENSES/Monero-CC-BY-SA-4.0.txt). The SVG has an added
orange fill; that modified vector remains under CC BY-SA 4.0. Its editable
source is `src/frontend/graphics/payments/monero.svg`.

These names and logos remain the marks of their respective owners; no
endorsement is implied.
