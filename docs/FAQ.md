# Frequently asked questions

## Does the README describe the latest downloadable release?

No. The default branch documents the in-development 3.9 rewrite. The latest
published 3.8 binaries are substantially older. See [STATUS.md](STATUS.md).

## Is payment live, and do older beta licenses work?

The backend handoff dated 6 October 2026 reports that NOWPayments is still sandboxed
and Patreon is disabled. This client targets the new commercial policy; it rejects
old beta credentials locally. Use a commercial-policy TEST credential for testing.
See [licensing architecture](LICENSING_ARCHITECTURE.md) for the release boundary.

## What happens after the update year?

Versions released on or before your update entitlement end remain licensed.
Newer versions require renewal. The separate seven-day offline grace still applies.
Renewal keeps the same key and installation UUID; refresh the license afterward.

## Can the CLI run without Qt?

Yes. CLI, shared, database-core, and licensing modules intentionally avoid Qt.
The CLI is intended to work on headless systems, including Termux.

## Where are development and installation instructions?

- [Development guide](FOR_DEVELOPERS.md)
- [Installation guide](INSTALLATION.md)
- [Supported websites](WEBSITES.md)
- [Security policy](../SECURITY.md)
