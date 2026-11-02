# Windows code signing

Windows release builds (GUI and CLI, x64 and ARM64) and manually dispatched
translation previews use the GitHub Environment `signing`. Other desktop matrix
jobs use the environment `build`, which needs no secrets. PR validation never
accesses the signing environment.

The `signing` environment must contain:

- `CERTUM_EMAIL`: the Certum SimplySign account email.
- `CERTUM_OTP`: the long-lived base32 TOTP seed from SimplySign enrollment, or its
  `otpauth://` URI. This must be the seed, not a current six-digit token.

The build uses [ssign v0.1.8](https://github.com/Le-Syl21/ssign/releases/tag/v0.1.8),
with a pinned download SHA256. The x64 tool also runs on Windows 11 ARM64 through
emulation. Credentials are supplied through step environment variables. Its
short-lived session is stored under the runner's temporary directory, excluded
from artifacts and caches, and removed in an `always()` cleanup step. Parallel
jobs retry failed logins in a new OTP window because Certum tokens are single use.

`packaging/sign_windows.ps1` signs unsigned `.exe`, `.dll` and `.pyd` files,
requests an RFC3161 timestamp from Certum and checks the result with Windows
Authenticode verification. Existing valid vendor signatures are preserved.
Kernel drivers (`.sys`) must already have a valid vendor signature; the
individual certificate cannot replace Microsoft's driver signing process.
Invalid dependency signatures, missing secrets or timestamp/signing failures
fail the job. The Qt maintenance base and completed setup are explicitly
re-signed; `binarycreator` can invalidate an inherited Qt template signature.

Signing order:

1. GUI helper programs (FFmpeg, PocketBase and Tor) are signed before bundling.
   The complete Nuitka distribution is then signed before creating its ZIP.
2. The CLI's PyInstaller spec copies native dependencies to a private build
   directory and signs those copies before creating the onefile executable.
   UPX is disabled on Windows to preserve their signatures. The final CLI EXE
   and the separately distributed PocketBase EXE are also signed.
3. The Windows Qt installer receives already signed application components.
   Its completed setup EXE is signed after `binarycreator` finishes.
4. Checksums and update repository metadata describe the signed bytes.

## Qt maintenance and uninstall tool

The existing IFW installer target is Windows x64; Windows ARM64 receives the
portable GUI ZIP. The x64 build copies IFW's `installerbase.exe`, signs it with
the Certum certificate even when the source has a valid Qt vendor signature,
and passes it as `--maintenance-tool` to `packaging/generate_repository.py`.

The signed executable is shipped in a mandatory, virtual, essential component
`to.pornfetch.echteralsfake.maintenance`. Its script calls
`installer.setInstallerBaseBinary()` during installation and component updates.
IFW installs this binary unchanged as `maintenancetool.exe`, keeping mutable
configuration in separate data files. The maintenance component shares the app's
release version/date and is included in the existing TUF repository manifest.
This follows Qt's documented
[maintenance component procedure](https://doc.qt.io/qtinstallerframework/ifw-updates.html#populating-the-maintenance-tool-component).

The Windows workflow performs an unattended installation in the runner's
temporary directory, verifies the resulting maintenance tool's signature and
exact SHA256 against the signed base, then uninstalls it before publishing the
installer artifacts. Signing only the setup EXE would leave the generated
maintenance tool without the application publisher's signature.

Local source builds remain possible without cloud credentials; CLI payload
signing is enabled only by `PORN_FETCH_WINDOWS_SIGNING=1`, and the maintenance
component is added only when `--maintenance-tool` is supplied.
