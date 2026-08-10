import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import QtQuick.Controls.impl
import QtQuick.Controls.Material

Pane {
    font.pointSize: appSettings.font_size
    id: window // 'id' allows us to reference this window from other parts of the code

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
                            width: scrollviewVideo.availableWidth
                            Layout.fillWidth: true


                            GridLayout {
                                columnSpacing: 15
                                rowSpacing: 15
                                width: scrollviewVideo.availableWidth
                                Layout.fillWidth: true
                                columns: 3


                                HelpButton {Layout.fillWidth: false}
                                Label {Layout.fillWidth: false; text: "Quality"}
                                ComboBox {
                                    Layout.fillWidth: true
                                    model: ["best", "half", "worst", "2160p", "1440p", "1080p", "720p", "540p", "480p", "360p", "240p", "144p"]
                                    currentIndex: appSettings.quality
                                    onCurrentIndexChanged: appSettings.quality = currentIndex
                                }

                                HelpButton {Layout.fillWidth: false}
                                Label {Layout.fillWidth: false; text: "Model Videos"}
                                ComboBox {
                                    Layout.fillWidth: true
                                    model: ["Both", "Uploaded Videos", "Featured Videos"]
                                    currentIndex: appSettings.model_videos
                                    onCurrentIndexChanged: appSettings.model_videos = currentIndex
                                }

                                HelpButton {Layout.fillWidth: false}
                                Label {Layout.fillWidth: false; text: "Max Result Limit"}
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 5000
                                    value: appSettings.result_limit
                                    onValueModified: appSettings.result_limit = value

                                }
                            }

                            GridLayout {
                                rowSpacing: 15
                                columnSpacing: 15
                                width: scrollviewVideo.availableWidth
                                Layout.fillWidth: true

                                Label {Layout.fillWidth: false; text: "Output Path"}
                                TextField {
                                    id: "outputPathInput"
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

                            GridLayout {
                                columnSpacing: 15
                                rowSpacing: 15
                                width: scrollviewVideo.availableWidth
                                Layout.fillWidth: false
                                columns: 2

                                HelpButton {Layout.fillWidth: false}
                                CheckBox {
                                    Layout.fillWidth: true
                                    text: "Write metadata"
                                    checked: appSettings.write_metadata
                                    onToggled: appSettings.write_metadata = checked

                                }

                                HelpButton {Layout.fillWidth: false}
                                CheckBox {
                                    Layout.fillWidth: true
                                    text: "Skip existing files"
                                    checked: appSettings.skip_existing_files
                                    onToggled: appSettings.skip_existing_files = checked
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
                            HelpButton {
                                Layout.fillWidth: false
                            }
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
                            HelpButton {
                                Layout.fillWidth: false
                            }
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
                            }
                            CheckBox {
                                text: "Search for Updates (On startup)"
                                Layout.fillWidth: true
                                checked: appSettings.update_checks
                                onToggled: appSettings.update_checks = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                text: "Anonymous mode"
                                Layout.fillWidth: true
                                checked: appSettings.anonymous_mode
                                onToggled: appSettings.anonymous_mode = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                text: "Ignore Errors"
                                Layout.fillWidth: true
                                checked: appSettings.supress_errors
                                onToggled: appSettings.supress_errors = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
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
                            }
                            CheckBox {
                                text: "Enable Proxy"
                                Layout.fillWidth: true
                                checked: appSettings.proxy.length > 0
                                onClicked: {
                                    if (checked)
                                        proxyWindow.openWithProxy(appSettings.proxy)
                                    else
                                        backend.applyProxy("", true)
                                }
                            }
                            HelpButton {
                                Layout.fillWidth: false
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
                            }
                            TextField {
                                id: "httpVersion"
                                placeholderText: "HTTP Version may be: v1; v2; v3"
                                Layout.fillWidth: true
                                text: appSettings.http_version
                                onEditingFinished: appSettings.http_version = text
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
                            }
                            CheckBox {
                                text: "Anonymous Mode"
                                Layout.fillWidth: true
                                checked: appSettings.anonymous_mode
                                onToggled: appSettings.anonymous_mode = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                text: "Encrypted Client Hello"
                                Layout.fillWidth: true
                                checked: appSettings.encrypted_ch
                                onToggled: appSettings.encrypted_ch = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                text: "DNS over HTTPS"
                                Layout.fillWidth: true
                                checked: appSettings.dns_over_https
                                onToggled: appSettings.dns_over_https = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
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
                            }
                            CheckBox {
                                text: "SNI Obfuscation"
                                Layout.fillWidth: true
                                checked: appSettings.sni_obfuscation
                                onToggled: appSettings.sni_obfuscation = checked
                            }
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
                            HelpButton {
                                Layout.fillWidth: false
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
                            }
                            Label {
                                text: "Font Size:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                to: 72
                                value: appSettings.font_size
                                onValueModified: appSettings.font_size = value
                            }
                            Label { text: "Application Style (Requires Restart):" }
                            ComboBox {
                                Layout.fillWidth: true
                                model: ["Material", "Fusion", "Universal", "Windows"]
                                // Automatically select the saved style
                                Component.onCompleted: currentIndex = find(appSettings.core_style)
                                onActivated: appSettings.core_style = currentText
                            }
                            HelpButton { Layout.fillWidth: false }

                            // 2. Dark/Light Mode
                            Label { text: "Dark Mode:" }
                            Switch {
                                Layout.fillWidth: true
                                checked: appSettings.dark_mode
                                onToggled: appSettings.dark_mode = checked
                            }
                            HelpButton { Layout.fillWidth: false }

                            // 3. Accent Color
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
                            HelpButton { Layout.fillWidth: false }

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
            color: "#333333" // Dark grey border
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
                    Material.background: appSettings ? appSettings.theme_primary_color : "#3b82f6" // Dynamic accent color
                    Material.foreground: "white"
                    text: "Apply (requires restart)"
                    onClicked: {appSettings.sync()}
                }
                Button {
                    Layout.fillWidth: true
                    Material.background: "#ef4444" // Danger Red color
                    Material.foreground: "white"
                    text: "Reset Porn Fetch to default settings"
                }
            }

            // Row 3
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Button {
                    Layout.fillWidth: true
                    Material.background: "#10b981" // Success Green color
                    Material.foreground: "white"
                    text: "Install Porn Fetch"
                }
                Button {
                    Layout.fillWidth: true
                    Material.background: "#ef4444" // Danger Red color
                    Material.foreground: "white"
                    text: "Uninstall Porn Fetch"
                }
                Button {
                    Layout.fillWidth: true
                    text: "Clear Temporary Files"
                }
            }
        }
    }
}
