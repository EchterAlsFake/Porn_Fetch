"""Create the offline root key, online signing key, and public TUF trust root."""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from securesystemslib.signer import CryptoSigner
from tuf.api.metadata import Metadata, Root


def initialize(private_dir: Path, root_file: Path) -> None:
    private_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    if root_file.exists() or any(private_dir.iterdir()):
        raise FileExistsError("CLI update keys or root metadata already exist; refusing to replace trust keys")

    root_signer = CryptoSigner.generate_ed25519()
    online_signer = CryptoSigner.generate_ed25519()
    root = Metadata(Root(expires=datetime.now(timezone.utc) + timedelta(days=3650)))
    root.signed.add_key(root_signer.public_key, "root")
    for role in ("targets", "snapshot", "timestamp"):
        root.signed.add_key(online_signer.public_key, role)
    root.sign(root_signer)
    root.signed.verify_delegate("root", root.signed_bytes, root.signatures)

    for name, signer in (("root.pem", root_signer), ("online.pem", online_signer)):
        path = private_dir / name
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as output:
            output.write(signer.private_bytes)

    root_file.parent.mkdir(parents=True, exist_ok=True)
    root_file.write_bytes(root.to_bytes())
    print(f"Public trust root: {root_file}")
    print(f"Private keys: {private_dir} (back these up securely; never commit them)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-dir", type=Path, default=Path(".private/cli-updates"))
    parser.add_argument("--root-file", type=Path, default=Path("src/cli/update_root.json"))
    args = parser.parse_args()
    initialize(args.private_dir, args.root_file)
