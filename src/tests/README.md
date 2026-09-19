# Tests

Run the interactive test selector from the repository root:

```bash
uv run src/tests/helper.py
```

Offline suites are safe by default. The helper asks for explicit confirmation
before real network requests and asks again before an active media download.

The test tree is grouped by purpose:

- `unit/` contains deterministic, offline tests.
- `integration/` covers Qt adapters and service boundaries.
- `smoke/` contains opt-in network and local-server checks.
- `manual/` contains release and SNI laboratory procedures.


# Checklist
- [] Updated version in window title
- [] Updated UI with update.sh script
- [] Updated dependencies for Nuitka / Qt
- [] Verified that a clean fresh run of Porn Fetch on an independent system works
- [] Test Installation on macOS, Windows and Linux
- [] Text Proxy and Kill Switch feature for reliability, disconnect connection to see what happens
- [] Test each supported function for each website with default settings (See urls.txt)
- [] Test all widgets of the GUI
- [] Test donation nag
- [] Especially test the update changelog with a fake update (temporary)
- [] Test all build scripts

## Fake update popup

Start the local fake-update server in one terminal:

```bash
python src/tests/smoke/fake_update_server.py
```

Then start the QML application from another terminal with the development
endpoint override:

```bash
PORNFETCH_UPDATE_URL=http://127.0.0.1:8765/update python main.py
```

The server advertises version 4.0 with fake HTML release notes and harmless
download-link test pages. It deliberately does not advertise a platform binary,
so it cannot be used to install or replace the application.
