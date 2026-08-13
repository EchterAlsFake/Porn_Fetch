import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import QtQuick.Controls.impl
import QtQuick.Controls.Material

Pane {
    font.pointSize: appSettings.font_size
    id: window // 'id' allows us to reference this window from other parts of the code

    background: Rectangle {
        color: "transparent"
        border.width: 2
        radius: 10
    }

    ProxyWindow {
        id: proxyWindow

        onProxyTestRequested: function(proxyUrl, verifySsl) {
            backend.testProxy(proxyUrl, verifySsl)
        }
        onProxyAccepted: function(proxyUrl, verifySsl) {
            backend.applyProxy(proxyUrl, verifySsl)
        }
        onProxyDisabled: backend.applyProxy("", true)
    }

    Connections {
        target: backend

        function onProxyTestSucceeded(proxyUrl, stats) {
            proxyWindow.showTestSuccess(proxyUrl, stats)
        }

        function onProxyTestFailed(proxyUrl, message) {
            proxyWindow.showTestFailure(proxyUrl, message)
        }

        function onProxySslError(proxyUrl, message) {
            proxyWindow.showSslWarning(proxyUrl, message)
        }
    }
    // We set a slightly custom background color.
    // Since we enabled Material Dark theme in Python, most things will automatically be dark,
    // but setting a specific background ensures a clean, cohesive look.
    // ColumnLayout arranges its children vertically.
    // This is the main structure: Main Content Area on top, Action Buttons on the bottom.
    ColumnLayout {
        anchors.fill: parent // Make the layout fill the entire window
        anchors.margins: 20 // Add some breathing room (padding) around the edges
        spacing: 20 // Space between the top area and the bottom buttons

        // RowLayout arranges its children horizontally.
        // This splits the upper part into Left (Sidebar) and Right (Settings Content)
        RowLayout {
            Layout.fillHeight: true // Take up all available vertical space
            Layout.fillWidth: true // Take up all available horizontal space
            spacing: 20 // Space between sidebar and content

            // ---------------------------------------------------------
            // LEFT SIDEBAR: Navigation Menu
            // ---------------------------------------------------------
            // Frame provides a modern, elevated background panel for the sidebar
            Frame {
                Layout.fillHeight: true
                Layout.preferredWidth: 200 // Fixed width for the sidebar
                padding: 0 // Remove internal padding so items go edge-to-edge

                // ListView displays a scrollable list of items based on a model
                ListView {
                    id: navList

                    anchors.fill: parent // Fill the frame

                    // Keep the selection synced with the content currently displayed
                    currentIndex: stackLayout.currentIndex

                    // The 'model' is the data. Here it's just a simple list of strings.
                    model: ["Video", "Performance", "System", "Privacy", "UI"]

                    // 'delegate' defines how each individual item in the list looks
                    delegate: ItemDelegate {
                        font.pixelSize: 15
                        // Make font bold if this item is currently selected
                        font.weight: ListView.isCurrentItem ? Font.Bold : Font.Normal
                        height: 50
                        highlighted: ListView.isCurrentItem // Visual highlight

                        text: modelData // 'modelData' refers to the string ("Video", etc.)
                        width: parent.width // Span full width of sidebar

                        // When clicked, switch both the list highlight and the content view
                        onClicked: {
                            stackLayout.currentIndex = index;
                            navList.currentIndex = index;
                        }
                    }
                }
            }

            // ---------------------------------------------------------
            // RIGHT CONTENT AREA: The actual settings forms
            // ---------------------------------------------------------
            Frame {
                Layout.fillHeight: true
                Layout.fillWidth: true
                padding: 20

                // StackLayout allows having multiple children, but only ONE is visible at a time.
                // It acts exactly like QStackedWidget from Qt Widgets.
                StackLayout {
                    id: stackLayout

                    anchors.fill: parent
                    currentIndex: 0 // Start by showing the first item (Video)

                    // ==========================================
                    // TAB 1: VIDEO SETTINGS
                    // ==========================================
                    // ScrollView ensures that if the window is too small, the user can scroll.
                    ScrollView {
                        id: "scrollviewVideo"
                        clip: true // Prevents content from drawing outside the scroll view

                        // GridLayout arranges items in a grid.
                        // Here we use 2 columns: Label on the left, Control on the right.

                        ColumnLayout {
                            id: videoSettingsLayout
                            width: scrollviewVideo.availableWidth
                            Layout.fillWidth: true

                            GridLayout {
                                columns: 3
                                columnSpacing: 15
                                rowSpacing: 15
                                Layout.fillWidth: true

                                // --- Row 1: Quality ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.videoQualityHelp
                                }
                                Label {
                                    Layout.fillWidth: false
                                    text: "Quality"
                                }
                                ComboBox {
                                    id: defaultQualityCombo
                                    Layout.fillWidth: true
                                    model: ["best", "half", "worst", "2160p", "1440p", "1080p", "720p", "540p", "480p", "360p", "240p", "144p"]
                                    currentIndex: appSettings.quality

                                    function qualityRequiresLicense(index) {
                                        return index === 0 || index === 1
                                                || index === 3 || index === 4 || index === 5
                                    }

                                    onActivated: (index) => {
                                        if (qualityRequiresLicense(index)
                                                && !(bridge && bridge.isPremium)) {
                                            currentIndex = Qt.binding(function() {
                                                return appSettings.quality
                                            })
                                            return
                                        }
                                        backend.set_default_quality(index)
                                    }

                                    delegate: ItemDelegate {
                                        id: qualityDelegate
                                        width: defaultQualityCombo.width
                                        highlighted: defaultQualityCombo.highlightedIndex === index
                                        readonly property bool qualityLocked:
                                            defaultQualityCombo.qualityRequiresLicense(index)
                                            && !(bridge && bridge.isPremium)
                                        enabled: !qualityLocked

                                        contentItem: RowLayout {
                                            Label {
                                                Layout.fillWidth: true
                                                text: modelData
                                                color: qualityDelegate.enabled
                                                       ? qualityDelegate.palette.text
                                                       : qualityDelegate.palette.mid
                                                verticalAlignment: Text.AlignVCenter
                                            }

                                            Text {
                                                text: "🔒"
                                                visible: qualityDelegate.qualityLocked
                                                verticalAlignment: Text.AlignVCenter
                                            }
                                        }
                                    }
                                }

                                // --- Row 2: Model Videos ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.modelVideosHelp
                                }
                                Label {
                                    Layout.fillWidth: false
                                    text: "Model Videos"
                                }
                                ComboBox {
                                    Layout.fillWidth: true
                                    model: ["Both", "Uploaded Videos", "Featured Videos"]
                                    currentIndex: appSettings.model_videos
                                    onCurrentIndexChanged: appSettings.model_videos = currentIndex
                                }

                                // --- Row 3: Content Language ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.contentLanguageHelp
                                }
                                Label {
                                    Layout.fillWidth: false
                                    text: "Content Language"
                                }
                                ComboBox {
                                    id: contentLanguageComboBox
                                    Layout.fillWidth: true
                                    textRole: "label"
                                    valueRole: "locale"
                                    model: ListModel {
                                        ListElement { label: "🇨🇿 Čeština"; locale: "cs-CZ" }
                                        ListElement { label: "🇩🇪 Deutsch"; locale: "de-DE" }
                                        ListElement { label: "🇺🇸 English"; locale: "en-US" }
                                        ListElement { label: "🇪🇸 Español"; locale: "es-ES" }
                                        ListElement { label: "🇵🇭 Filipino"; locale: "fil-PH" }
                                        ListElement { label: "🇫🇷 Français"; locale: "fr-FR" }
                                        ListElement { label: "🇮🇹 Italiano"; locale: "it-IT" }
                                        ListElement { label: "🇳🇱 Nederlands"; locale: "nl-NL" }
                                        ListElement { label: "🇯🇵 日本語"; locale: "ja-JP" }
                                        ListElement { label: "🇵🇱 Polski"; locale: "pl-PL" }
                                        ListElement { label: "🇵🇹 Português"; locale: "pt-PT" }
                                        ListElement { label: "🇷🇺 Русский"; locale: "ru-RU" }
                                        ListElement { label: "🇺🇦 Українська"; locale: "uk-UA" }
                                        ListElement { label: "🇨🇳 中文"; locale: "zh-CN" }
                                    }
                                    Component.onCompleted: {
                                        var savedIndex = indexOfValue(appSettings.locale)
                                        currentIndex = savedIndex >= 0 ? savedIndex : indexOfValue("en-US")
                                    }
                                    onActivated: appSettings.locale = currentValue
                                }

                                // --- Row 4: Strict Enforcement ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.strictEnforcementHelp
                                }
                                CheckBox {
                                    Layout.columnSpan: 2
                                    Layout.fillWidth: true
                                    text: "Strict Enforcement for content language"
                                    checked: appSettings.strict_enforcement
                                    onToggled: appSettings.strict_enforcement = checked
                                }

                                // --- Row 5: Max Result Limit ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.resultLimitHelp
                                }
                                Label {
                                    Layout.fillWidth: false
                                    text: "Max Result Limit"
                                }
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 5000
                                    value: appSettings.result_limit
                                    onValueModified: appSettings.result_limit = value
                                }

                                // --- Row 6: Output Path ---
                                Item { Layout.fillWidth: false } // Empty spacer for 1st column alignment
                                Label {
                                    Layout.fillWidth: false
                                    text: "Output Path"
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 10

                                    TextField {
                                        id: outputPathInput
                                        placeholderText: "Enter the output path for the videos..."
                                        Layout.fillWidth: true
                                        text: appSettings.output_path
                                        onEditingFinished: appSettings.output_path = text
                                    }
                                    Button {
                                        Layout.fillWidth: false
                                        text: "Select Path"
                                    }
                                }

                                // --- Row 7: Write Metadata ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.writeMetadataHelp
                                }
                                CheckBox {
                                    Layout.columnSpan: 2
                                    Layout.fillWidth: true
                                    text: "Write metadata"
                                    checked: appSettings.write_metadata
                                    onToggled: appSettings.write_metadata = checked
                                }

                                // --- Row 8: Skip Existing Files ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.skipExistingFilesHelp
                                }
                                CheckBox {
                                    Layout.columnSpan: 2
                                    Layout.fillWidth: true
                                    text: "Skip existing files"
                                    checked: appSettings.skip_existing_files
                                    onToggled: appSettings.skip_existing_files = checked
                                }

                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.trackVideosHelp
                                }
                                CheckBox {
                                    Layout.columnSpan: 2
                                    Layout.fillWidth: true
                                    text: "Track Videos (SQLite Database)"
                                    checked: appSettings.track_videos
                                    onToggled: appSettings.track_videos = checked
                                }

                                Item { Layout.fillWidth: false } // Empty spacer for 1st column alignment
                                Label {
                                    Layout.fillWidth: false
                                    text: "Database Path"
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 10

                                    TextField {
                                        id: databasePathInput
                                        placeholderText: "Enter the path for the database (.db file)"
                                        Layout.fillWidth: true
                                        text: appSettings.output_path
                                        onEditingFinished: appSettings.database_path = text
                                    }
                                    Button {
                                        Layout.fillWidth: false
                                        text: "Select Path"
                                    }
                                }
                            }
                        }
                    }

                    // ==========================================
                    // TAB 2: LEISTUNG SETTINGS (Performance)
                    // ==========================================
                    ScrollView {
                        id: "scrollviewPerformance"
                        clip: true

                        GridLayout {
                            columnSpacing: 15
                            columns: 3 // We use 6 columns to create two pairs of (Label, Spinbox)
                            width: scrollviewPerformance.availableWidth
                            Layout.fillWidth: true
                            rowSpacing: 15

                            // Left Pair                        // Right Pair
                            HelpButton {Layout.fillWidth: false; helpText: AppStrings.downloadWorkersHelp}
                            Label {
                                Layout.fillWidth: false
                                text: "Download workers:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.download_workers
                                onValueModified: appSettings.download_workers = value
                            }
                            HelpButton {Layout.fillWidth: false; helpText: AppStrings.networkDelayHelp}
                            Label {
                                text: "Network delay (requests/sec):"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.network_delay
                                onValueModified: appSettings.network_delay = value
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.parallelDownloadsHelp
                            }
                            Label {
                                text: "Parallel Downloads:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.parallel_downloads
                                onValueModified: appSettings.parallel_downloads = value
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.retriesHelp
                            }
                            Label {
                                text: "Maximum retries:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.retries
                                onValueModified: appSettings.retries = value
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.timeoutHelp
                            }
                            Label {
                                text: "Maximum timeout:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.timeout
                                onValueModified: appSettings.timeout = value
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.processingDelay
                            }
                            Label {
                                text: "Processing Delay (videos/sec):"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.processing_delay
                                onValueModified: appSettings.processing_delay = value
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.speedLimitHelp
                            }
                            Label {
                                text: "Speed Limit (MB/s):"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.speed_limit
                                onValueModified: appSettings.speed_limit = value
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.videosConcurrencyHelp
                            }
                            Label {
                                text: "Videos Concurrency:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.videos_concurrency
                                onValueModified: appSettings.videos_concurrency = value
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.pagesConcurrencyHelp
                            }
                            Label {
                                text: "Pages concurrency:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.pages_concurrency
                                onValueModified: appSettings.pages_concurrency = value
                            }

                            GridLayout {
                                columnSpacing: 15
                                Layout.columnSpan: 3
                                columns: 2 // We use 6 columns to create two pairs of (Label, Spinbox)
                                width: scrollviewPerformance.availableWidth
                                Layout.fillWidth: true
                                rowSpacing: 15

                                Label {
                                    text: "Response Cache Size (MB/s)"
                                }
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 2000
                                    value: appSettings.response_cache_size
                                    onValueModified: appSettings.response_cache_size = value
                                }

                                Label {
                                    text: "Response Cache TTL (Seconds)"
                                }
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 20000
                                    value: appSettings.response_cache_ttl
                                    onValueModified: appSettings.response_cache_ttl = value
                                }

                                Label {
                                    text: "Segment Cache Size (MB/s)"
                                }
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 2000
                                    value: appSettings.segment_cache_size
                                    onValueModified: appSettings.segment_cache_size = value
                                }

                                Label {
                                    text: "Segment Cache TTL (Seconds)"
                                }
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 20000
                                    value: appSettings.segment_cache_ttl
                                    onValueModified: appSettings.segment_cache_ttl = value
                                }

                                Label {
                                    text: "Request Initial Retry Delay"
                                }
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 20000
                                    value: appSettings.request_initial_retry_delay
                                    onValueModified: appSettings.request_initial_retry_delay = value
                                }

                                Label {
                                    text: "Request Retry Max Delay"
                                }
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 20000
                                    value: appSettings.request_retry_max_delay
                                    onValueModified: appSettings.request_retry_max_delay= value
                                }

                                Label {
                                    text: "Request Retry Multiplier"
                                }
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 20000
                                    value: appSettings.request_retry_multiplier
                                    onValueModified: appSettings.request_retry_multiplier = value
                                }

                                Label {
                                    text: "Request Retry Jitter"
                                }
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 20000
                                    value: appSettings.request_retry_jitter
                                    onValueModified: appSettings.request_retry_jitter = value
                                }
                            }
                            // Empty spaces for layout balance where the right side has no items
                            Item {
                                Layout.fillWidth: false
                            }
                            Item {
                                Layout.columnSpan: 3
                                Layout.fillHeight: true
                            }
                        }
                    }

                    // ==========================================
                    // TAB 3: SYSTEM SETTINGS
                    // ==========================================
                    ScrollView {
                        clip: true
                        id: "scrollviewSettings"

                        GridLayout {
                            columnSpacing: 15
                            columns: 2 // We use 6 columns to create two pairs of (Label, Spinbox)
                            width: scrollviewPerformance.availableWidth
                            Layout.fillWidth: true
                            rowSpacing: 15

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.updateChecks
                            }
                            CheckBox {
                                text: "Search for Updates"
                                Layout.fillWidth: true
                                checked: appSettings.update_checks
                                onToggled: appSettings.update_checks = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.supressErrors
                            }
                            CheckBox {
                                text: "Ignore Errors"
                                Layout.fillWidth: true
                                checked: appSettings.supress_errors
                                onToggled: appSettings.supress_errors = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.enableLoggingHelp
                            }
                            CheckBox {
                                // Use \n for multi-line text
                                text: "Allow error reports (100% anonymous)"
                                Layout.fillWidth: true
                                checked: appSettings.enable_logging
                                onToggled: appSettings.enable_logging  = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.trustEnvironmentHelp
                            }
                            CheckBox {
                                // Use \n for multi-line text
                                text: "Trust Environment (Advanced)"
                                Layout.fillWidth: true
                                checked: appSettings.trust_environment
                                onToggled: appSettings.trust_environment  = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.debugModeHelp
                            }
                            CheckBox {
                                text: "Enable Debug Mode (Not recommended)"
                                Layout.fillWidth: true
                                checked: appSettings.debug_mode
                                onToggled: appSettings.debug_mode = checked
                            }

                            ComboBox {
                                    Layout.fillWidth: true
                                    model: ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                                    currentIndex: appSettings.log_level
                                    onCurrentIndexChanged: appSettings.log_level = currentIndex
                                }
                                
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.httpVersionHelp
                            }
                            TextField {
                                id: "httpVersion"
                                placeholderText: "HTTP Version may be: v1; v2; v3"
                                Layout.fillWidth: true
                                text: appSettings.http_version
                                onEditingFinished: appSettings.http_version = text
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.impersonationHelp
                            }
                            TextField {
                                id: "impersonation"
                                placeholderText: "e.g., 'chrome', 'safari', 'edge'"
                                Layout.fillWidth: true
                                text: appSettings.impersonation
                                onEditingFinished: appSettings.impersonation = text
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.customJA3Help
                            }
                            TextField {
                                id: "customJA3"
                                placeholderText: "Custom JA3 String"
                                Layout.fillWidth: true
                                text: appSettings.custom_ja3
                                onEditingFinished: appSettings.custom_ja3 = text
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.interfaceHelp
                            }
                            TextField {
                                id: "interface"
                                placeholderText: "e.g., eth0, wlan0, tun0, 10.6.3.20"
                                Layout.fillWidth: true
                                text: appSettings.interface
                                onEditingFinished: appSettings.interace = text
                            }
                        }
                    }

                    // ===============
                    // TAB 4: Privacy Settings
                    // ===============

                    ScrollView {
                        clip: true
                        id: "scrollviewPrivacy"

                        GridLayout {
                            columnSpacing: 15
                            columns: 2 // We use 6 columns to create two pairs of (Label, Spinbox)
                            width: scrollviewPerformance.availableWidth
                            Layout.fillWidth: true
                            rowSpacing: 15

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.anonymousModeHelp
                            }
                            CheckBox {
                                text: "Anonymous Mode"
                                Layout.fillWidth: true
                                checked: appSettings.anonymous_mode
                                onToggled: appSettings.anonymous_mode = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.encryptedCHHelp
                            }
                            CheckBox {
                                text: "Encrypted Client Hello"
                                Layout.fillWidth: true
                                checked: appSettings.encrypted_ch
                                onToggled: appSettings.encrypted_ch = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.dnsOverHTTPSHelp
                            }
                            CheckBox {
                                text: "DNS over HTTPS"
                                Layout.fillWidth: true
                                checked: appSettings.dns_over_https
                                onToggled: appSettings.dns_over_https = checked
                            }

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.torIntegrationHelp
                            }
                            CheckBox {
                                text: "Enable Tor Integration"
                                Layout.fillWidth: true
                                checked: appSettings.sni_obfuscation
                                onToggled: appSettings.sni_obfuscation = checked
                            }

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.onionRoutingHelp
                            }
                            CheckBox {
                                text: "Route License / Update checking through .onion domain"
                                Layout.fillWidth: true
                                checked: appSettings.sni_obfuscation
                                onToggled: appSettings.sni_obfuscation = checked
                            }

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.dnsPrimaryHelp
                            }
                            TextField {
                                id: "dnsPrimaryInput"
                                placeholderText: "Enter Primary DNS (Must support DNS over HTTPS)"
                                Layout.fillWidth: true
                                text: appSettings.dns_server
                                onEditingFinished: appSettings.dns_server = text
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.fallbackDNSHelp
                            }
                            TextField {
                                id: "dnsFallbackInput"
                                placeholderText: "Enter Fallback DNS (Must support DNS over HTTPS)"
                                Layout.fillWidth: true
                                text: appSettings.fallback_dns
                                onEditingFinished: appSettings.fallback_dns = text
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.sniObfuscationHelp
                            }
                            CheckBox {
                                    text: "SNI Obfuscation"
                                    Layout.fillWidth: true
                                    checked: appSettings.sni_obfuscation
                                    onToggled: appSettings.sni_obfuscation = checked
                                }

                            GridLayout {
                                Layout.columnSpan: 2          // <--- Fixes the layout breakage
                                Layout.fillWidth: true
                                columns: 2
                                columnSpacing: 15
                                rowSpacing: 15

                                RadioButton {
                                    text: "Lite SNI Obfuscation"
                                    Layout.fillWidth: false
                                    checked: appSettings.sni_obfuscation_lite
                                    onToggled: appSettings.sni_obfuscation_life = checked
                                }
                                RadioButton {
                                    text: "Strict SNI Obfuscation (Requires Admin / root rights)"
                                    Layout.fillWidth: false
                                    checked: appSettings.sni_obfuscation_strict
                                    onToggled: appSettings.sni_obfuscation_strict = checked
                                }
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.proxySetupHelp
                            }
                            Button {
                                Layout.fillWidth: true
                                text: appSettings.proxy.length > 0
                                      ? qsTr("Configure or test proxy…")
                                      : qsTr("Set up proxy…")
                                onClicked: proxyWindow.openWithProxy(appSettings.proxy)
                            }


                        }
                    }
                    // ==========================================
                    // TAB 4: UI SETTINGS
                    // ==========================================
                    ScrollView {
                        id: "scrollviewUI"
                        clip: true

                        GridLayout {
                            width: scrollviewUI.availableWidth
                            columnSpacing: 15
                            columns: 3
                            rowSpacing: 15
                            Layout.fillWidth: true

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.guiLanguageHelp
                            }
                            Label {
                                text: "Graphical User Interface language:"
                            }
                            ComboBox {
                                Layout.fillWidth: true
                                model: ["System", "English", "German", "Chinese", "French"]
                                currentIndex: appSettings.language
                                onCurrentIndexChanged: appSettings.language = currentIndex
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.fontSizeHelp
                            }
                            Label {
                                text: "Font Size:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                from: 5
                                to: 72
                                value: appSettings.font_size
                                onValueModified: appSettings.font_size = value
                            }
                            HelpButton { Layout.fillWidth: false; helpText: AppStrings.appStyleHelp }
                            Label { text: "Application Style (Requires Restart):" }
                            ComboBox {
                                Layout.fillWidth: true
                                model: ["Material", "Fusion", "Universal", "Windows"]
                                // Automatically select the saved style
                                Component.onCompleted: currentIndex = find(appSettings.core_style)
                                onActivated: appSettings.core_style = currentText
                            }

                            // 2. Dark/Light Mode
                            HelpButton { Layout.fillWidth: false; helpText: AppStrings.darkModeHelp }
                            Label { text: "Dark Mode:" }
                            Switch {
                                Layout.fillWidth: true
                                checked: appSettings.dark_mode
                                onToggled: appSettings.dark_mode = checked
                            }

                            // 3. Accent Color
                            HelpButton { Layout.fillWidth: false; helpText: AppStrings.accentColorHelp }
                            Label { text: "Accent Color:" }
                            ComboBox {
                                Layout.fillWidth: true
                                textRole: "text"
                                valueRole: "value"
                                model: ListModel {
                                    ListElement { text: "Indigo"; value: "#6366f1" }
                                    ListElement { text: "Red"; value: "#f44336" }
                                    ListElement { text: "Green"; value: "#4caf50" }
                                    ListElement { text: "Orange"; value: "#ff9800" }
                                    ListElement { text: "Purple"; value: "#9c27b0" }
                                }
                                Component.onCompleted: currentIndex = indexOfValue(appSettings.accent_color)
                                onActivated: appSettings.accent_color = currentValue
                            }

                        }
                    }
                }
            }
        }

        // ---------------------------------------------------------
        // HORIZONTAL SEPARATOR LINE
        // ---------------------------------------------------------
        // A simple Rectangle acts as a line to visually separate content from bottom buttons
        Rectangle {
            Layout.fillWidth: true
            height: 1
        }

        // ---------------------------------------------------------
        // BOTTOM GLOBAL ACTION BUTTONS
        // ---------------------------------------------------------
        // A ColumnLayout containing 3 RowLayouts to perfectly align the buttons in a grid structure
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 10 // Space between rows of buttons

            // Row 1
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Button {
                    Layout.fillWidth: true
                    // Material styling overrides for specific buttons to make them stand out
                    Material.background: "#6366f1" // Premium Indigo color
                    Material.foreground: "white"   // White text
                    font.bold: true // Make text bold
                    text: "Buy License (19.99€)"

                    onClicked: {
                        Qt.openUrlExternally("https://echteralsfake.me/buy_license")
                    }

                }
                Button {
                    Layout.fillWidth: true
                    text: "Import License File"
                    // No custom colors here, defaults to normal Material dark button
                    onClicked: {
                        var component = Qt.createComponent("LicenseWindow.qml")
                        if (component.status == Component.Ready) {
                            var win = component.createObject(this)
                            win.show()
                        } else {
                            console.error("Error loading LicenseWindow:", component.errorString())
                        }

                    }

                }
            }

            // Row 2
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Button {
                    Layout.fillWidth: true
                    Material.background: "#ef4444" // Danger Red color
                    Material.foreground: "white"
                    text: "Reset Porn Fetch to default settings"
                    onClicked: {backend.reset_pornfetch()}
                }
                Button {
                    Layout.fillWidth: true
                    text: "Clear Temporary Files"
                    onClicked: {backend.clear_temporary_files()}
                }

            }

            // Row 3
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Loader {
                    id: dialogLoader
                }

                Button {
                    Layout.fillWidth: true
                    Material.background: "#10b981" // Success Green color
                    Material.foreground: "white"
                    text: "Install Porn Fetch"
                    onClicked: {
                        dialogLoader.source = "InstallDialog.qml"
                        dialogLoader.item.acceptedInput.connect(function(inputValue) {backend.install_pornfetch(inputValue)})
                        dialogLoader.item.open()
                    }
                }

                Button {
                    Layout.fillWidth: true
                    Material.background: "#ef4444" // Danger Red color
                    Material.foreground: "white"
                    text: "Uninstall Porn Fetch"
                    onClicked: {backend.uninstall_pornfetch()}
                }

            }
        }
    }
}
