# GUI accessibility verification

The application uses Qt Quick Controls and exposes accessible names and descriptions
where a control's purpose is not conveyed by its text. Both settings layouts offer
font sizing, reduced motion and high contrast. Decorative activity indicators are
excluded from the accessibility tree. Screen-reader access must use the same
privacy-redacted text as the visible interface.

The engineering target is applicable WCAG 2.2 AA behavior, not a certification.
A passing QML load or metadata assertion does not establish assistive-technology
usability. No real screen reader or Android device was available for this change.

## Repeatable checks

Run `uv run python scripts/audit_gui.py` for a per-component static inventory.
Annotations are counted, not graded: standard Qt controls inherit useful metadata;
custom graphics may need explicit roles and actions. Review every page even if its
annotation count is nonzero. Do not add redundant names to every text label.

Run `uv run python -m unittest src.tests.integration.test_ui_translation` and the
existing settings tests for preference persistence, catalog switching and selected
accessible-interface checks. Run desktop and Android `main.py --smoke-test`
(with `--android` for Android layout) for offline QML loading.

## Manual release gate

For every platform below, record app commit, Qt version, OS, assistive technology
version, result and any blocking issue. Until executed, each entry is UNVERIFIED.

| Platform | Assistive technology | Result |
| --- | --- | --- |
| Windows | NVDA | UNVERIFIED |
| macOS | VoiceOver | UNVERIFIED |
| Linux | Orca / AT-SPI | UNVERIFIED |
| Android device | TalkBack, touch exploration, external keyboard | UNVERIFIED |

On each supported platform:

- Navigate Downloads, Account, Settings, Statistics/history where available, Info,
  licensing, proxy and connection dialogs, installation and error flows. Complete
  a download using test fixtures or the existing explicit opt-in live checks.
- Use Tab/Shift+Tab, arrows, Space, Enter and Escape. Verify visible focus, logical
  order, no keyboard traps, focus on dialog entry and restoration on dismissal.
  Delete a focused row and ensure the next useful action receives focus.
- Inspect the real accessibility tree: names, roles, values, selected/checked states,
  disabled actions, label associations and duplicate/decorative announcements.
- Confirm errors and completion states are discoverable without relying on color.
  Progress must be available on demand without repeated speech on every update.
- Enable anonymous mode before and during a download: titles/authors must not leak
  through tooltips, accessible names/descriptions or announcements. Password fields
  must remain protected until explicitly revealed.
- Test English, German, CJK, long translated labels and RTL layout. For local RTL
  testing temporarily add Arabic to the registry and a test catalog; do not publish
  synthetic translations. Verify URLs and paths retain readable direction.
- At 200% text size and OS scaling, inspect every dialog and page for clipped text,
  overlapping controls and unreachable actions. Scrollbars must remain usable.
- Measure actual rendered contrast in normal and high-contrast modes: text at least
  4.5:1 (3:1 for qualifying large text), meaningful control boundaries/focus at least
  3:1. Inspect custom gradients, translucent cards and disabled controls separately.
- Enable reduced motion and verify activity glow, transitions and smooth scrolling
  stop animating. Android interactive targets must measure at least 48 dp; verify
  actual rendered geometry, not just the nominal control height.

Use Qt's accessibility tooling and native inspection tools with real assistive
technology: https://doc.qt.io/qt-6/accessible-qtquick.html . Track failures as release
blockers for the affected workflow; do not turn missing platform results into passes.

## Automated result for this implementation

The focused translation/settings suite passes 21 tests, including the Help button's
real accessible press action and 48 px minimum dimensions. All 32 compilable QML
files compile; desktop and Android layout offline smoke checks pass. Ruff and the
translation workflow's actionlint checks pass. Qt emits teardown binding messages
when smoke-test context objects are destroyed; this does not constitute a native
screen-reader test. Preview packaging and the Weblate deployment have not been
executed on their target hosts.

Static inventory (counts do not indicate conformance):

| Page/component | Controls | Accessible annotations | Raw text candidates |
| --- | ---: | ---: | ---: |
| AccountLoginHelp.qml | 0 | 0 | 0 |
| AccountPage.qml | 10 | 5 | 0 |
| ActivityEdge.qml | 0 | 1 | 0 |
| AndroidAccountPage.qml | 12 | 3 | 0 |
| AndroidDownloadsPage.qml | 31 | 10 | 0 |
| AndroidInfoPage.qml | 3 | 0 | 0 |
| AndroidMain.qml | 5 | 3 | 0 |
| AndroidMorePage.qml | 2 | 0 | 0 |
| AndroidSettingsPage.qml | 19 | 4 | 0 |
| AppStrings.qml | 0 | 0 | 0 |
| ApplicationShutdown.qml | 0 | 0 | 0 |
| BetaDisclaimerDialog.qml | 2 | 0 | 0 |
| DownloadsPage.qml | 33 | 11 | 0 |
| HelpButton.qml | 1 | 2 | 0 |
| InfoPage.qml | 3 | 0 | 0 |
| InstallDialog.qml | 1 | 1 | 0 |
| LicenseWidget.qml | 6 | 5 | 0 |
| LicenseWindow.qml | 0 | 0 | 0 |
| Main.qml | 7 | 0 | 0 |
| MessageBox.qml | 2 | 4 | 0 |
| ProcessingIndicator.qml | 0 | 3 | 0 |
| ProxyWindow.qml | 11 | 13 | 0 |
| QualityComboBox.qml | 2 | 0 | 3 |
| ScrollableMessageDialog.qml | 0 | 0 | 0 |
| ServiceTorFailureDialog.qml | 2 | 0 | 0 |
| SettingsPage.qml | 63 | 110 | 0 |
| SmoothScrollView.qml | 0 | 0 | 0 |
| SmoothWheelHandler.qml | 0 | 0 | 0 |
| SplashScreen.qml | 0 | 0 | 0 |
| StatisticsPage.qml | 1 | 0 | 0 |
| Theme.qml | 0 | 0 | 0 |
| TorRouting.qml | 1 | 2 | 0 |
