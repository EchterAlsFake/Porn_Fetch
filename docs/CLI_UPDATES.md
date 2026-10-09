# CLI updates for the current 3.9 source

> [!CAUTION]
> This guide describes the 3.9 source tree and planned first beta, not the older GPL 3.8 release. I am still working on this rewrite. Builds and updates can fail; please report the beta version, OS, and error if they do.

Standalone CLI builds use [The Update Framework (TUF)](https://theupdateframework.readthedocs.io/) to check and download signed updates. This is separate from the Qt Installer Framework repository used by desktop installers. Run `self-update --check` on your CLI executable to check, or `self-update` to install. The latter asks first; add `--yes` for an unattended install. Quit other running copies of the CLI before updating.

The update helper replaces the executable and bundled PocketBase binary, writes its result in the printed staging directory, and keeps the previous files there for recovery. If an update fails, please include the error and staging result in an issue. Source checkouts, package manager installations, and files in system managed directories must be updated through their original installation method.

The build produces Windows x64 and ARM64, macOS x64 and ARM64, and Linux x64 and ARM64 CLI artifacts. Workflow dispatch can also opt into experimental Linux 32-bit (x32 artifact) and riscv64 builds; each must pass its build and smoke test before it is included. Linux s390x and ppc64le are paused because `curl-cffi` does not support those architectures. Windows x86 is paused because the binary in pipeline #43 could not load `curl_cffi`. A target appears in the update repository only after its build artifact succeeds.

## Publishing and server layout

The public repository is `https://api.pornfetch.to/repo/cli/`. The MSI deployment
API accepts a tar.gz POST to `https://api.pornfetch.to/ci/deploy/cli` with the
`X-CI-TOKEN` header. The archive root contains `metadata/` and optionally
`targets/`, without an enclosing artifact or repository directory. There is no
SSH deployment configuration. Server filesystem paths are an implementation
detail of that API.

Serve all files under `metadata/` and `targets/` as static files over HTTPS.
Metadata should not be cached for long; archives can be cached. The server must
retain existing targets and versioned metadata when applying refreshes, install
new targets and metadata first, and make the new `timestamp.json` visible last.

Configure these Actions secrets:

| Name | Scope | Value |
| --- | --- | --- |
| `CI_TOKEN` | Repository Actions secret | Token accepted by the deployment API |
| `CLI_UPDATE_SIGNING_KEY` | `beta` environment secret | Complete online signing-key PEM; never the root key |

Build jobs do not receive the online key. Deployment selects `environment: beta`
and writes the PEM to a mode-0600 temporary file, deleting it after signing.
The desktop deployment also uses this online key for its signed release manifest.

In **Build All**, set `Legal review complete` and `Deploy signed CLI updates`. Creating a release also publishes CLI updates. CI appends the GitHub run number to the app version for each build. Publishing rejects a target whose version does not increase. **Refresh CLI Update Metadata** renews signed metadata every three days between releases and can also be run manually. A failed refresh needs attention before the timestamp expires after seven days.

Build All first runs the reusable offline CI suite on the same commit. Publishing runs
are queued separately from ordinary builds and are not automatically cancelled by a newer run.
CLI deployment and scheduled refresh share the `cli-update-deploy` concurrency
group with cancellation disabled. Build All downloads only `PornFetch_*_CLI_*`
artifacts into separate directories (`merge-multiple: false`), then runs
`packaging/publish_cli_updates.py` to create `dist/cli_tuf/metadata/` and
`dist/cli_tuf/targets/`. `scripts/deploy_cli_updates.sh` uploads that generated
repository rather than raw Actions artifacts.

After each upload, `packaging/verify_deployment.py` runs the
[TUF client workflow](https://theupdateframework.readthedocs.io/en/latest/api/tuf.ngclient.updater.html)
with the bundled public root and a fresh cache. It requires public metadata to
match this deployment, then downloads and verifies one bundle per represented
operating system, preferring newly published bundles. Missing files, invalid
signatures, expired or stale metadata, and mismatched hashes fail the job.
The GitHub Release job requires CLI deployment and verification to succeed.
Refresh-only uploads contain metadata and verify retained public targets.

## Signing keys

`src/cli/update_root.json` is the public trust anchor bundled into the CLI.
The root private key authorizes root changes; the online private key signs
targets, snapshot, and timestamp metadata. Keep the root key offline with
verified encrypted backups. Never commit `.private/`, put the root key in
GitHub, or upload it to the deployment API. Once clients have shipped, changing
their trust root requires a planned TUF root rotation signed by the old and new
root keys.

The online signing key is `.private/cli-updates/online.pem`. GitHub Actions reads it from the beta environment secret `CLI_UPDATE_SIGNING_KEY`; set the entire PEM file as the secret value and restrict access to the beta environment. If this key is exposed, stop publishing, rotate the delegated signing keys with the offline root key, and publish a new signed root before resuming.

### Recover the trust root before the first 3.9 release

The former `.private/cli-updates` directory, including `root.pem`, was lost.
The existing public root cannot recover that private key. No 3.9 CLI build was
distributed, so establish a fresh version-1 public root before building or
releasing 3.9. This is a new trust bootstrap, not a rotation for installed clients.
Production keys must be generated and backed up by an operator on a trusted
machine; automated development sessions should use disposable test keys only.

1. Stop publishing and disable scheduled refresh during recovery. From a trusted
   checkout with GitHub CLI authenticated, run `gh workflow disable refresh_cli_updates.yml`.
   Wait for active CLI publishing jobs to finish. Install locked dependencies
   with `uv sync --locked --no-dev` before disconnecting the key-generation
   machine from the network.
2. Generate into an empty ignored directory, leaving the old public root intact
   until the new keys are backed up. Run locally, offline:

   ```bash
   umask 077
   uv run --no-sync python packaging/init_cli_updates.py \
     --private-dir .private/cli-updates \
     --root-file .private/cli-updates/update_root.json
   stat -c '%a %n' .private/cli-updates/root.pem .private/cli-updates/online.pem
   ```

   Both PEM files must have mode `600`. The initializer refuses existing keys or
   root output; do not delete or overwrite surviving keys to bypass that check.
3. Back up to mounted encrypted offline storage (replace this example path with
   your actual mount). Verify the copies without displaying key contents:

   ```bash
   CLI_KEY_BACKUP=/media/ENCRYPTED_BACKUP/pornfetch-cli-3.9
   mkdir -m 700 "$CLI_KEY_BACKUP"
   cp -p .private/cli-updates/root.pem .private/cli-updates/online.pem \
     .private/cli-updates/update_root.json "$CLI_KEY_BACKUP/"
   cmp .private/cli-updates/root.pem "$CLI_KEY_BACKUP/root.pem"
   cmp .private/cli-updates/online.pem "$CLI_KEY_BACKUP/online.pem"
   cmp .private/cli-updates/update_root.json "$CLI_KEY_BACKUP/update_root.json"
   CLI_KEY_BACKUP="$CLI_KEY_BACKUP" uv run --no-sync python - <<'PY'
   import os
   from pathlib import Path
   from securesystemslib.signer import Signer
   from tuf.api.metadata import Metadata, Root

   backup = Path(os.environ['CLI_KEY_BACKUP'])
   root = Metadata[Root].from_file(str(backup / 'update_root.json'))
   root.signed.verify_delegate('root', root.signed_bytes, root.signatures)
   assert root.signed.version == 1 and not root.signed.is_expired()
   message = b'Porn Fetch 3.9 key backup verification'
   for role in ('root', 'targets', 'snapshot', 'timestamp'):
       keyid = root.signed.roles[role].keyids[0]
       key_file = backup / ('root.pem' if role == 'root' else 'online.pem')
       assert key_file.stat().st_mode & 0o777 == 0o600
       signer = Signer.from_priv_key_uri(f'file2:{key_file.resolve()}', root.signed.keys[keyid])
       root.signed.verify_delegate(role, message, {keyid: signer.sign(message)})
   print('Public root and backed-up private keys verified')
   PY
   ```

   Keep a second verified encrypted backup separately. Unmount backup media and
   keep the root key on offline storage; remove any working root-key copy using
   your storage's secure-removal procedure before reconnecting to GitHub.
4. Install the new public root with
   `cp .private/cli-updates/update_root.json src/cli/update_root.json`.
   Commit only that public root with the pipeline changes. Confirm
   `git check-ignore .private/cli-updates/online.pem` succeeds and
   `git ls-files .private` prints nothing. Build every 3.9 release artifact from
   this commit so its embedded trust anchor matches the publisher.
5. Reconnect the publishing operator machine and set only the online PEM:

   ```bash
   gh secret set CLI_UPDATE_SIGNING_KEY --env beta < .private/cli-updates/online.pem
   ```

   Leave `CI_TOKEN` as a repository Actions secret. Restrict deployment access to
   `beta`. The root PEM must never be uploaded to GitHub.
6. Have the server operator reset the unpublished CLI repository to an empty
   namespace while publishing is paused. Old root versions and metadata must
   not mix with the fresh root. Before bootstrap, this command must report HTTP
   `404` (connection failures, HTML responses, and other statuses require repair):

   ```bash
   curl -sS -o /dev/null -w '%{http_code}\n' \
     https://api.pornfetch.to/repo/cli/metadata/timestamp.json
   ```

   The publisher treats only a missing timestamp (`404`) as an initial repository;
   it fails on an existing repository that the new root cannot validate.
7. Run Build All from the new-root commit with **Legal review complete** and
   **Deploy signed CLI updates**, initially leaving release publication off.
   Require the public TUF verification step to pass. For an independent public
   check, use the TUF client directly (no private keys):

   ```bash
   uv run --no-sync python - <<'PY'
   import tempfile
   from pathlib import Path
   from tuf.ngclient import Updater

   with tempfile.TemporaryDirectory() as directory:
       base = Path(directory)
       updater = Updater(
           metadata_dir=str(base / 'metadata'),
           metadata_base_url='https://api.pornfetch.to/repo/cli/metadata/',
           target_dir=str(base / 'targets'),
           target_base_url='https://api.pornfetch.to/repo/cli/targets/',
           bootstrap=Path('src/cli/update_root.json').read_bytes(),
       )
       updater.refresh()
       target = updater.get_targetinfo('linux/amd64.zip')
       assert target is not None
       updater.download_target(target)
       print('Public TUF metadata and linux/amd64.zip verified:', target.custom['version'])
   PY
   gh workflow enable refresh_cli_updates.yml
   ```

   Check the printed target version equals the deployed `3.9.<run number>`.
   Once verified, the next Build All release run can publish newer signed bundles
   and create the gated GitHub Release.

### Disposable local publishing test

`uv run --no-sync python -m unittest src.tests.unit.test_cli_self_update src.tests.unit.test_deployment_verification src.tests.unit.test_build_pipeline`
generates fresh keys in temporary directories and serves a fake repository on
localhost. It checks initial publishing, a subsequent build, metadata-only
refresh with retained targets, client verification, stale metadata, and corrupted
payload rejection. It never reads production PEM files or contacts the production
API. For manual experiments, the publisher and verifier accept `--root-file`
to select a disposable public root without modifying the bundled root.

## Update entitlement

Signed target custom metadata and the hashed bundle manifest both contain
`release_timestamp`, taken from `src/shared/version.py` in the release commit.
`--check` reports whether the release is entitled. Installation refreshes licensing
and blocks before downloading when renewal is required or the signed date is missing.
Renewal keeps the same key; repeat the update check after refreshing. The date must
be fixed for each release and must never be generated from the installing device clock.
