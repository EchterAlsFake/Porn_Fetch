# CLI updates for the current 3.9 source

> [!CAUTION]
> This guide describes the 3.9 source tree and planned first beta, not the older GPL 3.8 release. I am still working on this rewrite. Builds and updates can fail; please report the beta version, OS, and error if they do.

Standalone CLI builds use [The Update Framework (TUF)](https://theupdateframework.readthedocs.io/) to check and download signed updates. This is separate from the Qt Installer Framework repository used by desktop installers. Run `self-update --check` on your CLI executable to check, or `self-update` to install. The latter asks first; add `--yes` for an unattended install. Quit other running copies of the CLI before updating.

The update helper replaces the executable and bundled PocketBase binary, writes its result in the printed staging directory, and keeps the previous files there for recovery. If an update fails, please include the error and staging result in an issue. Source checkouts, package manager installations, and files in system managed directories must be updated through their original installation method.

The repository can carry Windows x64 and ARM64; macOS x64 and ARM64; and Linux x64, ARM64, x32, riscv64, s390x, and ppc64le. The last four Linux targets are experimental. A target appears only after its build artifact succeeds. Windows x86 is currently unavailable because a required cryptography dependency no longer supports it.

## Publishing and server layout

The public repository is `https://api.echteralsfake.me/repo/cli/`, mapped on the server to `/srv/pornfetch-downloads/public/repo/cli/`. Caddy must serve all files under `metadata/` and `targets/` as static files over HTTPS. Metadata should not be cached for long; archives can be cached. The deployment script uses the existing `pornfetch-deploy` SSH account and `IFW_DEPLOY_*` beta environment configuration. It uploads targets and metadata first, then makes the new `timestamp.json` visible last.

In **Build All**, set `Legal review complete` and `Deploy signed CLI updates`. Creating a release also publishes CLI updates. CI appends the GitHub run number to the app version for each build. Publishing rejects a target whose version does not increase. **Refresh CLI Update Metadata** renews signed metadata every three days between releases and can also be run manually. A failed refresh needs attention before the timestamp expires after seven days.

## Signing keys

`src/cli/update_root.json` is the public trust anchor bundled into the CLI. The private root key is at `.private/cli-updates/root.pem` on the machine where the keys were initialized. **Back it up securely and keep it offline.** Losing it prevents a normal trust root rotation for installed clients. Never commit either private key, put the root key in GitHub, or replace the public root in a release without a planned TUF root rotation.

The online signing key is `.private/cli-updates/online.pem`. GitHub Actions reads it from the beta environment secret `CLI_UPDATE_SIGNING_KEY`; set the entire PEM file as the secret value and restrict access to the beta environment. If this key is exposed, stop publishing, rotate the delegated signing keys with the offline root key, and publish a new signed root before resuming.

`python packaging/init_cli_updates.py` initializes keys for a new repository. Do not run it against this repository: the trust root has already been generated.
