# Tests

See the [testing guide](../../docs/TESTING.md) for setup, runner commands and
manual platform checks.

- `unit/`: offline Python checks.
- `integration/`: Qt and service integration checks.
- `smoke/`: explicitly selected end-to-end checks, including real providers.
- `manual/`: device and laboratory procedures.

Start the selector from the repository root:

```sh
uv run --no-sync python src/tests/helper.py
```

Live tests need explicit opt-in. Do not add real downloads or browser-cookie
access to ordinary unit or integration discovery. Keep failures, unavailable
providers and missing private fixtures visible in reports.
