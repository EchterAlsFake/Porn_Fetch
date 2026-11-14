# Porn Fetch licensing and release checks

Releases that explicitly identify the Porn Fetch Source-Available License 1.0
use the repository [LICENSE](../LICENSE) for application-owned material. Older
copies distributed under GPL-3.0-or-later keep those grants; the historical
text is at [LICENSES/GPL-3.0-or-later.txt](../LICENSES/GPL-3.0-or-later.txt).
The source-available license is not an open-source license under the Open Source
Definition. It allows private sharing of modified builds, including local
premium bypasses, but does not allow public cracked builds or forks. Friends
means people with an existing personal friendship in real life who have met in
person. Direct online delivery to those friends or individual family members is
allowed, including a private group consisting only of those people. Distribution
to a Discord server or another online community extending beyond that personal
circle does not qualify as private sharing, including when the group is closed
or its members are called friends. Compliant public distribution remains subject
to the license's separate public-distribution conditions.

Premium credentials are separate from copyright permissions. Sharing the app
does not by itself grant another installation a premium entitlement. Section 4
expressly permits sharing your own valid credential within that private circle,
with ten active installations in total including your own. It does not authorize
publishing the credential or sharing it outside that private circle. Section 6
preserves mandatory statutory rights; the optional termination and cure-period
provisions have been removed. The source license's publication rule and website
Terms cannot bind people who never accepted them; independent discussion and
mandatory software rights must be respected.

The maintainer confirmed after a specific review that no earlier contributions
requiring additional relicensing permission remain in this release's
application-owned code or translation catalogs. Relevant earlier contributions
were removed. This records the maintainer's review; third-party dependencies and
assets retain their own licenses.

Before publishing a source-available release:

1. Preserve the reviewed ownership boundary when adding contributions,
   translations, or assets. Record any new grants needed for relicensing. The
   provider permission applies only to portions Johannes Habel may license
   separately; retain third-party license compliance.
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

The first-launch offer shows a one-time price of €29.99, payment by crypto or
Patreon Shop (one-time purchase) at <https://pornfetch.to>, support for 350+ currencies, and no subscription. A license can be
shared through private sharing with individual family members and personal
friends known in real life and met in person, within the total limit of ten active
installations including the holder's own. Community membership alone does not
qualify recipients for this permission.
No user account or hardware fingerprint is required; activation uses a random
installation ID and is not tied to an IP address.

Premium enables qualities above 720p, bulk downloading, parallel downloads and
desktop/CLI [Media Library Export](JELLYFIN_METADATA.md). Import a signed key or
license file in the GUI, or use License Management in the CLI. The current client
uses schema 2 and the commercial policy; old beta credentials are rejected.
Updates themselves are free and do not require a premium license.

Without an active premium license, public model, channel and playlist URLs show
only their first five videos. Account collections are exempt from this preview
limit. Free use supports up to 720p and one active download at a time.

A lifetime Premium license never expires and includes every future Porn Fetch update
and feature I release, on up to ten active installations. Future development has no
guaranteed duration. There are no release-date cutoffs or license-renewal purchases.
If I permanently close the licensing service, I will provide an offline unlock before
closure so existing buyers can continue using Premium. Periodic validation remains
required until that unlock is provided. Third-party websites and operating-system
compatibility can change; statutory rights remain unaffected.

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

## Lifetime release configuration

The deployed commercial policy remains `7038281b-2429-4aa4-81db-4f04a87e7184`,
with `duration=null`, newly issued license `expiry=null`, and ten active installation
slots. Its metadata is `commercialModel=pornfetch-permanent-v1`, `priceEur=29.99`.
Account, product, signing keys and the public API endpoint are unchanged. The server
rejects new renewal checkouts before creating an invoice. Existing beta records
remain unchanged and need no migration.

Both the signed key and the included license in the signed machine checkout must
contain an explicit null expiry. Missing or non-null expiry claims are invalid.
The checkout's separate `meta.expiry` and `meta.ttl` still bound offline access to
at most seven days after successful validation, even in future app versions.
Keep transport, signature, account/product/policy/license/installation identity,
suspension and installation-limit checks.

Server verification with a fresh TEST license confirmed activation, repeated
validation with null expiry, and entitlement in a future build. Updated GUI,
Android and CLI binaries must still be built and distributed. See the adjacent
Server repository's Keygen operations runbook for permanent-shutdown steps.
