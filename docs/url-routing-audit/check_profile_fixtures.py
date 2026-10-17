"""Opt-in, text-only curl GET checks for the recorded public profile fixtures.

Run from any directory. This checks HTTP availability, not GUI/API extraction.
403 means access restricted, not an invalid URL. Response bodies are temporary.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import shutil
import tempfile
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin


class PageIdentity(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.canonical_url: str | None = None
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical_url = urljoin(self.base_url, attrs.get("href", ""))
        elif tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


async def check_case(case, *, timeout):
    with tempfile.TemporaryDirectory(prefix="porn-fetch-url-check-") as directory:
        body = Path(directory) / "response.html"
        process = await asyncio.create_subprocess_exec(
            "curl", "--silent", "--show-error", "--location", "--max-redirs", "6",
            "--connect-timeout", "12", "--max-time", str(timeout),
            "--max-filesize", "12000000", "--compressed",
            "--proto", "=http,https", "--proto-redir", "=http,https",
            "--user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "--header", "Accept: text/html,application/xhtml+xml",
            "--output", str(body), "--write-out", "%{json}", "--url", case["url"],
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        metadata = json.loads(stdout) if stdout else {}
        status = metadata.get("http_code", metadata.get("response_code", 0))
        final_url = metadata.get("url_effective", case["url"])
        parser = PageIdentity(final_url)
        parser.feed(body.read_text(errors="replace") if body.exists() else "")
        missing = bool(re.search(r"\b404\b|not found|page unavailable", parser.title, re.I))
        if process.returncode:
            outcome = "transport_inconclusive"
        elif status == 403:
            outcome = "access_restricted"
        elif 200 <= status < 300 and not missing:
            outcome = "http_available"
        elif status in {404, 410} or missing:
            outcome = "unavailable_candidate"
        else:
            outcome = "http_other"
        return {
            "id": case["id"], "provider": case["provider"], "url": case["url"],
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "method": "GET", "curl_exit": process.returncode, "status": status,
            "final_url": final_url, "redirects": metadata.get("num_redirects", 0),
            "canonical_url": parser.canonical_url,
            "content_type": metadata.get("content_type"),
            "title_indicates_missing": missing, "outcome": outcome,
            "error": stderr.decode(errors="replace").strip() or None,
        }


async def run(args):
    manifest = json.loads(args.fixtures.read_text())
    cases = manifest["cases"]
    if args.case:
        wanted = set(args.case)
        cases = [case for case in cases if case["id"] in wanted]
        if {case["id"] for case in cases} != wanted:
            raise ValueError("Unknown --case ID")
    elif not args.include_variants:
        cases = [case for case in cases if case["tier"] == "primary"]
    semaphore = asyncio.Semaphore(6)
    provider_locks = {case["provider"]: asyncio.Lock() for case in cases}

    async def one(case):
        async with provider_locks[case["provider"]], semaphore:
            result = await check_case(case, timeout=args.timeout)
            print(f"{result['id']}: {result['status']} ({result['outcome']})", flush=True)
            return result

    results = await asyncio.gather(*(one(case) for case in cases))
    args.output.write_text(json.dumps({
        "scope": "curl HTTP availability; no media downloaded; no API/GUI success implied",
        "summary": dict(Counter(result["outcome"] for result in results)),
        "results": results,
    }, indent=2) + "\n")
    print(f"Saved {len(results)} observations to {args.output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).with_name("profile-fixtures.json"))
    parser.add_argument("--output", type=Path, default=Path("/tmp/porn-fetch-profile-url-checks.json"))
    parser.add_argument("--case", action="append", help="Check a particular fixture ID; repeat as needed")
    parser.add_argument("--include-variants", action="store_true")
    parser.add_argument("--timeout", type=int, default=40)
    args = parser.parse_args()
    if not shutil.which("curl"):
        parser.error("curl must be installed")
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
