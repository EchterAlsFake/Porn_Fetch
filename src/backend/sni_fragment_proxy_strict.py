from __future__ import annotations
#!/usr/bin/env python3
"""
AI Transparency:

Because this topic goes way behind my own engineering capabilities I had to generate this entirely with AI.
ChatGPT 4.6 SOL HIGH was used (Think time: 17 minutes)


"""


"""
App-local strict TCP packet fragmentation proxy for curl-cffi.

The proxy listens only on loopback and runs in a spawned helper process. Only
clients explicitly configured to use its SOCKS5/HTTP-CONNECT URL are affected.
For each outbound proxy connection, the helper opens an exact 4-tuple packet
capture before acknowledging the local CONNECT request. It then splits matching
TCP packets and re-injects valid segments with adjusted sequence numbers and
checksums.

Supported strict backends
-------------------------

* Windows x86-64: WinDivert through PyDivert 3.1+.
* Linux x86-64/aarch64: PyDivert 4 eBPF/TC backend (kernel 5.8+, libbpf).
* macOS: intentionally rejected. Apple's public Network Extension APIs require
  a signed app extension and a packet tunnel/user-space forwarding design; a
  local Python process cannot provide equivalent packet interception.
* Windows ARM64: rejected by default because the official WinDivert package
  does not ship a signed ARM64 kernel driver. A vendor-signed custom build may
  be tried with ``allow_unsupported_windows_arm64=True``.

The implementation fragments:

* the first outbound data packet on every proxy-created TCP connection; and
* recognizable plaintext HTTP/1.0/1.1 request starts on persistent sessions.

HTTPS request contents remain encrypted after the TLS handshake. Therefore, on
HTTPS/HTTP2 the useful strict split is the first TLS ClientHello packet of each
new connection. HTTP/3/QUIC is UDP and is not handled.

Administrator/root privileges are required. Python 3.10+.
"""



import argparse
import asyncio
import base64
import copy
import contextlib
import dataclasses
import ipaddress
import itertools
import logging
import multiprocessing as mp
import os
import platform
import queue
import signal
import socket
import ssl
import struct
import sys
import traceback
from dataclasses import dataclass
from typing import Final, Iterable, Optional, Protocol
from urllib.parse import unquote, urlsplit

try:
    from src.backend.tls_client_hello import TLSClientHelloStreamFragmenter
except (ImportError, ModuleNotFoundError):
    from tls_client_hello import TLSClientHelloStreamFragmenter

__all__ = [
    "StrictDesyncConfig",
    "StrictFragmentingProxyConfig",
    "StrictFragmentingProxyProcess",
    "StrictFragmentingProxyServer",
    "StrictProxyStartError",
    "StrictBackendUnavailable",
    "StrictFlowRegistrationError",
]

VERSION: Final[str] = "2.0.0"
LOGGER_NAME: Final[str] = "strict-fragmenting-proxy"
LOG = logging.getLogger(LOGGER_NAME)

SOCKS_VERSION: Final[int] = 5
SOCKS_AUTH_NONE: Final[int] = 0
SOCKS_AUTH_USERPASS: Final[int] = 2
SOCKS_AUTH_UNACCEPTABLE: Final[int] = 0xFF
SOCKS_CMD_CONNECT: Final[int] = 1
SOCKS_ATYP_IPV4: Final[int] = 1
SOCKS_ATYP_DOMAIN: Final[int] = 3
SOCKS_ATYP_IPV6: Final[int] = 4

DEFAULT_HTTP_PORTS: Final[tuple[int, ...]] = (80, 8000, 8080, 8888)


class StrictProxyStartError(RuntimeError):
    """Raised when the proxy child process cannot be started."""


class StrictBackendUnavailable(RuntimeError):
    """Raised when no supported strict packet backend is available."""


class StrictFlowRegistrationError(RuntimeError):
    """Raised when an exact outbound flow capture cannot be armed."""


class ProxyProtocolError(RuntimeError):
    """Raised for malformed or unsupported local/upstream proxy traffic."""


class UpstreamConnectError(ConnectionError):
    """Raised when the destination or configured upstream proxy rejects a connection."""


@dataclass(frozen=True, slots=True)
class StrictDesyncConfig:
    """Settings for the optional, intentionally invalid ClientHello decoy."""

    mode: str = "seq_ack"
    sequence_offset: int = 10_000
    acknowledgement_offset: int = 66_000
    fake_sni: str = "www.example.com"


@dataclass(frozen=True, slots=True)
class StrictFragmentingProxyConfig:
    """Configuration shared with the proxy child process.

    ``listen_port`` may be 0 to let the OS select a free port. The selected URL
    is returned by :meth:`StrictFragmentingProxyProcess.start`.

    ``upstream_proxy`` supports these URL schemes:

    * ``http://host:port``
    * ``https://host:port``
    * ``socks5://host:port``  (resolve destination locally in this process)
    * ``socks5h://host:port`` (let the upstream SOCKS proxy resolve it)

    ``source_address`` is an optional local IP address for outbound sockets.
    It is not an interface name. When curl-cffi connects to this loopback proxy,
    its own ``interface=...`` setting no longer controls the Internet-facing
    socket; use this field when binding to a specific source IP is required.
    """

    listen_host: str = "127.0.0.1"
    listen_port: int = 8080
    split_at: int = 2
    split_delay: float = 0.010
    plaintext_http_ports: tuple[int, ...] = DEFAULT_HTTP_PORTS
    reverse_fragments: bool = False
    desync_config: StrictDesyncConfig | None = None
    max_segment_payload: int = 1200
    backend_priority: int = 100
    capture_start_timeout: float = 12.0
    linux_interfaces: tuple[str, ...] | None = None
    allow_unsupported_windows_arm64: bool = False
    upstream_proxy: str | None = None
    upstream_proxy_auth: tuple[str, str] | None = None
    source_address: str | None = None
    connect_timeout: float = 20.0
    handshake_timeout: float = 15.0
    idle_timeout: float = 300.0
    read_size: int = 64 * 1024
    max_header_bytes: int = 128 * 1024
    tcp_nodelay: bool = True
    log_level: int = logging.WARNING
    allow_non_loopback: bool = False

    def validated(self) -> "StrictFragmentingProxyConfig":
        if not self.listen_host:
            raise ValueError("listen_host must not be empty")
        if not 0 <= self.listen_port <= 65535:
            raise ValueError("listen_port must be between 0 and 65535")
        if self.split_at <= 0:
            raise ValueError("split_at must be greater than zero")
        if self.split_delay < 0:
            raise ValueError("split_delay must not be negative")
        if self.max_segment_payload < 0:
            raise ValueError("max_segment_payload must not be negative")
        if self.max_segment_payload and self.max_segment_payload < self.split_at:
            raise ValueError("max_segment_payload must be zero or at least split_at")
        if not -30000 <= self.backend_priority <= 30000:
            raise ValueError("backend_priority must be between -30000 and 30000")
        if self.capture_start_timeout <= 0:
            raise ValueError("capture_start_timeout must be greater than zero")
        if self.linux_interfaces is not None:
            interfaces = tuple(dict.fromkeys(str(item) for item in self.linux_interfaces if str(item)))
            if not interfaces:
                raise ValueError("linux_interfaces must contain at least one interface")
            if interfaces != self.linux_interfaces:
                return dataclasses.replace(self, linux_interfaces=interfaces).validated()
        if self.connect_timeout <= 0:
            raise ValueError("connect_timeout must be greater than zero")
        if self.handshake_timeout <= 0:
            raise ValueError("handshake_timeout must be greater than zero")
        if self.idle_timeout < 0:
            raise ValueError("idle_timeout must not be negative")
        if self.read_size < 1024:
            raise ValueError("read_size must be at least 1024 bytes")
        if self.max_header_bytes < 4096:
            raise ValueError("max_header_bytes must be at least 4096 bytes")

        if self.desync_config is not None:
            desync = self.desync_config
            if desync.mode != "seq_ack":
                raise ValueError("desync mode must be 'seq_ack'")
            if not 1 <= desync.sequence_offset <= 0xFFFFFFFF:
                raise ValueError("desync sequence_offset must be between 1 and 2^32-1")
            if not 1 <= desync.acknowledgement_offset <= 0xFFFFFFFF:
                raise ValueError(
                    "desync acknowledgement_offset must be between 1 and 2^32-1"
                )
            try:
                fake_sni = desync.fake_sni.encode("idna").decode("ascii")
            except UnicodeError as exc:
                raise ValueError("desync fake_sni must be a valid DNS hostname") from exc
            labels = fake_sni.rstrip(".").split(".")
            if (
                not fake_sni
                or len(fake_sni) > 253
                or any(not label or len(label) > 63 for label in labels)
            ):
                raise ValueError("desync fake_sni must be a valid DNS hostname")
            if fake_sni != desync.fake_sni:
                return dataclasses.replace(
                    self,
                    desync_config=dataclasses.replace(desync, fake_sni=fake_sni),
                ).validated()

        ports = tuple(dict.fromkeys(self.plaintext_http_ports))
        for port in ports:
            if not 1 <= int(port) <= 65535:
                raise ValueError(f"invalid plaintext HTTP port: {port!r}")

        if not self.allow_non_loopback and not _is_loopback_host(self.listen_host):
            raise ValueError(
                "Refusing to expose an unauthenticated proxy on a non-loopback "
                "address. Set allow_non_loopback=True only if this is deliberate."
            )

        if self.upstream_proxy_auth is not None:
            if len(self.upstream_proxy_auth) != 2:
                raise ValueError("upstream_proxy_auth must be a (username, password) tuple")

        if self.upstream_proxy:
            _parse_upstream_proxy(self.upstream_proxy, self.upstream_proxy_auth)

        if ports != self.plaintext_http_ports:
            return dataclasses.replace(self, plaintext_http_ports=ports)
        return self


@dataclass(frozen=True, slots=True)
class _UpstreamProxySpec:
    scheme: str
    host: str
    port: int
    username: str | None
    password: str | None
    remote_dns: bool = False


class _AsyncWriter(Protocol):
    def write(self, data: bytes) -> object: ...

    async def drain(self) -> object: ...


class StrictFragmentingProxyProcess:
    """Lifecycle manager for a proxy running in a spawned child process.

    One manager should normally be shared by all ``BaseCore`` objects. Start it
    before creating/refreshing curl-cffi sessions and stop it after those
    sessions have been closed or replaced.

    The helper uses ``spawn`` to avoid directly forking a multithreaded Qt
    process. Call ``start`` from code protected by
    ``if __name__ == "__main__":`` and keep GUI creation out of imported code.
    """

    def __init__(self, config: StrictFragmentingProxyConfig | None = None) -> None:
        self.config = (config or StrictFragmentingProxyConfig()).validated()
        # Spawn avoids an unsafe direct fork of Qt threads. It imports __main__,
        # so the application also guards GUI creation in multiprocessing children.
        self._ctx = mp.get_context("spawn")
        self._process: mp.Process | None = None
        self._stop_event: object | None = None
        self._status_queue: object | None = None
        self._host: str | None = None
        self._port: int | None = None

    @property
    def is_running(self) -> bool:
        return self._process is not None and self._process.is_alive()

    @property
    def host(self) -> str:
        if self._host is None:
            raise RuntimeError("The proxy has not been started")
        return self._host

    @property
    def port(self) -> int:
        if self._port is None:
            raise RuntimeError("The proxy has not been started")
        return self._port

    @property
    def proxy_url(self) -> str:
        """SOCKS5 URL with client-side destination DNS resolution.

        This is the recommended URL for curl-cffi when ``CurlOpt.DOH_URL`` is
        used, because libcurl resolves the destination before the SOCKS request.
        """

        return f"socks5://{_format_url_host(self.host)}:{self.port}"

    @property
    def proxy_url_remote_dns(self) -> str:
        """SOCKS5H URL that lets this proxy resolve destination hostnames."""

        return f"socks5h://{_format_url_host(self.host)}:{self.port}"

    @property
    def http_connect_url(self) -> str:
        """HTTP CONNECT URL for clients that cannot use SOCKS5."""

        return f"http://{_format_url_host(self.host)}:{self.port}"

    def start(self, timeout: float = 15.0) -> str:
        """Start the child process and return the preferred curl-cffi proxy URL."""

        if self.is_running:
            return self.proxy_url
        if mp.current_process().name != "MainProcess":
            raise StrictProxyStartError(
                "StrictFragmentingProxyProcess.start() must be called from the main process"
            )
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self._clear_dead_process()
        stop_event = self._ctx.Event()
        status_queue = self._ctx.Queue(maxsize=2)
        process = self._ctx.Process(
            name="StrictFragmentingProxy",
            target=_strict_proxy_process_entry,
            args=(self.config, stop_event, status_queue),
            daemon=True,
        )

        self._stop_event = stop_event
        self._status_queue = status_queue
        self._process = process
        process.start()

        try:
            status = status_queue.get(timeout=timeout)
        except queue.Empty as exc:
            exitcode = process.exitcode
            self.stop(timeout=1.0)
            suffix = f" (child exit code {exitcode})" if exitcode is not None else ""
            raise StrictProxyStartError(f"Proxy did not become ready within {timeout:.1f}s{suffix}") from exc

        kind = status[0]
        if kind == "ready":
            _, host, port = status
            self._host = str(host)
            self._port = int(port)
            return self.proxy_url

        _, message = status
        self.stop(timeout=1.0)
        raise StrictProxyStartError(str(message))

    def stop(self, timeout: float = 5.0) -> None:
        """Request a graceful shutdown and terminate as a last resort."""

        process = self._process
        if process is None:
            self._reset_runtime_state()
            return

        stop_event = self._stop_event
        if stop_event is not None:
            with contextlib.suppress(Exception):
                stop_event.set()  # type: ignore[attr-defined]

        process.join(max(0.0, timeout))
        if process.is_alive():
            process.terminate()
            process.join(2.0)
        if process.is_alive() and hasattr(process, "kill"):
            process.kill()
            process.join(1.0)

        self._reset_runtime_state()

    def restart(
        self,
        config: StrictFragmentingProxyConfig | None = None,
        *,
        timeout: float = 15.0,
    ) -> str:
        self.stop()
        if config is not None:
            self.config = config.validated()
        return self.start(timeout=timeout)

    def __enter__(self) -> "StrictFragmentingProxyProcess":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()

    def _clear_dead_process(self) -> None:
        if self._process is not None and not self._process.is_alive():
            with contextlib.suppress(Exception):
                self._process.join(timeout=0)
            self._reset_runtime_state()

    def _reset_runtime_state(self) -> None:
        status_queue = self._status_queue
        if status_queue is not None:
            with contextlib.suppress(Exception):
                status_queue.close()  # type: ignore[attr-defined]
            with contextlib.suppress(Exception):
                status_queue.join_thread()  # type: ignore[attr-defined]
        self._process = None
        self._stop_event = None
        self._status_queue = None
        self._host = None
        self._port = None


@dataclass(frozen=True, slots=True)
class _FlowTuple:
    src_addr: str
    src_port: int
    dst_addr: str
    dst_port: int
    logical_target_port: int


class _StrictFlowPolicy:
    """Per-flow split decisions, including retransmission-safe boundaries."""

    _HTTP_METHODS: Final[tuple[bytes, ...]] = (
        b"GET ", b"HEAD ", b"POST ", b"PUT ", b"DELETE ", b"CONNECT ",
        b"OPTIONS ", b"PATCH ", b"TRACE ",
    )

    def __init__(
        self,
        *,
        split_at: int,
        plaintext_http: bool,
        max_segment_payload: int,
        desync_config: StrictDesyncConfig | None = None,
    ) -> None:
        self.split_at = split_at
        self.plaintext_http = plaintext_http
        self.max_segment_payload = max_segment_payload
        self.desync_config = desync_config
        self.first_data_seen = False
        self.desync_injected = False
        self._boundaries: set[int] = set()

    def split_offsets(self, seq_num: int, payload: bytes) -> list[int]:
        size = len(payload)
        if size <= 1:
            if size:
                self.first_data_seen = True
            return []

        offsets: set[int] = set()

        # Re-apply remembered split points to TCP retransmissions.
        for boundary in tuple(self._boundaries):
            offset = (boundary - seq_num) & 0xFFFFFFFF
            if 0 < offset < size:
                offsets.add(offset)

        if not self.first_data_seen:
            self.first_data_seen = True
            if self.split_at < size:
                offsets.add(self.split_at)
                self._remember((seq_num + self.split_at) & 0xFFFFFFFF)

        if self.plaintext_http:
            for request_start in _find_http1_request_starts(payload):
                offset = request_start + self.split_at
                if 0 < offset < size:
                    offsets.add(offset)
                    self._remember((seq_num + offset) & 0xFFFFFFFF)

        # Linux TC may expose a GSO-sized skb. Bound every emitted TCP segment
        # so raw re-injection does not depend on another segmentation pass.
        if self.max_segment_payload:
            cursor = 0
            while cursor + self.max_segment_payload < size:
                cursor += self.max_segment_payload
                offsets.add(cursor)

        return sorted(offsets)

    def _remember(self, boundary: int) -> None:
        self._boundaries.add(boundary)
        # Keep bounded state even on very long plaintext keep-alive sessions.
        if len(self._boundaries) > 4096:
            self._boundaries = set(sorted(self._boundaries)[-2048:])


def _find_http1_request_starts(payload: bytes) -> list[int]:
    starts: list[int] = []
    candidates = [0]
    marker = b"\r\n\r\n"
    search_from = 0
    while True:
        pos = payload.find(marker, search_from)
        if pos < 0:
            break
        candidates.append(pos + len(marker))
        search_from = pos + len(marker)

    for start in candidates:
        method = next(
            (item for item in _StrictFlowPolicy._HTTP_METHODS if payload.startswith(item, start)),
            None,
        )
        if method is None:
            continue
        line_end = payload.find(b"\r\n", start, min(len(payload), start + 8192))
        if line_end < 0:
            continue
        request_line = payload[start:line_end]
        if b" HTTP/1.0" in request_line or b" HTTP/1.1" in request_line:
            starts.append(start)
    return starts


class _StrictFlowGuard:
    def __init__(self, backend: "_StrictPacketBackend", key: _FlowTuple) -> None:
        self._backend = backend
        self._key = key
        self._closed = False

    async def close(self) -> None:
        if not self._closed:
            self._closed = True
            await self._backend.unregister(self._key)


class _StrictPacketBackend:
    """Owns one exact packet-divert handle per active proxy flow.

    Per-flow handles avoid globally modifying unrelated applications. The local
    SOCKS/CONNECT success is intentionally delayed until the exact handle is
    open, so the first TLS/HTTP bytes cannot race ahead of packet interception.
    """

    def __init__(self, config: StrictFragmentingProxyConfig) -> None:
        self.config = config
        self._pydivert = None
        self._divert_class = None
        self._tasks: dict[_FlowTuple, asyncio.Task[None]] = {}
        self._allocated_priorities: set[int] = set()
        self._closed = False
        self._validate_platform()

    def prepare(self) -> None:
        """Load the native backend before the proxy announces readiness."""
        system = platform.system().lower()
        if system == "linux" and hasattr(os, "geteuid") and os.geteuid() != 0:
            raise StrictBackendUnavailable(
                "Strict mode requires root privileges on Linux. Start Porn Fetch "
                "with sudo, or select Lite mode."
            )
        self._load()
        if system == "windows":
            try:
                import ctypes
                if not bool(ctypes.windll.shell32.IsUserAnAdmin()):
                    raise StrictBackendUnavailable(
                        "Strict mode must be started from an elevated Administrator process."
                    )
            except AttributeError:
                pass

    def _validate_platform(self) -> None:
        system = platform.system().lower()
        machine = platform.machine().lower()
        if system == "darwin":
            raise StrictBackendUnavailable(
                "macOS has no local Python packet-divert backend. A signed "
                "Network Extension plus a packet tunnel/user-space TCP forwarder "
                "is required; use the non-strict proxy on macOS."
            )
        if system == "windows" and _is_windows_arm64(machine):
            if not self.config.allow_unsupported_windows_arm64:
                raise StrictBackendUnavailable(
                    "Windows ARM64 is not supported by the official signed "
                    "WinDivert driver. Set allow_unsupported_windows_arm64=True "
                    "only when shipping your own vendor-signed ARM64 WinDivert build."
                )
        if system not in {"windows", "linux"}:
            raise StrictBackendUnavailable(f"Unsupported strict backend platform: {platform.system()}")

    def _load(self) -> None:
        if self._pydivert is not None:
            return
        try:
            import pydivert  # type: ignore
        except Exception as exc:
            raise StrictBackendUnavailable(
                "PyDivert could not be imported. Install pydivert on Windows; "
                "on Linux use the PyDivert 4 Linux/eBPF build and libbpf."
            ) from exc

        if platform.system().lower() == "linux":
            version = str(getattr(pydivert, "__version__", "0"))
            try:
                major = int(version.split(".", 1)[0])
            except ValueError:
                major = 0
            if major < 4:
                raise StrictBackendUnavailable(
                    f"Linux strict mode requires PyDivert 4.x; found {version!r}."
                )

        divert_class = getattr(pydivert, "Divert", None)
        if divert_class is None and platform.system().lower() == "windows":
            divert_class = getattr(pydivert, "WinDivert", None)
        if divert_class is None:
            raise StrictBackendUnavailable(
                "Installed PyDivert has no cross-platform Divert class. Linux "
                "requires PyDivert 4; Windows may use WinDivert from PyDivert 3.1+."
            )
        self._pydivert = pydivert
        self._divert_class = divert_class

    async def register(
        self,
        writer: asyncio.StreamWriter,
        *,
        logical_target_port: int,
    ) -> _StrictFlowGuard:
        if self._closed:
            raise StrictFlowRegistrationError("Strict packet backend is closed")
        self._load()
        key = _flow_tuple_from_writer(writer, logical_target_port)
        if key in self._tasks:
            raise StrictFlowRegistrationError(f"Flow already registered: {key}")

        priority = self._allocate_priority()
        ready: asyncio.Future[None] = asyncio.get_running_loop().create_future()
        task = asyncio.create_task(
            self._capture_flow(key, ready, priority),
            name=f"strict-flow-{key.src_port}-{key.dst_port}",
        )
        self._tasks[key] = task
        task.add_done_callback(lambda done, flow=key: self._task_done(flow, done))
        try:
            await asyncio.wait_for(asyncio.shield(ready), self.config.capture_start_timeout)
        except Exception:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
            self._tasks.pop(key, None)
            raise
        return _StrictFlowGuard(self, key)

    def _allocate_priority(self) -> int:
        """Reserve a unique WinDivert/TC priority for one active flow."""
        base = self.config.backend_priority
        candidates = itertools.chain(
            range(base, -30001, -1),
            range(30000, base, -1),
        )
        for priority in candidates:
            if priority not in self._allocated_priorities:
                self._allocated_priorities.add(priority)
                return priority
        raise StrictFlowRegistrationError(
            "No packet-divert priorities remain for another strict flow"
        )

    def _task_done(self, key: _FlowTuple, task: asyncio.Task[None]) -> None:
        self._tasks.pop(key, None)
        if task.cancelled():
            return
        exc = task.exception()
        if exc is not None:
            LOG.error("Strict flow capture failed for %s: %s", key, exc)

    async def unregister(self, key: _FlowTuple) -> None:
        task = self._tasks.pop(key, None)
        if task is None:
            return
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

    async def close(self) -> None:
        self._closed = True
        tasks = tuple(self._tasks.values())
        self._tasks.clear()
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _capture_flow(
        self,
        key: _FlowTuple,
        ready: asyncio.Future[None],
        priority: int,
    ) -> None:
        assert self._divert_class is not None
        filter_string = _build_exact_flow_filter(key)
        kwargs: dict[str, object] = {}
        if platform.system().lower() == "linux" and self.config.linux_interfaces:
            kwargs["interfaces"] = self.config.linux_interfaces

        policy = _StrictFlowPolicy(
            split_at=self.config.split_at,
            plaintext_http=key.logical_target_port in self.config.plaintext_http_ports,
            max_segment_payload=self.config.max_segment_payload,
            desync_config=self.config.desync_config,
        )

        try:
            diverter = self._divert_class(
                filter_string,
                priority=priority,
                **kwargs,
            )
            async with diverter:
                try:
                    if not ready.done():
                        ready.set_result(None)
                    async for packet in diverter:
                        await _process_strict_packet(
                            diverter,
                            packet,
                            policy,
                            flow=key,
                            reverse=self.config.reverse_fragments,
                        )
                finally:
                    _prepare_linux_diverter_close(diverter)
        except asyncio.CancelledError:
            if not ready.done():
                ready.cancel()
            raise
        except BaseException as exc:
            if not ready.done():
                ready.set_exception(
                    StrictFlowRegistrationError(
                        f"Could not open strict capture for {key}: {exc}"
                    )
                )
            else:
                raise
        finally:
            self._allocated_priorities.discard(priority)


def _prepare_linux_diverter_close(diverter: object) -> None:
    """Work around PyDivert 4 passing attach-only fields to bpf_tc_detach.

    libbpf populates ``prog_fd`` and ``prog_id`` during attachment but rejects
    both fields during detachment. PyDivert currently reuses the populated
    options structure, causing ``-EINVAL`` and stale TC filters. Clear only
    those two documented attach-only inputs immediately before ``__aexit__``.
    """
    if platform.system().lower() != "linux":
        return
    implementation = getattr(diverter, "_impl", None)
    for _hook, options in tuple(getattr(implementation, "_hooks", ())):
        options.prog_fd = 0
        options.prog_id = 0


def _flow_tuple_from_writer(
    writer: asyncio.StreamWriter,
    logical_target_port: int,
) -> _FlowTuple:
    sock = writer.get_extra_info("socket")
    if sock is None:
        raise StrictFlowRegistrationError("Outbound transport exposes no socket")
    local = sock.getsockname()
    remote = sock.getpeername()
    if not isinstance(local, tuple) or not isinstance(remote, tuple) or len(local) < 2 or len(remote) < 2:
        raise StrictFlowRegistrationError("Unsupported outbound socket address")
    return _FlowTuple(
        src_addr=_strip_ipv6_scope(str(local[0])),
        src_port=int(local[1]),
        dst_addr=_strip_ipv6_scope(str(remote[0])),
        dst_port=int(remote[1]),
        logical_target_port=int(logical_target_port),
    )


def _strip_ipv6_scope(value: str) -> str:
    return value.split("%", 1)[0]


def _is_windows_arm64(machine: str | None = None) -> bool:
    values = {
        (machine or platform.machine()).lower(),
        os.environ.get("PROCESSOR_ARCHITECTURE", "").lower(),
        os.environ.get("PROCESSOR_ARCHITEW6432", "").lower(),
    }
    return bool(values & {"arm64", "aarch64"})


def _generate_decoy_client_hello(fake_sni: str) -> bytes:
    sni_bytes = fake_sni.encode("ascii")
    sni_len = len(sni_bytes)

    random_bytes = os.urandom(32)
    session_id = os.urandom(32)

    ciphers = b"\x13\x01\x13\x02\x13\x03\xc0\x2b\xc0\x2f\xc0\x2c\xc0\x30\xcc\xa9\xcc\xa8\xc0\x13\xc0\x14\x00\x9c\x00\x9d\x00\x2f\x00\x35"
    ciphers_len = len(ciphers)

    sni_ext_data = (
        b"\x00\x00" +
        (sni_len + 5).to_bytes(2, "big") +
        (sni_len + 3).to_bytes(2, "big") +
        b"\x00" +
        sni_len.to_bytes(2, "big") +
        sni_bytes
    )

    extensions = sni_ext_data + b"\x00\x0b\x00\x02\x01\x00"
    ext_len = len(extensions)

    hello_data = (
        b"\x03\x03" +
        random_bytes +
        b"\x20" + session_id +
        ciphers_len.to_bytes(2, "big") + ciphers +
        b"\x01\x00" +
        ext_len.to_bytes(2, "big") + extensions
    )

    record = (
        b"\x16\x03\x01" +
        (len(hello_data) + 4).to_bytes(2, "big") +
        b"\x01" +
        len(hello_data).to_bytes(3, "big") +
        hello_data
    )

    return record


async def _inject_desync_decoy(
    diverter: object,
    packet: object,
    config: StrictDesyncConfig,
) -> None:
    """Send a cloned ClientHello outside the receiver's TCP window.

    A stateless listener may parse the decoy, while a conforming endpoint drops
    it because both TCP sequence-space values are deliberately stale. The real
    packet is never mutated here, so injection failure cannot damage the flow.
    """

    decoy = copy.copy(packet)
    tcp = getattr(decoy, "tcp", None)
    if tcp is None:
        raise TypeError("captured packet has no TCP header")
    decoy.payload = _generate_decoy_client_hello(config.fake_sni)
    tcp.seq_num = (int(tcp.seq_num) - config.sequence_offset) & 0xFFFFFFFF
    tcp.ack_num = (
        int(tcp.ack_num) - config.acknowledgement_offset
    ) & 0xFFFFFFFF
    tcp.psh = True
    tcp.fin = False
    tcp.syn = False
    if hasattr(decoy, "recalculate_checksums"):
        decoy.recalculate_checksums()
    await diverter.send_async(decoy)  # type: ignore[attr-defined]


def _build_exact_flow_filter(key: _FlowTuple) -> str:
    src = ipaddress.ip_address(key.src_addr)
    dst = ipaddress.ip_address(key.dst_addr)
    if src.version != dst.version:
        raise StrictFlowRegistrationError("Local and remote address families differ")

    common = (
        "outbound and tcp "
        "and !loopback "
        "and !tcp.Syn and !tcp.Fin and !tcp.Rst "
        f"and tcp.SrcPort == {key.src_port} "
        f"and tcp.DstPort == {key.dst_port}"
    )
    if platform.system().lower() == "linux":
        # PyDivert 4's eBPF transpiler currently enforces IPv4 addresses in
        # kernel but treats IPv6 addresses and PayloadLength as user-space
        # concerns. Keep the kernel rule portable and verify the full tuple in
        # _packet_matches_flow before modifying anything.
        return common

    prefix = "ip" if src.version == 4 else "ipv6"
    return (
        common
        + " and tcp.PayloadLength > 0 "
        + f"and {prefix}.SrcAddr == {src.compressed} "
        + f"and {prefix}.DstAddr == {dst.compressed}"
    )


def _packet_matches_flow(packet: object, key: _FlowTuple) -> bool:
    try:
        return (
            _strip_ipv6_scope(str(getattr(packet, "src_addr"))) == key.src_addr
            and int(getattr(packet, "src_port")) == key.src_port
            and _strip_ipv6_scope(str(getattr(packet, "dst_addr"))) == key.dst_addr
            and int(getattr(packet, "dst_port")) == key.dst_port
        )
    except (TypeError, ValueError):
        return False


async def _process_strict_packet(
    diverter: object,
    packet: object,
    policy: _StrictFlowPolicy,
    *,
    flow: _FlowTuple | None = None,
    reverse: bool,
) -> None:
    if flow is not None and not _packet_matches_flow(packet, flow):
        await diverter.send_async(packet)  # type: ignore[attr-defined]
        return
    payload = bytes(getattr(packet, "payload", b"") or b"")
    tcp = getattr(packet, "tcp", None)
    if tcp is None or not payload:
        await diverter.send_async(packet)  # type: ignore[attr-defined]
        return

    seq_num = int(tcp.seq_num)
    offsets = policy.split_offsets(seq_num, payload)
    if not offsets:
        await diverter.send_async(packet)  # type: ignore[attr-defined]
        return

    LOG.debug(
        "Splitting strict flow %s payload at offsets %s (payload length %d)",
        flow,
        offsets,
        len(payload),
    )

    boundaries = [0, *offsets, len(payload)]
    segments = [
        (boundaries[index], boundaries[index + 1])
        for index in range(len(boundaries) - 1)
        if boundaries[index] < boundaries[index + 1]
    ]
    if reverse:
        segments.reverse()

    original_psh = bool(getattr(tcp, "psh", False))
    original_fin = bool(getattr(tcp, "fin", False))
    original_syn = bool(getattr(tcp, "syn", False))

    if (
        policy.desync_config is not None
        and not policy.desync_injected
        and not policy.plaintext_http
        and payload.startswith(b"\x16\x03")
    ):
        policy.desync_injected = True
        try:
            await _inject_desync_decoy(diverter, packet, policy.desync_config)
            LOG.debug(
                "Injected strict-flow ClientHello decoy for %s with SNI %r",
                flow,
                policy.desync_config.fake_sni,
            )
        except Exception:
            # Decoy injection is additive. Preserve connectivity and continue
            # sending all genuine fragments if the platform cannot clone/send it.
            LOG.warning("Failed to inject DPI desynchronization decoy", exc_info=True)

    sent = False
    try:
        for start, end in segments:
            packet.payload = payload[start:end]
            packet.tcp.seq_num = (seq_num + start) & 0xFFFFFFFF
            is_final_bytes = end == len(payload)
            packet.tcp.psh = original_psh if is_final_bytes else False
            packet.tcp.fin = original_fin if is_final_bytes else False
            packet.tcp.syn = original_syn if start == 0 else False
            if hasattr(packet, "recalculate_checksums"):
                packet.recalculate_checksums()
            await diverter.send_async(packet)  # type: ignore[attr-defined]
            sent = True
    except BaseException:
        # If no replacement was sent, preserve connectivity by reinjecting the
        # original packet. Once a partial replacement is on the wire, sending
        # the original as well would duplicate bytes and corrupt the stream.
        if not sent:
            packet.payload = payload
            packet.tcp.seq_num = seq_num
            packet.tcp.psh = original_psh
            packet.tcp.fin = original_fin
            packet.tcp.syn = original_syn
            if hasattr(packet, "recalculate_checksums"):
                packet.recalculate_checksums()
            with contextlib.suppress(Exception):
                await diverter.send_async(packet)  # type: ignore[attr-defined]
        raise


class StrictFragmentingProxyServer:
    """Async SOCKS5 and HTTP-CONNECT proxy implementation.

    The same listening port accepts both protocols. curl-cffi should normally
    use the SOCKS5 URL exposed by :class:`StrictFragmentingProxyProcess`.
    """

    def __init__(self, config: StrictFragmentingProxyConfig | None = None) -> None:
        self.config = (config or StrictFragmentingProxyConfig()).validated()
        self._upstream = (
            _parse_upstream_proxy(
                self.config.upstream_proxy,
                self.config.upstream_proxy_auth,
            )
            if self.config.upstream_proxy
            else None
        )
        self._backend = _StrictPacketBackend(self.config)
        self._server: asyncio.AbstractServer | None = None
        self._client_tasks: set[asyncio.Task[None]] = set()
        self._bound_host: str | None = None
        self._bound_port: int | None = None

    @property
    def host(self) -> str:
        if self._bound_host is None:
            raise RuntimeError("Server is not running")
        return self._bound_host

    @property
    def port(self) -> int:
        if self._bound_port is None:
            raise RuntimeError("Server is not running")
        return self._bound_port

    async def start(self) -> tuple[str, int]:
        if self._server is not None:
            return self.host, self.port

        self._backend.prepare()
        self._server = await asyncio.start_server(
            self._accept_client,
            host=self.config.listen_host,
            port=self.config.listen_port,
            limit=self.config.max_header_bytes + 4096,
            start_serving=True,
        )
        sockets = self._server.sockets or []
        if not sockets:
            raise RuntimeError("Proxy server started without a listening socket")

        sockname = sockets[0].getsockname()
        self._bound_host = str(sockname[0])
        self._bound_port = int(sockname[1])
        LOG.info(
            "Listening on %s:%d (SOCKS5 and HTTP CONNECT)",
            self._bound_host,
            self._bound_port,
        )
        return self._bound_host, self._bound_port

    async def close(self) -> None:
        server = self._server
        self._server = None
        if server is not None:
            server.close()
            await server.wait_closed()

        tasks = tuple(self._client_tasks)
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        await self._backend.close()

        self._bound_host = None
        self._bound_port = None

    async def serve_until(self, stop_event: object) -> None:
        await self.start()
        await asyncio.to_thread(stop_event.wait)  # type: ignore[attr-defined]
        await self.close()

    def _accept_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        task = asyncio.create_task(
            self._handle_client(reader, writer),
            name="strict-fragmenting-proxy-client",
        )
        self._client_tasks.add(task)
        task.add_done_callback(self._client_tasks.discard)

    async def _handle_client(
        self,
        client_reader: asyncio.StreamReader,
        client_writer: asyncio.StreamWriter,
    ) -> None:
        peer = client_writer.get_extra_info("peername")
        upstream_writer: asyncio.StreamWriter | None = None
        flow_guard: _StrictFlowGuard | None = None
        try:
            first = await _read_exactly(
                client_reader,
                1,
                timeout=self.config.handshake_timeout,
            )
            if first == b"\x05":
                target_host, target_port, upstream_reader, upstream_writer, flow_guard = (
                    await self._handle_socks5_handshake(client_reader, client_writer)
                )
            else:
                target_host, target_port, upstream_reader, upstream_writer, flow_guard = (
                    await self._handle_http_connect_handshake(
                        client_reader,
                        client_writer,
                        first,
                    )
                )

            LOG.debug("Tunnel %r -> %s:%d", peer, target_host, target_port)
            await self._relay_tunnel(
                client_reader,
                client_writer,
                upstream_reader,
                upstream_writer,
                target_port=target_port,
            )
        except asyncio.CancelledError:
            raise
        except (ConnectionError, asyncio.TimeoutError, ProxyProtocolError) as exc:
            LOG.debug("Client %r closed with proxy error: %s", peer, exc)
        except Exception:
            LOG.exception("Unhandled proxy error for client %r", peer)
        finally:
            if flow_guard is not None:
                await flow_guard.close()
            if upstream_writer is not None:
                await _close_writer(upstream_writer)
            await _close_writer(client_writer)

    async def _handle_socks5_handshake(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> tuple[str, int, asyncio.StreamReader, asyncio.StreamWriter, _StrictFlowGuard]:
        nmethods = (
            await _read_exactly(reader, 1, timeout=self.config.handshake_timeout)
        )[0]
        methods = await _read_exactly(
            reader,
            nmethods,
            timeout=self.config.handshake_timeout,
        )
        if SOCKS_AUTH_NONE not in methods:
            writer.write(bytes((SOCKS_VERSION, SOCKS_AUTH_UNACCEPTABLE)))
            await writer.drain()
            raise ProxyProtocolError("Local SOCKS client did not offer no-auth mode")

        writer.write(bytes((SOCKS_VERSION, SOCKS_AUTH_NONE)))
        await writer.drain()

        request_head = await _read_exactly(
            reader,
            4,
            timeout=self.config.handshake_timeout,
        )
        version, command, reserved, address_type = request_head
        if version != SOCKS_VERSION or reserved != 0:
            await self._send_socks_reply(writer, 1)
            raise ProxyProtocolError("Malformed SOCKS5 request")
        if command != SOCKS_CMD_CONNECT:
            await self._send_socks_reply(writer, 7)
            raise ProxyProtocolError("Only SOCKS5 CONNECT is supported")

        target_host = await _read_socks_address(
            reader,
            address_type,
            timeout=self.config.handshake_timeout,
        )
        target_port = struct.unpack(
            "!H",
            await _read_exactly(reader, 2, timeout=self.config.handshake_timeout),
        )[0]

        try:
            upstream_reader, upstream_writer = await self._open_destination(
                target_host,
                target_port,
            )
        except Exception as exc:
            await self._send_socks_reply(writer, _socks_error_code(exc))
            raise

        flow_guard = await self._backend.register(
            upstream_writer,
            logical_target_port=target_port,
        )
        bound = upstream_writer.get_extra_info("sockname")
        await self._send_socks_reply(writer, 0, bound)
        return target_host, target_port, upstream_reader, upstream_writer, flow_guard

    async def _handle_http_connect_handshake(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        first_byte: bytes,
    ) -> tuple[str, int, asyncio.StreamReader, asyncio.StreamWriter, _StrictFlowGuard]:
        header = await _read_header_block(
            reader,
            prefix=first_byte,
            timeout=self.config.handshake_timeout,
            maximum=self.config.max_header_bytes,
        )
        try:
            request_line = header.split(b"\r\n", 1)[0].decode("iso-8859-1")
            method, authority, version = request_line.split(" ", 2)
        except (UnicodeDecodeError, ValueError) as exc:
            await _send_http_error(writer, 400, "Bad Request")
            raise ProxyProtocolError("Malformed HTTP proxy request") from exc

        if method.upper() != "CONNECT":
            await _send_http_error(writer, 405, "CONNECT Required")
            raise ProxyProtocolError(
                "This local HTTP proxy accepts CONNECT tunnels only; use its "
                "SOCKS5 URL or CURLOPT_HTTPPROXYTUNNEL"
            )
        if not version.startswith("HTTP/1."):
            await _send_http_error(writer, 505, "HTTP Version Not Supported")
            raise ProxyProtocolError("Unsupported HTTP proxy version")

        target_host, target_port = _parse_authority(authority, default_port=443)
        try:
            upstream_reader, upstream_writer = await self._open_destination(
                target_host,
                target_port,
            )
        except Exception as exc:
            await _send_http_error(writer, 502, "Bad Gateway")
            raise UpstreamConnectError(str(exc)) from exc

        flow_guard = await self._backend.register(
            upstream_writer,
            logical_target_port=target_port,
        )
        writer.write(
            b"HTTP/1.1 200 Connection Established\r\n"
            b"Proxy-Agent: AppStrictFragmentProxy/1.0\r\n"
            b"\r\n"
        )
        await writer.drain()
        return target_host, target_port, upstream_reader, upstream_writer, flow_guard

    async def _send_socks_reply(
        self,
        writer: asyncio.StreamWriter,
        reply: int,
        bound: object | None = None,
    ) -> None:
        host = "0.0.0.0"
        port = 0
        if isinstance(bound, tuple) and len(bound) >= 2:
            host = str(bound[0])
            port = int(bound[1])
        address_type, address_bytes = _encode_socks_address(host)
        writer.write(
            bytes((SOCKS_VERSION, reply, 0, address_type))
            + address_bytes
            + struct.pack("!H", port)
        )
        await writer.drain()

    async def _open_destination(
        self,
        target_host: str,
        target_port: int,
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        if self._upstream is None:
            return await self._open_tcp(target_host, target_port)
        if self._upstream.scheme in {"http", "https"}:
            return await self._open_via_http_proxy(
                self._upstream,
                target_host,
                target_port,
            )
        if self._upstream.scheme in {"socks5", "socks5h"}:
            return await self._open_via_socks5_proxy(
                self._upstream,
                target_host,
                target_port,
            )
        raise UpstreamConnectError(
            f"Unsupported upstream proxy scheme: {self._upstream.scheme}"
        )

    async def _open_tcp(
        self,
        host: str,
        port: int,
        *,
        ssl_context: ssl.SSLContext | bool | None = None,
        server_hostname: str | None = None,
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        local_addr = (
            (self.config.source_address, 0)
            if self.config.source_address
            else None
        )
        connect = asyncio.open_connection(
            host=host,
            port=port,
            ssl=ssl_context,
            server_hostname=server_hostname if ssl_context else None,
            local_addr=local_addr,
            limit=self.config.max_header_bytes + 4096,
        )
        reader, writer = await asyncio.wait_for(
            connect,
            timeout=self.config.connect_timeout,
        )
        _configure_tcp_writer(writer, tcp_nodelay=self.config.tcp_nodelay)
        return reader, writer

    async def _open_via_http_proxy(
        self,
        proxy: _UpstreamProxySpec,
        target_host: str,
        target_port: int,
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        ssl_context: ssl.SSLContext | bool | None = None
        server_hostname: str | None = None
        if proxy.scheme == "https":
            ssl_context = ssl.create_default_context()
            server_hostname = proxy.host

        reader, writer = await self._open_tcp(
            proxy.host,
            proxy.port,
            ssl_context=ssl_context,
            server_hostname=server_hostname,
        )
        authority = _format_authority(target_host, target_port)
        lines = [
            f"CONNECT {authority} HTTP/1.1",
            f"Host: {authority}",
            "Proxy-Connection: Keep-Alive",
            "User-Agent: AppStrictFragmentProxy/1.0",
        ]
        if proxy.username is not None:
            credentials = f"{proxy.username}:{proxy.password or ''}".encode("utf-8")
            token = base64.b64encode(credentials).decode("ascii")
            lines.append(f"Proxy-Authorization: Basic {token}")
        request = ("\r\n".join(lines) + "\r\n\r\n").encode("iso-8859-1")
        writer.write(request)
        await writer.drain()

        try:
            response = await _read_header_block(
                reader,
                timeout=self.config.handshake_timeout,
                maximum=self.config.max_header_bytes,
            )
            status_line = response.split(b"\r\n", 1)[0].decode("iso-8859-1")
            _, status_code_text, *_ = status_line.split(" ")
            status_code = int(status_code_text)
        except Exception as exc:
            await _close_writer(writer)
            raise UpstreamConnectError("Invalid response from HTTP upstream proxy") from exc

        if not 200 <= status_code < 300:
            await _close_writer(writer)
            raise UpstreamConnectError(
                f"HTTP upstream proxy rejected CONNECT with status {status_code}"
            )
        return reader, writer

    async def _open_via_socks5_proxy(
        self,
        proxy: _UpstreamProxySpec,
        target_host: str,
        target_port: int,
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        reader, writer = await self._open_tcp(proxy.host, proxy.port)
        methods = [SOCKS_AUTH_NONE]
        if proxy.username is not None:
            methods.append(SOCKS_AUTH_USERPASS)
        writer.write(bytes((SOCKS_VERSION, len(methods), *methods)))
        await writer.drain()

        response = await _read_exactly(
            reader,
            2,
            timeout=self.config.handshake_timeout,
        )
        if response[0] != SOCKS_VERSION:
            await _close_writer(writer)
            raise UpstreamConnectError("Invalid SOCKS5 upstream response")
        selected_method = response[1]

        if selected_method == SOCKS_AUTH_USERPASS:
            username = (proxy.username or "").encode("utf-8")
            password = (proxy.password or "").encode("utf-8")
            if len(username) > 255 or len(password) > 255:
                await _close_writer(writer)
                raise UpstreamConnectError("SOCKS5 username/password is too long")
            writer.write(
                bytes((1, len(username)))
                + username
                + bytes((len(password),))
                + password
            )
            await writer.drain()
            auth_reply = await _read_exactly(
                reader,
                2,
                timeout=self.config.handshake_timeout,
            )
            if auth_reply != b"\x01\x00":
                await _close_writer(writer)
                raise UpstreamConnectError("SOCKS5 upstream authentication failed")
        elif selected_method != SOCKS_AUTH_NONE:
            await _close_writer(writer)
            raise UpstreamConnectError("SOCKS5 upstream has no acceptable auth method")

        connect_host = target_host
        if not proxy.remote_dns:
            connect_host = await _resolve_one_address(
                target_host,
                target_port,
                timeout=self.config.connect_timeout,
            )
        address_type, address_bytes = _encode_socks_address(connect_host)
        writer.write(
            bytes((SOCKS_VERSION, SOCKS_CMD_CONNECT, 0, address_type))
            + address_bytes
            + struct.pack("!H", target_port)
        )
        await writer.drain()

        reply_head = await _read_exactly(
            reader,
            4,
            timeout=self.config.handshake_timeout,
        )
        if reply_head[0] != SOCKS_VERSION or reply_head[2] != 0:
            await _close_writer(writer)
            raise UpstreamConnectError("Malformed SOCKS5 upstream CONNECT response")
        if reply_head[1] != 0:
            await _close_writer(writer)
            raise UpstreamConnectError(
                f"SOCKS5 upstream CONNECT failed with code {reply_head[1]}"
            )
        await _discard_socks_address(
            reader,
            reply_head[3],
            timeout=self.config.handshake_timeout,
        )
        await _read_exactly(reader, 2, timeout=self.config.handshake_timeout)
        return reader, writer

    async def _relay_tunnel(
        self,
        client_reader: asyncio.StreamReader,
        client_writer: asyncio.StreamWriter,
        upstream_reader: asyncio.StreamReader,
        upstream_writer: asyncio.StreamWriter,
        *,
        target_port: int,
    ) -> None:
        del target_port
        fragmenter = TLSClientHelloStreamFragmenter(
            fallback_split_at=self.config.split_at,
            split_delay=self.config.split_delay,
        )
        client_to_upstream = asyncio.create_task(
            _relay_fragmented(
                client_reader,
                upstream_writer,
                fragmenter,
                read_size=self.config.read_size,
                idle_timeout=self.config.idle_timeout,
            ),
            name="strict-fragmenting-proxy-upstream",
        )
        upstream_to_client = asyncio.create_task(
            _relay_raw(
                upstream_reader,
                client_writer,
                read_size=self.config.read_size,
                idle_timeout=self.config.idle_timeout,
            ),
            name="strict-fragmenting-proxy-downstream",
        )
        tasks = (client_to_upstream, upstream_to_client)
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, asyncio.CancelledError):
                    raise result
                if isinstance(result, Exception) and not isinstance(
                    result, (ConnectionError, asyncio.TimeoutError)
                ):
                    LOG.debug("Relay ended with: %r", result)
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)


async def _relay_raw(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    *,
    read_size: int,
    idle_timeout: float,
) -> None:
    try:
        while True:
            data = await _read_some(reader, read_size, idle_timeout)
            if not data:
                break
            await _write_bytes(writer, data)
        await _write_eof(writer)
    except (ConnectionError, asyncio.TimeoutError):
        pass


async def _relay_fragmented(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    fragmenter: TLSClientHelloStreamFragmenter,
    *,
    read_size: int,
    idle_timeout: float,
) -> None:
    try:
        while True:
            data = await _read_some(reader, read_size, idle_timeout)
            if not data:
                await fragmenter.finish(writer)
                break
            await fragmenter.feed(data, writer)
        await _write_eof(writer)
    except (ConnectionError, asyncio.TimeoutError):
        pass


async def _read_some(
    reader: asyncio.StreamReader,
    size: int,
    timeout: float,
) -> bytes:
    if timeout == 0:
        return await reader.read(size)
    return await asyncio.wait_for(reader.read(size), timeout=timeout)


async def _read_exactly(
    reader: asyncio.StreamReader,
    size: int,
    *,
    timeout: float,
) -> bytes:
    return await asyncio.wait_for(reader.readexactly(size), timeout=timeout)


async def _read_header_block(
    reader: asyncio.StreamReader,
    *,
    prefix: bytes = b"",
    timeout: float,
    maximum: int,
) -> bytes:
    try:
        rest = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=timeout)
    except asyncio.LimitOverrunError as exc:
        raise ProxyProtocolError("Proxy header exceeds configured limit") from exc
    data = prefix + rest
    if len(data) > maximum:
        raise ProxyProtocolError("Proxy header exceeds configured limit")
    return data


async def _write_bytes(writer: _AsyncWriter, data: bytes) -> None:
    if not data:
        return
    writer.write(data)
    await writer.drain()


async def _write_eof(writer: asyncio.StreamWriter) -> None:
    with contextlib.suppress(Exception):
        if writer.can_write_eof():
            writer.write_eof()
            await writer.drain()


async def _close_writer(writer: asyncio.StreamWriter) -> None:
    with contextlib.suppress(Exception):
        writer.close()
    with contextlib.suppress(Exception):
        await writer.wait_closed()


def _configure_tcp_writer(
    writer: asyncio.StreamWriter,
    *,
    tcp_nodelay: bool,
) -> None:
    if not tcp_nodelay:
        return
    sock = writer.get_extra_info("socket")
    if sock is not None:
        with contextlib.suppress(OSError):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


def _parse_upstream_proxy(
    value: str,
    explicit_auth: tuple[str, str] | None,
) -> _UpstreamProxySpec:
    raw = value.strip()
    if "://" not in raw:
        raw = "http://" + raw
    parsed = urlsplit(raw)
    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https", "socks5", "socks5h"}:
        raise ValueError(
            "upstream_proxy must use http, https, socks5 or socks5h"
        )
    if not parsed.hostname:
        raise ValueError("upstream_proxy has no hostname")

    defaults = {"http": 80, "https": 443, "socks5": 1080, "socks5h": 1080}
    try:
        port = parsed.port or defaults[scheme]
    except ValueError as exc:
        raise ValueError("upstream_proxy has an invalid port") from exc

    if explicit_auth is not None:
        username, password = explicit_auth
    else:
        username = unquote(parsed.username) if parsed.username is not None else None
        password = unquote(parsed.password) if parsed.password is not None else None

    return _UpstreamProxySpec(
        scheme=scheme,
        host=parsed.hostname,
        port=port,
        username=username,
        password=password,
        remote_dns=scheme == "socks5h",
    )


def _parse_authority(authority: str, *, default_port: int) -> tuple[str, int]:
    parsed = urlsplit("//" + authority)
    if not parsed.hostname:
        raise ProxyProtocolError("CONNECT request has no target hostname")
    try:
        port = parsed.port or default_port
    except ValueError as exc:
        raise ProxyProtocolError("CONNECT request has an invalid port") from exc
    return parsed.hostname, port


def _format_authority(host: str, port: int) -> str:
    return f"{_format_url_host(host)}:{port}"


def _format_url_host(host: str) -> str:
    if ":" in host and not host.startswith("["):
        return f"[{host}]"
    return host


def _is_loopback_host(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


async def _read_socks_address(
    reader: asyncio.StreamReader,
    address_type: int,
    *,
    timeout: float,
) -> str:
    if address_type == SOCKS_ATYP_IPV4:
        raw = await _read_exactly(reader, 4, timeout=timeout)
        return str(ipaddress.IPv4Address(raw))
    if address_type == SOCKS_ATYP_IPV6:
        raw = await _read_exactly(reader, 16, timeout=timeout)
        return str(ipaddress.IPv6Address(raw))
    if address_type == SOCKS_ATYP_DOMAIN:
        length = (await _read_exactly(reader, 1, timeout=timeout))[0]
        raw = await _read_exactly(reader, length, timeout=timeout)
        try:
            return raw.decode("idna")
        except UnicodeDecodeError as exc:
            raise ProxyProtocolError("Invalid SOCKS5 domain name") from exc
    raise ProxyProtocolError(f"Unsupported SOCKS5 address type: {address_type}")


async def _discard_socks_address(
    reader: asyncio.StreamReader,
    address_type: int,
    *,
    timeout: float,
) -> None:
    if address_type == SOCKS_ATYP_IPV4:
        await _read_exactly(reader, 4, timeout=timeout)
    elif address_type == SOCKS_ATYP_IPV6:
        await _read_exactly(reader, 16, timeout=timeout)
    elif address_type == SOCKS_ATYP_DOMAIN:
        length = (await _read_exactly(reader, 1, timeout=timeout))[0]
        await _read_exactly(reader, length, timeout=timeout)
    else:
        raise UpstreamConnectError("Invalid SOCKS5 upstream address type")


def _encode_socks_address(host: str) -> tuple[int, bytes]:
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        encoded = host.encode("idna")
        if len(encoded) > 255:
            raise ProxyProtocolError("SOCKS5 domain name is too long")
        return SOCKS_ATYP_DOMAIN, bytes((len(encoded),)) + encoded

    if isinstance(address, ipaddress.IPv4Address):
        return SOCKS_ATYP_IPV4, address.packed
    return SOCKS_ATYP_IPV6, address.packed


async def _resolve_one_address(host: str, port: int, *, timeout: float) -> str:
    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass

    loop = asyncio.get_running_loop()
    infos = await asyncio.wait_for(
        loop.getaddrinfo(
            host,
            port,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        ),
        timeout=timeout,
    )
    if not infos:
        raise socket.gaierror(f"No address found for {host}")
    return str(infos[0][4][0])


def _socks_error_code(exc: BaseException) -> int:
    if isinstance(exc, ConnectionRefusedError):
        return 5
    if isinstance(exc, socket.gaierror):
        return 4
    if isinstance(exc, TimeoutError):
        return 6
    if isinstance(exc, OSError):
        if exc.errno in {101, 51, 10051}:  # network unreachable
            return 3
        if exc.errno in {113, 65, 10065}:  # host unreachable
            return 4
    return 1


async def _send_http_error(
    writer: asyncio.StreamWriter,
    status: int,
    reason: str,
) -> None:
    body = f"{status} {reason}\n".encode("utf-8")
    writer.write(
        f"HTTP/1.1 {status} {reason}\r\n".encode("ascii")
        + b"Connection: close\r\n"
        + b"Content-Type: text/plain; charset=utf-8\r\n"
        + f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        + body
    )
    with contextlib.suppress(ConnectionError):
        await writer.drain()


def _configure_logging(level: int) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(processName)s %(name)s: %(message)s",
    )
    LOG.setLevel(level)


def _strict_proxy_process_entry(
    config: StrictFragmentingProxyConfig,
    stop_event: object,
    status_queue: object,
) -> None:
    _configure_logging(config.log_level)

    async def runner() -> None:
        server = StrictFragmentingProxyServer(config)
        try:
            host, port = await server.start()
            status_queue.put(("ready", host, port))  # type: ignore[attr-defined]
            await asyncio.to_thread(stop_event.wait)  # type: ignore[attr-defined]
        finally:
            await server.close()

    try:
        asyncio.run(runner())
    except BaseException:
        message = traceback.format_exc()
        with contextlib.suppress(Exception):
            status_queue.put(("error", message))  # type: ignore[attr-defined]
        raise


async def _run_foreground(config: StrictFragmentingProxyConfig) -> None:
    server = StrictFragmentingProxyServer(config)
    host, port = await server.start()
    print(f"SOCKS5:  socks5://{_format_url_host(host)}:{port}")
    print(f"SOCKS5H: socks5h://{_format_url_host(host)}:{port}")
    print(f"CONNECT: http://{_format_url_host(host)}:{port}")

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        with contextlib.suppress(NotImplementedError, RuntimeError, ValueError):
            loop.add_signal_handler(sig, stop.set)
    try:
        await stop.wait()
    finally:
        await server.close()


def _parse_ports(value: str) -> tuple[int, ...]:
    ports: list[int] = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        port = int(item)
        if not 1 <= port <= 65535:
            raise argparse.ArgumentTypeError(f"invalid port: {port}")
        ports.append(port)
    if not ports:
        raise argparse.ArgumentTypeError("at least one port is required")
    return tuple(dict.fromkeys(ports))


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="App-local strict TCP packet fragmentation proxy",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--split-at", type=int, default=2)
    parser.add_argument("--split-delay-ms", type=float, default=10.0)
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument(
        "--desync",
        action="store_true",
        help="send one wrong-sequence/wrong-ACK ClientHello decoy per TLS flow",
    )
    parser.add_argument("--fake-sni", default="www.example.com")
    parser.add_argument("--max-segment-payload", type=int, default=1200)
    parser.add_argument("--backend-priority", type=int, default=100)
    parser.add_argument("--linux-interface", action="append", dest="linux_interfaces")
    parser.add_argument("--allow-unsupported-windows-arm64", action="store_true")
    parser.add_argument(
        "--http-ports",
        type=_parse_ports,
        default=DEFAULT_HTTP_PORTS,
        help="Comma-separated plaintext HTTP ports",
    )
    parser.add_argument("--upstream-proxy")
    parser.add_argument("--upstream-user")
    parser.add_argument("--upstream-password")
    parser.add_argument("--source-address")
    parser.add_argument("--connect-timeout", type=float, default=20.0)
    parser.add_argument("--idle-timeout", type=float, default=300.0)
    parser.add_argument("--allow-non-loopback", action="store_true")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    auth = None
    if args.upstream_user is not None:
        auth = (args.upstream_user, args.upstream_password or "")

    level = logging.WARNING
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose >= 2:
        level = logging.DEBUG

    config = StrictFragmentingProxyConfig(
        listen_host=args.host,
        listen_port=args.port,
        split_at=args.split_at,
        split_delay=args.split_delay_ms / 1000.0,
        reverse_fragments=args.reverse or args.desync,
        desync_config=(
            StrictDesyncConfig(fake_sni=args.fake_sni) if args.desync else None
        ),
        max_segment_payload=args.max_segment_payload,
        backend_priority=args.backend_priority,
        linux_interfaces=tuple(args.linux_interfaces) if args.linux_interfaces else None,
        allow_unsupported_windows_arm64=args.allow_unsupported_windows_arm64,
        plaintext_http_ports=args.http_ports,
        upstream_proxy=args.upstream_proxy,
        upstream_proxy_auth=auth,
        source_address=args.source_address,
        connect_timeout=args.connect_timeout,
        idle_timeout=args.idle_timeout,
        allow_non_loopback=args.allow_non_loopback,
        log_level=level,
    ).validated()
    _configure_logging(level)

    try:
        asyncio.run(_run_foreground(config))
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    mp.freeze_support()
    raise SystemExit(main())
