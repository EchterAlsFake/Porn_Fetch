This file is reserved for AI agents and shall not be used by other developers!


# Project 
- Name: Porn Fetch
- Status: Source Available (Development v3.9)
- Repository: https://github.com/EchterAlFake/Porn_Fetch
- Maintainer: EchterAlsFake (Johannes Habel)
- Description: A legally compliant privacy respecting application to download adult media


# Tech Stack
- Language: Python 3.14
- Framework: Qt 6.11+ 
- Frontend: QML 
- Networking: curl-cffi (async)

# Target Platforms
- Windows (x64, ARM64)
- Linux (x64, ARM64)
- macOS (x64, Universal2)
- Android: (aarch64, x86_64, armv7a, i686)
- Possible iOS support not yet started

# Important Notice
- Entire Project is asynchronous
- Entire project is legally developed under German Law
- PySide6 has custom patches applied


# Project Structure

# The Root
- .python-version -> defines Python 3.14 for UV Project management
- BACKEND.md -> Explains the eaf_base_api library
- CONTEXT.md -> This file
- CONTRIBUTING.md -> Contribute guide and reference
- main.py -> Entry Point
- Porn_Fetch_CLI.py -> The CLI of Porn Fetch (not relevant during development unless explicitly told)
- pyproject.toml -> Defines dependencies for UV
- SECURITY.md -> Document to follow European Security laws for software
- uv.lock -> Locks dependencies with UV

# Frontend
Path: src/frontend/UI/

- Main.qml -> Entry Point for the app
- AccountPage.qml -> Related to account specific actions
- AppStrings.qml -> Translation strings for e.g., settings page
- DownloadsPage.qml -> The main download page where users can download videos
- HelpButton.qml -> Custom QML button to show help messages
- InfoPage.qml -> Shwos credits and about for the application
- InstallDialog.qml -> Dialog where a user can initiate the installation and enter a custom app name
- LicenseManager.qml > Used for managing and importing the license to unlock premium features
- LicenseWidget.qml -> Widget for LicenseManager.qml
- LicenseWindow.qml -> Window
- MessageBox.qml -> a simple Message Box to show the user an information
- ProxyWindow.qml -> custom window to apply proxies to all clients
- qmldir -> Defines the singleton instances e.g., AppStrings.qml
- QualityComboBox.qml -> Custom Combobox with licensing logic applied
- SettingsPage.qml -> Settings page to configure Porn Fetch settings. Options: System. Privacy, UI, Video, Performance
- SplashScreen.qml -> Splash Screen for startup
- StatisticsPage.qml -> Uses an internal database to show download statistics
- SupportedWebsitesPage.qml -> A page dedicated to show which websites are supported
- Theme.qml -> Handles theming across the application e.g., Material UI vs. Native, Dark and Light mode

Path:
src/frontend/

- resources.qrc -> Holds all translations, Markdown files and graphics
- update.ps1 -> Script for Windows to automatically update the frontend
- update.sh -> Does the same but for Linux and macOS

Path: src/frontend/graphics
- Description: Holds .png and .svg files that are used during runtime

Path: src/frontend/translations
- Description: Holds the translation files for different languages

Path: src/frontend/screenshots
- Description: Shows screenshots of the app for GitHub

# The Backend (important)
Path: src/backend/
- Description: Holds a lot of files that do the underlying work

- check_license.py -> Validates the imported license against a cryptographic asymetric public key
- clients.py -> Holds helper functions and the clients which Porn Fetch uses to fetch data and interact with the websites
- config.py -> Holds the global settings instance using QSettings, connected to the SettingsPage.qml using Signals
- database.py -> Logic for setting up the database for the statistics part
- download_manager.py -> Connects the backend which adds the videos into the download manager class which is connected to the QML frontend. 
- errors.py -> Custom App errors to be raised inside the app
- handle_ssl.py -> Legacy file for implementing SSL support per system using truststore (not needed anymore)
- helper_functions.py -> Some legacy functions
- installation.py -> class responsible for installing Porn Fetch on Windows and Linux
- license_bridge.py -> Connects the frontend QML Licensing logic to the backend
- login_manager.py -> Handles login to the different supported sites
- macos_setup.py -> Custom logic for macOS startup that tells users to move the app into /Applications
- proxy_tester.py -> Tests the proxy the user entered during the proxy setup and shows statistics about the proxy
- shared_functions -> contains functions used by the CLI and the GUI
- shared_gui -> useless file that needs to be abandoned
- sni_fragment_proxy_lite.py -> Please see: SNI_PROXY_AGENT_HANDOFF.md
- sni_fragment_proxy_strict.py -> Please see: SNI_PROXY_AGENT_HANDOFF.md
- sni_proxy_manager.py -> Connects both SNI proxies and manages them e.g., startup and shutdown
- splashscreen.py -> Starts the actual splashscreen
- tests.py -> Runs a fully automatic test suite that uses real network requests
- theme_manager.py -> manages Porn Fetch's theme e.g., dark vs. light
- tls_client_hello.py -> See SNI_PROXY_AGENT_HANDOFF.md
- uninstallation.py -> Handles the uninstallation of Porn Fetch
- update_service.py -> Handles automatic update checking using the Sparkle Framework on macOS and my own website for all other system. Fetches update information and changelogs and can also automatically update Porn Fetch

The sparkle folder contains the entire Sparkle Framework as well as a custom bridge in Objective-C which
makes the sparkle framework usable in Python.

### The Networking Backend
All network traffic is fundamentally routed through the eaf_base_api library / the BaseCore class.
It creates a curl-cffi async session and allows the user to heavily configure it through the SettingsPage.qml. 

The clients.py file reloads all these clients and applies the full configuration each time. A RuntimeConfig class is used for this.
The BaseCore class has different methods e.g., an iterator which allows to asynchronously fetch websites using a special consumer
producer pattern. This can also be configured. 

For a full reference read BACKEND.md

# Building
Path: src/build/

Building is done through the official pyside6-deploy tool.
The scripts are based on their platform. 

The nuitka package config file additionally imports AV and Sparkle.

Android building is done through pyside6-android-deploy with custom patches to the tool to build successfuly
and custom recipes for the C components.


# Scripts and Custom Patches 
Path: src/scripts/

- install.sh -> Installs Porn Fetch from source on Linux
- install_termux.sh -> Installs the CLI on Termux
- install_windows.ps1 -> Installs Porn Fetch on Windows
- patch_macos_bundle.py -> Injects sparkle to Info.plist
- patch_qtasyncio.py -> Patches the QtAsyncio library to add support for specific curl_cffi functions

# Testing
/testing
- Description: Contains automated scripts for testing. Not relevant for development.


# Commercial Aspect
The Project is freemium and a License is needed to unlock all features. 
The entire application is still source available though.


# Python Code Quick Reference

This index covers every project `.py` file currently present (including generated Qt files and isolated test tooling, but excluding virtual-environment dependencies and bytecode caches). It lists every module-level class and function; class entries summarize their methods and properties so this remains a quick architectural map rather than a duplicate API manual.

## Application entry points

### `Porn_Fetch_CLI.py`

- **`CLI`** — Implements the interactive command-line application, including setup, persisted user settings, licensing, site/model/playlist discovery, searches, downloads, progress, and error handling.
- **`Batch`** — Extends `CLI` with a non-interactive test mode and the CLI program entry point.

### `main.py`

- **`_NullApplication`** — No-op `QGuiApplication` substitute used by multiprocessing helper children so they do not initialize the GUI.
- **`_NullSplash`** — No-op splash-screen substitute used outside the main GUI process.
- **`DownloadStopEvent`** — `asyncio.Event` subclass whose identity survives API configuration copies and can cancel an active download cooperatively.
- **`custom_unraisable_hook()`** — Reports otherwise-unraisable exceptions while filtering known harmless Qt/Python shutdown noise.
- **`ProcessVideos`** — Consumes an async video iterator, loads metadata, applies filters, creates output paths, and registers prepared `VideoObject` instances with `DownloadManager`.
- **`Backend`** — Main QObject façade exposed to QML; owns client refreshes, preparation and download tasks, proxy testing, updates, installation, selection/model state, licensing enforcement, and orderly shutdown.
- **`main()`** — Composes the GUI backend, database and license bridges, exposes them to QML, loads `Main.qml`, and starts the Qt/asyncio event loop.
- **`get_imported_licenses()`** — Collects package names, versions, and license metadata for currently imported third-party distributions.
- **`print_runtime_version_info()`** — Prints the collected runtime dependency/version information as a formatted table.

## Backend modules

### `src/backend/check_license.py`

- **`_canonical_json_bytes()`** — Serializes license payloads deterministically so Ed25519 signatures can be verified reliably.
- **`LicenseCheckResult`** — Immutable result object containing license validity, a user-facing reason, and optional decoded license data.
- **`LicenseManager`** — Loads, validates, installs, and queries offline Ed25519-signed license files against the embedded public key and expected product.

### `src/backend/clients.py`

- **`generate_locale_headers_and_cookies()`** — Converts a configured locale into normalized `Accept-Language` headers and site locale cookies, falling back safely to English.
- **`refresh_clients()`** — Applies current settings to the shared `RuntimeConfig`, replaces all site clients/cores, and retires old sessions for asynchronous cleanup.
- **`close_retired_sessions()`** — Closes sessions displaced by a client refresh and clears the retirement list.
- **`schedule_retired_session_cleanup()`** — Schedules retired-session cleanup on the active asyncio loop when one is available.
- **`close_all_clients()`** — Closes every active and retired `BaseCore`/site client during application shutdown.
- **`get_video()`** — Validates a URL or unwraps an existing scrape/video object, detects its provider, and returns the matching site API video instance.
- **`load_video_attributes()`** — Loads provider-specific metadata and qualities and normalizes them into the application’s `VideoObject` model.
- **`get_direct_url_legacy()`** — Resolves a direct media URL for legacy non-HLS providers and a requested quality.
- **`get_available_qualities()`** — Retrieves, normalizes, deduplicates, and sorts the qualities supported by a provider video.
- **`_safe_getattr()`** — Reads an attribute defensively, returning a fallback when access fails.
- **`resolve_path()`** — Resolves dotted formatting paths such as `author.name` against a metadata context.
- **`parse_publish_date()`** — Normalizes provider date values and relative date strings into UTC datetimes.
- **`write_tags()`** — Writes normalized video metadata into downloaded files through PyAV.
- **`parse_length()`** — Converts provider-specific duration representations into a rounded minute count.

### `src/backend/config.py`

- **`SettingsManager`** — Central QSettings-backed QObject exposed to QML. It validates and signals video, performance, cache, networking, privacy, proxy/SNI, update, database, locale, and UI settings; it also provides path conversion, reset/sync, atomic proxy application, and atomic SNI mode migration helpers.

### `src/backend/database.py`

- **`DatabaseBridge`** — QObject persistence/dashboard bridge that asynchronously saves added or updated `VideoObject` state and exposes iterator, failure, and aggregate statistics queries to QML.
- **`ListField`** — Peewee text field that transparently converts Python lists to and from JSON.
- **`BaseModel`** — Common Peewee model base bound to the module-level database proxy.
- **`OriginIterator`** — Stores a unique source iterator URL and its display name for grouping tracked videos.
- **`VideoRecord`** — Stores the latest tracked metadata, status, output details, and source association for a unique video URL.
- **`initialize_database()`** — Opens/configures SQLite and creates tracking tables when video tracking is enabled; otherwise returns `None`.
- **`get_available_iterators()`** — Returns all stored iterator names and URLs as dictionaries.
- **`get_failed_videos_for_iterator()`** — Queries failed records belonging to one iterator directly in SQLite.

### `src/backend/download_manager.py`

- **`quality_requires_premium()`** — Determines whether a named or numeric quality exceeds the free-access limit.
- **`select_allowed_quality()`** — Selects the preferred available stream or the best permitted fallback based on license state.
- **`VideoFilters`** — Dataclass containing optional duration, regex, quality, and publication-date filters for discovery.
- **`VideoObject`** — Mutable application video model containing normalized metadata plus download lifecycle, source, output, HLS, and resume state.
- **`DownloadListModel`** — QAbstractListModel backing the QML download table; manages rows, selections, qualities, statuses, progress, and premium enforcement.
- **`DownloadManager`** — Owns live `VideoObject` instances by identifier and emits add/update/remove lifecycle signals consumed by UI and persistence components.

### `src/backend/errors.py`

- **`InvalidInput`** — Signals invalid or unsupported user/provider input.
- **`CookiesNotFound`** — Signals that required browser cookies could not be located.
- **`LoginError`** — Signals a provider login failure.
- **`UnsupportedPlatform`** — Signals that an operation is unavailable on the current OS or architecture.
- **`SomethingStupidHappened`** — Generic internal invariant/error condition used when provider data reaches an unexpected state.
- **`MetadataWriteError`** — Signals failure while writing metadata into a downloaded file.
- **`UpdateCheckFailed`** — Signals an explicit update-check failure.
- **`SNILeak`** — Signals that an SNI/privacy constraint was violated or could not be enforced.
- **`AppNetworkError`** — Application-level normalized network failure.
- **`AppNotFoundError`** — Application-level normalized missing-resource failure.
- **`AppBotBlocked`** — Application-level normalized bot-protection denial.
- **`AppDownloadFailed`** — Application-level normalized download failure.
- **`safe_api_call()`** — Awaits a provider call and translates provider/library exceptions into the application’s normalized error types.

### `src/backend/handle_ssl.py`

- **`build_ssl_context()`** — Builds a hardened TLS client context using system trust where possible and safe certificate defaults otherwise.

### `src/backend/helper_functions.py`

- **`make_debug_log()`** — Formats/logs an exception with operation and video context and returns a user-facing error message.
- **`get_original_executable_path()`** — Resolves the real executable path while ignoring temporary one-file extraction paths.
- **`copy_overwrite_atomic()`** — Copies to a temporary sibling and atomically replaces the target file.
- **`write_text_atomic()`** — Writes text through Qt’s `QSaveFile` to avoid partial files after crashes.
- **`chmod_755()`** — Applies executable user and read/execute group/other permissions to a path.
- **`default_license_path()`** — Returns the platform-appropriate default installed-license path.
- **`safe_rmtree()`** — Removes an existing directory tree while tolerating an already-missing target.
- **`get_widget_value()`** — Extracts a value from supported legacy Qt widget types.
- **`set_widget_value()`** — Applies a value to supported legacy Qt widget types.

### `src/backend/installation.py`

- **`InstallPornFetch`** — Installs a user-local copy of Porn Fetch, dispatching to Linux desktop-file or Windows shortcut/start-menu setup as appropriate.

### `src/backend/license_bridge.py`

- **`LicenseBridge`** — QObject adapter exposing `LicenseManager` validity, reason, key, feature list, premium status, and file installation to QML.

### `src/backend/license_manager.py`

- **`_canonical_json_bytes()`** — Produces deterministic JSON bytes for license signature validation.
- **`LicenseCheckResult`** — Immutable license validation result carrying status, explanation, and optional payload.
- **`LicenseManager`** — Verifies, installs, loads, and checks features in offline Ed25519-signed license documents.

### `src/backend/login_manager.py`

- **`get_site_cookies()`** — Searches supported desktop browsers for cookies matching a provider’s domain keywords.
- **`LoginPornhub`** — Authenticates the PornHub client using discovered browser cookies.
- **`LoginXhamster`** — Authenticates the XHamster client using discovered browser cookies.
- **`LoginXVideos`** — Authenticates the XVideos client using discovered browser cookies.

### `src/backend/macos_setup.py`

- **`_is_running_from_dmg()`** — Detects whether the current application bundle is running from a mounted disk image.
- **`_find_app_bundle()`** — Walks parent paths to locate the enclosing `.app` bundle.
- **`_install_and_relaunch_mac()`** — Copies the application into the user Applications directory and relaunches it.
- **`macos_setup()`** — Performs the macOS first-run bundle-location check and prompts/moves the app when required.

### `src/backend/proxy_tester.py`

- **`ProxyTestResult`** — Dataclass containing normalized proxy URL, status, latency, response code, and endpoint details, with QML-map conversion.
- **`validate_proxy_url()`** — Validates and normalizes supported HTTP/SOCKS proxy URLs with UI-safe error messages.
- **`test_proxy()`** — Performs a timed HTTPS request through a proposed proxy and returns connection statistics.

### `src/backend/shared_functions.py`

- **`aenumerate()`** — Async-generator equivalent of Python’s `enumerate()`.
- **`send_to_server()`** — Sends diagnostic/error information to the project server when reporting is enabled.
- **`build_quality_options()`** — Builds display-label/download-value pairs for available qualities and named fallbacks.
- **`handle_error_gracefully()`** — Converts an exception into logging, optional reporting, and a user-visible message according to settings.
- **`get_os_and_arch()`** — Maps the current platform and machine architecture to the project’s release asset identifier.

### `src/backend/shared_gui.py`

- **`_get_qml_engine()`** — Lazily creates the private QML engine used for standalone message boxes.
- **`_PopupDispatcher`** — QObject that marshals popup requests onto the Qt GUI thread.
- **`_get_dispatcher()`** — Lazily creates and places the popup dispatcher on the application thread.
- **`_fallback_popup()`** — Displays a legacy `QMessageBox` when the QML message component cannot be used.
- **`_show_qml_popup_impl()`** — Loads, positions, runs, and disposes the custom QML message window.
- **`ui_popup()`** — Thread-safe public helper for displaying a short QML notification or console fallback.
- **`reset_pornfetch()`** — Legacy reset completion notification helper.
- **`show_error()`** — Displays an error-styled popup.
- **`Signals`** — Legacy QObject signal collection for download progress, errors, login, installation, updates, and tree-model operations.
- **`on_checkbox_clicked()`** — Shows the debug-mode warning when its legacy checkbox becomes enabled.
- **`debug_mode_warning()`** — Explains the performance and privacy implications of verbose debug logging.
- **`available_title_formatting_options()`** — Displays the supported custom output-title template fields and examples.

### `src/backend/sni_fragment_proxy_lite.py`

- **`ProxyStartError`** — Raised when the Lite helper process cannot become ready.
- **`ProxyProtocolError`** — Raised for malformed or unsupported local/upstream proxy protocol data.
- **`UpstreamConnectError`** — Raised when a direct destination or configured upstream proxy rejects a tunnel.
- **`FragmentingProxyConfig`** — Validated, process-safe configuration for the Lite loopback proxy, fragmentation, binding, and upstream chaining.
- **`_UpstreamProxySpec`** — Parsed immutable description of an HTTP or SOCKS upstream proxy.
- **`_AsyncWriter`** — Structural protocol for async stream writers used by relay helpers.
- **`FragmentingProxyProcess`** — Starts, monitors, restarts, and stops the spawned Lite proxy process and exposes its SOCKS/HTTP URLs.
- **`FragmentingProxyServer`** — Async loopback SOCKS5/HTTP-CONNECT server that opens destinations and relays client traffic through SNI-aware fragmentation.
- **`_StreamFragmenter`** — Protocol shared by incremental stream-fragmentation strategies.
- **`_FirstDataFragmenter`** — Fallback strategy that splits the first outbound data at a configured byte offset.
- **`_Http1RequestFragmenter`** — Incrementally frames persistent HTTP/1.x requests so each request header can be fragmented safely.
- **`_relay_fragmented()`** — Reads one stream direction and forwards it through an incremental fragmenter.
- **`_relay_raw()`** — Copies one stream direction without fragmentation.
- **`_read_some()`** — Reads an available chunk and translates low-level stream errors consistently.
- **`_read_exactly()`** — Reads an exact byte count for proxy handshakes with protocol-aware failures.
- **`_read_header_block()`** — Reads through an HTTP header terminator subject to a maximum size.
- **`_write_bytes()`** — Writes and drains a complete byte block.
- **`_write_fragmented()`** — Writes fragments separately with the configured inter-fragment delay.
- **`_write_eof()`** — Half-closes a writer when its transport supports EOF.
- **`_close_writer()`** — Closes a stream writer and waits for shutdown defensively.
- **`_configure_tcp_writer()`** — Applies socket-level TCP behavior used to reduce fragment coalescing.
- **`_parse_http1_request_header()`** — Validates an HTTP/1 request header and extracts framing information.
- **`_is_http_token()`** — Checks whether bytes satisfy HTTP token grammar.
- **`_parse_upstream_proxy()`** — Validates an upstream proxy URL and converts it into `_UpstreamProxySpec`.
- **`_parse_authority()`** — Splits a host/port authority, including bracketed IPv6 forms.
- **`_format_authority()`** — Formats a host and port for HTTP CONNECT authority syntax.
- **`_format_url_host()`** — Brackets IPv6 hosts when embedding them in proxy URLs.
- **`_is_loopback_host()`** — Determines whether a host name or address resolves to loopback.
- **`_read_socks_address()`** — Decodes a SOCKS5 address from a client stream.
- **`_discard_socks_address()`** — Consumes an unused SOCKS5 address from a reply.
- **`_encode_socks_address()`** — Encodes a host as a SOCKS5 address field.
- **`_resolve_one_address()`** — Resolves one bindable destination address asynchronously.
- **`_socks_error_code()`** — Maps connection exceptions to SOCKS5 reply codes.
- **`_send_http_error()`** — Sends a minimal HTTP proxy error response.
- **`_configure_logging()`** — Initializes child-process logging for the proxy.
- **`_proxy_process_entry()`** — Spawn-safe child entry point that constructs the async proxy runtime and reports readiness.
- **`_run_foreground()`** — Runs the Lite server in the current process until stopped.
- **`_parse_ports()`** — Parses and validates comma-separated HTTP port values.
- **`_build_arg_parser()`** — Builds the standalone Lite proxy command-line parser.
- **`main()`** — Runs the Lite proxy as a standalone command-line program.

### `src/backend/sni_fragment_proxy_strict.py`

- **`StrictProxyStartError`** — Raised when the Strict helper process cannot start successfully.
- **`StrictBackendUnavailable`** — Raised when the current platform, privileges, or native packet backend cannot support Strict mode.
- **`StrictFlowRegistrationError`** — Raised when interception for an exact outbound TCP flow cannot be armed.
- **`ProxyProtocolError`** — Raised for invalid local or upstream tunnel protocol data.
- **`UpstreamConnectError`** — Raised when a Strict proxy destination/upstream connection fails.
- **`StrictDesyncConfig`** — Configuration for the optional out-of-window fake ClientHello decoy.
- **`StrictFragmentingProxyConfig`** — Validated configuration for Strict stream fragmentation, exact-flow packet interception, reverse order, and desync behavior.
- **`_UpstreamProxySpec`** — Parsed HTTP/SOCKS upstream proxy description.
- **`_AsyncWriter`** — Structural protocol for async relay writers.
- **`StrictFragmentingProxyProcess`** — Owns the spawned Strict proxy lifecycle and publishes its local SOCKS/HTTP endpoints.
- **`_FlowTuple`** — Immutable source/destination address and port tuple identifying one intercepted TCP flow.
- **`_StrictFlowPolicy`** — Chooses and remembers packet split boundaries per flow, including retransmission-safe behavior.
- **`_find_http1_request_starts()`** — Locates plaintext HTTP/1 request boundaries inside captured TCP payloads.
- **`_StrictFlowGuard`** — Async context/lifetime guard that unregisters an armed strict flow on close.
- **`_StrictPacketBackend`** — Loads PyDivert, validates platform support, allocates unique priorities, and captures/reinjects packets for exact active flows.
- **`_prepare_linux_diverter_close()`** — Clears incompatible libbpf attach-only fields before PyDivert detaches Linux TC hooks.
- **`_flow_tuple_from_writer()`** — Derives the exact outbound flow tuple from an established asyncio writer.
- **`_strip_ipv6_scope()`** — Removes an IPv6 zone identifier before address comparison/filter construction.
- **`_is_windows_arm64()`** — Detects unsupported native Windows ARM64 execution.
- **`_generate_decoy_client_hello()`** — Builds a small parseable TLS ClientHello containing the configured fake SNI.
- **`_inject_desync_decoy()`** — Clones a captured packet and injects the fake ClientHello outside the receiver’s expected TCP window.
- **`_build_exact_flow_filter()`** — Constructs the PyDivert expression for one outbound TCP four-tuple.
- **`_packet_matches_flow()`** — Verifies that a captured packet belongs to the registered exact flow.
- **`_process_strict_packet()`** — Applies split/reverse/desync policy, recalculates checksums, and emits bounded genuine packet fragments.
- **`StrictFragmentingProxyServer`** — Async local tunnel server that registers each Internet-facing connection with the strict packet backend before relaying data.
- **`_relay_raw()`** — Relays one stream direction unchanged.
- **`_relay_fragmented()`** — Relays client data through the TLS ClientHello stream fragmenter.
- **`_read_some()`** — Reads a stream chunk with normalized protocol errors.
- **`_read_exactly()`** — Reads exact handshake fields with normalized failures.
- **`_read_header_block()`** — Reads a bounded HTTP CONNECT header block.
- **`_write_bytes()`** — Writes and drains one complete byte block.
- **`_write_eof()`** — Attempts a clean half-close on an async stream.
- **`_close_writer()`** — Closes and awaits an async writer defensively.
- **`_configure_tcp_writer()`** — Applies TCP socket options used by strict stream handling.
- **`_parse_upstream_proxy()`** — Parses and validates configured upstream HTTP/SOCKS proxies.
- **`_parse_authority()`** — Parses host/port authorities with IPv6 support.
- **`_format_authority()`** — Formats a CONNECT authority safely.
- **`_format_url_host()`** — Formats IPv4/host names and bracketed IPv6 for URLs.
- **`_is_loopback_host()`** — Rejects upstream configurations that would loop back into the local proxy.
- **`_read_socks_address()`** — Reads and decodes a SOCKS5 address.
- **`_discard_socks_address()`** — Consumes an unused address in a SOCKS5 response.
- **`_encode_socks_address()`** — Encodes a destination into SOCKS5 wire format.
- **`_resolve_one_address()`** — Asynchronously resolves one usable destination endpoint.
- **`_socks_error_code()`** — Converts connection failures to SOCKS reply codes.
- **`_send_http_error()`** — Sends a small HTTP proxy failure response.
- **`_configure_logging()`** — Configures Strict helper-process logging.
- **`_strict_proxy_process_entry()`** — Spawn-safe Strict child entry point that preloads the packet backend before reporting ready.
- **`_run_foreground()`** — Runs the Strict proxy in the current process until shutdown.
- **`_parse_ports()`** — Parses the configured plaintext HTTP port list.
- **`_build_arg_parser()`** — Builds the standalone Strict proxy CLI parser.
- **`main()`** — Runs Strict mode as a standalone command-line tool.

### `src/backend/sni_proxy_manager.py`

- **`resolve_source_address()`** — Resolves an IP literal or Linux interface name to the address used by Internet-facing proxy sockets.
- **`SNIProxyManager`** — Selects, starts, restarts, and stops one Lite or Strict helper, maps Strict profiles, chains the user proxy, and publishes a fail-closed runtime URL.
- **`_is_ip_literal()`** — Tests whether a configured interface value is already an IPv4/IPv6 literal.

### `src/backend/splashscreen.py`

- **`SplashController`** — Loads and controls the startup QML splash screen, including centering, status messages, and teardown.

### `src/backend/tests.py`

- **`normalize_quality()`** — Converts accepted numeric or `###p` quality forms to integers and rejects named/malformed values.
- **`validate_qualities()`** — Validates that a provider returned a non-empty list of supported normalized resolutions.
- **`WebsiteTest`** — Immutable descriptor for one live provider smoke-test URL and its metadata requirements.
- **`test_url()`** — Processes one live URL and verifies QML model insertion, identifiers, metadata, and selected/available qualities.
- **`run_smoke_tests()`** — Runs the live website matrix, reports pass/fail details, and returns a process exit code.

### `src/backend/theme_manager.py`

- **`ThemeManager`** — QObject exposed to QML that synchronizes light/dark color scheme and accent settings, applies Fusion palettes, and reports available Qt Quick styles.

### `src/backend/tls_client_hello.py`

- **`ClientHelloState`** — Parser result enum distinguishing incomplete, found, and non-ClientHello data.
- **`ClientHelloSNI`** — Stores the located hostname and its byte offsets and calculates a safe split point inside it.
- **`locate_client_hello_sni()`** — Bounded parser that locates the first TLS ClientHello `host_name` entry across TLS record boundaries.
- **`_locate_server_name()`** — Parses ClientHello extensions and returns the server-name position relative to the handshake.
- **`AsyncWriter`** — Minimal writer protocol required by the TLS stream fragmenter.
- **`TLSClientHelloStreamFragmenter`** — Buffers the start of a connection, splits inside SNI when found, and safely falls back for non-TLS/incomplete input.
- **`_write()`** — Writes one fragment and applies the configured inter-fragment delay.

### `src/backend/uninstallation.py`

- **`UninstallPornFetch`** — Removes the user-local Linux or Windows installation and uses a delayed cleanup batch file when Windows cannot delete the running executable.

### `src/backend/update_service.py`

- **`get_update_url()`** — Returns the production update endpoint or the development environment override.
- **`SparkleUpdater`** — QObject wrapper around the bundled macOS Sparkle bridge for update availability and user-triggered checks.
- **`CheckUpdates`** — Fetches release metadata, compares numeric version components, and reports whether a newer release exists without blocking startup on failure.
- **`AutoUpdater`** — Downloads the correct platform asset, emits progress/status, and replaces the executable directly or through a Windows helper script.

## Frontend Python and generated Qt modules

### `src/frontend/UI/macOS.py`

- **`Notification`** — Legacy Qt widget implementing a styled macOS notification window.
- **`check_macos()`** — Shows the legacy macOS-specific notification/check when applicable.

### `src/frontend/UI/resources.py`

- **`qInitResources()`** — Generated Qt resource registration function for embedded graphics, credits, and translations.
- **`qCleanupResources()`** — Generated Qt resource unregistration function.

### `src/frontend/UI/ui_form_main_window.py`

- **`Ui_PornFetch_UI`** — Generated legacy Qt Designer form class whose `setupUi()` builds widgets and whose `retranslateUi()` applies translated labels.

### `src/frontend/translations/strings.py`

- **`TRANSLATE_MAIN`** — Namespace for main-window translation constants.
- **`TRANSLATE_PAGE_DOWNLOAD`** — Namespace for download-page translation constants.
- **`TRANSLATE_PAGE_LOGIN`** — Namespace for login-page translation constants.
- **`TRANSLATE_PAGE_SETTINGS`** — Namespace for settings-page translation constants.
- **`TRANSLATE_ERRORS`** — Namespace for translated error strings.

## Build and maintenance scripts

### `src/scripts/patch.py`

This module has no classes or functions. Its top-level CI action changes `IS_SOURCE_RUN = True` to `False` in `config.py` for packaged builds.

### `src/scripts/patch_macos_bundle.py`

- **`main()`** — Locates a built macOS application bundle and injects the required Sparkle framework metadata into its `Info.plist`.

### `src/scripts/patch_qtasyncio.py`

- **`PatchError`** — Raised when installed QtAsyncio sources or versions are incompatible with the patch plan.
- **`EnvironmentInfo`** — Dataclass describing the target interpreter, PySide version, and QtAsyncio source locations.
- **`SourceChange`** — Represents one source file’s original and patched text and reports whether it changed.
- **`LineEdit`** — Represents a replacement of a half-open source-line range.
- **`sha256_text()`** — Computes a SHA-256 digest for text content.
- **`sha256_file()`** — Computes a SHA-256 digest for a file.
- **`parse_version()`** — Converts a version string into comparable numeric components.
- **`target_python()`** — Resolves the Python interpreter whose PySide installation should be patched.
- **`inspect_environment()`** — Discovers and validates the target PySide6/QtAsyncio installation and source files.
- **`find_class()`** — Locates a named top-level class in a parsed Python AST.
- **`class_method()`** — Locates a named method within an AST class definition.
- **`is_not_implemented_placeholder()`** — Detects methods whose body is only a `NotImplementedError` placeholder.
- **`apply_line_edits()`** — Applies validated non-overlapping line edits to source text.
- **`render_import_from()`** — Renders a modified `from ... import ...` AST node back to source.
- **`find_qtcore_import()`** — Finds the QtCore import statement that must receive additional names.
- **`find_close_insertion_line()`** — Finds the safe insertion point for patched event-loop close logic.
- **`patch_events_source()`** — Produces the required QtAsyncio event-loop source changes.
- **`patch_tasks_source()`** — Produces the required QtAsyncio task/future source changes.
- **`build_changes()`** — Builds the complete set of pending source changes for the target environment.
- **`default_backup_root()`** — Returns the default directory for timestamped patch backups.
- **`backup_changes()`** — Saves original files and a manifest before applying modifications.
- **`atomic_write_text()`** — Writes patched source through an atomic temporary-file replacement.
- **`apply_changes()`** — Applies all changed sources, optionally using a requested backup location.
- **`latest_backup()`** — Finds the newest compatible backup set.
- **`restore_backup()`** — Restores source files from a patch backup manifest.
- **`verify_sources()`** — Verifies that installed sources contain the expected patched behavior.
- **`verify_imports()`** — Imports the patched modules in the target interpreter as a runtime sanity check.
- **`print_environment()`** — Prints the inspected interpreter/PySide/source information.
- **`validate_version()`** — Enforces the supported PySide version range unless explicitly overridden.
- **`main()`** — Implements the patcher CLI for inspect, apply, verify, and restore operations.

## Testing and lab tooling

### `testing/fake_update_server.py`

- **`FakeUpdateHandler`** — Small HTTP handler that serves deterministic update metadata and downloadable test assets while suppressing default request logs.
- **`main()`** — Parses server options and runs the local fake update HTTP server.

### `testing/geneva_isolated/geneva_runner.py`

- **`parse_args()`** — Parses Geneva strategy, port, output, and target-command arguments inside the isolated namespace.
- **`terminate_process_group()`** — Gracefully terminates a spawned process group and escalates when it does not exit.
- **`main()`** — Starts Geneva and the requested app/test command together, then coordinates exit and cleanup.

### `testing/sni_proxy_smoke.py`

- **`request_through_proxy()`** — Starts a selected Lite/Strict local proxy, performs an HTTP request through it, and reports the response before cleanup.
- **`main()`** — Parses smoke-test flags and runs the async request workflow.

### `testing/test_client_refresh.py`

- **`ClientRefreshTests`** — Async regression test ensuring an active SNI proxy URL replaces live client sessions and forces the intended routing configuration.

### `testing/test_sni_fragmentation.py`

- **`build_client_hello()`** — Creates a minimal TLS ClientHello fixture containing a chosen SNI hostname.
- **`RecordingWriter`** — Async writer double that records emitted fragments for assertions.
- **`ClientHelloLocatorTests`** — Tests SNI location in single/multiple TLS records and incomplete handshakes.
- **`StreamFragmenterTests`** — Tests buffering, hostname splitting, and non-TLS fallback behavior.
- **`StrictLinuxCompatibilityTests`** — Tests privilege errors, unique flow priorities, and the Linux libbpf detach workaround.
- **`StrictDesyncTests`** — Tests decoy validity, cloning, reverse fragment order, failure fallback, and desync-mode validation.

### `testing/test_sni_proxy_manager.py`

- **`_Signal`** — Minimal connect/emit signal double for manager tests.
- **`_Settings`** — In-memory settings double containing the SNI/proxy fields consumed by the manager.
- **`_Process`** — Fake Lite/Strict helper process that records lifecycle calls and returns a loopback URL.
- **`SNIProxyManagerTests`** — Tests Lite startup/restart, invalid-mode fail-closed behavior, and Strict Desync profile mapping.

### `testing/test_sni_settings.py`

- **`_MemorySettings`** — Dictionary-backed QSettings double supporting value, write, sync, and clear operations.
- **`SNISettingsTests`** — Tests legacy mode migration, atomic mode persistence, and the default-to-Lite repair path.
