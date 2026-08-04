#!/usr/bin/env python3
"""
AI Transparency:

Because this topic goes way behind my own engineering capabilities I had to generate this entirely with AI.
ChatGPT 4.6 SOL HIGH was used (Think time: 11 minutes)


"""

"""
App-local, non-strict TCP stream fragmentation proxy for curl-cffi.

The module runs a loopback SOCKS5/HTTP-CONNECT proxy in a separate
``multiprocessing`` process. Only clients explicitly configured to use this
proxy are affected; system-wide traffic is untouched.

Primary use with curl-cffi::

    proxy = FragmentingProxyProcess(
        FragmentingProxyConfig(
            listen_host="127.0.0.1",
            listen_port=8080,
            split_at=2,
            split_delay=0.050,
            plaintext_http_ports=(80, 8000, 8080, 8888),
            upstream_proxy=None,  # or the user's existing proxy URL
        )
    )

    # Call this below ``if __name__ == "__main__":`` on Windows/macOS.
    local_proxy_url = proxy.start()  # socks5://127.0.0.1:8080

    # curl-cffi resolves destination names itself with socks5://. This is the
    # preferred form when CurlOpt.DOH_URL is enabled. Use
    # proxy.proxy_url_remote_dns for socks5h:// if the local proxy should
    # resolve destination names instead.
    session = AsyncSession(proxy=local_proxy_url, ...)

    proxy.stop()

What the proxy does
-------------------

* For TLS and other non-HTTP TCP streams, it divides the first client-to-server
  write after ``split_at`` bytes.
* For plaintext HTTP/1.0 and HTTP/1.1 ports, it divides every request header,
  including later requests on a persistent keep-alive connection.
* It sets TCP_NODELAY on the outbound socket, drains the first part and waits a
  configurable short interval before writing the rest.
* It can chain through an existing HTTP, HTTPS, SOCKS5 or SOCKS5H upstream
  proxy. Proxy credentials can be supplied in the URL or separately.

Important limitation
--------------------

This is intentionally the non-strict implementation. TCP is a byte stream, so
separate writes are not a protocol-level guarantee of separate packets on the
wire. Kernels, NIC offload and intermediate systems may coalesce data. This
module does not install packet-filter drivers and does not require
administrator/root privileges for direct operation.

HTTP/3/QUIC is UDP based and is not supported by this TCP CONNECT proxy. Use
HTTP/1.1 or HTTP/2 in curl-cffi while this feature is enabled.

Python 3.10+; standard library only.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import contextlib
import dataclasses
import ipaddress
import logging
import multiprocessing as mp
import os
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

__all__ = [
    "FragmentingProxyConfig",
    "FragmentingProxyProcess",
    "FragmentingProxyServer",
    "ProxyStartError",
]

VERSION: Final[str] = "1.0.0"
LOGGER_NAME: Final[str] = "fragmenting-proxy"
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


class ProxyStartError(RuntimeError):
    """Raised when the proxy child process cannot be started."""


class ProxyProtocolError(RuntimeError):
    """Raised for malformed or unsupported local/upstream proxy traffic."""


class UpstreamConnectError(ConnectionError):
    """Raised when the destination or configured upstream proxy rejects a connection."""


@dataclass(frozen=True, slots=True)
class FragmentingProxyConfig:
    """Configuration shared with the proxy child process.

    ``listen_port`` may be 0 to let the OS select a free port. The selected URL
    is returned by :meth:`FragmentingProxyProcess.start`.

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

    def validated(self) -> "FragmentingProxyConfig":
        if not self.listen_host:
            raise ValueError("listen_host must not be empty")
        if not 0 <= self.listen_port <= 65535:
            raise ValueError("listen_port must be between 0 and 65535")
        if self.split_at <= 0:
            raise ValueError("split_at must be greater than zero")
        if self.split_delay < 0:
            raise ValueError("split_delay must not be negative")
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


class FragmentingProxyProcess:
    """Lifecycle manager for a proxy running in a spawned child process.

    One manager should normally be shared by all ``BaseCore`` objects. Start it
    before creating/refreshing curl-cffi sessions and stop it after those
    sessions have been closed or replaced.

    The ``spawn`` start method is used deliberately on every platform so the
    behavior is consistent with Windows and macOS. Therefore, call ``start``
    from code protected by ``if __name__ == "__main__":``.
    """

    def __init__(self, config: FragmentingProxyConfig | None = None) -> None:
        self.config = (config or FragmentingProxyConfig()).validated()
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
            raise ProxyStartError(
                "FragmentingProxyProcess.start() must be called from the main process"
            )
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self._clear_dead_process()
        stop_event = self._ctx.Event()
        status_queue = self._ctx.Queue(maxsize=2)
        process = self._ctx.Process(
            name="FragmentingProxy",
            target=_proxy_process_entry,
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
            raise ProxyStartError(f"Proxy did not become ready within {timeout:.1f}s{suffix}") from exc

        kind = status[0]
        if kind == "ready":
            _, host, port = status
            self._host = str(host)
            self._port = int(port)
            return self.proxy_url

        _, message = status
        self.stop(timeout=1.0)
        raise ProxyStartError(str(message))

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
        config: FragmentingProxyConfig | None = None,
        *,
        timeout: float = 15.0,
    ) -> str:
        self.stop()
        if config is not None:
            self.config = config.validated()
        return self.start(timeout=timeout)

    def __enter__(self) -> "FragmentingProxyProcess":
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


class FragmentingProxyServer:
    """Async SOCKS5 and HTTP-CONNECT proxy implementation.

    The same listening port accepts both protocols. curl-cffi should normally
    use the SOCKS5 URL exposed by :class:`FragmentingProxyProcess`.
    """

    def __init__(self, config: FragmentingProxyConfig | None = None) -> None:
        self.config = (config or FragmentingProxyConfig()).validated()
        self._upstream = (
            _parse_upstream_proxy(
                self.config.upstream_proxy,
                self.config.upstream_proxy_auth,
            )
            if self.config.upstream_proxy
            else None
        )
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
            name="fragmenting-proxy-client",
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
        try:
            first = await _read_exactly(
                client_reader,
                1,
                timeout=self.config.handshake_timeout,
            )
            if first == b"\x05":
                target_host, target_port, upstream_reader, upstream_writer = (
                    await self._handle_socks5_handshake(client_reader, client_writer)
                )
            else:
                target_host, target_port, upstream_reader, upstream_writer = (
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
            if upstream_writer is not None:
                await _close_writer(upstream_writer)
            await _close_writer(client_writer)

    async def _handle_socks5_handshake(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> tuple[str, int, asyncio.StreamReader, asyncio.StreamWriter]:
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

        bound = upstream_writer.get_extra_info("sockname")
        await self._send_socks_reply(writer, 0, bound)
        return target_host, target_port, upstream_reader, upstream_writer

    async def _handle_http_connect_handshake(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        first_byte: bytes,
    ) -> tuple[str, int, asyncio.StreamReader, asyncio.StreamWriter]:
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

        writer.write(
            b"HTTP/1.1 200 Connection Established\r\n"
            b"Proxy-Agent: AppFragmentProxy/1.0\r\n"
            b"\r\n"
        )
        await writer.drain()
        return target_host, target_port, upstream_reader, upstream_writer

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
            "User-Agent: AppFragmentProxy/1.0",
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
        if target_port in self.config.plaintext_http_ports:
            fragmenter: _StreamFragmenter = _Http1RequestFragmenter(
                split_at=self.config.split_at,
                split_delay=self.config.split_delay,
                max_header_bytes=self.config.max_header_bytes,
            )
        else:
            fragmenter = _FirstDataFragmenter(
                split_at=self.config.split_at,
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
            name="fragmenting-proxy-upstream",
        )
        upstream_to_client = asyncio.create_task(
            _relay_raw(
                upstream_reader,
                client_writer,
                read_size=self.config.read_size,
                idle_timeout=self.config.idle_timeout,
            ),
            name="fragmenting-proxy-downstream",
        )

        tasks = (client_to_upstream, upstream_to_client)
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, asyncio.CancelledError):
                    raise result
                if isinstance(result, Exception) and not isinstance(
                    result,
                    (ConnectionError, asyncio.TimeoutError),
                ):
                    LOG.debug("Relay ended with: %r", result)
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)


class _StreamFragmenter(Protocol):
    async def feed(self, data: bytes, writer: _AsyncWriter) -> None: ...

    async def finish(self, writer: _AsyncWriter) -> None: ...


class _FirstDataFragmenter:
    def __init__(self, *, split_at: int, split_delay: float) -> None:
        self.split_at = split_at
        self.split_delay = split_delay
        self._prefix = bytearray()
        self._prefix_sent = False
        self._done = False

    async def feed(self, data: bytes, writer: _AsyncWriter) -> None:
        if not data:
            return
        if self._done:
            await _write_bytes(writer, data)
            return

        if not self._prefix_sent:
            needed = self.split_at - len(self._prefix)
            self._prefix.extend(data[:needed])
            data = data[needed:]
            if len(self._prefix) < self.split_at:
                return

            await _write_bytes(writer, bytes(self._prefix))
            self._prefix.clear()
            self._prefix_sent = True
            if self.split_delay:
                await asyncio.sleep(self.split_delay)

        if data:
            await _write_bytes(writer, data)
            self._done = True

    async def finish(self, writer: _AsyncWriter) -> None:
        if self._prefix:
            await _write_bytes(writer, bytes(self._prefix))
            self._prefix.clear()
        self._done = True


class _Http1RequestFragmenter:
    """Incremental HTTP/1.x request framer for persistent connections."""

    _HEADERS = "headers"
    _FIXED_BODY = "fixed-body"
    _CHUNK_SIZE = "chunk-size"
    _CHUNK_DATA = "chunk-data"
    _CHUNK_CRLF = "chunk-crlf"
    _TRAILERS = "trailers"
    _RAW = "raw"

    def __init__(
        self,
        *,
        split_at: int,
        split_delay: float,
        max_header_bytes: int,
    ) -> None:
        self.split_at = split_at
        self.split_delay = split_delay
        self.max_header_bytes = max_header_bytes
        self._buffer = bytearray()
        self._state = self._HEADERS
        self._remaining = 0
        self._fragmented_requests = 0

    async def feed(self, data: bytes, writer: _AsyncWriter) -> None:
        if not data:
            return
        if self._state == self._RAW:
            await _write_bytes(writer, data)
            return

        self._buffer.extend(data)
        await self._process(writer)

    async def finish(self, writer: _AsyncWriter) -> None:
        if self._buffer:
            if self._fragmented_requests == 0:
                await _write_fragmented(
                    writer,
                    bytes(self._buffer),
                    split_at=self.split_at,
                    split_delay=self.split_delay,
                )
            else:
                await _write_bytes(writer, bytes(self._buffer))
            self._buffer.clear()

    async def _process(self, writer: _AsyncWriter) -> None:
        while self._buffer:
            if self._state == self._RAW:
                await _write_bytes(writer, bytes(self._buffer))
                self._buffer.clear()
                return

            if self._state == self._HEADERS:
                end = self._buffer.find(b"\r\n\r\n")
                if end < 0:
                    if len(self._buffer) > self.max_header_bytes:
                        await self._fallback_to_raw(writer)
                    return

                header_length = end + 4
                header = bytes(self._buffer[:header_length])
                del self._buffer[:header_length]
                parsed = _parse_http1_request_header(header)
                if parsed is None:
                    if self._fragmented_requests == 0:
                        await _write_fragmented(
                            writer,
                            header,
                            split_at=self.split_at,
                            split_delay=self.split_delay,
                        )
                    else:
                        await _write_bytes(writer, header)
                    self._state = self._RAW
                    continue

                content_length, chunked, upgrade = parsed
                await _write_fragmented(
                    writer,
                    header,
                    split_at=self.split_at,
                    split_delay=self.split_delay,
                )
                self._fragmented_requests += 1

                if upgrade:
                    self._state = self._RAW
                elif chunked:
                    self._state = self._CHUNK_SIZE
                elif content_length > 0:
                    self._remaining = content_length
                    self._state = self._FIXED_BODY
                else:
                    self._state = self._HEADERS
                continue

            if self._state == self._FIXED_BODY:
                amount = min(self._remaining, len(self._buffer))
                if amount:
                    await _write_bytes(writer, bytes(self._buffer[:amount]))
                    del self._buffer[:amount]
                    self._remaining -= amount
                if self._remaining == 0:
                    self._state = self._HEADERS
                    continue
                return

            if self._state == self._CHUNK_SIZE:
                line_end = self._buffer.find(b"\r\n")
                if line_end < 0:
                    if len(self._buffer) > 4096:
                        await self._fallback_to_raw(writer)
                    return
                line_length = line_end + 2
                line = bytes(self._buffer[:line_length])
                del self._buffer[:line_length]
                try:
                    size_token = line[:-2].split(b";", 1)[0].strip()
                    chunk_size = int(size_token, 16)
                except ValueError:
                    await _write_bytes(writer, line)
                    await self._fallback_to_raw(writer)
                    return
                await _write_bytes(writer, line)
                if chunk_size == 0:
                    self._state = self._TRAILERS
                else:
                    self._remaining = chunk_size
                    self._state = self._CHUNK_DATA
                continue

            if self._state == self._CHUNK_DATA:
                amount = min(self._remaining, len(self._buffer))
                if amount:
                    await _write_bytes(writer, bytes(self._buffer[:amount]))
                    del self._buffer[:amount]
                    self._remaining -= amount
                if self._remaining == 0:
                    self._state = self._CHUNK_CRLF
                    continue
                return

            if self._state == self._CHUNK_CRLF:
                if len(self._buffer) < 2:
                    return
                marker = bytes(self._buffer[:2])
                del self._buffer[:2]
                await _write_bytes(writer, marker)
                if marker != b"\r\n":
                    await self._fallback_to_raw(writer)
                    return
                self._state = self._CHUNK_SIZE
                continue

            if self._state == self._TRAILERS:
                if self._buffer.startswith(b"\r\n"):
                    trailer_length = 2
                else:
                    trailer_end = self._buffer.find(b"\r\n\r\n")
                    if trailer_end < 0:
                        if len(self._buffer) > self.max_header_bytes:
                            await self._fallback_to_raw(writer)
                        return
                    trailer_length = trailer_end + 4
                await _write_bytes(writer, bytes(self._buffer[:trailer_length]))
                del self._buffer[:trailer_length]
                self._state = self._HEADERS
                continue

    async def _fallback_to_raw(self, writer: _AsyncWriter) -> None:
        if self._buffer:
            if self._fragmented_requests == 0:
                await _write_fragmented(
                    writer,
                    bytes(self._buffer),
                    split_at=self.split_at,
                    split_delay=self.split_delay,
                )
            else:
                await _write_bytes(writer, bytes(self._buffer))
            self._buffer.clear()
        self._state = self._RAW


async def _relay_fragmented(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    fragmenter: _StreamFragmenter,
    *,
    read_size: int,
    idle_timeout: float,
) -> None:
    try:
        while True:
            data = await _read_some(reader, read_size, idle_timeout)
            if not data:
                break
            await fragmenter.feed(data, writer)
        await fragmenter.finish(writer)
        await _write_eof(writer)
    except (ConnectionError, asyncio.TimeoutError):
        pass


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


async def _write_fragmented(
    writer: _AsyncWriter,
    data: bytes,
    *,
    split_at: int,
    split_delay: float,
) -> None:
    if len(data) <= split_at:
        await _write_bytes(writer, data)
        return
    await _write_bytes(writer, data[:split_at])
    if split_delay:
        await asyncio.sleep(split_delay)
    await _write_bytes(writer, data[split_at:])


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


def _parse_http1_request_header(
    header: bytes,
) -> tuple[int, bool, bool] | None:
    try:
        lines = header[:-4].split(b"\r\n")
        request_line = lines[0]
        method, _target, version = request_line.split(b" ", 2)
    except (IndexError, ValueError):
        return None

    if not _is_http_token(method):
        return None
    if version not in {b"HTTP/1.0", b"HTTP/1.1"}:
        return None

    values: dict[bytes, list[bytes]] = {}
    for line in lines[1:]:
        if not line:
            continue
        if line[:1] in {b" ", b"\t"}:
            return None
        if b":" not in line:
            return None
        name, value = line.split(b":", 1)
        name = name.strip().lower()
        if not name or not _is_http_token(name):
            return None
        values.setdefault(name, []).append(value.strip().lower())

    transfer_encoding = b",".join(values.get(b"transfer-encoding", []))
    chunked = any(
        item.strip() == b"chunked" for item in transfer_encoding.split(b",") if item
    )

    content_lengths = values.get(b"content-length", [])
    content_length = 0
    if content_lengths:
        normalized = {item.strip() for item in content_lengths}
        if len(normalized) != 1:
            return None
        try:
            content_length = int(next(iter(normalized)), 10)
        except ValueError:
            return None
        if content_length < 0:
            return None

    connection = b",".join(values.get(b"connection", []))
    upgrade = b"upgrade" in {item.strip() for item in connection.split(b",")}
    upgrade = upgrade and bool(values.get(b"upgrade"))
    return content_length, chunked, upgrade


def _is_http_token(value: bytes) -> bool:
    if not value:
        return False
    separators = b'()<>@,;:\\"/[]?={} \t'
    return all(33 <= byte <= 126 and byte not in separators for byte in value)


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


def _proxy_process_entry(
    config: FragmentingProxyConfig,
    stop_event: object,
    status_queue: object,
) -> None:
    _configure_logging(config.log_level)

    async def runner() -> None:
        server = FragmentingProxyServer(config)
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


async def _run_foreground(config: FragmentingProxyConfig) -> None:
    server = FragmentingProxyServer(config)
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
        description="App-local non-strict TCP stream fragmentation proxy",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--split-at", type=int, default=2)
    parser.add_argument("--split-delay-ms", type=float, default=10.0)
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

    config = FragmentingProxyConfig(
        listen_host=args.host,
        listen_port=args.port,
        split_at=args.split_at,
        split_delay=args.split_delay_ms / 1000.0,
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