# Installation & Build Guide

> [!CAUTION]
> **This guide is for the 3.9 source tree and the upcoming 3.9 beta.**
> The published 3.8 download is an older GPL release with a different architecture,
> UI, and installation process. I'm actively rewriting 3.9, so if you run into any
> issues, please report them on GitHub along with your OS, the artifact name, and the commit ID or version.

You can run Porn Fetch in three ways depending on what you want:
1. **Pre-built binaries and installers** (fastest if you just want to run it)
2. **Automated install scripts** (builds from source for your system automatically)
3. **Manual source build** (recommended for development and tweaking)

---

## 1. Pre-built Binaries & Installers

Pre-built binaries for Windows, Linux, and macOS are available on the [GitHub Releases](https://github.com/EchterAlsFake/Porn_Fetch/releases) page.

### Which version do you need?
- **GUI (Desktop App):** Offers the full graphical interface built with PySide6/QML.
- **CLI (Terminal):** Headless, lightweight command-line interface with interactive menus (Questionary/Rich). Requires no Qt libraries or display server.

### Types of Release Packages

#### A. Qt Installer Framework (`*_Setup` packages)
- **Windows:** `PornFetch_windows_GUI_x64_Setup.exe`
- **Linux:** `PornFetch_linux_GUI_x64_Setup.run`
- **macOS:** `PornFetch_macos_GUI_x64_Setup.dmg` / `PornFetch_macos_GUI_arm64_Setup.dmg`

These installers set up the application and bundle the Qt `maintenancetool`, which lets you check for and apply updates directly from the official repository.

*Note for Linux:* Make the downloaded `.run` installer executable before launching:
```bash
chmod +x PornFetch_linux_GUI_x64_Setup.run
./PornFetch_linux_GUI_x64_Setup.run
```

*Note for macOS:* The macOS builds are currently ad-hoc signed. If macOS Gatekeeper warns you about an unidentified developer, right-click the app (or installer) and select **Open**, or allow it under **System Settings > Privacy & Security**.

#### B. Standalone Portable Bundles (`.zip` / `.dmg`)
If you prefer not to install anything into system directories, grab the portable ZIP bundle:
- Extract the archive to any folder where your user account has write permissions.
- **Important:** Ensure the `pocketbase` (or `pocketbase.exe`) executable remains right next to the main app binary. Porn Fetch needs PocketBase for persistent download queues, statistics, and history tracking.
- On Linux, ensure both files are executable:
  ```bash
  chmod +x PornFetch_linux_GUI_x64.bin pocketbase
  ./PornFetch_linux_GUI_x64.bin
  ```

#### C. Standalone CLI Executables
- Single portable binary (e.g. `PornFetch_linux_CLI_x64` or `PornFetch_windows_CLI_x64.exe`).
- Includes a built-in cryptographically verified updater:
  ```bash
  # Check for updates
  ./PornFetch_linux_CLI_x64 self-update --check

  # Apply update
  ./PornFetch_linux_CLI_x64 self-update
  ```

---

## 2. Automated Install & Build Scripts

If you want to build and run the latest code without manually configuring Python or cloning repositories, run the setup script:

### Linux & macOS
```bash
curl -sSL https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/scripts/install.sh | bash
```
Or from an existing clone:
```bash
bash scripts/install.sh
```
*What it does:* Detects your package manager (apt, pacman, dnf, zypper, brew), installs required build dependencies, sets up `uv` and Python 3.14, downloads the matching PocketBase binary, applies the QtAsyncio patch, and builds or starts the app.

### Windows (PowerShell)
Open PowerShell as **Administrator** and run:
```powershell
irm https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/scripts/install_windows.ps1 | iex
```
*What it does:* Checks prerequisites, installs `uv`, configures the Python 3.14 environment, fetches PocketBase, and compiles the Windows binary using `pyside6-deploy`.

---

## 3. Building & Running from Source

Porn Fetch targets Python 3.14 and uses [`uv`](https://docs.astral.sh/uv/) for fast, deterministic dependency management.

### Prerequisites

1. **Git:** To clone the repo.
2. **uv:** If you don't have `uv` installed yet:
   - **Linux / macOS:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - **Windows:** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (or `winget install --id=astral-sh.uv`)
3. **System libraries (Linux GUI only):**
   PySide6 requires basic graphics and window system libraries.
   - **Debian / Ubuntu:**
     ```bash
     sudo apt-get update && sudo apt-get install -y \
       build-essential cmake python3-dev libssl-dev libgl1 libegl1 \
       libxkbcommon-x11-0 libdbus-1-3 git curl
     ```
   - **Arch Linux:**
     ```bash
     sudo pacman -S --needed base-devel git cmake curl qt6-base
     ```
   - **Fedora:**
     ```bash
     sudo dnf install -y gcc gcc-c++ make cmake git curl mesa-libGL mesa-libEGL
     ```
   - **macOS:** Install Xcode Command Line Tools:
     ```bash
     xcode-select --install
     ```

### Step-by-Step Build Instructions

#### Step 1: Clone the repository
```bash
git clone https://github.com/EchterAlsFake/Porn_Fetch.git
cd Porn_Fetch
```

#### Step 2: Install Python dependencies
`uv` will automatically fetch and manage Python 3.14 for you.

- **To run both Desktop GUI and CLI:**
  ```bash
  uv sync --extra gui
  ```

- **For developers (includes test runners, linter, type checker):**
  ```bash
  uv sync --extra gui --group dev
  ```

- **Headless CLI only (no GUI / no Qt dependencies):**
  ```bash
  uv sync
  ```

- **(Optional) PyAV hardware media processing:**
  ```bash
  uv sync --extra gui --extra av --group dev
  ```

#### Step 3: Download PocketBase
Porn Fetch uses an embedded PocketBase server for persistent download management and statistics. Download the matching binary for your platform into the project root:
```bash
uv run python scripts/fetch_pocketbase.py
```
This automatically detects your OS and architecture and places `pocketbase` (or `pocketbase.exe`) in the current folder.

#### Step 4: Patch QtAsyncio (Desktop GUI on Python 3.14)
Python 3.14 + PySide6 requires an event loop descriptor patch for non-blocking networking and async task cancellation. Run this once after syncing:
```bash
uv run python scripts/patch_qtasyncio.py .venv
```
*(Skip this step if you're only using the headless CLI).*

#### Step 5: Launch the Application
- **Run Desktop GUI:**
  ```bash
  uv run main.py
  ```
- **Run Headless CLI:**
  ```bash
  uv run Porn_Fetch_CLI.py
  ```
  Or using the installed script alias:
  ```bash
  uv run porn-fetch-cli
  ```

---

## 4. Compiling Standalone Executables from Source

If you want to package the app into a standalone distributable binary:

### Compile the CLI binary
Uses PyInstaller to generate a single-file executable:
```bash
uv run pyinstaller --clean packaging/pyinstaller_cli.spec
```
The output binary is placed in `dist/`.

### Compile the GUI application
Uses `pyside6-deploy`:
```bash
# Linux
uv run pyside6-deploy -c packaging/pysidedeploy_linux.spec

# Windows
uv run pyside6-deploy -c packaging/pysidedeploy_windows.spec

# macOS
uv run pyside6-deploy -c packaging/pysidedeploy_macos.spec
```

---

## 5. Android / Termux (CLI Only)

The CLI has no PySide6/Qt dependencies and runs cleanly inside [Termux](https://termux.dev/) on Android:

```bash
# In Termux:
pkg update
pkg install python git clang
git clone https://github.com/EchterAlsFake/Porn_Fetch.git
cd Porn_Fetch
pip install -e .
python Porn_Fetch_CLI.py
```

---

## 6. Verifying Download Checksums

Official release builds come with a `.sha256` checksum file. To verify integrity:

- **Linux / macOS:**
  ```bash
  sha256sum -c PornFetch_linux_GUI_x64.bin.sha256
  ```
- **Windows (PowerShell):**
  ```powershell
  Get-FileHash PornFetch_windows_GUI_x64.zip -Algorithm SHA256
  ```
  Compare the resulting hash with the content of `PornFetch_windows_GUI_x64.zip.sha256`.

---

## 7. License & Premium Features

- The core downloader and features work without a license.
- A commercial policy license from [pornfetch.to](https://pornfetch.to/) unlocks 1080p+ resolutions and concurrent downloads.
- **GUI:** Click **Purchase / renew license** or **Import License File**.
- **CLI:** Open **License Management** and paste your key or JSON license file.
- Licenses remain valid offline for up to 7 days before needing a re-check.

---

## Need Help?

If anything fails during building or installation:
1. Check the [FAQ](FAQ.md) and [Known Antivirus Flags](ANTIVIRUS_FLAGS.md).
2. Open an issue on [GitHub Issues](https://github.com/EchterAlsFake/Porn_Fetch/issues). Please include your operating system, CPU architecture, whether you used pre-built binaries or built from source, and the terminal output or log error.
