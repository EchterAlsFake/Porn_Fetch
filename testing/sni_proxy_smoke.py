#!/usr/bin/env python3
"""Small end-to-end request through either SNI fragmentation proxy."""

from __future__ import annotations

import argparse
import asyncio
import logging
import multiprocessing as mp
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from curl_cffi.const import CurlHttpVersion, CurlIpResolve, CurlOpt
from curl_cffi.requests import AsyncSession

from src.backend.sni_fragment_proxy_lite import (
    FragmentingProxyConfig,
    FragmentingProxyProcess,
)
from src.backend.sni_fragment_proxy_strict import (
    StrictDesyncConfig,
    StrictFragmentingProxyConfig,
    StrictFragmentingProxyProcess,
)


async def request_through_proxy(
    url: str,
    *,
    strict: bool,
    interface: str | None,
    concurrency: int,
    reverse: bool,
    desync: bool,
) -> int:
    if strict:
        proxy = StrictFragmentingProxyProcess(
            StrictFragmentingProxyConfig(
                listen_host="127.0.0.1",
                listen_port=0,
                linux_interfaces=(interface,) if interface else None,
                reverse_fragments=reverse or desync,
                desync_config=StrictDesyncConfig() if desync else None,
                log_level=logging.DEBUG,
            )
        )
    else:
        proxy = FragmentingProxyProcess(
            FragmentingProxyConfig(listen_host="127.0.0.1", listen_port=0)
        )
    proxy_url = proxy.start()
    mode = "Strict" if strict else "Lite"
    print(f"{mode} SNI proxy: {proxy_url}", flush=True)
    sessions = [
        AsyncSession(
            proxy=proxy_url,
            timeout=30,
            curl_options={
                CurlOpt.HTTP_VERSION: CurlHttpVersion.V2_0,
                # The Geneva harness intentionally disables IPv6 because this
                # Geneva release installs only iptables (not ip6tables) rules.
                CurlOpt.IPRESOLVE: CurlIpResolve.V4,
                CurlOpt.ECH: b"false",
            },
        )
        for _ in range(concurrency)
    ]
    try:
        responses = await asyncio.gather(*(session.get(url) for session in sessions))
        for index, response in enumerate(responses, start=1):
            print(f"GET {url} [{index}]: HTTP {response.status_code}", flush=True)
        return 0 if all(200 <= response.status_code < 400 for response in responses) else 1
    finally:
        await asyncio.gather(*(session.close() for session in sessions))
        proxy.stop()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--interface")
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--desync", action="store_true")
    parser.add_argument("url", nargs="?", default="https://example.com/")
    args = parser.parse_args()
    if args.concurrency < 1:
        parser.error("--concurrency must be at least 1")
    return asyncio.run(
        request_through_proxy(
            args.url,
            strict=args.strict,
            interface=args.interface,
            concurrency=args.concurrency,
            reverse=args.reverse,
            desync=args.desync,
        )
    )


if __name__ == "__main__":
    mp.freeze_support()
    raise SystemExit(main())
