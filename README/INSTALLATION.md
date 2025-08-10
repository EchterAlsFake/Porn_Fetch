# Porn Fetch — Simple Install Guide

**Download the latest release:** https://github.com/EchterAlsFake/Porn_Fetch/releases/

> [!NOTE]
> **Read this first (1 minute):**
> 1. Choose **GUI** (app window) unless you specifically want the **CLI** (terminal-only).
> 2. Pick the right **file/architecture** (see below).
> 3. Decide between **Install** (adds an app shortcut) or **Portable** (runs from the download folder).

---

## Table of contents
- [Quick download picker](#quick-download-picker)
- [GUI vs CLI](#gui-vs-cli)
- [Which file do I need? (x64 / x86 / ARM)](#which-file-do-i-need-x64--x86--arm)
- [Install vs Portable](#install-vs-portable)
- [Updating Porn Fetch](#updating-porn-fetch)
- [Windows](#windows)
- [Linux](#linux)
- [macOS](#macos)
- [Android](#android)
- [Verifying the download (GPG signature)](#verifying-the-download-gpg-signature)
- [Torrent download](#torrent-download)
- [FAQ](#faq)
- [Need help?](#need-help)

---

## Quick download picker

| Platform | File to download | Then do this |
|---|---|---|
| **Windows (64‑bit)** | `PornFetch_Windows_GUI_x64.exe` | Double‑click → choose **Install** or **Portable**. |
| **Linux (64‑bit)** | `PornFetch_Linux_GUI_x64.bin` | Make executable → run → choose **Install** or **Portable**. |
| **macOS** | `PornFetch_macOS_x86-64.dmg` | Open DMG → drag **Porn Fetch** to **Applications** → run (may need Rosetta). |
| **Android** | `pornfetch-…-arm64-v8a-debug.apk` (start with this) | Install APK (allow unknown apps). If incompatible, try `armeabi-v7a`, then `x86_64`. |

> [!TIP]
> If you're unsure which one to pick, choose **GUI** and **x64** for desktop. On phones, try **arm64‑v8a (aarch64)** first.

---

## GUI vs CLI

- **GUI (Graphical User Interface):** The full app with windows/buttons. This is what most people want.  
- **CLI (Command Line Interface):** Runs in a terminal. For advanced users, scripting, servers, or tools like Termux/iSH.

---

## Which file do I need? (x64 / x86 / ARM)

- **x64 (aka 64‑bit):** Almost every modern Windows/Linux/macOS computer.  
- **x86 / x32 (aka 32‑bit):** Only very old PCs or 32‑bit OS installs.  
- **ARM / aarch64:** Most phones/tablets; Apple Silicon Macs (M1/M2/M3) are ARM **but** this app currently ships as **Intel (x64)** and runs via **Rosetta** on macOS.

**How to check quickly**  
- **Windows:** *Settings → System → About → System type*. If it says **64‑bit**, pick **x64**.  
- **macOS:**  → *About This Mac* → *Chip*. If you see **Apple M‑series**, you’re on Apple Silicon. Install Rosetta when prompted.  
- **Linux:** Run `uname -m` in a terminal. `x86_64` = x64; `i686`/`i386` = x86; `aarch64` = ARM.  
- **Android:** Almost always **arm64‑v8a (aarch64)**.

> [!IMPORTANT]
> **macOS (Apple Silicon)**
> Porn Fetch is built as **x86_64 (Intel)**. On M‑series Macs it should run under **Rosetta** (Apple’s translator). If it doesn’t start or you see issues, please open a GitHub issue with details. The macOS build is tested via virtualization.

---

## Install vs Portable

When you first launch Porn Fetch, you'll choose one of two modes:

- **Install:** Adds a proper app entry/shortcut so you can search for “Porn Fetch” (or a custom app name you choose).  
- **Portable:** Keeps everything in the download folder. Double‑click the executable to run. Great for USB sticks, separate folders, or keeping multiple versions.

Both modes work the same. Pick whatever you prefer.

---

## Updating Porn Fetch

Porn Fetch checks for updates on startup and shows a link if a new version is available.

- **Installed mode:** Installing a new version **overwrites the app and your `config.ini`** (settings reset to defaults).  
- **Portable mode:** Your `config.ini` is next to the executable. Replacing the old executable keeps your config file as long as you don’t delete it.

**Tip:** Back up your `config.ini` before updating if you want to keep your settings.

---

## Windows

1. Download **`PornFetch_Windows_GUI_x64.exe`** from the [Releases](https://github.com/EchterAlsFake/Porn_Fetch/releases/).  
2. Double‑click it and choose **Install** (or **Portable**).

> [!NOTE]
> **SmartScreen / “unknown publisher” prompts:** Click **More info → Run anyway** if you downloaded the file from the official releases page.

---

## Linux

1. Download **`PornFetch_Linux_GUI_x64.bin`**.  
2. Make it executable:  
   - File manager: Right‑click → **Properties** → **Permissions** → “Allow executing file as program”  
   - **Or** in a terminal in the download folder:  
     ```bash
     chmod +x PornFetch_Linux_GUI_x64.bin
     ```
3. Run it (double‑click or):  
   ```bash
   ./PornFetch_Linux_GUI_x64.bin
   ```
4. Choose **Install** or **Portable**.  

> [!NOTE]
> Porn Fetch uses **Qt**. Most distros have the needed runtimes. If it fails to start, your package manager may need to install Qt runtime packages. If it prints errors and exits, please open a GitHub issue and include the terminal output and your distro/version.

---

## macOS

1. Download **`PornFetch_macOS_x86-64.dmg`**.  
2. Open the DMG and drag **Porn Fetch** into **Applications**.  
3. Launch from Launchpad (search “Porn Fetch”).  
4. If asked to install **Rosetta**, click **Install** (this lets Intel apps run on Apple Silicon).

> [!TIP]
> If macOS blocks the app: Right‑click the app in **Applications** → **Open** → **Open** (bypasses Gatekeeper once).

---

## Android

There are three APK builds for different CPU types:
- **arm64‑v8a (aarch64):** `pornfetch-*-arm64-v8a-debug.apk` *(try this one first)*  
- **armeabi‑v7a (armv7‑a):** `pornfetch-*-armeabi-v7a-debug.apk`  
- **x86_64:** `pornfetch-*-x86_64-debug.apk`

1. Download an APK (start with **arm64‑v8a**).  
2. Install it (allow “Install unknown apps” if prompted).  
3. If you get “not compatible”, try the other two builds.

**Output folder (important):** Videos are saved to  
```
/storage/emulated/0/Download
```
—that’s your **Download** directory. If you don’t see videos there, the download failed.

> [!NOTE]
> Advanced users can run the **CLI** in **Termux** on Android.

---

## Verifying the download (GPG signature)

If you’re in a censored environment or want to be extra safe, verify the release files with GPG.

Every release asset has a matching `.sig` file, e.g.  
- `PornFetch_Windows_GUI_x64.exe` **and** `PornFetch_Windows_GUI_x64.exe.sig`

**Example (Linux GUI file):**
```bash
gpg --verify PornFetch_Linux_GUI_x64.bin.sig PornFetch_Linux_GUI_x64.bin
```

It should report a **good signature**. If it says it can’t verify the signer, import and trust the public key:

- Public key: https://github.com/EchterAlsFake/EchterAlsFake/blob/main/public-key.asc

> [!NOTE]
> You need `gpg` installed on your system to verify signatures.

---

## Torrent download

A torrent is a peer‑to‑peer (P2P) way of distributing files. If you prefer it:
1. Install a torrent client such as **qBittorrent**.  
2. Open the `.torrent` file or paste the magnet link from the release.  
3. Wait for **seeds** (people who already have 100% of the file). The project maintainer seeds most days for several hours; sometimes other seeds will appear too.

---

## FAQ

**What’s the difference between x64 and ARM?**  
- **x64** is the standard for modern desktops/laptops.  
- **ARM** is common in phones/tablets and Apple Silicon Macs. On macOS, Porn Fetch runs as an **Intel (x64)** app via **Rosetta** on Apple Silicon.

**Where are Android downloads saved?**  
- `~/Download` on your device, i.e. `/storage/emulated/0/Download`.

**Do I have to install Porn Fetch?**  
- No. **Portable** mode runs directly from the file you downloaded.

**Will updating erase my settings?**  
Yes, always.

---

## Need help?

- **Releases & downloads:** https://github.com/EchterAlsFake/Porn_Fetch/releases/  
- **Open an issue (include OS, version, and any terminal output):** https://github.com/EchterAlsFake/Porn_Fetch/issues