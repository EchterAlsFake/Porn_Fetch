# SNI proxy agent handoff

Last updated: 2026-08-15 (Europe/Berlin)

This is the primary handoff for another AI agent continuing work on Porn
Fetch's application-local SNI obfuscation proxy. Read this file first, then read
[`testing/SNI_PROXY_LAB.md`](testing/SNI_PROXY_LAB.md) before changing the
native Linux backend or the Geneva harness.

## Current status

Lite and Strict modes both work. Strict Fragmentation, Strict Reverse, and the
new Strict Desync profile are wired into settings and the UI. Unit tests, QML
validation, live Strict requests, and an isolated Geneva Lite run have passed.

The repository has a dirty working tree containing user work and the proxy
implementation. Many relevant files are currently untracked. Do not reset,
clean, replace, or broadly reformat the tree. Inspect `git status` and preserve
unrelated changes before editing.

The active project and virtual environments are:

```text
project:        /home/asuna/PycharmProjects/Porn_Fetch
Porn Fetch:     /home/asuna/PycharmProjects/Porn_Fetch/.venv/bin/python3
Geneva checkout:/home/asuna/geneva
Geneva Python:  /home/asuna/geneva/.venv/bin/python3
```

## Work completed during the last two hours

In roughly chronological order, this session:

1. Audited `test.py`, settings, client construction, Qt signal/slot wiring, and
   both proxy implementations. Corrected lifecycle and fail-closed routing so
   the local proxy starts before refreshed curl-cffi sessions use it.
2. Added the shared TLS ClientHello parser and SNI-aware stream fragmenter, then
   integrated it into Lite and Strict.
3. Installed and exercised PyDivert 4's Linux backend. Diagnosed the outbound
   filter failure to eBPFDivert's Ethernet-offset heuristic, built the patched
   BPF object, and saved the upstream object beside it.
4. Diagnosed PyDivert's libbpf TC-detach failure and added an app-local cleanup
   workaround. Added unique priorities for concurrent exact-flow hooks.
5. Built the `pasta`-based rootless Geneva harness, kept all NFQUEUE rules in an
   isolated namespace, added the modern Scapy inbound pass-through workaround,
   and captured a successful Lite request.
6. Examined GoodbyeDPI and compared its fragmentation/desynchronization methods
   with this proxy. Added the Strict Reverse and safer first Strict Desync
   profile, deliberately leaving wrong-checksum and TTL methods disabled.
7. Added packet doubles/real `Packet` regression coverage, manager/client tests,
   strict live smoke flags, and clean-install/lab documentation.
8. Rewrote the user-facing SNI explanation to describe the implementation and
   limitations accurately.
9. Diagnosed the latest startup failure to simultaneous persisted Lite+Strict
   flags. Replaced QML toggle writes with an atomic mode slot, added migration
   tests, hid Strict-only choices in Lite, and documented the `sudo -E` settings
   requirement.

The sections below record the resulting design rather than just the sequence of
edits.

## Architecture at a glance

```text
curl-cffi sessions owned by Porn Fetch
        |
        | SOCKS5 URL stored only in app_settings.active_sni_proxy_url
        v
127.0.0.1 local SNI proxy
        |
        +-- Lite: SNI-aware ClientHello socket-write fragmentation
        |
        +-- Strict: the same stream fragmentation
                   + exact outbound 4-tuple PyDivert capture
                   + real TCP packet segmentation/reinjection
                   + optional reverse order / desync decoy
        |
        +-- direct destination, or the user-configured upstream proxy
```

Only Porn Fetch clients are explicitly pointed at the loopback proxy. This is
not a system-wide proxy. For Strict mode, every Internet-facing socket is
registered as an exact source-address/source-port/destination-address/
destination-port flow before the local proxy acknowledges CONNECT, preventing
the first ClientHello bytes from racing ahead of interception.

When SNI proxying is active, `clients.py`:

- replaces the configured live proxy with the loopback URL;
- forces HTTP/2 over TCP, avoiding HTTP/3/QUIC bypass;
- leaves the Internet-facing interface/source binding to the local proxy; and
- refreshes the curl-cffi sessions so stale sessions do not bypass the proxy.

If startup fails, `SNIProxyManager` fails closed by assigning
`socks5://127.0.0.1:9`. This deliberately blocks requests instead of silently
sending unobfuscated traffic.

## ClientHello parsing and stream fragmentation

[`src/backend/tls_client_hello.py`](src/backend/tls_client_hello.py) contains a
bounded TLS record/handshake parser and `TLSClientHelloStreamFragmenter`.

The fragmenter buffers only the beginning of a connection until it can locate
the ClientHello SNI extension, including when the handshake crosses TLS record
or socket-read boundaries. It chooses a split point inside the hostname,
normally near its midpoint. The two writes therefore contain different pieces
of the name. It waits 10 ms between writes by default. Non-TLS or unparseable
traffic falls back to the configured byte offset, currently byte 2, without
indefinite buffering.

This is stronger than blindly splitting at byte 2 at the stream layer, but it
is not encryption: a TCP/TLS reassembler can reconstruct the hostname.

## Lite mode

Implementation: [`src/backend/sni_fragment_proxy_lite.py`](src/backend/sni_fragment_proxy_lite.py)

Lite is a loopback SOCKS5/HTTP-CONNECT proxy using normal asynchronous sockets.
It runs in a spawned helper process and applies the shared SNI-aware stream
fragmenter to client-to-upstream traffic.

Advantages:

- no root/Administrator rights;
- no native packet driver;
- application-only routing; and
- cross-platform standard socket behavior.

Limitation: separate socket writes are not a wire-packet guarantee. The kernel,
offload hardware, a virtual network layer, or a later proxy may coalesce them.

## Strict mode

Implementation: [`src/backend/sni_fragment_proxy_strict.py`](src/backend/sni_fragment_proxy_strict.py)

Strict uses the same loopback and stream layer, then intercepts the exact
outbound proxy-created TCP flow with PyDivert:

- Windows x86-64: WinDivert;
- Linux x86-64/aarch64: PyDivert 4's eBPF/TC backend;
- macOS and Windows ARM64: rejected with a specific error.

Linux requires kernel 5.8+, libbpf, the patched eBPF object described below,
and root. Windows requires an elevated Administrator process. A new explicit
Linux preflight reports a clear root-privilege error before loading PyDivert.

The packet policy:

- splits the first outbound data packet of a new flow;
- remembers sequence boundaries and reapplies them to retransmissions;
- detects later plaintext HTTP/1.x request starts on configured HTTP ports;
- bounds emitted payloads to 1200 bytes so a GSO-sized skb does not depend on a
  later segmentation pass; and
- recalculates IP/TCP checksums after every genuine packet mutation.

### Strict profiles

`Strict Fragmentation`

: Sends genuine TCP segments in normal sequence order.

`Strict Reverse`

: Sends later genuine bytes first, then earlier bytes. A conforming destination
  TCP stack buffers/reorders the data. This is inspired by GoodbyeDPI's reverse
  native fragmentation behavior.

`Strict Desync`

: Sends one cloned, parseable fake ClientHello before the genuine data. The
  decoy uses SNI `www.example.com`, TCP sequence number minus 10,000, and ACK
  number minus 66,000. It has valid recalculated checksums but falls outside the
  receiver's expected TCP window, so the endpoint should discard it. Some
  stateless DPI may parse the decoy. Genuine fragments are then sent in reverse
  order.

The decoy is cloned from the captured packet. It never mutates the original
packet. If cloning or injection fails, the exception is logged and all genuine
fragments are still sent. It is injected only once, only for a recognizable TLS
record, and not for configured plaintext HTTP flows.

Wrong-checksum and TTL/hop-limit decoys were investigated but intentionally not
enabled. They have more network-specific failure modes and require separate
controlled testing.

## Application lifecycle

[`src/backend/sni_proxy_manager.py`](src/backend/sni_proxy_manager.py) owns one
Lite or Strict helper for the whole application. It:

- resolves a Linux interface name to a source IP;
- passes an existing user proxy as the SNI proxy's upstream;
- maps the selected Strict profile to reverse/desync configuration;
- publishes only the ephemeral loopback URL through the runtime-only
  `active_sni_proxy_url`; and
- restarts the proxy when the configured network interface or upstream proxy
  changes.

[`test.py`](main.py) creates this singleton, starts it before entering the main
GUI, refreshes the client sessions, displays a fail-closed startup error, and
stops the proxy during shutdown. Multiprocessing uses `spawn`; the GUI startup
is guarded so a Strict helper child does not create another Qt application.

## Settings bug fixed at the end of the session

The original QML radio buttons used `onToggled` for two separate Boolean
properties. QML initialization and ButtonGroup transitions could persist an
invalid pair. The real user settings file was found in this state:

```text
sni_obfuscation_lite=true
sni_obfuscation_strict=true
```

That caused startup to fail with the manager's exactly-one-mode check.

[`src/backend/config.py`](src/backend/config.py) now provides
`set_sni_obfuscation_mode(mode)`, which writes both Boolean keys before emitting
either notification and calls `QSettings.sync()`. QML invokes this slot only
from `onClicked`; automatic unchecks no longer write settings.

Startup migration behavior is:

- both Lite and Strict true: keep Strict and clear Lite, because Strict required
  an explicit prior choice;
- SNI enabled with neither mode selected: select Lite; and
- valid existing pairs: leave unchanged.

The current normal-user settings are repaired to:

```text
sni_obfuscation=true
sni_obfuscation_lite=false
sni_obfuscation_strict=true
strict profile key absent, therefore default = Strict Fragmentation
```

[`src/frontend/UI/SettingsPage.qml`](src/frontend/UI/SettingsPage.qml) now hides
the Strict profile ComboBox completely unless SNI obfuscation and Strict mode
are both selected. Lite users no longer see unavailable strategies.

### Important sudo/QSettings behavior

Plain `sudo` sets `HOME=/root` on this host. A separate file exists at:

```text
/root/.config/EchterAlsFake/Porn Fetch.conf
```

It contains no SNI selection, so launching the GUI with plain `sudo` can look as
though Strict reverted to Lite/defaults. The normal settings are at:

```text
/home/asuna/.config/EchterAlsFake/Porn Fetch.conf
```

For a Linux source run, use:

```bash
sudo -E .venv/bin/python3 main.py
```

On this machine `sudo -E` preserves `HOME=/home/asuna`; an elevated read test
confirmed it loads `True, False, True, Strict Fragmentation`. A temporary-file
test also confirmed QSettings preserved the existing user's file ownership.
This launch requirement is now explained in `AppStrings.qml`.

A future improvement should elevate only the Strict helper through a carefully
designed polkit/system helper instead of running the entire GUI as root.

## UI help text

[`src/frontend/UI/AppStrings.qml`](src/frontend/UI/AppStrings.qml) contains the
rewritten `sniObfuscationHelp`. The old text incorrectly described SNI as its
own packet, overstated guarantees, described Strict as an isolated device, and
used alarmist legal claims.

The new text accurately covers:

- SNI as a TLS ClientHello extension;
- Lite, Fragmentation, Reverse, and Desync behavior;
- application-only routing and upstream proxy chaining;
- platform/elevation requirements;
- TCP reassembly, DNS and destination-IP leakage;
- ECH as the direct cryptographic solution when supported;
- HTTP/2/TCP scope and lack of HTTP/3/UDP handling; and
- the lack of anonymity or a universal bypass guarantee.

## Upstream Linux backend and patches

Installed PyDivert is `4.0.0` from commit:

```text
0b84da51df8bddb6c5843181ca1f11d026975067
```

PyDivert currently bundles eBPFDivert `v0.0.2`. Its L2-offset heuristic could
mistake destination-MAC byte 4 for a raw IPv4/IPv6 header. On this network that
byte was `0x65`, so outbound filters did not match.

The source patch is:

[`testing/pydivert_linux/ebpfdivert-v0.0.2-ethernet.patch`](testing/pydivert_linux/ebpfdivert-v0.0.2-ethernet.patch)

It checks Ethernet ethertype at bytes 12-13 before raw-IP offsets. The patched
object is installed at PyDivert's package-local `bpf/ebpfdivert.bpf.o`.

Known hashes from this build:

```text
patched: 811f36fea8f84a826221706a5a3799493f8e50243c027440f3046542e9c23c01
upstream:38ef33829ed316619d27d6c7baf1c6021cd6b26fc05c3a1d26cfd587b2331b07
```

The installed backup is named `ebpfdivert.bpf.o.upstream-v0.0.2`.

There is a separate PyDivert TC-detach bug: libbpf rejects populated attach-only
`prog_fd` and `prog_id` fields during detach, returning `-EINVAL` and leaving
filters behind. `_prepare_linux_diverter_close()` zeros only those fields before
PyDivert exits. This workaround is application-local; installed Python source
was not patched.

Concurrent flows also require unique PyDivert/TC priorities. The strict backend
allocates priorities per active flow and releases them on close.

PyDivert is currently installed manually and is not yet a clean, locked project
dependency. `uv sync` or a reinstall may restore the upstream eBPF object.
Packaging/pinning this backend and applying or eliminating the object patch is
important release work.

Full clean Linux and Windows instructions are in
[`testing/SNI_PROXY_LAB.md`](testing/SNI_PROXY_LAB.md).

## GoodbyeDPI work

GoodbyeDPI was inspected at commit:

```text
f593a276f9ec753889f80208c6a7c5cf455df94a
```

Relevant behavior in its modern presets included native TCP fragmentation,
reverse fragment order, fake TLS ClientHello packets with wrong sequence/ACK or
checksum, a 1200-byte maximum payload, and QUIC blocking. Porn Fetch already
forced HTTP/2/TCP and already had native segmentation/max-payload handling.

The safe first extension implemented here was Reverse plus an opt-in,
wrong-sequence/wrong-ACK fake ClientHello. No GoodbyeDPI source or driver was
copied into Porn Fetch.

## Isolated Geneva test environment

Files:

```text
testing/geneva_isolated/run.sh
testing/geneva_isolated/geneva_runner.py
testing/geneva_isolated/README.md
testing/geneva_runs/                 # ignored, private run artifacts
```

The harness uses rootless `pasta` to create a fresh user/network namespace.
Geneva and exactly one requested app/test command run inside it. Geneva's
iptables/NFQUEUE rules exist only in the namespace; host firewall, routes, DNS,
UID rules, and forwarding sysctls remain unchanged. The boundary is IPv4-only
because this Geneva version programs iptables but not ip6tables.

Default strategy `\/` observes and passes traffic. A compatibility subclass
accepts untouched inbound bytes directly when there is no inbound action tree,
avoiding an old-Geneva/current-Scapy SYN/ACK reserialization bug. No Geneva
checkout files were modified.

Run the repeatable Lite baseline with:

```bash
./testing/geneva_isolated/run.sh \
  .venv/bin/python3 testing/sni_proxy_smoke.py https://example.com/
```

Each run produces a mode-0700 directory and `namespace-wire.pcap`. Captures can
contain sensitive traffic and must not be committed casually.

Strict cannot load BPF in this rootless namespace because the host has:

```text
kernel.unprivileged_bpf_disabled = 2
```

Strict is therefore tested as root on the host. Its PyDivert filter remains
limited to the proxy's exact flow. A combined Geneva+Strict lab would require a
deliberately built root-owned network namespace.

## Tests and observed evidence

Current regression command:

```bash
.venv/bin/python3 -m unittest \
  testing.test_sni_settings \
  testing.test_sni_fragmentation \
  testing.test_sni_proxy_manager \
  testing.test_client_refresh

qmllint src/frontend/UI/SettingsPage.qml src/frontend/UI/AppStrings.qml
.venv/bin/python3 -m compileall -q src testing main.py
git diff --check
```

Latest result: 19 tests passed; both QML files passed `qmllint`; compilation and
`git diff --check` passed.

Coverage includes:

- ClientHello SNI discovery across TLS records;
- stream splitting inside the hostname;
- non-TLS fallback;
- parseable fake ClientHello generation;
- stale decoy sequence/ACK values;
- reverse genuine fragment order;
- genuine-data preservation when decoy injection fails;
- desync configuration rejection;
- explicit non-root Linux error;
- unique concurrent priorities;
- TC detach-field cleanup;
- Lite manager startup/restart/fail-closed behavior;
- Strict Desync profile mapping;
- curl-cffi session refresh through the active local URL;
- legacy double-mode migration; and
- atomic Strict selection persistence.

Live Strict Desync was run as root on `enp10s0` against
`https://example.com/`. It returned HTTP 200. PyDivert logs showed:

1. one 150-byte first TLS payload captured;
2. a parseable `www.example.com` decoy injected first;
3. the 148-byte later genuine segment injected next;
4. the 2-byte earlier genuine segment injected last; and
5. the handle closed cleanly.

Afterward, both commands returned no filters:

```bash
sudo tc filter show dev enp10s0 ingress
sudo tc filter show dev enp10s0 egress
```

The Geneva-isolated Lite smoke request also returned HTTP 200. Its boundary
capture showed `example.com` divided between individual outbound payloads:
`examp` in one frame and `le.com` in the next. Wireshark displayed the complete
SNI on the later frame because it reassembled the TLS stream, which is expected.

Local `tcpdump` on the same Linux physical interface did not observe IPv4 frames
re-injected below PyDivert's TC hook, although the request succeeded and
PyDivert logged each injection. Do not treat that local capture-hook ordering as
wire proof. Obtain definitive Strict evidence from a peer, router, mirrored
bridge, or external capture adapter. Temporary root-owned test captures were
deleted.

## Working-file map

```text
src/backend/tls_client_hello.py              TLS/SNI parser and stream fragmenter
src/backend/sni_fragment_proxy_lite.py       portable loopback proxy
src/backend/sni_fragment_proxy_strict.py     exact-flow PyDivert backend/profiles
src/backend/sni_proxy_manager.py             application lifecycle/fail-closed route
src/backend/clients.py                       curl-cffi routing/session integration
src/backend/config.py                        QSettings properties and atomic mode API
src/frontend/UI/SettingsPage.qml             Lite/Strict/profile controls
src/frontend/UI/AppStrings.qml               user-facing technical explanation
test.py                                      startup, refresh, error and shutdown wiring
testing/sni_proxy_smoke.py                   repeatable Lite/Strict HTTP smoke client
testing/test_sni_fragmentation.py            TLS/packet/backend regression tests
testing/test_sni_proxy_manager.py            manager/profile tests
testing/test_sni_settings.py                 persistence/migration tests
testing/test_client_refresh.py               live client-route refresh test
testing/SNI_PROXY_LAB.md                     clean install and lab operations
testing/pydivert_linux/                      Linux eBPF patch and rebuild notes
testing/geneva_isolated/                     rootless app-only Geneva harness
```

## Known limitations and recommended next work

1. Do not claim the hostname is cryptographically hidden. Stateful TCP/TLS
   reassembly recovers plaintext SNI; DNS and destination IP remain signals.
2. Replace whole-GUI elevation with a narrow authenticated helper before
   treating Strict mode as production-ready.
3. Pin/package the PyDivert revision and patched BPF object reproducibly, or get
   both Linux fixes accepted upstream.
4. Validate Strict on Windows x86-64 with WinDivert and an external capture.
5. Capture Strict from a true downstream observation point and compare all
   three profiles against realistic stateful DPI.
6. Keep Desync opt-in. Some middleboxes may react differently to stale packets.
7. Do not add wrong-checksum or TTL tricks without connectivity fallbacks and
   controlled tests across local/LAN/WAN paths.
8. Translate the new `qsTr` source text if the project maintains compiled
   translation catalogs; only the source string was updated here.
9. Preserve fail-closed behavior whenever changing startup or settings logic.
10. Preserve the user's dirty worktree and private Geneva captures.
