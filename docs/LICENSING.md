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
   required for Qt, PocketBase, Sparkle, FFmpeg, and Python dependencies.
3. Confirm the delivered source and builds display the same application license
   and make the license and third-party notices easy to find in the GUI and CLI.
4. Obtain German/EU legal review of the custom license, the separate tutorial
   rule, the Terms acceptance flow, and any consumer-facing paid offer. The
   current test checkout checks an explicit acceptance flag but does not yet
   retain the accepted Terms version or a durable acceptance record; add that
   evidence before a live paid checkout.

The related Server repository remains a separate project. Its Terms and Privacy
Policy must describe the code and actual deployment at the time a service is
offered. The payment and licensing flows in this development environment are
test-only; this document does not represent that money is processed.

For the first 3.9 beta, users go to https://echteralsfake.me/ and press the
crypto sandbox purchase button to obtain a license file. The application then
uses its normal import and validation flow. This is not a real transaction:
no money is processed and users do not need to send cryptocurrency.
