# Install or build Porn Fetch
This guide is for the 3.9 source tree. Older releases have different build steps.

## Download an app

Use [pornfetch.to/download](https://pornfetch.to/download).

- A desktop **Setup** installer installs the app and Qt Maintenance Tool.
  In Settings, use **Manage installation** to add or remove components, or
  **Uninstall Porn Fetch** to open the uninstaller. These actions close the app
  after saving download progress. The maintenance tool asks what to change.
- A **portable GUI** is a complete folder or macOS `.app`. Keep all its files.
  Windows uses ZIP, Linux uses `.tar.gz`, and macOS uses DMG. Portable copies do
  not have a maintenance tool. Replace the complete folder when updating.
- A **CLI** runs in a terminal. Official standalone builds support
  **Check for Updates** in the interactive main menu, as well as
  `self-update --check` and `self-update`. The menu asks before installing and
  closes the session when an update is ready to replace the CLI. Source copies
  use their package manager.
- [Android](ANDROID.md) and [iOS](iOS.md) have separate instructions.

On macOS, Setup offers **Open Porn Fetch** on its final screen and adds a
shortcut in your user Applications folder (`~/Applications`). You can also
search for **Porn Fetch** with Spotlight. The app stays in its selected install
folder so Qt Maintenance Tool can update it. Uninstalling removes the shortcut.
These conveniences require an installer built with this support; older installers
do not add the shortcut.

PocketBase is optional. It stores download history and statistics; it does not
store the download queue. FFmpeg is used to make MP4 files and write metadata.
Both are optional installer components. A compatible copy on `PATH` also works.

## Signatures and antivirus warnings

Your own build does **not** have the Porn Fetch publisher's signature. Building
from source does not give you access to the release signing keys.

- Windows builds are unsigned unless you sign them yourself. SmartScreen or
  antivirus software may flag a new or self-compiled executable.
- Local macOS GUI builds have an **ad-hoc signature** so the bundle can run. This
  does not identify a developer and is not Apple notarization. Gatekeeper can
  still block the app, especially after it is copied or downloaded.
- Linux builds do not receive a publisher code-signing certificate.
- Android source builds are signed automatically with a development key unless
  you configure a release key. iOS requires your own device signing or sideloading setup.

A successful compilation does not prove a file is safe. If a security tool flags
it, check the source commit, dependency list and build log. Do not disable your
antivirus or add a broad exclusion. Report suspected false positives to the
security vendor. A checksum checks file integrity; it is not a publisher signature.
See [release signing](RELEASING.md) if you plan to distribute your builds.

## Run from source

Install Git and [uv](https://docs.astral.sh/uv/getting-started/installation/).
Use a normal user account. A stable Python 3.15 release is required; the checkout
selects Python 3.15.2, matching CI, and uv can install it for you.

```sh
git clone https://github.com/EchterAlsFake/Porn_Fetch.git
cd Porn_Fetch
uv sync --upgrade --extra gui --group dev
uv run --no-sync python scripts/patch_qtasyncio.py .venv
uv run --no-sync python main.py
```

For the headless CLI, no Qt packages or QtAsyncio patch are needed:

```sh
uv sync --upgrade
uv run --no-sync python Porn_Fetch_CLI.py
```

`--upgrade` resolves the newest packages allowed by `pyproject.toml`. The locally
created `uv.lock` is not a release input. After syncing, use `--no-sync` during a
build so a later command does not replace patched packages. Repeat the QtAsyncio
patch after upgrading PySide6. If an update breaks a build, keep its log and
report the installed package versions (`uv pip freeze`).

For source runs, put FFmpeg on `PATH`, or build it as described below. To add
PocketBase, run:

```sh
uv run --no-sync python scripts/fetch_pocketbase.py --dest third_party
```

## Desktop build tools

Build on the same operating system and CPU architecture as the intended app.
The shared desktop builder supports Linux, Windows and macOS on x64 and ARM64.
It does not cross-compile. Python and all native libraries must use the same CPU.

### Linux

On Ubuntu/Debian:

```sh
sudo apt-get update
sudo apt-get install -y build-essential cmake git curl pkg-config zlib1g-dev \
  libssl-dev libegl1 libgles2 libxkbcommon-x11-0 libdbus-1-3 libxcb-cursor0 \
  libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 \
  libxcb-xinerama0 libxcb-xkb1
```

On Arch Linux:

```sh
sudo pacman -S --needed base-devel cmake git curl pkgconf zlib mesa libxkbcommon-x11 libxcb
```

On Fedora:

```sh
sudo dnf install gcc gcc-c++ make cmake git curl pkgconf-pkg-config zlib-devel \
  openssl-devel mesa-libEGL libxkbcommon-x11 xcb-util-cursor xcb-util-wm \
  xcb-util-image xcb-util-keysyms xcb-util-renderutil
```

The PySide6 wheel supplies Qt. You do not need Qt 5 development packages.
Linux ARM64 builds that bundle Tor also need libevent, OpenSSL and zlib development
packages; on Ubuntu add `libevent-dev libssl-dev zlib1g-dev`.

### macOS

Install Xcode Command Line Tools (`xcode-select --install`), Git, CMake and GNU
make. With Homebrew, use `brew install git cmake make pkg-config lz4`.
LZ4 is a build prerequisite for Python wheels linked to Homebrew's native library;
packaging copies it into the app so end users do not need Homebrew.
Finish any Xcode license or first-launch prompts before building.

### Windows

Use native x64 or ARM64 Python through uv. Install Git for Windows and a C/C++
compiler supported by Nuitka. Visual Studio Build Tools with **Desktop development
with C++** is one option. The convenience script installs these prerequisites
automatically, including the Windows SDK.

The Windows convenience script below installs MSYS2 and its FFmpeg Clang
toolchain automatically. For a manual build, install [MSYS2](https://www.msys2.org/).
In its shell:

```sh
pacman -Syu
pacman -S --needed make diffutils pkgconf mingw-w64-clang-x86_64-toolchain mingw-w64-clang-x86_64-zlib
```

For Windows ARM64, use CLANGARM64 and replace `x86_64` with `aarch64` in those
package names. Restart the MSYS2 shell if its update asks you to, then finish
the update. Run the Porn Fetch build from PowerShell, not WSL.

## Compile the desktop GUI

From the repository root:

```sh
uv python install 3.15.2
uv sync --python 3.15.2 --upgrade --extra gui --extra build --extra desktop-build
uv run --no-sync python scripts/build_desktop.py
```

The convenience installers select the same Python version explicitly when syncing,
so an old `.venv` cannot keep using a Python 3.15 alpha. If the installed uv cannot
install 3.15.2, the installers update uv and retry once; its Python download catalog
is bundled with each uv release. The builder checks the
interpreter and imports `curl_cffi` before downloading or compiling helpers.
Early Python 3.15 alphas cannot load current `abi3t` native extensions; this can
appear as `ModuleNotFoundError: curl_cffi._wrapper`. Update the checkout and rerun
the installer. To repair that environment directly:

```sh
uv python install 3.15.2
uv sync --python 3.15.2 --upgrade --reinstall-package curl-cffi --extra gui --extra build --extra desktop-build
uv run --no-sync python scripts/build_desktop.py
```

On Windows, pass the MSYS2 installation path:

```powershell
uv run --no-sync python scripts/build_desktop.py --msys2-root C:/msys64
```

The builder patches QtAsyncio, builds resources, scans QML imports, compiles with
Nuitka, adds helper programs and license files, and runs an offline startup check.
It keeps the whole application folder. Default output:

- Linux/Windows: `dist/local-gui/`
- macOS: `dist/local-gui/Porn Fetch.app`

Local macOS notices are in `Contents/Resources/LEGAL/` and `LEGAL.zip`, before
the final ad-hoc signature is created. Their distribution directories can have
dotted names such as `boolean.py`, which codesign rejects under `Contents/MacOS`.

Run `Porn Fetch` or `Porn Fetch.exe` inside that folder, or open the macOS app.
An offscreen check on Linux/Windows does not replace testing your real desktop.
The macOS check uses Cocoa.

Existing output is never overwritten. Move the old build or choose a new path:

```sh
uv run --no-sync python scripts/build_desktop.py --output dist/my-gui
```

On macOS, the output name must end in `.app`. Other useful options:

- `--without-ffmpeg`: use FFmpeg from `PATH` instead of bundling it.
- `--without-pocketbase`: omit the bundled history/statistics server.
- `--without-tor`: omit managed Tor. Use a fresh checkout without a staged
  `src/shared/tor` folder for this option.

All build scripts always display full command output and build/patch diagnostics.
The old `--verbose` flag remains accepted for compatibility; no flag or environment
setting is needed to see output. Dependency installation, FFmpeg and GUI compilation
stream output while retaining logs in the system temporary directory. Compiler
logs use `porn-fetch-build-logs`; each step prints its log path. Silent compiler
steps report that they are still running every 60 seconds.

Interactive GUI builds preserve a terminal connection for Nuitka, so its native
module/C-compilation progress bars stay active while output is logged. Windows
uses ConPTY through the `desktop-build` extra's pywinpty dependency; Unix uses a
pseudo-terminal. Captured/noninteractive builds retain streaming text logs.
Nuitka does not provide percentage progress during final C linking/LTO; that
stage still reports the 60-second heartbeat when otherwise silent.

The convenience scripts use this same builder:

```sh
bash scripts/install.sh
```

```powershell
./scripts/install_windows.ps1 -Msys2Root C:/msys64
```

The Unix script installs the listed build dependencies and may ask for sudo.
It never starts a full Linux system upgrade. On Arch it uses `pacman -S --needed`
without refreshing package databases. On macOS it installs the required Homebrew
formulae with automatic updates and installed-formula upgrades disabled
([Homebrew options](https://docs.brew.sh/Manpage)).

The Windows script installs missing Git for Windows with `winget`, refreshes PATH and continues in
the same terminal. If winget is unavailable, install Microsoft's App Installer
or Git for Windows and rerun it. Unless `-WithoutFFmpeg` is set, the Windows script
also installs missing MSYS2 under `-Msys2Root` (default `C:\msys64`), finishes its
core/system updates in fresh processes and installs make, diffutils, pkgconf,
the Clang toolchain and zlib. It selects CLANG64 or CLANGARM64 from the actual
Python architecture and checks the tools before building FFmpeg. Before syncing
Python dependencies, it checks for Microsoft C++ tools and a Windows SDK using
vswhere. Missing tools are installed with the Visual Studio 2022 Build Tools C++
workload, including ARM64 components when needed. An incomplete Build Tools
installation is modified to add the workload. If Windows needs a restart, the
script reports that requirement without restarting the machine automatically.
The FFmpeg builder reads the zlib notice directly from the selected MSYS2 Clang
prefix; MSYS2 tools do not need to be on PowerShell's global PATH. Its post-build
output names the executable being verified and the notice being collected.
Both scripts use the current
checkout when available. They do not switch tags or overwrite local source changes.
When the Windows script needs a new checkout, it clones into `Porn_Fetch` under
your user profile, even if PowerShell starts in `C:\Windows\System32`.
The Windows script saves its console transcript under
`%TEMP%\porn-fetch-build-logs\install-windows-*.log`, prints the full error and
waits for Enter on an interactive failure. Use `-NoPause` for unattended runs.
The uv installer runs in a child PowerShell process so its failure cannot close
the terminal running the README's `irm ... | iex` command.

On Windows and macOS, application and provider debug logs are stored in the shared
user data folder's `logs` directory. Normally this is
`%LOCALAPPDATA%\EchterAlsFake\Porn Fetch\logs` on Windows and
`~/Library/Application Support/Porn Fetch/logs` on macOS. Startup does not need
write access to the executable's folder or the current working directory for
logging. Build smoke tests keep their logs in a disposable directory.

## Compile the CLI

```sh
uv sync --upgrade --extra build
uv run --no-sync python scripts/build_desktop.py --target cli
```

On Windows add `--msys2-root C:/msys64`, or `--without-ffmpeg` if you use a system
FFmpeg. The result is in `dist/local-cli/`. Keep its `third_party` and `LEGAL`
folders if you copy the binary. The CLI itself has no Qt dependency.

For a bare PyInstaller binary without preparing helper programs:

```sh
uv run --no-sync pyinstaller --clean packaging/pyinstaller_cli.spec
```

This writes `dist/Porn_Fetch_CLI` (`.exe` on Windows). It is a local build, not an
official release update target. Do not publish it through the production updater.

## FFmpeg

The desktop builder compiles a small LGPL-only FFmpeg. Its source version and
SHA-256 are in `packaging/build_ffmpeg.py`; features are in
`packaging/ffmpeg_configure_flags.txt`. Changing the version requires updating the
hash and checking the build. Do not replace it with an arbitrary GPL/nonfree bundle.

It supports local MPEG-TS/MP4 remuxing, MP4 metadata and attached pictures. It does
not encode video, download streams or provide general transcoding.

To build just FFmpeg:

```sh
uv run --no-sync python packaging/build_ffmpeg.py --dest third_party
```

On Windows add `--msys2-root C:/msys64`. Other options are `--jobs`, `--work-dir`
and `--source-archive`. Keep `ffmpeg-legal/` with the executable when distributing
it: this contains the matching source, notices and build information.

## Problems

- **Missing Qt plugin or DLL:** copy the complete output folder. Do not copy only
  the `.exe`. Rebuild after changing Python or PySide6.
- **Old build output:** move it before retrying. In particular,
  `deployment/deploy_main.dist` must not be reused as a new Windows build.
- **QtAsyncio patch fails:** keep the failure visible. Report the PySide6 version
  and patch log; do not continue with a partly patched runtime.
- **macOS missing library or framework:** rebuild with
  `packaging/repair_macos_bundle.py` in the same environment used for that build,
  then repeat signing and `--smoke-test`. The release must include its native
  dependencies so users do not need Homebrew libraries to launch it.
- **Antivirus or Gatekeeper warning:** see the signature section above.

Include your OS, CPU, source commit, command and build log in a bug report.
