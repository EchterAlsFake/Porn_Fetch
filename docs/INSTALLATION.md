# Installing the current 3.9 source and first beta

> [!CAUTION]
> **This guide is for the 3.9 source tree and its planned first beta.** The
> latest published 3.8 binary is an older GPL release with a different app and
> install process. These instructions do not describe it. I am still working
> through the 3.9 rewrite, and beta builds can have errors. Please report what
> happened, your OS, the artifact name, and the beta version or commit ID.

## Get the right file

When the first beta is published, get its files from the
[GitHub Releases page](https://github.com/EchterAlsFake/Porn_Fetch/releases/).
Read the beta release notes and use only a file listed there. The current build
workflow targets Windows, Linux, and macOS GUI and CLI artifacts. Availability
of a target in that workflow does not mean that I have manually verified it or
that it will be included in the first beta.

The GUI opens an app window. The CLI runs in a terminal and does not need Qt.
Choose the file matching your operating system and CPU architecture (`x64` or
`arm64`, where offered). Windows GUI currently targets x64; Windows CLI targets x64 and ARM64. The current workflow has no
Android GUI APK or iOS artifact. The CLI can also be run from source on Termux.

### Standalone beta build

If the release asset is a standalone `.exe` or `.bin`, download its matching
`PornFetch_<platform>_GUI_<architecture>.zip` bundle and extract it into a
folder you can write to. The bundle keeps the matching `pocketbase` or
`pocketbase.exe` beside the app; download tracking needs it. Keep the matching
legal notices archive from the same release as well. On Linux, make the `.bin`
and `pocketbase` executable first:

```bash
chmod +x PornFetch_linux_GUI_x64.bin
chmod +x pocketbase
./PornFetch_linux_GUI_x64.bin
```

Use the exact filename from the release page if yours differs. A standalone
build does not include the Qt Maintenance Tool, so update it by downloading
the next beta build. Follow its release notes before replacing any files.

On macOS, the current workflow creates architecture specific DMGs and a
universal DMG. Open the DMG and drag the app to Applications. The macOS build
is currently ad hoc signed; if the operating system blocks it, report the
message you see. Do not assume it has been notarized.

### Qt Installer Framework build

If the release asset is explicitly named as an installer, run it and follow
its prompts. A Qt Installer Framework installation places a maintenance tool
beside the app. That tool can install later updates from the repository
configured in the installer. CI now builds installers for Windows x64, Linux
x64, and macOS x64/ARM64, but they still need manual install and update testing
and a deployed repository before beta distribution. See
[the maintainer guide](QT_INSTALLER_FRAMEWORK.md) for the current status. Do
not expect automatic updates from a standalone GUI binary or DMG.

On Linux, make a downloaded `*_Setup.run` installer executable with `chmod +x`
before running it. On macOS, the standalone app DMG and the `*_Setup.dmg`
installer are different release assets; choose the one named in the beta
release notes.

### Standalone CLI updates

The current 3.9 standalone CLI can check the signed update repository with
`self-update --check` and install a newer build with `self-update` (add `--yes`
to skip the confirmation prompt). Run the command from the CLI executable you
want to update and close other copies before installing. If the CLI came from
a source checkout or package manager, update it with that method instead.
See the [CLI update guide](CLI_UPDATES.md) for supported architectures and
what to do if an update fails.

## Get and import the beta license

The beta uses the actual license import and validation flow. To get a test
license, visit [pornfetch.to](https://pornfetch.to/) and press the
**sandbox purchase** button. Follow the site's instructions to obtain the
license file. **This is not a real transaction. No money is processed. You do
not need to send cryptocurrency or pay a fee; pressing the button is the test.**
The purpose is to exercise the license checkout and activation flow before a
real product exists.

In the desktop app, open Settings, choose **Import License File**, and select
the file you received. In the CLI, open **License Management**, choose
**Import License Key / File**, and enter the file path. The app verifies the
license against the licensing service, so an initial connection is needed.
If the site does not give you a file or activation fails, include the error
message in a bug report. Do not post your license file publicly.

The license unlocks the beta's gated features, including quality above 720p
and parallel downloads. It is a test credential, not evidence of a purchase.

## Verify a download

The build workflow produces a `.sha256` file for each main artifact. Download
it alongside the artifact and compare the recorded hash with your local file.
For example, on Linux:

```bash
sha256sum PornFetch_linux_GUI_x64.bin
cat PornFetch_linux_GUI_x64.bin.sha256
```

The values must match. A checksum catches accidental corruption; it does not
by itself prove who published a file. The current workflow does not generate
the `.sig` files described in older guides.

## Getting help

Open a [GitHub issue](https://github.com/EchterAlsFake/Porn_Fetch/issues) with
the OS and version, artifact filename, steps you took, and the full error
message. Please mention whether you used a standalone build, a Qt installer,
or a source run. I am actively working on the rewrite and beta feedback is
especially useful while the install and update process is being finished.
