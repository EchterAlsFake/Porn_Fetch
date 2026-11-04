# Porn Fetch licensing and release checks

Releases that explicitly identify the Porn Fetch Source-Available License 1.0
use the repository [LICENSE](../LICENSE) for application-owned material. Older
copies distributed under GPL-3.0-or-later keep those grants; the historical
text is at [LICENSES/GPL-3.0-or-later.txt](../LICENSES/GPL-3.0-or-later.txt).
The source-available license is not an open-source license under the Open Source
Definition. It allows private sharing of modified builds, including local
premium bypasses, but does not allow public cracked builds or forks.

Premium credentials are separate from copyright permissions. Sharing the app
does not grant another installation a premium entitlement. The source license's
publication rule and website Terms cannot bind people who never accepted them;
independent discussion and mandatory software rights must be respected.

Before publishing a source-available release:

1. Confirm rights to all surviving app contributions, translations, and assets.
   Record any separate grants needed for provider packages, including
   contributors other than Johannes Habel.
2. Build each supported artifact and inspect its actual dependency set. Bundle
   the exact applicable notices, license texts, and source/relinking information
   required for Qt, PocketBase, FFmpeg, and Python dependencies.
3. Confirm the delivered source and builds display the same application license
   and make the license and third-party notices easy to find in the GUI and CLI.
4. Obtain German/EU legal review of the custom license, the separate tutorial
   rule, the Terms acceptance flow, and any consumer-facing paid offer. The
   current test checkout checks an explicit acceptance flag but does not yet
   retain the accepted Terms version or a durable acceptance record; add that
   evidence before a live paid checkout.

The related Server repository remains a separate project. Its Terms and Privacy
Policy must describe the code and actual deployment at the time a service is
offered. Current operational progress belongs in the
[server checklist](https://pornfetch.to/checklist), rather than a deployment
status inferred from this checkout. The production client targets the new
commercial policy and explicitly rejects older beta credentials.

## Premium licenses

The first-launch offer shows a one-time price of €19.99, payment by crypto or
credit card at <https://pornfetch.to>, support for 350+ currencies, and no subscription. A license can be
shared with friends and family within the total limit of ten active installations.
No user account or hardware fingerprint is required; activation uses a random
installation ID and is not tied to an IP address.

Premium enables qualities above 720p, bulk downloading and parallel downloads. Import a signed key or
license file in the GUI, or use License Management in the CLI. The current client
uses schema 2 and the commercial policy; old beta credentials are rejected.
Updates themselves are free and do not require a premium license.

Without an active premium license, public model, channel and playlist URLs show
only their first five videos. Account collections are exempt from this preview
limit. Free use supports up to 720p and one active download at a time.

A license covers builds released within one year (31,556,952 seconds) of first
activation, on up to ten installations. Entitled builds remain usable after
that year, subject to validation. Renewal extends build eligibility.

First activation tries online validation. A valid signed production license can
receive a three-day initial grace period for connection failures or timeouts.
Explicit rejection, HTTP errors, malformed responses and TLS trust errors do not
qualify. Reimporting or restarting does not reset the period. After successful
validation, offline use lasts up to seven days. A rejection remains effective
through later outages. The client also checks for clock rollback.

## Client implementation

`src/licensing/` is shared by the Qt-free CLI and the GUI's license bridge.
The client verifies the signed payload before trusting its claims. Keep its
serialized bytes and signing format compatible with the server. Public keys
belong in the client; private signing keys never do.

An installation has a random identifier, not a hardware fingerprint. The GUI
and CLI share the licensing data location through the common storage code.
Storage uses platform-specific writable application data paths. Existing GUI
storage is reused where supported; do not move it without a migration.

The payment and validation server is deployed separately. Test-client results
do not establish that checkout, consent records, email delivery or recovery are
ready in production. Track those items on the website checklist. Keep signing
keys and recovery backups outside this repository.
