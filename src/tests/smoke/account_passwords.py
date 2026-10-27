"""Live password login checks; collect the shared test password through Zenity."""
from __future__ import annotations

import argparse
import asyncio
import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

from src.tests.smoke.account_cookies import run

PASSWORD_PROVIDERS = ("pornhub", "xhamster")


def prompt_password():
    executable = shutil.which("zenity")
    if executable is None:
        raise SystemExit("Zenity must be installed to prompt for the account test password")
    dialog = subprocess.run(
        [executable, "--password", "--title=Porn Fetch — temporary account password"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
    )
    if dialog.returncode != 0:
        return None
    return dialog.stdout.removesuffix("\n") or None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=PASSWORD_PROVIDERS, action="append")
    parser.add_argument("--pornhub-email", default="")
    parser.add_argument("--xhamster-username", default="")
    parser.add_argument("--items", type=int, choices=(1, 2, 3), default=2)
    parser.add_argument("--timeout", type=float, default=90)
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-account-passwords.json")
    args = parser.parse_args()
    args.providers = list(dict.fromkeys(args.provider or PASSWORD_PROVIDERS))
    usernames = {"pornhub": args.pornhub_email, "xhamster": args.xhamster_username}
    if any(not usernames[provider] for provider in args.providers) or args.timeout <= 0:
        parser.error("Provide each selected provider's email/username and a positive timeout")
    args.playlists = {}
    args.browser = None
    args.pornhub_username = ""
    logging.disable(logging.CRITICAL)
    password = prompt_password()
    if password is None:
        print("Password prompt cancelled.")
        return 130
    try:
        return asyncio.run(run(args, password=password, usernames=usernames))
    except KeyboardInterrupt:
        print(f"Stopped. Last saved report: {args.report}", flush=True)
        return 130
    finally:
        password = None


if __name__ == "__main__":
    raise SystemExit(main())
