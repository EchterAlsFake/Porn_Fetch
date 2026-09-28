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

The planned first 3.9 beta uses the actual license import and validation flow
with a crypto checkout sandbox. The website's sandbox purchase button is a test:
no real transaction takes place and no money is processed. Installation and
update artifacts are still being prepared and may have errors. The maintainer
is actively working on the rewrite; see the [3.9 installation guide](INSTALLATION.md)
and [Qt Installer Framework handoff](QT_INSTALLER_FRAMEWORK.md).
