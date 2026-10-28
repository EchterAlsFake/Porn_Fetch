# Release payload size

Every executable build job writes a `size-diagnostics-*` artifact and a size table
in the GitHub Actions summary. Diagnostics stay separate from public downloads.
JSON reports contain byte counts, largest-first file lists, SHA-256 hashes and
identical-content groups. Directory symlinks are not counted twice. ZIP/APK and
TAR contents are inspected without extraction. DMGs and PyInstaller executables
are opaque files: their content byte count describes the container, not installed
size. The matching macOS app inventory and PyInstaller collection diagnostics
provide the additional payload breakdown. Do not add container and directory
sizes together; they describe different representations of the same application.

Desktop builds also preserve Nuitka's `deployment/compilation-report.xml`.
CLI builds preserve PyInstaller TOCs, import cross-references, warnings and
`payload-inventory.json`. The latter records collection inputs, so Python module
source sizes are not their final compiled/compressed sizes.

To compare reports from two runs of the same target, use the same source version,
lockfile, runner/toolchain and signing setup. Download the older JSON and run:

```bash
python packaging/report_sizes.py --label linux-x64 \
  --paths 'PornFetch_linux_GUI_x64.tar.gz' \
  --baseline previous.json --output current.json
```

Comparisons match artifact paths and record byte and percentage differences in
`comparison`. Negative deltas mean a reduction. Labels and checksums need not
match; artifact paths must match. Timing, native dependency changes and signing
can affect results, so compare equivalent builds.

## Compression experiments

Manual cross-platform workflows expose `benchmark_compression` (default false).
It compares Qt IFW levels 5, 7 and 9 on identical staged inputs for each installer
and repository. It retains the smallest output, choosing the lower level on ties,
and records elapsed seconds and bytes in `*.compression.json` diagnostics. These
experiments build each output three times and may exceed normal job timeouts;
run them separately from publishing. Normal builds retain IFW level 5.

The repository builder also accepts `--compression 7` or
`--benchmark-compression` for local experiments with the existing build arguments.
Benchmark destinations must not already exist.

## Payload changes

- Portable desktop bundles keep PocketBase only under `third_party`, already
  supported by executable discovery. Desktop launchers are renamed instead of copied.
- Frozen desktop GUI builds include `resources.rcc` and exclude its generated
  Python fallback. Development and Android retain the fallback. All translations,
  Qt styles, diagnostics and runtime resources remain supported.
- CLI collection follows ordinary imports, with explicit dynamic provider imports
  taken from the shared provider registry, including Empflix and Tnaflix.
- Android excludes source trees used only for tests, packaging and development.
  Runtime JSON, compiled translations, generated resources, native build recipes
  and Java build hooks remain available to the build. The docs fixture directory
  remains available for diagnostics.

Native stripping, UPX changes, alternate archive formats and further Qt module
removal are deferred until inventories and platform smoke checks establish a
measurable benefit. Make any future native payload edits before signing and
checksum/update metadata generation. Preserve bundled notices and provenance.

## Initial local measurement

On the development Linux x64 environment, the previous and optimized CLI specs
were built with the same installed dependencies and PyInstaller. The previous
executable was 45,468,464 bytes; the optimized executable was 45,131,920 bytes:
a reduction of 336,544 bytes (0.74%). Both local builds excluded CI's fetched Tor
payload. The optimized archive contained all 15 provider packages and no PySide6
modules; its four packaged offline self-checks passed. This is a local comparison,
not a size prediction for other architectures or release dependency sets.
