# Live browser-cookie account tests

## Complete account-page checks

In `uv run src/tests/helper.py`, select **Complete account GUI checks (real Brave
cookies, desktop/mobile ListViews)**. This runs deterministic QML control/error
contracts, then live account imports and list loading using the real
`browser_cookie3`, provider clients, GUI backend, `ProcessVideos`, Qt list model
and production Downloads delegates. Existing cookies and populated account lists
are local prerequisites; missing/expired sessions fail rather than producing a
simulated successful login.

```bash
PYTHONPATH=../unofficial-api-for-xhamster uv run python -m src.tests.smoke.account_gui --browser brave
```

The default live checklist has **36 checks** across the desktop and mobile QML
layouts. It covers every visible account action and verifies that the action
inventory has no untested additions:

| Area | Checks |
| --- | --- |
| Login | All three browser sessions; native server verification; busy and duplicate-request guards |
| Manual tokens | Actual Brave XVideos tokens entered through each layout; fresh token login followed by account liked-video loading |
| Collections | PornHub history/recommendations/feed/favorites, XHamster likes/account playlist, XVideos watch later/history/likes, on both layouts |
| Rendered rows | All nine Qt model roles and actual ListView delegate properties; visible title/author/duration; video identity, tags, thumbnail URL and origin collection |
| State | Loading/idle transitions, disabled duplicate actions, row insertion notifications, removal and reuse of the list |
| Help and inputs | Provider-specific real help dialogs; credential/token routing, masked secret fields, required input gating and Android browser-import exclusion |
| Errors and cancellation | Invalid collections/playlists, unsupported provider, expired/rejected login, unexpected failures, stale account notification, cancellation and recovery |

Positive data paths make real requests and prepare real video metadata. The
separate deterministic contracts use a recording bridge for form arguments and
explicit exceptions for recovery paths; they do not fabricate successful
provider responses or account rows, or submit deliberately invalid credentials.
Media downloads remain blocked. Native password authentication was verified
separately with the Zenity runner below; default GUI runs do not need passwords.
The account iterator policy treats HTTP 404 on later pagination pages as the end
of a collection. First-page, access-denied and item-metadata failures remain
visible; unavailable later pages cannot abort already available recommendations.

The report `/tmp/porn-fetch-account-gui.json` records `planned_checks`, individual
outcomes, deterministic-contract results and `action_coverage`. **100% here means
every check in the selected GUI action checklist passed**, not 100% Python
line/branch coverage or proof against all future upstream behavior. Missing checks
cannot silently count as passes. Mobile checks render the real Android QML
pages on desktop with real browser sessions; they do not test Android OS cookie
extraction, which the app does not offer.

On HTTP 429, the GUI runner waits **at least 30 seconds**, honors any longer
server `Retry-After`, then retries the same safe read request. From that point
on, requests are serialized across all provider cores with **at least 5 seconds
between requests**, including prefetches. Recovery is limited to two retries per
request. GET/HEAD/OPTIONS and the known read-only XVideos account-list POST
endpoints may be replayed; password submissions and other writes are not.

HTTP 401/403/451, explicit CAPTCHA pages and unsupported JavaScript challenges
still stop the run immediately. The recognized HTTP-200 PornHub math payload on
HTTPS `pornhub.com` hosts passes unchanged to `eaf_base_api`'s existing handler;
the test guard does not calculate answers or inject cookies. The GUI report's
`native_challenges` records these delegations without challenge tokens or cookies.
An exhausted 429 retry budget also stops with `BLOCKED`. No identity/proxy
rotation is performed. Expected anonymous
401/403 denials are permitted only inside the final private-playlist probe,
which never attempts to bypass them.

Console messages announce cooldowns; the report records every 429 recovery,
server delay, retry decision and total waiting time. Intentional cooldown/pacing
waits extend the check deadline rather than exhausting its network-work budget.
`--request-delay 5` starts a cautious run with five-second spacing immediately.
`--rate-cooldown` (minimum 30), `--recovery-delay` (minimum 5) and `--rate-retries`
(default 2; 0 stops immediately) configure this policy. Ctrl+C can interrupt waits.

An earlier extended run encountered XVideos HTTP 429 responses. Those results
remain visible rather than being counted as passes; later runs use the recovery
policy above.

Use repeated `--provider pornhub|xhamster|xvideos`, `--layout desktop|mobile|all`,
`--items 1|2|3`, `--timeout SECONDS` or `--report PATH` to focus a run. `--live-only`
skips the deterministic contracts for troubleshooting and records that omission.
The helper optionally accepts an XVideos playlist fixture too:

```bash
uv run python -m src.tests.smoke.account_gui --browser brave \
  --xvideos-playlist 'https://de.xvideos.com/favorite/PLAYLIST_ID/name'
```

That adds actual playlist loading through the GUI backend into the rendered
list. For a **genuinely private** fixture, also pass `--xvideos-private` (or answer
the helper's private-playlist question). This additionally requires authenticated
rows and denial/empty results for a fresh anonymous client. Public playlists
fail that privacy assertion. With no private fixture, private authorization is
explicitly unverified; cookie presence alone is not recorded as a test result.

## Lightweight account API checks

This opt-in suite reads cookies for PornHub, XHamster and XVideos from one
explicit browser and exercises the actual provider libraries and the app's CLI
account service. It prepares real video metadata without downloading media.
Normal unit/integration discovery and CI do not run it.

```bash
uv run python -m src.tests.smoke.account_cookies --browser brave
```

The interactive test helper includes **Live Brave cookie login and account lists**
and asks before accessing browser sessions. Direct module invocation opts in to
reading the selected browser's site cookies and making authenticated requests.
Browser cookies stay in memory. The suite never submits passwords, signs out the
browser, edits playlists or likes, or saves the cookie jar. The provider's native
PornHub recommendations method also invokes its cookie-consent helper, matching
the normal account flow.

## Checks

- Cookie import and a live, uncached server check of the authenticated account
  menu/state. Constructing an `Account` object alone does not count as login.
- PornHub history, favorites, recommendations, subscription feed and an account
  playlist. The username is discovered from the authenticated menu; optionally
  use `--pornhub-username NAME` to require a particular account.
- XHamster liked videos and an account playlist. Both modern
  `/my/favorites/videos/ID` and legacy `/my/playlists/ID` URLs are accepted.
- XVideos history, liked videos, watch later and a supplied account playlist.
  The provider's `get_recommended_videos()` method actually reads history.
- Returned video URLs route to the correct provider. Real video metadata must
  load with usable titles. The default sample is two videos per collection,
  with one listing page and bounded concurrency.
- A separate fresh anonymous client must fail the authentication check for
  each provider. The authenticated clients are closed independently.

Seed history, liked/favorite videos and playlists before running. An empty
seeded collection fails. An empty recommendations/feed/watch-later list is
reported separately as `EMPTY`; it does not count as verified video content.
A playlist that cannot be discovered is `UNVERIFIED`, not a successful test.

The checks establish authentication, collection access and metadata preparation.
They do not compare every result with a manually supplied inventory of expected
video IDs, or drive QML account buttons. A public playlist verifies playlist
loading, not private-playlist authorization; authentication has its own check.

## Focused runs and playlist URLs

```bash
# Use one provider; --provider can be repeated.
uv run python -m src.tests.smoke.account_cookies --browser brave --provider xvideos

# Supply a playlist when the account dashboard renders its links through JavaScript.
# Localized site hosts are accepted. Use your own URL, not a session/token URL.
uv run python -m src.tests.smoke.account_cookies --browser brave --provider xvideos \
  --playlist 'xvideos=https://de.xvideos.com/favorite/PLAYLIST_ID/name'
```

`--playlist PROVIDER=URL` can be repeated for all three sites. Playlist fixtures
remain command arguments rather than embedding personal account URLs in source.
`--items` accepts 1–3. `--timeout` limits each check (default 90 seconds).

The XHamster account extractor fix lives in the sibling source checkout until
the updated provider package is published. To use that actual implementation:

```bash
PYTHONPATH=../unofficial-api-for-xhamster uv run python -m src.tests.smoke.account_cookies --browser brave
```

The same source selection works for the helper and complete GUI suite:

```bash
PYTHONPATH=../unofficial-api-for-xhamster uv run src/tests/helper.py
```

Installed XHamster 2.6.3 without the account JSON parser fix can authenticate
successfully yet return zero liked-video rows on both layouts. Check the
report's `xhamster_source` and `xhamster_account_json_fix` fields. The tests do
not silently substitute a different library; use the fixed checkout explicitly
or publish/install a new provider release containing the fix.

After publishing the provider fix, update the project environment:

```bash
uv lock --upgrade-package unofficial-api-for-xhamster
uv sync --extra gui --group dev
```

## Reports

The default report is `/tmp/porn-fetch-account-cookies.json` on Linux, or the
equivalent system temporary directory elsewhere. Change it with `--report PATH`.
It contains provider/check names, results, sample counts, numeric metadata,
library versions and the actual XHamster source path. It excludes cookie/token
values, account names, raw responses, video titles and video/playlist URLs.
Upstream exception messages are omitted because they can contain signed URLs.

Any failed or unverified check yields exit code 1. Ctrl+C records the interrupted
check and closes the client pool, then exits with code 130. Browsers can require
OS keyring access for cookie extraction; extraction failure is not a login pass.

## Password login through Zenity

The separate password runner uses fresh clients and the native PornHub and
XHamster password-login methods. It then runs the same account-list, playlist,
metadata and anonymous-client checks. It does not read browser cookies.

```bash
PYTHONPATH=../unofficial-api-for-xhamster uv run python -m src.tests.smoke.account_passwords \
  --pornhub-email 'your-test-email@example.com' --xhamster-username 'your-test-username'
```

Zenity must be installed. Its password dialog collects one shared password for
the temporary test accounts. The password is captured directly into process
memory; it is not passed as a command argument, environment variable or report
field. Cancelling the dialog makes no login attempts. `--provider pornhub` or
`--provider xhamster` narrows the run and requires only that site's identifier.
The report defaults to `porn-fetch-account-passwords.json` in the system
temporary directory. `--items`, `--timeout` and `--report` work as above.

XVideos is excluded from the password runner: its provider library exposes
cookie/token authentication only. The website's account page also references
Friendly CAPTCHA in its form configuration. No XVideos password submission or
CAPTCHA/access-control bypass was attempted. Its cookie tests remain available
in the cookie runner.
