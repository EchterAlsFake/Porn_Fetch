# Commercial licensing implementation audit — 6 October 2026

## Outcome

Implemented the client flow and offline regression coverage. This is not a claim
that the packaged application or payment system is commercially ready. Existing
uncommitted work was preserved. No production machine/license was created, deleted,
suspended, renewed, or migrated by this task. The implementation audit preceded the requested Git commit; no production deployment was performed.

The later operator handoff superseded the initial requested policy:
`7038281b-2429-4aa4-81db-4f04a87e7184` is commercial;
`564897fa-b8d9-4871-82a4-0b49fd50bc1e` is beta and is rejected locally.
The other supplied production values match exactly, and the URL is now explicitly
included in `production.json`. Tests compare the bundled Qt configuration to that file.

## Files changed by this task

The following list excludes unrelated modifications that already existed when the
task started. Some listed files also had existing user edits, which were preserved.

| Area | Files |
| --- | --- |
| Licensing | `src/licensing/client.py`, `service.py`, `production.json`; new `transport.py` |
| Shared state/builds | `src/shared/paths.py`, `version.py`; new `release.py` |
| Qt adapters/application | `src/backend/license_bridge.py`, `update_service.py`, `application.py` |
| CLI | `src/cli/self_update.py`, `update_build.json`, `flows/settings.py`, `flows/ui.py` |
| QML | `src/frontend/UI/LicenseWidget.qml`, `AndroidSettingsPage.qml`, `SettingsPage.qml`, `Main.qml` |
| Embedded resources | `src/frontend/resources.qrc`, generated `src/frontend/UI/resources.py` |
| Generated translations | `src/frontend/translations/ts/{de_DE,en,fr,zh_CN}.ts`, `qm/{de_DE,zh_CN}.qm` |
| Packaging | `packaging/generate_repository.py`, `publish_cli_updates.py`, `write_cli_build_version.py`, `installer/packages/com.echteralsfake.pornfetch/meta/package.xml`; new `sign_desktop_release.py`, `write_build_version.py` |
| Release CI/deployment | `.github/workflows/build_all.yml`, `scripts/deploy_ifw_repositories.sh` |
| Existing tests/fixtures | `src/tests/unit/test_license_client.py`, `test_update_service.py`; `src/tests/integration/test_license_integration.py`; `src/tests/license_fixtures.py` |
| New tests/fixtures | `src/tests/unit/test_release_entitlement.py`, `test_licensing_paths.py`; `src/tests/integration/test_keygen_production_opt_in.py`; `src/tests/fixtures/keygen_ed25519_vector.json` |
| Documentation | `README.md`, `docs/CLI_UPDATES.md`, `FAQ.md`, `INSTALLATION.md`, `LICENSING.md`, `QT_INSTALLER_FRAMEWORK.md`, `STATUS.md`; new `LICENSING_ARCHITECTURE.md`, `LICENSING_AUDIT.md` |

## Bugs found and corrected

- Missing `/accounts/{account}` in licensing API paths.
- Premium provisionally unlocked before any successful online activation.
- Machine creation followed by checkout without validating again.
- Update expiry treated as subscription expiry, including rejecting signed permits
  for entitled old builds after the update year.
- The verifier required a null policy duration, incompatible with the commercial
  one-calendar-year policy.
- Permanent-key expiry was used as current renewal information. The new client
  requires the current signed machine checkout's entitlement end.
- Generic BaseCore HTTP handling discarded activation error codes. The specialized
  adapter preserves JSON:API responses and avoids scraper challenge handling/logging.
- Runtime scraper networking settings could influence license TLS/proxy behavior.
- No explicit bounded licensing request/connect deadlines.
- Non-JSON authentication denials and `NOT_FOUND` validation with null data could
  be treated as temporary outages. Those now deny access and remain sticky.
- Missing fresh process-start validation in the reusable client itself.
- Desktop QStandardPaths and CLI platformdirs could create separate installation IDs.
  Both now reuse the shared/legacy data resolver; Android retains private Qt storage.
- Generic local-state errors could leave the service's previous Premium status active.
- A long-running frontend could retain a cached allowed status after the grace deadline.
- Raw signed-key paste was missing; the CLI could stat a key as an oversized filename.
- Beta acquisition/"license expired" UI instructions did not describe the commercial model.
- Qt launched an unrestricted remote maintenance update without entitlement or artifact
  binding; CLI TUF metadata lacked entitlement release dates.
- Qt artifact build versions were not embedded for accurate newer-version comparisons.

## Implemented behavior

The client locally authenticates the original signed bytes and pinned identities,
loads a persistent random UUIDv4, validates, activates only for the three documented
unactivated-install responses, validates again, and verifies a signed seven-day
checkout before unlocking. Lost creation responses and duplicate fingerprints are
reconciled without blindly creating more machines. Server machine limits and
suspension/authentication denials produce separate, safe statuses.

The signed message format was confirmed against Keygen's public implementation and
the supplied deployed-server handoff. Deterministic tests cover signature and claims
tampering; a fixed OpenSSL-generated synthetic Keygen-format vector adds an independent
fixture. A local genuine beta license's signature was also verified with the production
public key, without printing or committing the credential. It was correctly identified
as beta. A live commercial-license verification remains an opt-in release check.

Grace starts only after successful validation and signed checkout. It lasts at most
seven days, never extends on failure, and requires a valid signed cache. Entitlement
is a separate inclusive comparison of the compiled release timestamp against the
signed update deadline. `valid=true, EXPIRED` remains usable for an entitled build.
Renewal refreshes the signed deadline using the same key and installation UUID.

CLI TUF metadata now includes the signed release timestamp, repeated in the hashed
bundle manifest. Qt uses signed release metadata with every repository file hash and
hands IFW a verified local repository. Unentitled or unauthenticated updates cannot
automatically replace the current installation. Both show renewal information.

The UUID lives in `licensing.sqlite3`:

- Windows: `%LOCALAPPDATA%\EchterAlsFake\Porn Fetch\licensing.sqlite3`.
- Linux: `${XDG_DATA_HOME:-~/.local/share}/Porn Fetch/licensing.sqlite3`.
- macOS: `~/Library/Application Support/Porn Fetch/licensing.sqlite3`.
- Android: private Qt `QStandardPaths.AppDataLocation/licensing.sqlite3`.
- Existing desktop Qt database paths are reused in place when present and no shared
  preferred database exists; exact legacy paths are in the architecture document.

The original old account/product/policy/key values are listed in
[LICENSING_ARCHITECTURE.md](LICENSING_ARCHITECTURE.md). Their production replacements
were already in the working tree before this task; the obsolete account remains
only for explicit rejection. No active `api.keygen.sh` or obsolete licensing hostname
was found. Synthetic fixture identities and TUF release trust keys were not replaced.

## Verification

- `uv run --no-sync python -m unittest discover -s src/tests/unit -p 'test_*.py' -q`:
  **149 tests passed**.
- `uv run --no-sync python -m unittest src.tests.integration.test_license_integration src.tests.integration.test_keygen_production_opt_in -q`:
  **11 passed, 1 skipped** (explicit live-server opt-in).
- Targeted Ruff checks on changed licensing, shared, updater, packaging and test modules:
  **passed**. The large application composition module has existing lint findings;
  it was not reformatted or cleaned up as unrelated work.
- Qt frontend resource/translation generation completed; the final resource module
  was rebuilt with `pyside6-rcc`.
- Deployment script `bash -n`: **passed**.

Tests cover the requested 23 scenarios and additional activation response loss,
malformed denial handling, null commercial expiry, migration, TLS isolation, paths,
long-running feature-gate expiry, updater signature/date/artifact binding, and denial
before installation. The wider unit suite emits some existing simulated-failure and
SQLite ResourceWarning diagnostics, but all tests pass.

## Remaining release blockers

1. Run the opt-in public check with an authorized, already activated commercial TEST
   credential/UUID. No such credential was provided here; the local file is beta.
2. Exercise actual packaged Windows/Linux/macOS maintenance-tool launches, update
   replacement, Android import/private storage, and OS artifact signing/notarization.
   Mocked updater tests do not substitute for those platform checks.
3. Publish the newly signed Qt/CLI repositories with the existing protected release
   targets key. Keep each release's approved timestamp immutable. Qt manifests expire
   in 30 days and need an operator refresh process; its root rotation currently needs
   an application update.
4. Complete the server's customer renewal selection UI and payment launch work from
   the handoff. NOWPayments is still sandboxed and Patreon disabled. This task changed
   no payment configuration or server secret.

Protocol details, security boundaries and reproduction commands:
[LICENSING_ARCHITECTURE.md](LICENSING_ARCHITECTURE.md).
