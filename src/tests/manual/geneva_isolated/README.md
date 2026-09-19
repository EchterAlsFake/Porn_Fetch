# Isolated Geneva harness

`run.sh` creates a fresh rootless user/network namespace with `pasta`, starts
Geneva inside it, and then starts Porn Fetch in the same namespace. Geneva's
iptables/NFQUEUE rules exist only in that namespace. No host-wide OUTPUT rule,
UID rule, route, DNS setting, or forwarding sysctl is changed.

The namespace is deliberately IPv4-only. This Geneva release programs
`iptables` but not `ip6tables`; allowing IPv6 would let an application connect
to an IPv6 destination without entering Geneva's NFQUEUE.

The default Geneva strategy is `\/` (observe and pass packets unchanged) on
ports 80 and 443. This is the appropriate baseline for checking what the SNI
proxy emits without Geneva itself fragmenting or tampering with the flow.

The runner also includes a compatibility path for this old Geneva checkout on
modern Scapy/NetfilterQueue: if the strategy has no inbound action forest,
incoming packets are accepted byte-for-byte. Geneva's stock callback otherwise
reserializes even untouched SYN/ACK packets and breaks the TCP handshake on this
machine. Strategies with inbound actions still use Geneva's stock behavior and
must be validated separately.

Run Porn Fetch:

```bash
./src/tests/manual/geneva_isolated/run.sh
```

Run a smaller command through the same harness:

```bash
./src/tests/manual/geneva_isolated/run.sh curl -I https://example.com
```

Run the repeatable Lite-proxy smoke request used for SNI inspection:

```bash
./src/tests/manual/geneva_isolated/run.sh \
    .venv/bin/python3 src/tests/smoke/sni_proxy_smoke.py https://example.com/
```

The smoke client disables ECH so a plaintext ClientHello SNI is available to
inspect, forces HTTP/2/TCP, and pins name resolution to IPv4 to match this
harness's IPv4-only boundary. It does not change Porn Fetch's saved settings.

To inspect the outbound application packets in the newest run, use the path
printed by `run.sh`:

```bash
tshark -r src/tests/manual/geneva_runs/RUN_ID/namespace-wire.pcap \
    -Y 'tcp.dstport == 443 && tcp.len > 0' \
    -T fields -e frame.number -e tcp.seq -e tcp.len \
    -e tls.handshake.extensions_server_name -e tcp.payload
```

Wireshark may display the reassembled SNI on the second frame. The decisive
field is each frame's individual `tcp.payload`: the full hostname must not be
present in any one payload.

Override the strategy or monitored ports when needed:

```bash
GENEVA_STRATEGY='[TCP:flags:PA]-fragment{tcp:2:True}-|' \
GENEVA_PORTS='443' \
./src/tests/manual/geneva_isolated/run.sh
```

Every run creates a mode-0700 directory below `src/tests/manual/geneva_runs/`. It
contains Geneva logs/captures and `namespace-wire.pcap`, a pasta capture scoped
to traffic crossing that namespace boundary. Captures can contain destination
names, IP addresses, cookies, or other private application traffic; do not
commit or share them casually.

The namespace and all NFQUEUE rules disappear when the launcher exits. Host
ports are not forwarded into the namespace, and the namespace cannot use the
special pasta host-loopback gateway mapping.
