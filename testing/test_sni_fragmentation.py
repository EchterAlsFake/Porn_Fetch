from __future__ import annotations

import unittest
from unittest.mock import patch

from src.backend.tls_client_hello import (
    ClientHelloState,
    TLSClientHelloStreamFragmenter,
    locate_client_hello_sni,
)
from src.backend.sni_fragment_proxy_strict import (
    StrictBackendUnavailable,
    StrictDesyncConfig,
    StrictFragmentingProxyConfig,
    _StrictFlowPolicy,
    _StrictPacketBackend,
    _generate_decoy_client_hello,
    _process_strict_packet,
    _prepare_linux_diverter_close,
)


def build_client_hello(hostname: str, *, record_split: int | None = None) -> bytes:
    host = hostname.encode("ascii")
    server_name = b"\x00" + len(host).to_bytes(2, "big") + host
    server_name_list = len(server_name).to_bytes(2, "big") + server_name
    extension = b"\x00\x00" + len(server_name_list).to_bytes(2, "big") + server_name_list
    body = (
        b"\x03\x03"
        + (b"R" * 32)
        + b"\x00"
        + b"\x00\x02\x13\x01"
        + b"\x01\x00"
        + len(extension).to_bytes(2, "big")
        + extension
    )
    handshake = b"\x01" + len(body).to_bytes(3, "big") + body

    def record(payload: bytes) -> bytes:
        return b"\x16\x03\x01" + len(payload).to_bytes(2, "big") + payload

    if record_split is None:
        return record(handshake)
    return record(handshake[:record_split]) + record(handshake[record_split:])


class RecordingWriter:
    def __init__(self) -> None:
        self.writes: list[bytes] = []

    def write(self, data: bytes) -> None:
        self.writes.append(bytes(data))

    async def drain(self) -> None:
        return None


class ClientHelloLocatorTests(unittest.TestCase):
    def test_locates_hostname_in_single_record(self) -> None:
        hello = build_client_hello("video.example.com")
        result = locate_client_hello_sni(hello)
        self.assertIs(result.state, ClientHelloState.SNI_FOUND)
        self.assertEqual(
            hello[result.hostname_start:result.hostname_end],
            b"video.example.com",
        )
        self.assertGreater(result.split_offset, result.hostname_start)
        self.assertLess(result.split_offset, result.hostname_end)

    def test_locates_hostname_across_tls_records(self) -> None:
        hello = build_client_hello("cross-record.example", record_split=48)
        result = locate_client_hello_sni(hello)
        self.assertIs(result.state, ClientHelloState.SNI_FOUND)
        self.assertEqual(
            hello[result.hostname_start:result.hostname_end],
            b"cross-record.example",
        )

    def test_reports_incomplete_client_hello(self) -> None:
        hello = build_client_hello("incomplete.example")
        self.assertIs(
            locate_client_hello_sni(hello[:20]).state,
            ClientHelloState.NEED_MORE,
        )


class StreamFragmenterTests(unittest.IsolatedAsyncioTestCase):
    async def test_buffers_then_splits_inside_hostname(self) -> None:
        hostname = b"fragment-me.example"
        hello = build_client_hello(hostname.decode("ascii"))
        writer = RecordingWriter()
        fragmenter = TLSClientHelloStreamFragmenter(split_delay=0)

        await fragmenter.feed(hello[:35], writer)
        self.assertEqual(writer.writes, [])
        await fragmenter.feed(hello[35:], writer)

        self.assertEqual(b"".join(writer.writes), hello)
        self.assertEqual(len(writer.writes), 2)
        self.assertNotIn(hostname, writer.writes[0])
        self.assertNotIn(hostname, writer.writes[1])
        self.assertTrue(writer.writes[0].endswith(hostname[: len(hostname) // 2]))
        self.assertTrue(writer.writes[1].startswith(hostname[len(hostname) // 2 :]))

    async def test_non_tls_falls_back_without_buffering(self) -> None:
        writer = RecordingWriter()
        fragmenter = TLSClientHelloStreamFragmenter(
            fallback_split_at=2,
            split_delay=0,
        )
        await fragmenter.feed(b"GET / HTTP/1.1\r\n", writer)
        self.assertEqual(writer.writes, [b"GE", b"T / HTTP/1.1\r\n"])


class StrictLinuxCompatibilityTests(unittest.TestCase):
    @patch("src.backend.sni_fragment_proxy_strict.os.geteuid", return_value=1000)
    @patch("src.backend.sni_fragment_proxy_strict.platform.system", return_value="Linux")
    def test_linux_prepare_reports_missing_root_clearly(self, _system, _geteuid) -> None:
        backend = _StrictPacketBackend(StrictFragmentingProxyConfig())

        with self.assertRaisesRegex(StrictBackendUnavailable, "requires root"):
            backend.prepare()

    def test_active_flows_receive_unique_priorities(self) -> None:
        backend = _StrictPacketBackend(
            StrictFragmentingProxyConfig(backend_priority=100)
        )

        first = backend._allocate_priority()
        second = backend._allocate_priority()

        self.assertEqual((first, second), (100, 99))
        backend._allocated_priorities.discard(first)
        self.assertEqual(backend._allocate_priority(), 100)

    @patch("src.backend.sni_fragment_proxy_strict.platform.system", return_value="Linux")
    def test_linux_close_clears_attach_only_libbpf_fields(self, _system) -> None:
        class Options:
            prog_fd = 17
            prog_id = 23

        class Implementation:
            _hooks = [(object(), Options())]

        class Diverter:
            _impl = Implementation()

        _prepare_linux_diverter_close(Diverter())

        options = Diverter._impl._hooks[0][1]
        self.assertEqual(options.prog_fd, 0)
        self.assertEqual(options.prog_id, 0)


class StrictDesyncTests(unittest.IsolatedAsyncioTestCase):
    class RecordingDiverter:
        def __init__(self, *, fail_first: bool = False) -> None:
            self.fail_first = fail_first
            self.attempts = 0
            self.sent: list[tuple[bytes, int, int]] = []

        async def send_async(self, packet) -> None:
            self.attempts += 1
            if self.fail_first and self.attempts == 1:
                raise OSError("simulated decoy send failure")
            self.sent.append(
                (bytes(packet.payload), int(packet.tcp.seq_num), int(packet.tcp.ack_num))
            )

    @staticmethod
    def packet(payload: bytes):
        try:
            from pydivert import Packet
        except (ImportError, ModuleNotFoundError) as exc:
            raise unittest.SkipTest("pydivert is not installed") from exc

        total_length = 20 + 20 + len(payload)
        ipv4 = (
            b"\x45\x00"
            + total_length.to_bytes(2, "big")
            + b"\x00\x01\x40\x00\x40\x06\x00\x00"
            + b"\x7f\x00\x00\x01\x7f\x00\x00\x01"
        )
        tcp = (
            b"\xc3\x50\x01\xbb"
            + (100_000).to_bytes(4, "big")
            + (200_000).to_bytes(4, "big")
            + b"\x50\x18\x20\x00\x00\x00\x00\x00"
        )
        return Packet(ipv4 + tcp + payload)

    def test_decoy_is_a_parseable_client_hello(self) -> None:
        hello = _generate_decoy_client_hello("www.example.com")
        located = locate_client_hello_sni(hello)
        self.assertIs(located.state, ClientHelloState.SNI_FOUND)
        self.assertEqual(
            hello[located.hostname_start:located.hostname_end],
            b"www.example.com",
        )

    async def test_decoy_is_cloned_and_genuine_fragments_are_reversed(self) -> None:
        genuine = build_client_hello("private.example")
        packet = self.packet(genuine)
        diverter = self.RecordingDiverter()
        policy = _StrictFlowPolicy(
            split_at=2,
            plaintext_http=False,
            max_segment_payload=0,
            desync_config=StrictDesyncConfig(),
        )

        await _process_strict_packet(
            diverter,
            packet,
            policy,
            reverse=True,
        )

        self.assertEqual(len(diverter.sent), 3)
        decoy, second, first = diverter.sent
        self.assertEqual(decoy[1:], (90_000, 134_000))
        self.assertEqual(second[1:], (100_002, 200_000))
        self.assertEqual(first[1:], (100_000, 200_000))
        self.assertEqual(first[0] + second[0], genuine)
        self.assertEqual(bytes(packet.payload), first[0])

    async def test_decoy_failure_does_not_drop_genuine_fragments(self) -> None:
        genuine = build_client_hello("private.example")
        diverter = self.RecordingDiverter(fail_first=True)
        policy = _StrictFlowPolicy(
            split_at=2,
            plaintext_http=False,
            max_segment_payload=0,
            desync_config=StrictDesyncConfig(),
        )

        await _process_strict_packet(
            diverter,
            self.packet(genuine),
            policy,
            reverse=False,
        )

        self.assertEqual(diverter.attempts, 3)
        self.assertEqual(b"".join(item[0] for item in diverter.sent), genuine)

    def test_rejects_unknown_desync_mode(self) -> None:
        with self.assertRaisesRegex(ValueError, "desync mode"):
            StrictFragmentingProxyConfig(
                desync_config=StrictDesyncConfig(mode="wrong_checksum")
            ).validated()


class ElevationHelperTests(unittest.TestCase):
    def test_build_cli_args_for_config(self) -> None:
        from src.backend.sni_fragment_proxy_strict import (
            StrictDesyncConfig,
            StrictFragmentingProxyConfig,
            _build_cli_args_for_config,
            _get_elevation_command,
        )

        config = StrictFragmentingProxyConfig(
            listen_host="127.0.0.1",
            listen_port=0,
            reverse_fragments=True,
            desync_config=StrictDesyncConfig(fake_sni="test.example.com"),
            upstream_proxy="socks5://127.0.0.1:9050",
        )
        args = _build_cli_args_for_config(config)

        self.assertIn("--reverse", args)
        self.assertIn("--desync", args)
        self.assertIn("test.example.com", args)
        self.assertIn("socks5://127.0.0.1:9050", args)

        cmd = _get_elevation_command(args)
        self.assertGreater(len(cmd), len(args))
        self.assertIn(cmd[0], ("pkexec", "sudo", "powershell.exe"))



if __name__ == "__main__":
    unittest.main()
