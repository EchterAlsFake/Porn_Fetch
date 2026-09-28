# Third-party notices and release inventory

Porn Fetch's [application license](LICENSE) covers only material for which its
licensor has the required rights. The components below keep their own licenses.
The exact components shipped in an executable must be checked against the
artifact and the pinned dependency versions for that platform. This document
is an inventory, not a substitute for those license texts.

| Component | Current license evidence | Distribution note |
| --- | --- | --- |
| `eaf_base_api` and the thirteen `unofficial-api-for-*` packages in `pyproject.toml` | Installed metadata: AGPL-3.0-or-later for `eaf_base_api`; AGPL-3.0-only for the providers | The [additional permission](LICENSES/Provider-permission.txt) applies only to portions Johannes Habel may license separately. Audit other contributions before distribution. |
| PySide6 and Qt 6 | PySide6 metadata: LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only; [Qt licensing](https://www.qt.io/development/open-source-lgpl-obligations) | Audit each bundled Qt module; preserve the LGPL notices and source availability, and verify that users can replace the LGPL libraries in the actual installer or one-file build. |
| `browser-cookie3`, `pydivert` | Installed metadata: LGPL; LGPL-3.0-or-later OR GPL-2.0-or-later | Include the exact distribution licenses and comply with the chosen LGPL/GPL terms. |
| PocketBase executable | [MIT](https://github.com/pocketbase/pocketbase/blob/master/LICENSE.md) | Installer and CI workflows download and bundle this executable; include its copyright and MIT text with each affected artifact. |
| PyAV / FFmpeg | PyAV metadata: BSD-3-Clause; FFmpeg configuration can vary by build | Inspect the FFmpeg libraries in the shipped PyAV wheel and include their actual LGPL/GPL and codec notices. Do not label all FFmpeg builds as GPL without checking. |
| Other Python packages | `uv.lock` and installed package metadata | Generate an artifact-specific list and include the packages' license and notice files; account for platform extras and transitive dependencies. |
| Application graphics | [Asset provenance](docs/ASSET_PROVENANCE.md) | Newly drawn SVGs are part of the application. Preserve the documented provenance of the PNG logo and splash assets; replace or clear any uncertain asset before release. |

The obsolete library list in `docs/CREDITS.md` is retained as historical
acknowledgment. It does not establish the shipped dependency list or license
obligations. Third-party notices and source availability must be present in the
delivered package, not only in this repository.
