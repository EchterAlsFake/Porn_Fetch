# PocketBase binary layout

Download tracking uses the PocketBase executable directly; no Python PocketBase
SDK is required. Builds must ship the PocketBase v0.40+ executable beside the
Porn Fetch executable:

- Linux/macOS: `pocketbase`
- Windows: `pocketbase.exe`

The file must be executable on Linux and macOS. For source runs, the same file
can be placed in the repository root, installed on `PATH`, or selected with the
`PORN_FETCH_POCKETBASE_BINARY` environment variable.

PocketBase listens only on a random `127.0.0.1` port. Porn Fetch creates the
schema through an embedded migration, authenticates as a local superuser, and
stops the child process during application shutdown. The configured data folder
contains PocketBase's `data.db`, auxiliary files, and the applied migration.
