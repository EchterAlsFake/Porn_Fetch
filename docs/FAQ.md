# Frequently asked questions

## Does the README describe the latest downloadable release?

No. The default branch documents the in-development 3.9 rewrite. The latest
published 3.8 binaries are substantially older. See [STATUS.md](STATUS.md).

## Is the 3.9 beta license a real purchase?

No. The beta uses the normal license import and validation path, but its crypto
checkout is a sandbox. Visit [pornfetch.to](https://pornfetch.to/),
press the sandbox purchase button, and import the resulting license file.
There is no real transaction and no money is processed. See the
[3.9 installation guide](INSTALLATION.md).

## Can the CLI run without Qt?

Yes. CLI, shared, database-core, and licensing modules intentionally avoid Qt.
The CLI is intended to work on headless systems, including Termux.

## Where are development and installation instructions?

- [Development guide](FOR_DEVELOPERS.md)
- [Installation guide](INSTALLATION.md)
- [Supported websites](WEBSITES.md)
- [Security policy](../SECURITY.md)
