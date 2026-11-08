# Emergency licensing

The service at `https://echteralsfake.me/api/pornfetch-emergency/v1/permit`
accepts a valid Keygen-signed production lifetime key and returns a separate,
seven-day Ed25519 JWS permit. It has no customer database and makes no requests
to Keygen. New installations and unlimited license sharing are intentionally
allowed while issuance is enabled. Revocations are not available offline.

## Operate the deployed service

On `asuna@192.168.178.200` (`eaf-node`), only enable issuance when the primary
licensing service is genuinely unavailable:

```sh
sudo pornfetch-emergencyctl enable
sudo pornfetch-emergencyctl status
sudo pornfetch-emergencyctl disable
```

The service runs continuously but starts disabled after every service restart
or host reboot. Turning it off prevents new permits. Existing permits remain
valid for their remaining lifetime, up to seven days. An authoritative primary
rejection takes precedence as soon as the app can reach the primary again.
The service cannot distinguish deliberately blocked primary connections from
an actual outage; the manual issuance switch is the control for this.

Check deployment without enabling issuance:

```sh
systemctl status pornfetch-emergency
curl -i -X POST -H 'Content-Type: application/json' --data '{}' \
  https://echteralsfake.me/api/pornfetch-emergency/v1/permit
```

The expected response is HTTP 503 with `{"error":"emergency_disabled"}`.

## Client and protocol

The app tries the primary first. Only connection failures, timeouts, HTTP
408/425/429 and 5xx responses qualify for emergency requests. Invalid responses,
certificate failures and explicit rejections do not. A valid emergency permit
may clear a historical rejection during a later primary outage. A successful
primary validation removes the emergency permit and restores normal enforcement.

Each request contains exactly `license_key`, `installation_id` (existing UUIDv4),
and `nonce` (32 random bytes encoded as 64 lowercase hex characters).
The response contains `permit`, a compact JWS with a fixed EdDSA algorithm and
`emergency-2026-01` key ID. Its signature binds version, issuer, audience,
license ID, SHA-256 of the complete license key, installation ID, nonce, issue
time and expiry. The original license is independently verified on both sides.
Only the public emergency key ships in `src/licensing/production.json`.

The client checks the nonce before caching a response and verifies all signed
bindings on reuse. Emergency renewal is attempted after a day; primary retries
retain their existing backoff. Failed renewal does not extend a permit. Existing
clock rollback checks and initial/normal offline grace remain in force.

Fallback requests are direct-only. With Tor selected, the app explains that the
user must turn Tor routing Off in Privacy settings and refresh to try the fallback.
It never changes that preference or silently connects directly. Already cached
permits can still be used without a fallback request.

An updated app build is required. Older distributed clients do not know this
endpoint or its verification key.

## Deployment and key custody

The deployed backend listens on `127.0.0.1:8014`; the existing Caddy site imports
`/etc/caddy/pornfetch-emergency.caddy`. No DNS or VPS changes were needed. The
Acer origin is independent of the MSI primary, but the documented topology uses
the same public VPS relay. Failure of that shared edge can affect both services.

Runtime files:

- `/opt/pornfetch-emergency`: minimal server package and isolated Python environment.
- `/etc/pornfetch-emergency`: public Keygen configuration and emergency public key.
- `/etc/credstore.encrypted/pornfetch-emergency-signing`: TPM/host-encrypted key.
- `/run/pornfetch-emergency-control/enabled`: root-controlled volatile issuance flag.
- `/var/backups/pornfetch-emergency`: pre-deployment Caddy configuration backups.

The private key was generated on the fallback host and piped into `systemd-creds`
without saving a plaintext file. The service receives it through
`LoadCredentialEncrypted`. Request/access logs are disabled and error responses
never include credentials. A single worker applies a global token bucket
(120-request burst, 10 requests/second); this does not count installations or
licenses. Requests are limited to 20 KiB, 10 seconds to read the body, and 64
concurrent connections.

For a first installation, bundle this directory with `src/licensing/crypto.py`
as `crypto.py` and `src/licensing/production.json` as `production.json`, then run
`sudo bash install.sh` on the fallback host. Review its existing-site anchor and
port first. The script backs up Caddy, validates the candidate, and starts issuance
disabled. Copy the generated public key into the app configuration and rebuild
resources before shipping. The installer refuses to overwrite a running service.
For upgrades, disable issuance, install reviewed code from the same source,
restart, verify disabled status, and manually re-enable only if the outage persists.
Never regenerate the signing key during an ordinary update.

Keep an independent encrypted offline backup of the signing key before relying
on recovery of the fallback host itself. The TPM-sealed file alone is not a
portable backup. On a trusted host console, decrypt with `systemd-creds decrypt
--name=signing.pem` and pipe directly into an authenticated encryption tool such
as `age`, using an independently held recipient key. Do not print the decrypted
key or put it in source control. Restore through a pipe into `systemd-creds
encrypt --name=signing.pem` on the replacement host; verify the resulting public
key matches the bundled app key. No portable private-key backup was created by
this deployment. A new key requires a client update.

To roll back routing, disable issuance and restore the saved Caddyfile, validate
it, and reload Caddy. Stop/disable `pornfetch-emergency` once routing is removed.
Retain the encrypted signing key and public configuration for recovery.

## Verify changes

```sh
uv sync --python 3.15.2 --extra gui --extra emergency-server --group dev
uv run --no-sync python -m unittest src.tests.unit.test_emergency_licensing
```

These tests use synthetic keys and cover binding verification, the manual switch,
invalid licenses, new-installation fallback, expiry, primary recovery/rejection,
and the Tor notice. They never enable production issuance or contact live Keygen.
