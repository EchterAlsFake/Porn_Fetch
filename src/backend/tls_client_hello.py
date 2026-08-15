"""Small, dependency-free TLS ClientHello/SNI locator and stream fragmenter."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol


MAX_TLS_RECORD = 18_432
MAX_CLIENT_HELLO = 1_048_576


class ClientHelloState(Enum):
    NEED_MORE = auto()
    SNI_FOUND = auto()
    NO_SNI = auto()
    NOT_CLIENT_HELLO = auto()
    MALFORMED = auto()


@dataclass(frozen=True, slots=True)
class ClientHelloSNI:
    state: ClientHelloState
    hostname_start: int | None = None
    hostname_end: int | None = None

    @property
    def split_offset(self) -> int | None:
        if self.hostname_start is None or self.hostname_end is None:
            return None
        length = self.hostname_end - self.hostname_start
        if length < 2:
            return None
        return self.hostname_start + max(1, length // 2)


def locate_client_hello_sni(data: bytes) -> ClientHelloSNI:
    """Locate the first host_name entry and return offsets in the TCP byte stream."""

    if not data:
        return ClientHelloSNI(ClientHelloState.NEED_MORE)
    if data[0] != 22:  # TLS handshake record
        return ClientHelloSNI(ClientHelloState.NOT_CLIENT_HELLO)

    handshake = bytearray()
    stream_offsets: list[int] = []
    cursor = 0
    required_handshake_size: int | None = None

    while True:
        if len(data) - cursor < 5:
            return ClientHelloSNI(ClientHelloState.NEED_MORE)
        content_type = data[cursor]
        record_length = int.from_bytes(data[cursor + 3:cursor + 5], "big")
        if record_length > MAX_TLS_RECORD:
            return ClientHelloSNI(ClientHelloState.MALFORMED)
        record_end = cursor + 5 + record_length
        if len(data) < record_end:
            return ClientHelloSNI(ClientHelloState.NEED_MORE)
        if content_type != 22:
            return ClientHelloSNI(ClientHelloState.MALFORMED)

        payload_start = cursor + 5
        handshake.extend(data[payload_start:record_end])
        stream_offsets.extend(range(payload_start, record_end))

        if required_handshake_size is None and len(handshake) >= 4:
            if handshake[0] != 1:  # ClientHello
                return ClientHelloSNI(ClientHelloState.NOT_CLIENT_HELLO)
            body_length = int.from_bytes(handshake[1:4], "big")
            if body_length > MAX_CLIENT_HELLO:
                return ClientHelloSNI(ClientHelloState.MALFORMED)
            required_handshake_size = 4 + body_length

        if required_handshake_size is not None and len(handshake) >= required_handshake_size:
            break
        cursor = record_end
        if cursor >= len(data):
            return ClientHelloSNI(ClientHelloState.NEED_MORE)

    hello = memoryview(handshake)[:required_handshake_size]
    try:
        pos = 4 + 2 + 32
        session_id_length = hello[pos]
        pos += 1 + session_id_length
        cipher_length = int.from_bytes(hello[pos:pos + 2], "big")
        pos += 2 + cipher_length
        compression_length = hello[pos]
        pos += 1 + compression_length
        extensions_length = int.from_bytes(hello[pos:pos + 2], "big")
        pos += 2
        extensions_end = pos + extensions_length
        if extensions_end > len(hello):
            return ClientHelloSNI(ClientHelloState.MALFORMED)

        while pos + 4 <= extensions_end:
            extension_type = int.from_bytes(hello[pos:pos + 2], "big")
            extension_length = int.from_bytes(hello[pos + 2:pos + 4], "big")
            extension_start = pos + 4
            extension_end = extension_start + extension_length
            if extension_end > extensions_end:
                return ClientHelloSNI(ClientHelloState.MALFORMED)
            if extension_type == 0:
                return _locate_server_name(hello, stream_offsets, extension_start, extension_end)
            pos = extension_end
    except (IndexError, ValueError):
        return ClientHelloSNI(ClientHelloState.MALFORMED)

    return ClientHelloSNI(ClientHelloState.NO_SNI)


def _locate_server_name(
    hello: memoryview,
    stream_offsets: list[int],
    extension_start: int,
    extension_end: int,
) -> ClientHelloSNI:
    if extension_start + 2 > extension_end:
        return ClientHelloSNI(ClientHelloState.MALFORMED)
    names_length = int.from_bytes(hello[extension_start:extension_start + 2], "big")
    pos = extension_start + 2
    names_end = pos + names_length
    if names_end > extension_end:
        return ClientHelloSNI(ClientHelloState.MALFORMED)
    while pos + 3 <= names_end:
        name_type = hello[pos]
        name_length = int.from_bytes(hello[pos + 1:pos + 3], "big")
        name_start = pos + 3
        name_end = name_start + name_length
        if name_end > names_end:
            return ClientHelloSNI(ClientHelloState.MALFORMED)
        if name_type == 0:
            if name_length == 0:
                return ClientHelloSNI(ClientHelloState.MALFORMED)
            return ClientHelloSNI(
                ClientHelloState.SNI_FOUND,
                hostname_start=stream_offsets[name_start],
                hostname_end=stream_offsets[name_end - 1] + 1,
            )
        pos = name_end
    return ClientHelloSNI(ClientHelloState.NO_SNI)


class AsyncWriter(Protocol):
    def write(self, data: bytes) -> object: ...
    async def drain(self) -> object: ...


class TLSClientHelloStreamFragmenter:
    """Buffer the first TLS ClientHello and split inside its SNI hostname."""

    def __init__(
        self,
        *,
        fallback_split_at: int = 2,
        split_delay: float = 0.010,
        max_buffer: int = MAX_CLIENT_HELLO + (16 * 1024),
    ) -> None:
        self.fallback_split_at = fallback_split_at
        self.split_delay = split_delay
        self.max_buffer = max_buffer
        self._buffer = bytearray()
        self._done = False

    async def feed(self, data: bytes, writer: AsyncWriter) -> None:
        if not data:
            return
        if self._done:
            await _write(writer, data)
            return
        self._buffer.extend(data)
        result = locate_client_hello_sni(self._buffer)
        if result.state is ClientHelloState.NEED_MORE and len(self._buffer) <= self.max_buffer:
            return
        split_at = result.split_offset or self.fallback_split_at
        await self._flush(writer, split_at)

    async def finish(self, writer: AsyncWriter) -> None:
        if self._buffer:
            result = locate_client_hello_sni(self._buffer)
            await self._flush(writer, result.split_offset or self.fallback_split_at)
        self._done = True

    async def _flush(self, writer: AsyncWriter, split_at: int) -> None:
        data = bytes(self._buffer)
        self._buffer.clear()
        self._done = True
        if not 0 < split_at < len(data):
            await _write(writer, data)
            return
        await _write(writer, data[:split_at])
        if self.split_delay:
            await asyncio.sleep(self.split_delay)
        await _write(writer, data[split_at:])


async def _write(writer: AsyncWriter, data: bytes) -> None:
    if data:
        writer.write(data)
        await writer.drain()
