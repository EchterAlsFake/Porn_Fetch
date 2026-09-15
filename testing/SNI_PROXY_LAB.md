# SNI proxy development and test lab

This note records the non-obvious upstream dependencies, local compatibility
patches, and isolated Geneva setup used while developing Porn Fetch's Lite and
Strict SNI proxies. It is intended to make the environment reproducible after a
clean installation.

## Known-working snapshot

The last verified Linux environment was:

- Arch Linux, Linux `7.1.7-arch1-1`, x86-64
- Porn Fetch Python `3.14.7`, `curl-cffi 0.16.0`
- PyDivert `4.0.0` from commit
  `0b84da51df8bddb6c5843181ca1f11d026975067`
- PyDivert's bundled eBPFDivert ABI/version: `v0.0.2`
- Geneva commit `28a3fa63dff1eebe7e92dcf00f69ca480a81cd3a`
- Geneva Python `3.13.12`, NetfilterQueue `1.1.0`, Scapy `2.7.0`
- `passt/pasta 2026_07_28.f8df3f1`, iptables `1.8.13`, libbpf `1.7.0`
- TShark `4.7.2`

GoodbyeDPI was examined at commit
`f593a276f9ec753889f80208c6a7c5cf455df94a`. Its reverse fragmentation and
wrong-sequence/wrong-ACK fake-ClientHello techniques informed the optional
Strict Reverse and Strict Desync profiles. No GoodbyeDPI code or Windows driver
is embedded in Porn Fetch.

Exact versions are useful forensic context, not permanent requirements. Retest
the patches whenever PyDivert or eBPFDivert changes.

## What is patched, and why

There are two upstream compatibility problems and two app-local mitigations.

### 1. eBPFDivert Ethernet offset detection (Linux object patch)

PyDivert 4 downloads/bundles the eBPFDivert `v0.0.2` BPF object. That version
tries to identify a raw IP packet at offsets 0 and 4 before testing for an
Ethernet header at offset 14. A destination-MAC byte can coincidentally have an
IPv4/IPv6-looking high nibble. On the test network, byte 4 was `0x65`, so the
program selected the wrong L3 offset and outbound TCP port filters never
matched.

The source patch in
[`pydivert_linux/ebpfdivert-v0.0.2-ethernet.patch`](pydivert_linux/ebpfdivert-v0.0.2-ethernet.patch)
checks the Ethernet ethertype at bytes 12-13 first, then falls back to raw-IP
offset heuristics. This is an ABI-compatible replacement for the bundled
`v0.0.2` object; it does not patch the installed Python package.

The test installation contained:

```text
patched object SHA-256: 811f36fea8f84a826221706a5a3799493f8e50243c027440f3046542e9c23c01
upstream object SHA-256: 38ef33829ed316619d27d6c7baf1c6021cd6b26fc05c3a1d26cfd587b2331b07
```

Compiler versions affect BPF object hashes, so a fresh valid build need not
match the patched hash exactly.

### 2. PyDivert TC detach options (application workaround)

After a Linux TC program is attached, libbpf populates `prog_fd` and `prog_id`.
Those are attach-only fields and libbpf rejects them during detach. The tested
PyDivert revision reuses the populated options structure and receives
`-EINVAL`, leaving stale TC filters behind.

`_prepare_linux_diverter_close()` in
[`sni_fragment_proxy_strict.py`](../src/backend/sni_fragment_proxy_strict.py)
zeros only those two fields immediately before PyDivert closes the hook. This
is intentionally app-local so no second edit inside `site-packages` is needed.

### 3. Concurrent strict flows (application workaround)

Each active exact-flow capture receives a unique PyDivert priority. Reusing one
priority for simultaneous TC hooks caused collisions. Priorities are returned
to the allocator when a flow closes.

### 4. Geneva inbound pass-through (harness compatibility subclass)

With the installed modern Scapy/NetfilterQueue versions, the old Geneva
callback reserialized even an untouched incoming SYN/ACK and broke the TCP
handshake. `geneva_runner.py` accepts the original NFQUEUE bytes directly when
the strategy has no inbound action tree. Strategies that contain inbound
actions still use Geneva's normal callback and must be tested separately.

No files below `/home/asuna/geneva` were edited for this workaround.

## Clean Linux strict-mode installation

Strict mode currently supports Linux x86-64/aarch64 with kernel 5.8+ and must
run with root privileges. On Arch, install the build/runtime tools first:

```bash
sudo pacman -S --needed git base-devel clang llvm libbpf iptables-nft passt wireshark-cli
```

Create/sync Porn Fetch's environment, then install the tested PyDivert commit:

```bash
uv sync --extra gui
uv pip install --python .venv/bin/python3 \
  'git+https://github.com/ffalcinelli/pydivert.git@0b84da51df8bddb6c5843181ca1f11d026975067'
```

Build and install the patched eBPF object from the repository root:

```bash
patch_work_dir=$(mktemp -d)
git clone https://github.com/ffalcinelli/ebpfdivert.git \
  "$patch_work_dir/ebpfdivert"
git -C "$patch_work_dir/ebpfdivert" checkout v0.0.2
git -C "$patch_work_dir/ebpfdivert" apply \
  "$PWD/testing/pydivert_linux/ebpfdivert-v0.0.2-ethernet.patch"
make -C "$patch_work_dir/ebpfdivert" ebpfdivert.bpf.o

object_dir=$(
  .venv/bin/python3 -c \
    'from pathlib import Path; import pydivert; print(Path(pydivert.__file__).parent / "bpf")'
)
cp "$object_dir/ebpfdivert.bpf.o" \
  "$object_dir/ebpfdivert.bpf.o.upstream-v0.0.2"
cp "$patch_work_dir/ebpfdivert/ebpfdivert.bpf.o" \
  "$object_dir/ebpfdivert.bpf.o"
```

An environment reinstall may restore PyDivert's upstream object; reapply the
object copy afterward. Do not use this `v0.0.2` patch against a newer source
tree without reviewing its L2 parser first.

Find the actual Internet-facing interface, then smoke-test as root:

```bash
ip route get 1.1.1.1
sudo .venv/bin/python3 testing/sni_proxy_smoke.py \
  --strict --interface INTERFACE --concurrency 2 https://example.com/
sudo .venv/bin/python3 testing/sni_proxy_smoke.py \
  --strict --interface INTERFACE --desync https://example.com/
```

`kernel.unprivileged_bpf_disabled=2` was set on the test host, so a rootless
strict process could not load the TC/BPF program. The GUI itself must therefore
be launched elevated when Strict mode is enabled. Lite mode needs no elevated
rights or PyDivert.

After a test, verify that no filter remains. A harmless empty `clsact` qdisc may
remain, but both filter listings should be empty:

```bash
sudo tc filter show dev INTERFACE ingress
sudo tc filter show dev INTERFACE egress
```

Do not delete an existing qdisc automatically; it may belong to the host's
network manager or another application.

## Clean Windows strict-mode installation

Use 64-bit Python on x86-64 Windows and install the same PyDivert revision in
Porn Fetch's virtual environment:

```powershell
uv sync --extra gui
uv pip install --python .venv\Scripts\python.exe `
  "git+https://github.com/ffalcinelli/pydivert.git@0b84da51df8bddb6c5843181ca1f11d026975067"
```

Run Porn Fetch from an elevated Administrator terminal so PyDivert can load
WinDivert. The Linux eBPF object patch and TC-detach workaround do not apply on
Windows. Official WinDivert packages do not provide the expected signed ARM64
driver, so Windows ARM64 is rejected unless a vendor-signed custom driver is
deliberately supplied and the unsupported override is enabled.

The Geneva harness below is Linux-only because it relies on user/network
namespaces, `pasta`, iptables and NFQUEUE. On Windows, test strict mode with
Wireshark/Npcap on the physical adapter. Capture filters do not isolate a
process, so close unrelated applications and filter by the exact source port or
remote IP printed during a debug run.

## Isolated Geneva environment

The harness files are:

- [`geneva_isolated/run.sh`](geneva_isolated/run.sh): creates the namespace and
  starts one chosen command.
- [`geneva_isolated/geneva_runner.py`](geneva_isolated/geneva_runner.py): runs
  Geneva and the command in that namespace.
- [`geneva_isolated/README.md`](geneva_isolated/README.md): short operator
  reference.
- `geneva_runs/`: mode-0700 per-run captures/logs; ignored by Git.

The topology is:

```text
host network (unchanged)
        |
        | pasta userspace boundary + namespace-wire.pcap
        |
fresh user/network namespace
        +-- Geneva + namespace-local iptables/NFQUEUE
        +-- exactly one requested Porn Fetch/test command
```

`pasta --config-net --ipv4-only --no-map-gw --tcp-ports none --udp-ports none`
provides outbound connectivity without forwarding host ports or exposing the
special host-loopback gateway. The namespace is IPv4-only because this Geneva
revision installs only iptables rules; IPv6 would otherwise bypass Geneva.

For the default client-side ports `80,443`, Geneva creates namespace-local
rules equivalent to:

```text
iptables -A OUTPUT -p tcp -m multiport --dports 80,443 -j NFQUEUE --queue-num 2
iptables -A INPUT  -p tcp -m multiport --sports 80,443 -j NFQUEUE --queue-num 1
iptables -A OUTPUT -p udp -m multiport --dports 80,443 -j NFQUEUE --queue-num 2
iptables -A INPUT  -p udp -m multiport --sports 80,443 -j NFQUEUE --queue-num 1
```

No host `OUTPUT`, UID/owner, route, DNS or forwarding-sysctl rule is changed.
An owner match is unnecessary because only Geneva and the requested application
exist in the fresh namespace. Geneva deletes its rules on normal context exit;
if it crashes, destroying the namespace destroys the rules anyway.

The default strategy is `\/` (observe/pass) so Geneva records what the proxy
emits without adding another fragmentation strategy:

```bash
./testing/geneva_isolated/run.sh \
  .venv/bin/python3 testing/sni_proxy_smoke.py https://example.com/
```

Override strategy and ports for experiments:

```bash
GENEVA_STRATEGY='[TCP:flags:PA]-fragment{tcp:2:True}-|' \
GENEVA_PORTS='443' \
./testing/geneva_isolated/run.sh \
  .venv/bin/python3 testing/sni_proxy_smoke.py https://example.com/
```

Every run prints a directory below `testing/geneva_runs/`. The most useful
artifact is `namespace-wire.pcap`, produced at the `pasta` boundary. Inspect
outbound TLS payloads with:

```bash
tshark -r testing/geneva_runs/RUN_ID/namespace-wire.pcap \
  -Y 'tcp.dstport == 443 && tcp.len > 0' \
  -T fields -e frame.number -e tcp.seq -e tcp.ack -e tcp.len \
  -e tls.handshake.extensions_server_name -e tcp.payload
```

Wireshark may show the reassembled SNI on a later frame. That proves an
endpoint-quality TCP/TLS reassembler can recover it; it does not mean a single
wire packet leaked the whole hostname. Check each frame's `tcp.payload` when
testing packet-level fragmentation, and check the reconstructed stream when
testing resistance to a stateful listener.

The smoke tool disables ECH, forces HTTP/2 over IPv4/TCP, and does not alter
saved Porn Fetch settings. It supports `--reverse`, `--desync`, and
`--concurrency` for strict-profile testing.

On the verified Linux host, `tcpdump` attached to the same physical interface
did not see IPv4 frames re-injected below PyDivert's TC hook, although the
PyDivert trace recorded each injection and the HTTPS exchange succeeded. Do not
mistake this local capture-hook ordering for proof that a packet was absent on
the wire. For independent Strict-mode evidence, capture on a peer, router,
bridge mirror, or external adapter. The `pasta` boundary capture remains valid
for the rootless Lite/Geneva environment.

Strict mode cannot currently run inside this rootless Geneva namespace on the
test host because unprivileged BPF is disabled. Use the Geneva namespace for
Lite/baseline tests. Test Strict on the host as root: its own capture filter is
limited to the exact outbound 4-tuple opened by the loopback proxy, so it does
not intercept unrelated host flows. A future combined strict+Geneva test would
need a deliberately created root-owned network namespace rather than the
rootless `pasta` harness.

Packet captures can contain IP addresses, hostnames, cookies, and other private
application data. Keep `geneva_runs` private and do not commit or share its
contents casually.

## Regression checklist

1. Run the unit suite:

   ```bash
   .venv/bin/python3 -m unittest \
     testing.test_sni_fragmentation \
     testing.test_sni_proxy_manager \
     testing.test_client_refresh
   ```

2. Run Lite through the default Geneva pass-through strategy and confirm an
   HTTP 2xx/3xx response.
3. Run Strict Fragmentation, Strict Reverse, and Strict Desync as root against
   a harmless HTTPS endpoint.
4. Repeat Strict with `--concurrency 2` to exercise unique hook priorities.
5. Inspect the capture by individual payload and by reassembled TLS stream.
6. Confirm no TC ingress/egress filters remain after Strict exits.
