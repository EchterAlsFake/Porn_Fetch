# Production licensing client

This document describes the commercial client implementation, with backend facts
from the operator's 6 October 2026 Keygen CE 1.8 handoff. It does not declare a
commercial launch. NOWPayments remains sandboxed and Patreon disabled. The server's
customer renewal selection UI still needs wiring, according to that handoff.

## Public configuration and migration

`src/licensing/production.json` and the compiled Qt resource contain only:

| Field | Production value |
| --- | --- |
| Base URL | `https://licenses.pornfetch.to` |
| Account | `b0fab530-8614-45cb-8627-12ee594fb973` |
| Product | `5d5e8829-838b-4dd4-8bfc-2491aa0f82d3` |
| Commercial policy | `7038281b-2429-4aa4-81db-4f04a87e7184` |
| Account Ed25519 public key | `d24ec8bb5f78cc79f95751a3e1988107379a00cb89246b7f3318977dd2be9477` |

**The operator handoff supersedes the initial requested policy ID.** Policy
`564897fa-b8d9-4871-82a4-0b49fd50bc1e` is the preserved beta policy, not the
commercial policy. Accepting it would not implement the promised update model.
Its credentials are rejected locally with the beta migration message. They are
never submitted to the commercial server by validation or deactivation.

The initial Git HEAD configuration also contained these obsolete identifiers:

| Field | Old value |
| --- | --- |
| Account | `2779db33-8e9b-4c5f-b1b5-ee5957939c20` |
| Product | `770dddd7-fa42-4ab7-bed5-e6db5dd301b5` |
| Policy | `0700dec3-90a0-4c7f-a22d-e1a82ca43d53` |
| Public key | `c8988868d2034ef531279bf87970d39e4dc967e61b8215d059a682323d38c1f2` |

The working configuration already replaced those four values before this audit.
The old account is retained only for local rejection, with documentation and tests.
The codebase scan found no `api.keygen.sh` endpoint or other obsolete licensing
hostname in active source. `api.pornfetch.to` remains the update host, not the
licensing host. Synthetic test identifiers and the separate TUF update public keys
are deliberately unchanged. Historical beta changelog entries remain historical.
Current UI/docs no longer direct users to obtain an old beta-policy license.

Schema-2 JSON envelopes and raw signed keys are accepted. Schema-1 and known beta
claims get an explicit migration error. Unknown/wrong signatures or identities are
rejected locally. Old provisional/cache state cannot grant offline access: a new
successful production validation and signed checkout are required. Migration never
silently regenerates the installation UUID, transfers licenses, or consumes a seat.

## Verification and activation

The shared implementation (`src/licensing`) is Qt-free and is used by GUI, Android,
and CLI. Qt signals/properties live in `src/backend/license_bridge.py`.

1. Read a bounded file/JSON envelope or pasted signed key.
2. Verify Ed25519 over the **original ASCII `key/<base64url payload>` string**,
   including the prefix, Base64 padding and original encoding. Do not decode and
   reserialize the JSON for verification. Check pinned account, product, policy,
   license UUID and timestamp claims. The license never supplies its own trust key.
3. Load or create the persistent UUIDv4, using Python's OS-random `uuid.uuid4()`.
4. POST `/v1/accounts/ACCOUNT/licenses/actions/validate-key` with `meta.key` and
   fingerprint/product/policy scope, using `Authorization: License <key>`.
5. Only `NO_MACHINE`, `NO_MACHINES`, or `FINGERPRINT_SCOPE_MISMATCH` permits automatic
   creation of a machine with the same fingerprint and license relationship.
   Keygen assigns the machine resource ID. The ten-machine cap is enforced by the server.
6. Validate again. A 201 creation response alone never unlocks Premium. Duplicate
   fingerprint responses and ambiguous creation timeouts are reconciled by validation;
   machine creation itself is not automatically retried.
7. Resolve the machine by fingerprint and POST its `actions/check-out` with
   `algorithm=base64+ed25519`, `ttl=604800`, `include=["license"]`.
8. Verify the signed machine file and persist its certificate and successful
   validation timestamp. Only then return an allowed status for an entitled build.

Machine-file signature verification uses the exact ASCII **`machine/<enc>`**.
Outer PEM/Base64 wrapping is transport encoding; `enc` itself is never normalized.
Check account, product, license, policy, fingerprint, suspension, issue time, expiry,
and bounded TTL. The commercial checkout must contain a non-null entitlement end.
The permanent key initially has null expiry and is not a current entitlement receipt.

Signature format references: [Keygen signing algorithms](https://keygen.sh/docs/api/cryptography/)
and [machine checkout implementation](https://github.com/keygen-sh/keygen-api/blob/master/app/services/machine_checkout_service.rb).
The deployed 1.8 facts above come from the supplied operator handoff; the public
repository did not expose a `v1.8.0` tag during this audit. Tests pin observed response
codes instead of pretending another revision is the deployed source.

## Network behavior and privacy

`LicensingCore` keeps BaseCore's owned asynchronous curl session, but uses its raw
request interface to preserve non-2xx JSON:API bodies. BaseCore's generic scraper
request method discards those bodies and runs website challenge/logging handlers.
The licensing adapter does neither. It uses TLS verification, no redirects, no
scraper cookies/proxy/insecure TLS settings, a 5-second connect timeout, a 20-second
curl request timeout, and a 25-second coroutine deadline. Only GET and validation
have a second safe attempt. Mutating operations are not blindly retried.

Status distinguishes invalid/rejected, suspended, authentication denied, activation
limit, expired update entitlement, network outage, server outage, and malformed
responses. HTTP authentication denials are sticky even when the body is not JSON.
A subsequent outage never converts an explicit denial into offline access.
`valid=false, EXPIRED` is not silently overridden; it indicates a server policy issue.

The client sends only the random installation fingerprint as machine attributes.
It never reads or derives identity from MAC, disk/CPU/motherboard serials, username,
hostname, IP, TPM, or OS machine ID. The server necessarily sees a connection's source
IP; the application does not send it as identity. No license key, full signed customer
payload, HTTP authorization header, or raw server error body is logged. License data
is stored locally in the user's protected app-data database; it is not encrypted
using an embedded "secret." Customer devices contain no admin token, signing private
key, encryption key, payment secret, or database credential.

## Installation identity and storage

The SQLite database is named `licensing.sqlite3`. Its single state row contains
`installation_id` and license records (credential, signed permit, validation time,
retry state and sticky denial). Transactions prevent concurrent local clients from
creating different identities. POSIX directory/file modes are 0700/0600. Existing
unreadable IDs/databases are preserved and rejected, never silently replaced.

| Platform | New-install database path |
| --- | --- |
| Windows | `%LOCALAPPDATA%\EchterAlsFake\Porn Fetch\licensing.sqlite3` |
| Linux | `${XDG_DATA_HOME:-~/.local/share}/Porn Fetch/licensing.sqlite3` |
| macOS | `~/Library/Application Support/Porn Fetch/licensing.sqlite3` |
| Android GUI | Qt `QStandardPaths.AppDataLocation/licensing.sqlite3`, within the application's private data sandbox |
| Termux CLI | Platformdirs' per-user data directory, typically `$HOME/.local/share/Porn Fetch/licensing.sqlite3` |

Desktop and CLI share the same resolver. When no preferred database exists, an
existing older Qt database is reused **in place**: Windows `%APPDATA%\EchterAlsFake\Porn Fetch`,
Linux `$XDG_DATA_HOME/EchterAlsFake/Porn Fetch`, or macOS
`~/Library/Application Support/EchterAlsFake/Porn Fetch`. If both already exist,
the shared preferred location wins; databases/identities are not merged automatically.
Android uses Qt's resolved private path directly because platformdirs discovery is
not reliable in every PySide Android bundle. No desktop fallback is used for Android GUI.

Restart/update/reinstall reuses the UUID when that directory survives. Uninstalling
an Android app or deleting its app data normally removes its identity. Copying a
whole profile copies the UUID. A new independent app-data directory generates a
new UUID and consumes another server machine slot. Deactivation frees the server
seat but keeps the local UUID for future reactivation.

## Seven-day offline grace

Startup always attempts validation. GUI also checks the local state every minute
and normally refreshes online daily; CLI checks on its existing workflow boundaries.
Outages use exponential retry backoff up to one hour. Explicit refresh bypasses it.

Offline permission is bounded by the earlier of the signed permit's expiry and
`last_successful_validation + 604800`. No initial activation grace exists. Failed
requests and reimports never extend an old signed permit. Cached entitlement fields
alone cannot grant entitlement: each decision reads the verified signed certificate.
Malformed/non-finite timestamps, incorrect UUIDs, identity mismatch, bad signatures,
TTL excess, implausible cache/issuance times and obvious clock rollback are rejected.
The signed server issue time bounds the local timestamp even if the cache is edited.
This is modest cache protection, not invasive anti-tamper DRM; a fully user-controlled
clock/binary cannot be made into a trustworthy hardware root.

## Perpetual update entitlement and renewals

`src/shared/version.py` embeds the approved immutable release timestamp:
`1791244800` = **2026-10-06T00:00:00Z**. CI embeds the artifact build version separately;
it never replaces the release date with build time, file mtime, or the runtime clock.
The release owner must commit the correct new timestamp with each new release and
keep it fixed for all rebuilds of that release.

The running build is entitled iff its release timestamp is at or before the signed
checkout's license expiry. The current wall clock only controls the separate offline
window and the informational "Update entitlement expired" message. Keygen's commercial
policy has `duration=31556952` (one calendar year), `FROM_FIRST_ACTIVATION`,
`MAINTAIN_ACCESS`, and `FROM_NOW_IF_EXPIRED`. The client accepts `valid=true, EXPIRED`.
An old entitled build continues working after the update year when freshness checks
succeed. A later build reports renewal required. A null initial key expiry never means
unlimited updates.

Renewal is performed server-side/payment-side. The client never calls the renewal
administration action. Refreshing obtains a new signed checkout with the renewed
expiry, keeping the original key and UUID. No extra activation is consumed. Qt emits
an entitlement-change signal to refresh update discovery immediately. CLI update
checks validate again. Both frontends link to the website; completing its customer
renewal selection UI is a server release dependency.

## Updater integrity and behavior

**CLI:** existing TUF root/targets verification binds version, release timestamp and
bundle hash. The hashed archive manifest repeats the timestamp and must agree. The
client reports eligibility during discovery and blocks an unentitled/missing-date
update before downloading or staging. Publisher metadata refresh preserves target
custom fields. New signed targets obtain the date from the release source commit.

**Qt:** `packaging/sign_desktop_release.py` signs TUF Targets metadata as `release.json`
using the existing release targets key (a CI/operator-only secret, never Keygen's
account private key). It binds platform, version, release timestamp, and hashes/lengths
of **all** repository files, including `Updates.xml` and archives. The bundled TUF root
is also in the Qt resources. Deployment publishes payloads first, then Updates.xml,
then the signed release manifest. A partial deployment fails verification safely.

Discovery verifies signatures and metadata expiration, then shows the signed version,
release date and eligibility/renewal message. Before installation, it refreshes both
metadata and license, checks entitlement again, verifies every repository file into
private local staging, and checks the XML version/date. It launches IFW with
`--set-temp-repository file:///...`, which replaces the remote repositories for that
fetch. This prevents a mutable remote feed from switching versions after entitlement
was checked. Denial never runs pre-update cleanup or closes the current installation.
Unsigned legacy discovery can display availability but cannot enable automatic install.

The Qt manifest currently expires after 30 days and must be republished/refreshed by
the release operator, preserving version/date/artifact hashes. CLI already has a
scheduled TUF metadata refresh. Qt signature validation uses the bundled root directly;
root rotation requires a new app release. Verified Qt staging remains available to the
external maintenance tool after app exit and can be removed after installation.

The authenticated archive binds the shipped binary containing release constants.
Directly running a manually patched binary or launching an independent external
installer is outside the application's updater gate. OS code signing/notarization
and native packaged installer behavior still need their platform release checks.

## Tests and release evidence

Offline tests cover all 23 requested cases, plus activation response loss, sticky
non-JSON denials, policy migration, same-key renewal, cache tampering, null commercial
expiry, scoped account routes, TLS isolation, Qt feature gates, signed update metadata,
artifact tampering and both updater denial paths. The fixed synthetic vector was
signed independently with OpenSSL using a test-only seed and Keygen's exact format;
other fixtures use deterministic synthetic Ed25519 keys. It is not represented as a
production-issued credential. The existing local beta license also verified against
the production public key during this audit, without printing or copying its payload;
its beta policy was correctly rejected. It is not committed as a fixture.

Run offline tests:

```sh
uv run --no-sync python -m unittest discover -s src/tests/unit -p 'test_*.py' -q
uv run --no-sync python -m unittest src.tests.integration.test_license_integration -q
```

An opt-in public test only validates/checks out an **existing activated TEST install**.
It creates/deletes no machine, renews nothing and performs no purchase. Validation and
checkout can update server audit timestamps. Pass a private file path, not a key on
the command line:

```sh
PF_KEYGEN_INTEGRATION=1 \
PF_KEYGEN_TEST_LICENSE_FILE=/private/commercial-test.license \
PF_KEYGEN_TEST_INSTALLATION_ID=<existing-UUID4> \
uv run --no-sync python -m unittest src.tests.integration.test_keygen_production_opt_in
```

Do not enable this in ordinary CI. No live production mutation test was run for this
client task. The supplied server handoff's passing matrix is separate evidence, not
proof that a packaged client was exercised.

Before commercial release: run the opt-in check with an authorized commercial TEST
installation; publish signed repositories using the existing protected release key;
exercise actual Windows/macOS/Linux Qt maintenance tools and Android import/storage;
confirm artifact signing and committed release dates; finish the server's renewal
selection UI and payment enablement requirements. Offline passing tests alone do not
establish production readiness.
