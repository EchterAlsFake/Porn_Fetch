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

## Live GUI profile tests

Select **Online GUI profile/list-model checks** in the helper, or run explicitly:

```bash
# Thirty primary profile branches across eleven providers.
uv run python -m src.tests.smoke.profile_urls

# Also check localized URLs, aliases, tabs, filters and replacements.
uv run python -m src.tests.smoke.profile_urls --include-variants

# Focus on one provider; write JSON results and a sibling diagnostic log.
uv run python -m src.tests.smoke.profile_urls --include-variants --filter eporner --report /tmp/eporner-profiles.json
```

This runner uses offscreen Qt and isolated settings. Each case traverses the real
Backend, ProcessVideos, DownloadManager and DownloadListModel with one page and
at most two videos (`--items 1`, `2` or `3`). It checks insertion signals, profile
identity, video metadata, list roles, output paths and pending download state.
HLS playlists must resolve to a nonempty list of absolute segment URLs. Direct
file URLs are validated without fetching them. Download entry points and media
requests are blocked; thumbnails are checked as URLs without loading images.

RedTube and Tube8 numeric User profiles currently expose valid public metadata
but no public video feed. Their feeds are attempted, then reported as explicit
skips if still unavailable. A 403 from curl does not exclude a fixture: the app
transport must get its own chance to load it.

The default JSON report and `.log` are in the system temporary directory. A
failed case produces a nonzero exit code; skips are counted separately. Live
checks are opt-in and are excluded from normal offline test discovery and CI.

The existing desktop test entry point now supports:

```bash
uv run main.py --test                   # Existing video cases plus primary profiles
uv run main.py --test-profiles          # Primary profiles only
uv run main.py --test-profile-variants  # All positive profile variants
```

The standalone runner avoids normal database/license/update startup while
retaining the real preparation pipeline and Qt signals/model. The desktop
entry point uses the full backend startup. Both use the same profile validator.
Fixtures, source provenance, exclusions and coverage are documented in
[URL_TEST_FIXTURES.md](../../docs/URL_TEST_FIXTURES.md).


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
