"""Real loopback HTTP/TLS endpoints for controlled native-client setting effects.

These are diagnostic servers, not simulated provider clients or media responses.
"""
from __future__ import annotations

import asyncio
import json
import ssl
import time
from collections import Counter
from urllib.parse import parse_qs, urlsplit


class NetworkLab:
    def __init__(self, directory):
        self.directory = directory
        self.requests = []
        self.counts = Counter()
        self.hellos = []
        self.servers = []
        self.tasks = set()

    async def start(self):
        self.http = await asyncio.start_server(self.handle, "127.0.0.1", 0)
        self.servers.append(self.http)
        self.url = f"http://127.0.0.1:{self.http.sockets[0].getsockname()[1]}"
        key, cert = self.directory / "key.pem", self.directory / "cert.pem"
        process = await asyncio.create_subprocess_exec(
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
            "-subj", "/CN=localhost", "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1",
            "-keyout", str(key), "-out", str(cert),
            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL,
        )
        await process.wait()
        if process.returncode:
            raise RuntimeError("OpenSSL could not create the isolated TLS test certificate")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert, key)
        context.set_alpn_protocols(["http/1.1"])
        self.tls = await asyncio.start_server(self.handle, "127.0.0.1", 0, ssl=context)
        self.servers.append(self.tls)
        relay = await asyncio.start_server(self.relay, "127.0.0.1", 0)
        self.servers.append(relay)
        port = relay.sockets[0].getsockname()[1]
        # A genuine SOCKS proxy may resolve localhost to IPv6 first.
        try:
            self.servers.append(await asyncio.start_server(self.relay, "::1", port))
        except OSError:
            pass
        self.tls_url = f"https://localhost:{port}"
        return self

    async def handle(self, reader, writer):
        task = asyncio.current_task()
        self.tasks.add(task)
        try:
            header = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), 10)
            lines = header.decode("latin1").split("\r\n")
            method, target, protocol = lines[0].split(" ")
            headers = {name.lower(): value.strip() for line in lines[1:] if ":" in line
                       for name, value in [line.split(":", 1)]}
            length = int(headers.get("content-length", 0))
            body = await reader.readexactly(length) if length else b""
            path = urlsplit(target).path
            query = parse_qs(urlsplit(target).query)
            self.counts[target] += 1
            record = {"method": method, "target": target, "protocol": protocol, "headers": headers,
                      "body": body.decode(errors="replace"), "at": time.monotonic()}
            self.requests.append(record)
            status = 200
            payload = json.dumps({"count": self.counts[target], "headers": headers}).encode()
            if path == "/retry" and self.counts[target] <= int(query.get("fail", [1])[0]):
                status = 503
            if path == "/slow":
                await asyncio.sleep(float(query.get("seconds", [1.3])[0]))
            if path == "/report":
                status, payload = 204, b""
            if path == "/blob":
                payload = b"x" * int(query.get("bytes", [1048576])[0])
            writer.write(f"HTTP/1.1 {status} Test\r\nContent-Length: {len(payload)}\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n".encode())
            if method != "HEAD":
                writer.write(payload)
            await writer.drain()
        except (ConnectionError, asyncio.IncompleteReadError, asyncio.LimitOverrunError, TimeoutError):
            pass
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except (OSError, ssl.SSLError):
                pass
            self.tasks.discard(task)

    async def relay(self, reader, writer):
        task = asyncio.current_task()
        self.tasks.add(task)
        upstream = None
        try:
            header = await reader.readexactly(5)
            data = header + await reader.readexactly(int.from_bytes(header[3:5], "big"))
            self.hellos.append(hello(data))
            remote_reader, upstream = await asyncio.open_connection("127.0.0.1", self.tls.sockets[0].getsockname()[1])
            upstream.write(data)
            await upstream.drain()

            async def copy(source, target):
                try:
                    while chunk := await source.read(65536):
                        target.write(chunk)
                        await target.drain()
                except (ConnectionError, OSError):
                    pass
                finally:
                    target.close()

            await asyncio.gather(copy(reader, upstream), copy(remote_reader, writer))
        except (ConnectionError, asyncio.IncompleteReadError, OSError):
            pass
        finally:
            writer.close()
            if upstream:
                upstream.close()
            self.tasks.discard(task)

    async def close(self):
        for server in self.servers:
            server.close()
            await server.wait_closed()
        for task in tuple(self.tasks):
            task.cancel()
        await asyncio.gather(*tuple(self.tasks), return_exceptions=True)


def hello(data):
    """Read cipher/extension IDs from our own bounded ClientHello capture."""
    grease = {0x0A0A + i * 0x1010 for i in range(16)}
    body = memoryview(data)[5:]
    try:
        position = 4 + 2 + 32
        position += 1 + body[position]
        width = int.from_bytes(body[position:position + 2], "big")
        position += 2
        ciphers = [int.from_bytes(body[i:i + 2], "big") for i in range(position, position + width, 2)]
        position += width
        position += 1 + body[position]
        end = position + 2 + int.from_bytes(body[position:position + 2], "big")
        position += 2
        extensions = []
        while position + 4 <= min(end, len(body)):
            extensions.append(int.from_bytes(body[position:position + 2], "big"))
            position += 4 + int.from_bytes(body[position + 2:position + 4], "big")
        return {"ciphers": [v for v in ciphers if v not in grease],
                "extensions": [v for v in extensions if v not in grease]}
    except (IndexError, ValueError):
        return {"unparsed": True}
