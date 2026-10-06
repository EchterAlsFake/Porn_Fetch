# Development status

> [!CAUTION]
> The latest published binary release, version 3.8, is massively outdated.
> Porn Fetch 3.9 is an active rewrite, and the current source and documentation
> may not describe the behavior, interface, platform support, or licensing flow
> of the downloadable 3.8 application.

Documentation on the default branch follows the development source. For an
accurate description of a release, use that release's Git tag and bundled
documentation. Bugs reproduced only on 3.8 should be identified as release
bugs; bugs reproduced from the default branch should include the commit ID.

Current development targets Python 3.14, a QML/PySide6 desktop application, and
a Qt-free Questionary CLI suitable for headless platforms.

The 3.9 client now targets the commercial licensing policy, with first activation,
signed offline permits, perpetual build entitlement, and update eligibility checks.
The backend handoff dated 6 October 2026 still reports sandboxed NOWPayments and
disabled Patreon. Commercial launch requires packaged platform testing, publication
of signed update repositories, and the server/payment release work described in
[LICENSING_ARCHITECTURE.md](LICENSING_ARCHITECTURE.md). Older beta credentials are
intentionally rejected by this client.
