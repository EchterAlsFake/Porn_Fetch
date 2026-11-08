#!/bin/bash
# Run as root on the fallback host from a prepared source bundle.
set -euo pipefail
cd "$(dirname "$0")"
test "$(id -u)" = 0
backup_dir=/var/backups/pornfetch-emergency/$(date -u +%Y%m%dT%H%M%SZ)
install -d -m 0700 "$backup_dir"
cp -a /etc/caddy/Caddyfile "$backup_dir/Caddyfile"
if systemctl is-active --quiet pornfetch-emergency; then
    echo 'Existing emergency installation found. Review and deploy an upgrade manually.' >&2
    exit 1
fi
getent passwd pornfetch-emergency >/dev/null || useradd --system --no-create-home --shell /usr/bin/nologin pornfetch-emergency
install -d -m 0755 /opt/pornfetch-emergency/src/licensing /etc/pornfetch-emergency /run/pornfetch-emergency-control
install -m 0644 server.py /opt/pornfetch-emergency/server.py
install -m 0644 crypto.py /opt/pornfetch-emergency/src/licensing/crypto.py
# Minimal server package: it deliberately excludes client/networking dependencies.
 touch /opt/pornfetch-emergency/src/licensing/__init__.py
install -m 0644 production.json /etc/pornfetch-emergency/production.json
uv venv --python /usr/bin/python3 /opt/pornfetch-emergency/.venv
uv pip install --python /opt/pornfetch-emergency/.venv/bin/python -r requirements.txt
install -d -m 0700 /etc/credstore.encrypted
if ! test -f /etc/credstore.encrypted/pornfetch-emergency-signing; then
    /opt/pornfetch-emergency/.venv/bin/python - <<'PY' | systemd-creds encrypt --name=signing.pem --with-key=host+tpm2 --tpm2-device=/dev/tpmrm0 --tpm2-pcrs=7 - /etc/credstore.encrypted/pornfetch-emergency-signing
import sys
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
key = Ed25519PrivateKey.generate()
Path('/etc/pornfetch-emergency/public-key.txt').write_text(key.public_key().public_bytes_raw().hex() + '\n')
sys.stdout.buffer.write(key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()))
PY
fi
chmod 0600 /etc/credstore.encrypted/pornfetch-emergency-signing
install -m 0644 pornfetch-emergency.service /etc/systemd/system/pornfetch-emergency.service
install -m 0755 pornfetch-emergencyctl /usr/local/sbin/pornfetch-emergencyctl
install -m 0644 route.caddy /etc/caddy/pornfetch-emergency.caddy
python3 - <<'PY'
from pathlib import Path
p = Path('/etc/caddy/Caddyfile')
s = p.read_text()
anchor = 'echteralsfake.me, www.echteralsfake.me {\n'
assert s.count(anchor) == 1, 'Review the Caddy site block before installing the emergency route'
if 'import /etc/caddy/pornfetch-emergency.caddy' not in s:
    s = s.replace(anchor, anchor + '\timport /etc/caddy/pornfetch-emergency.caddy\n')
Path('/etc/caddy/Caddyfile.emergency-candidate').write_text(s)
PY
/usr/local/bin/caddy validate --config /etc/caddy/Caddyfile.emergency-candidate --adapter caddyfile
systemctl daemon-reload
systemctl enable --now pornfetch-emergency
systemctl is-active --quiet pornfetch-emergency
install -m 0644 /etc/caddy/Caddyfile.emergency-candidate /etc/caddy/Caddyfile
if ! systemctl reload caddy; then
    cp -a "$backup_dir/Caddyfile" /etc/caddy/Caddyfile
    systemctl reload caddy
    exit 1
fi
/usr/local/sbin/pornfetch-emergencyctl status
printf 'Emergency public key: '
cat /etc/pornfetch-emergency/public-key.txt
printf 'Caddy backup: %s\n' "$backup_dir/Caddyfile"
