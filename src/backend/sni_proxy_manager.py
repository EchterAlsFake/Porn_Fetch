"""Application-owned lifecycle for the local SNI fragmentation proxy."""

from __future__ import annotations

import atexit
import contextlib
import ipaddress
import logging
import socket
import struct
import sys
from typing import Any

from src.backend.sni_fragment_proxy_lite import (
    FragmentingProxyConfig,
    FragmentingProxyProcess,
)
from src.backend.sni_fragment_proxy_strict import (
    StrictFragmentingProxyConfig,
    StrictFragmentingProxyProcess,
    StrictDesyncConfig,
)


LOG = logging.getLogger("sni-proxy-manager")
FAIL_CLOSED_PROXY_URL = "socks5://127.0.0.1:9"


def resolve_source_address(interface_or_address: str) -> str | None:
    """Resolve an IP literal or a Linux interface name to a bindable address."""

    value = interface_or_address.strip()
    if not value:
        return None
    with contextlib.suppress(ValueError):
        return str(ipaddress.ip_address(value.split("%", 1)[0]))

    if sys.platform.startswith("linux"):
        import fcntl

        request = struct.pack("256s", value[:15].encode("utf-8"))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            response = fcntl.ioctl(sock.fileno(), 0x8915, request)  # SIOCGIFADDR
        return socket.inet_ntoa(response[20:24])

    # Interface names are platform-specific. Returning None is safer than
    # binding the proxy to an unrelated address; IP literals work everywhere.
    LOG.warning("Could not resolve interface name %r on %s", value, sys.platform)
    return None


class SNIProxyManager:
    def __init__(self, settings: Any) -> None:
        self.settings = settings
        self._process: FragmentingProxyProcess | StrictFragmentingProxyProcess | None = None
        self._connections_installed = False
        self.last_error: str | None = None
        atexit.register(self.stop)

    @property
    def is_running(self) -> bool:
        return bool(self._process and self._process.is_running)

    @property
    def active_url(self) -> str | None:
        return getattr(self.settings, "active_sni_proxy_url", None)

    def install_settings_connections(self) -> None:
        if self._connections_installed:
            return
        self.settings.proxyChanged.connect(self._restart_for_network_change)
        self.settings.interfaceChanged.connect(self._restart_for_network_change)
        self._connections_installed = True

    def start(self) -> str | None:
        self.install_settings_connections()
        self.stop(clear_active=False)
        self.last_error = None

        if not self.settings.sni_obfuscation:
            self.settings.active_sni_proxy_url = None
            return None

        lite = bool(self.settings.sni_obfuscation_lite)
        strict = bool(self.settings.sni_obfuscation_strict)
        if lite == strict:
            return self._fail_closed(
                "SNI obfuscation requires exactly one mode: Lite or Strict."
            )

        interface = str(self.settings.interface or "")
        try:
            source_address = resolve_source_address(interface)
        except OSError as exc:
            return self._fail_closed(f"Could not resolve network interface {interface!r}: {exc}")

        try:
            if strict:
                linux_interfaces = None
                if sys.platform.startswith("linux") and interface:
                    if not _is_ip_literal(interface):
                        linux_interfaces = (interface,)

                profile = str(
                    getattr(
                        self.settings,
                        "sni_obfuscation_strict_profile",
                        "Strict Fragmentation",
                    )
                    or ""
                )
                reverse_fragments = False
                desync_config = None

                if profile == "Strict Reverse":
                    reverse_fragments = True
                elif profile == "Strict Desync":
                    reverse_fragments = True
                    desync_config = StrictDesyncConfig(mode="seq_ack")
                elif profile != "Strict Fragmentation":
                    return self._fail_closed(f"Unknown strict SNI profile: {profile!r}")

                process: FragmentingProxyProcess | StrictFragmentingProxyProcess = (
                    StrictFragmentingProxyProcess(
                        StrictFragmentingProxyConfig(
                            listen_host="127.0.0.1",
                            listen_port=0,
                            upstream_proxy=self.settings.proxy or None,
                            source_address=source_address,
                            linux_interfaces=linux_interfaces,
                            reverse_fragments=reverse_fragments,
                            desync_config=desync_config,
                        )
                    )
                )
            else:
                process = FragmentingProxyProcess(
                    FragmentingProxyConfig(
                        listen_host="127.0.0.1",
                        listen_port=0,
                        upstream_proxy=self.settings.proxy or None,
                        source_address=source_address,
                    )
                )
            local_url = process.start()
        except Exception as exc:
            LOG.exception("Could not start the SNI fragmentation proxy")
            return self._fail_closed(f"Could not start SNI obfuscation: {exc}")

        self._process = process
        self.settings.active_sni_proxy_url = local_url
        LOG.info("SNI fragmentation proxy ready at %s", local_url)
        return local_url

    def restart(self) -> str | None:
        return self.start()

    def stop(self, *, clear_active: bool = True) -> None:
        process, self._process = self._process, None
        if process is not None:
            with contextlib.suppress(Exception):
                process.stop()
        if clear_active:
            self.settings.active_sni_proxy_url = None

    def _restart_for_network_change(self, _value: object = None) -> None:
        if self.settings.sni_obfuscation:
            self.restart()

    def _fail_closed(self, message: str) -> str:
        self.last_error = message
        self._process = None
        self.settings.active_sni_proxy_url = FAIL_CLOSED_PROXY_URL
        LOG.error(message)
        return FAIL_CLOSED_PROXY_URL


def _is_ip_literal(value: str) -> bool:
    try:
        ipaddress.ip_address(value.split("%", 1)[0])
    except ValueError:
        return False
    return True
