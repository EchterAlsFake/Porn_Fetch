# PyDivert 4 Linux compatibility patch

PyDivert 4 currently bundles the eBPFDivert v0.0.2 object. Its L2-offset
heuristic can mistake byte 4 of an Ethernet destination MAC for the start of a
raw IPv4/IPv6 packet. The result is that outbound port filters never match on
affected networks even though inbound capture works.

Porn Fetch works around PyDivert's separate TC-detach bug in
`sni_fragment_proxy_strict.py`. The bundled eBPF object still needs this
ABI-compatible v0.0.2 source patch until PyDivert ships an updated object.

Rebuild and install it into the active Porn Fetch virtual environment:

```bash
workdir=$(mktemp -d)
git clone https://github.com/ffalcinelli/ebpfdivert.git "$workdir/ebpfdivert"
git -C "$workdir/ebpfdivert" checkout v0.0.2
git -C "$workdir/ebpfdivert" apply \
  "$PWD/src/tests/manual/pydivert_linux/ebpfdivert-v0.0.2-ethernet.patch"
make -C "$workdir/ebpfdivert" ebpfdivert.bpf.o

object_dir=$(
  .venv/bin/python -c \
    'from pathlib import Path; import pydivert; print(Path(pydivert.__file__).parent / "bpf")'
)
cp "$object_dir/ebpfdivert.bpf.o" \
  "$object_dir/ebpfdivert.bpf.o.upstream-v0.0.2"
cp "$workdir/ebpfdivert/ebpfdivert.bpf.o" "$object_dir/ebpfdivert.bpf.o"
```

Strict mode must run as root and should normally be restricted to the actual
Internet-facing interface:

```bash
sudo .venv/bin/python src/tests/smoke/sni_proxy_smoke.py \
  --strict --interface enp10s0 --concurrency 2
```
