import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs as Dialogs
import QtQuick.Layouts
import QtQuick.Window
import QtQuick.Controls.impl
import QtQuick.Controls.Material

Pane {
    font.pointSize: androidLayoutMode ? Math.max(12, appSettings.font_size) : appSettings.font_size
    id: window // 'id' allows us to reference this window from other parts of the code
    readonly property bool materialStyle: appSettings.core_style === "Material"
    readonly property bool compact: width < 700
    readonly property bool androidLayoutMode: Qt.platform.os === "android"
                                              || (typeof androidLayout !== "undefined" && androidLayout)

    component DecimalSpinBox: SpinBox {
        property int decimals: 2
        property real realFrom: 0
        property real realTo: 100
        property real realStepSize: 0.1
        property real realValue: 0
        readonly property real factor: Math.pow(10, decimals)

        signal realValueModified(real newValue)

        editable: true
        from: Math.round(realFrom * factor)
        to: Math.round(realTo * factor)
        stepSize: Math.max(1, Math.round(realStepSize * factor))
        value: Math.round(realValue * factor)

        textFromValue: function(value, locale) {
            return Number(value / factor).toLocaleString(locale, "f", decimals)
        }

        valueFromText: function(text, locale) {
            return Math.round(Number.fromLocaleString(locale, text) * factor)
        }

        onValueModified: realValueModified(value / factor)
    }

    Dialogs.FolderDialog {
        id: outputFolderDialog
        objectName: "outputFolderDialog"

        title: qsTr("Choose video output folder")
        currentFolder: appSettings.path_to_file_url(appSettings.output_path)

        onAccepted: {
            var chosen = (selectedFolder && selectedFolder.toString() !== "") ? selectedFolder : currentFolder
            var selectedPath = appSettings.local_path_from_url(chosen)
            if (selectedPath !== "")
                appSettings.output_path = selectedPath
        }
    }

    Dialogs.FolderDialog {
        id: pocketbaseFolderDialog
        objectName: "pocketbaseFolderDialog"

        title: qsTr("Choose a PocketBase data folder")
        acceptLabel: qsTr("Use Folder")
        currentFolder: appSettings.parent_directory_url(appSettings.pocketbase_data_path)

        onAccepted: {
            var chosen = (selectedFolder && selectedFolder.toString() !== "") ? selectedFolder : currentFolder
            var selectedPath = appSettings.local_path_from_url(chosen)
            if (selectedPath !== "")
                appSettings.pocketbase_data_path = selectedPath
        }
    }

    background: Rectangle {
        color: "transparent"
        border.width: 2
        radius: 10
    }

    ProxyWindow {
        id: proxyWindow
        objectName: "proxyWindow"

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
        anchors.margins: window.compact ? 8 : 20
        spacing: window.compact ? 8 : 20

        RowLayout {
            visible: window.compact
            Layout.fillWidth: true
            ComboBox {
                Layout.fillWidth: true
                model: [qsTr("Video"), qsTr("Performance"), qsTr("System"), qsTr("Privacy"), qsTr("UI")]
                currentIndex: stackLayout.currentIndex
                onActivated: stackLayout.currentIndex = currentIndex
            }
            Button {
                text: qsTr("Actions")
                onClicked: mobileActions.open()
                Menu {
                    id: mobileActions
                    MenuItem { text: qsTr("Purchase / renew license"); onTriggered: Qt.openUrlExternally("https://pornfetch.to/") }
                    MenuItem { text: qsTr("Import License File"); onTriggered: mobileLicenseDialog.open() }
                    MenuItem { text: qsTr("Reset settings"); onTriggered: backend.reset_pornfetch() }
                    MenuItem { text: qsTr("Clear temporary files"); onTriggered: backend.clear_temporary_files() }
                }
            }
        }

        Dialog {
            id: mobileLicenseDialog
            parent: Overlay.overlay
            anchors.centerIn: parent
            width: Math.min(window.width - 24, 520)
            height: Math.min(window.height - 24, 650)
            modal: true
            title: qsTr("Import License File")
            contentItem: ScrollView {
                contentWidth: availableWidth
                clip: true
                LicenseWidget { width: parent.width; height: implicitHeight }
            }
        }

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
                visible: !window.compact
                Layout.fillHeight: true
                Layout.preferredWidth: visible ? 200 : 0
                padding: 0 // Remove internal padding so items go edge-to-edge

                // ListView displays a scrollable list of items based on a model
                ListView {
                    id: navList
                    Accessible.role: Accessible.List
                    Accessible.name: qsTr("Settings sections")

                    anchors.fill: parent // Fill the frame

                    // Keep the selection synced with the content currently displayed
                    currentIndex: stackLayout.currentIndex

                    // The 'model' is the data. Here it's just a simple list of strings.
                    model: ["Video", "Performance", "System", "Privacy", "UI"]

                    SmoothWheelHandler {
                        id: navigationWheelHandler
                        flickable: navList
                    }

                    ScrollBar.vertical: ScrollBar {
                        policy: ScrollBar.AsNeeded
                        active: size < 1.0 || hovered || pressed
                                || navigationWheelHandler.scrolling
                    }

                    // 'delegate' defines how each individual item in the list looks
                    delegate: ItemDelegate {
                        Accessible.role: Accessible.ListItem
                        Accessible.name: qsTr(modelData + " settings")
                        font.pixelSize: 15 * appSettings.font_size / 12
                        // Make font bold if this item is currently selected
                        font.weight: ListView.isCurrentItem ? Font.Bold : Font.Normal
                        height: 50
                        highlighted: ListView.isCurrentItem // Visual highlight

                        icon.source: "qrc:/images/graphics/settings/"
                                     + ["video", "gauge", "settings", "shield", "palette"][index] + ".svg"
                        icon.width: 22
                        icon.height: 22
                        display: AbstractButton.TextBesideIcon
                        text: modelData // 'modelData' refers to the string ("Video", etc.)
                        width: navList.width // Span full width of sidebar

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
                padding: window.compact ? 8 : 20

                // StackLayout allows having multiple children, but only ONE is visible at a time.
                // It acts exactly like QStackedWidget from Qt Widgets.
                StackLayout {
                    objectName: "settingsStack"
                    id: stackLayout

                    anchors.fill: parent
                    currentIndex: 0 // Start by showing the first item (Video)

                    // ==========================================
                    // TAB 1: VIDEO SETTINGS
                    // ==========================================
                    // ScrollView ensures that if the window is too small, the user can scroll.
                    SmoothScrollView {
                        id: "scrollviewVideo"
                        clip: true // Prevents content from drawing outside the scroll view

                        // GridLayout arranges items in a grid.
                        // Here we use 2 columns: Label on the left, Control on the right.

                        ColumnLayout {
                            id: videoSettingsLayout
                            width: scrollviewVideo.availableWidth
                            Layout.fillWidth: true

                            GridLayout {
                                columns: window.compact ? 1 : 3
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
                                    text: qsTr("Quality")
                                }
                                ComboBox {
                                    id: defaultQualityCombo
                                    objectName: "defaultQualityCombo"
                                    Accessible.name: qsTr("Quality")
                                    Accessible.description: AppStrings.videoQualityHelp
                                    Layout.fillWidth: true
                                    model: ["best", "half", "worst", "2160p", "1440p", "1080p", "720p", "540p", "480p", "360p", "250p", "240p", "144p"]
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
                                                color: window.materialStyle
                                                       ? (qualityDelegate.enabled
                                                          ? qualityDelegate.Material.foreground
                                                          : qualityDelegate.Material.hintTextColor)
                                                       : (qualityDelegate.enabled
                                                          ? qualityDelegate.palette.text
                                                          : qualityDelegate.palette.mid)
                                                verticalAlignment: Text.AlignVCenter
                                            }

                                            Image {
                                                source: "qrc:/images/graphics/lock.png"
                                                visible: qualityDelegate.qualityLocked
                                                Layout.preferredWidth: 16
                                                Layout.preferredHeight: 16
                                                fillMode: Image.PreserveAspectFit
                                                Layout.alignment: Qt.AlignVCenter
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
                                    text: qsTr("Model Videos")
                                }
                                ComboBox {
                                    objectName: "modelVideosCombo"
                                    Accessible.name: qsTr("Model Videos")
                                    Accessible.description: AppStrings.modelVideosHelp
                                    Layout.fillWidth: true
                                    model: ["Both", "Uploaded Videos", "Featured Videos"]
                                    currentIndex: appSettings.model_videos
                                    onActivated: appSettings.model_videos = currentIndex
                                }

                                // --- Row 3: Content Language ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.contentLanguageHelp
                                }
                                Label {
                                    Layout.fillWidth: false
                                    text: qsTr("Content Language")
                                }
                                ComboBox {
                                    id: contentLanguageComboBox
                                    objectName: "contentLanguageComboBox"
                                    Accessible.name: qsTr("Content Language")
                                    Accessible.description: AppStrings.contentLanguageHelp
                                    Layout.fillWidth: true
                                    textRole: "label"
                                    valueRole: "locale"
                                    model: ListModel {
                                        ListElement { label: qsTr("🇨🇿 Čeština"); locale: "cs-CZ" }
                                        ListElement { label: qsTr("🇩🇪 Deutsch"); locale: "de-DE" }
                                        ListElement { label: qsTr("🇺🇸 English"); locale: "en-US" }
                                        ListElement { label: qsTr("🇪🇸 Español"); locale: "es-ES" }
                                        ListElement { label: qsTr("🇵🇭 Filipino"); locale: "fil-PH" }
                                        ListElement { label: qsTr("🇫🇷 Français"); locale: "fr-FR" }
                                        ListElement { label: qsTr("🇮🇹 Italiano"); locale: "it-IT" }
                                        ListElement { label: qsTr("🇳🇱 Nederlands"); locale: "nl-NL" }
                                        ListElement { label: "🇯🇵 日本語"; locale: "ja-JP" }
                                        ListElement { label: qsTr("🇵🇱 Polski"); locale: "pl-PL" }
                                        ListElement { label: qsTr("🇵🇹 Português"); locale: "pt-PT" }
                                        ListElement { label: "🇷🇺 Русский"; locale: "ru-RU" }
                                        ListElement { label: "🇺🇦 Українська"; locale: "uk-UA" }
                                        ListElement { label: "🇨🇳 中文"; locale: "zh-CN" }
                                    }
                                    currentIndex: {
                                        // Re-evaluate when the model becomes ready; indexOfValue alone
                                        // does not establish a dependency on the available options.
                                        if (count === 0)
                                            return -1
                                        var savedIndex = indexOfValue(appSettings.locale)
                                        return savedIndex >= 0 ? savedIndex : indexOfValue("en-US")
                                    }
                                    onActivated: appSettings.locale = currentValue
                                }

                                // --- Row 4: Strict Enforcement ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.strictEnforcementHelp
                                }
                                CheckBox {
                                    objectName: "strictEnforcementCheckBox"
                                    Accessible.name: qsTr("Strict Enforcement for content language")
                                    Accessible.description: AppStrings.strictEnforcementHelp
                                    Layout.columnSpan: 2
                                    Layout.fillWidth: true
                                    text: qsTr("Strict Enforcement for content language")
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
                                    text: qsTr("Max Result Limit")
                                }
                                SpinBox {
                                    objectName: "resultLimitSpinBox"
                                    Accessible.name: qsTr("Max Result Limit")
                                    Accessible.description: AppStrings.resultLimitHelp
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
                                    text: qsTr("Output Path")
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 10

                                    TextField {
                                        id: outputPathInput
                                        objectName: "outputPathInput"
                                        Accessible.name: qsTr("Output Path")
                                        Accessible.description: qsTr("Directory where downloaded videos are saved")
                                        placeholderText: qsTr("Enter the output path for the videos...")
                                        Layout.fillWidth: true
                                        readOnly: window.androidLayoutMode
                                        text: appSettings.output_path
                                        onEditingFinished: {
                                            var trimmed = text.trim()
                                            if (trimmed.length > 0)
                                                appSettings.output_path = trimmed
                                            else
                                                text = appSettings.output_path
                                        }
                                    }
                                    Button {
                                        Accessible.name: qsTr("Choose video output folder")
                                        Layout.fillWidth: false
                                        visible: !window.androidLayoutMode
                                        text: qsTr("Choose Folder…")
                                        onClicked: outputFolderDialog.open()
                                    }
                                }

                                // --- Row 7: Write Metadata ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.writeMetadataHelp
                                }
                                CheckBox {
                                    objectName: "writeMetadataCheckBox"
                                    Accessible.name: qsTr("Write metadata")
                                    Accessible.description: AppStrings.writeMetadataHelp
                                    Layout.columnSpan: 2
                                    Layout.fillWidth: true
                                    text: qsTr("Write metadata")
                                    checked: appSettings.write_metadata
                                    onToggled: appSettings.write_metadata = checked
                                }

                                // --- Row 8: Skip Existing Files ---
                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.skipExistingFilesHelp
                                }
                                CheckBox {
                                    objectName: "skipExistingFilesCheckBox"
                                    Accessible.name: qsTr("Skip existing files")
                                    Accessible.description: AppStrings.skipExistingFilesHelp
                                    Layout.columnSpan: 2
                                    Layout.fillWidth: true
                                    text: qsTr("Skip existing files")
                                    checked: appSettings.skip_existing_files
                                    onToggled: appSettings.skip_existing_files = checked
                                }

                                HelpButton {
                                    Layout.fillWidth: false
                                    helpText: AppStrings.trackVideosHelp
                                }
                                CheckBox {
                                    objectName: "trackVideosCheckBox"
                                    Accessible.name: window.androidLayoutMode ? qsTr("Track Videos") : qsTr("Track Videos in PocketBase")
                                    Accessible.description: AppStrings.trackVideosHelp
                                    Layout.columnSpan: 2
                                    Layout.fillWidth: true
                                    text: window.androidLayoutMode ? qsTr("Track Videos") : qsTr("Track Videos (PocketBase)")
                                    checked: appSettings.track_videos
                                    onToggled: appSettings.track_videos = checked
                                }

                                Item { Layout.fillWidth: false } // Empty spacer for 1st column alignment
                                Label {
                                    Layout.fillWidth: false
                                    text: window.androidLayoutMode ? qsTr("History Data Folder") : qsTr("PocketBase Data Folder")
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 10

                                    TextField {
                                        id: databasePathInput
                                        objectName: "databasePathInput"
                                        Accessible.name: qsTr("PocketBase Data Folder")
                                        Accessible.description: qsTr("Directory where PocketBase data files are stored")
                                        placeholderText: qsTr("Enter the PocketBase data directory")
                                        Layout.fillWidth: true
                                        readOnly: window.androidLayoutMode
                                        text: appSettings.pocketbase_data_path
                                        onEditingFinished: {
                                            var trimmed = text.trim()
                                            if (trimmed.length > 0)
                                                appSettings.pocketbase_data_path = trimmed
                                            else
                                                text = appSettings.pocketbase_data_path
                                        }
                                    }
                                    Button {
                                        Accessible.name: qsTr("Choose PocketBase data folder")
                                        Layout.fillWidth: false
                                        visible: !window.androidLayoutMode
                                        text: qsTr("Choose Folder…")
                                        onClicked: pocketbaseFolderDialog.open()
                                    }
                                }
                            }
                        }
                    }

                    // ==========================================
                    // TAB 2: LEISTUNG SETTINGS (Performance)
                    // ==========================================
                    SmoothScrollView {
                        id: "scrollviewPerformance"
                        clip: true

                        GridLayout {
                            columnSpacing: 15
                            columns: window.compact ? 1 : 3
                            width: scrollviewPerformance.availableWidth
                            Layout.fillWidth: true
                            rowSpacing: 15

                            // Left Pair                        // Right Pair
                            HelpButton {Layout.fillWidth: false; helpText: AppStrings.downloadWorkersHelp}
                            Label {
                                Layout.fillWidth: false
                                text: qsTr("Download workers:")
                            }
                            SpinBox {
                                objectName: "downloadWorkersSpinBox"
                                Accessible.name: qsTr("Download workers")
                                Accessible.description: AppStrings.downloadWorkersHelp
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.download_workers
                                onValueModified: appSettings.download_workers = value
                            }
                            HelpButton {Layout.fillWidth: false; helpText: AppStrings.networkDelayHelp}
                            Label {
                                text: qsTr("Network delay (requests/sec):")
                            }
                            SpinBox {
                                objectName: "networkDelaySpinBox"
                                Accessible.name: qsTr("Network delay")
                                Accessible.description: AppStrings.networkDelayHelp
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
                                text: qsTr("Parallel Downloads:")
                            }
                            SpinBox {
                                objectName: "parallelDownloadsSpinBox"
                                Accessible.name: qsTr("Parallel Downloads")
                                Accessible.description: AppStrings.parallelDownloadsHelp
                                Layout.fillWidth: true
                                editable: true
                                from: 1
                                to: bridge.isPremium ? 100 : 1
                                value: appSettings.parallel_downloads
                                onValueModified: backend.set_parallel_downloads(value)
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.retriesHelp
                            }
                            Label {
                                text: qsTr("Maximum retries:")
                            }
                            SpinBox {
                                objectName: "retriesSpinBox"
                                Accessible.name: qsTr("Maximum retries")
                                Accessible.description: AppStrings.retriesHelp
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
                                text: qsTr("Maximum timeout:")
                            }
                            SpinBox {
                                objectName: "timeoutSpinBox"
                                Accessible.name: qsTr("Maximum timeout")
                                Accessible.description: AppStrings.timeoutHelp
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
                                text: qsTr("Processing Delay (videos/sec):")
                            }
                            SpinBox {
                                objectName: "processingDelaySpinBox"
                                Accessible.name: qsTr("Processing Delay")
                                Accessible.description: AppStrings.processingDelay
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
                                text: qsTr("Speed Limit (MB/s):")
                            }
                            DecimalSpinBox {
                                objectName: "speedLimitSpinBox"
                                Accessible.name: qsTr("Speed Limit")
                                Accessible.description: AppStrings.speedLimitHelp
                                Layout.fillWidth: true
                                realTo: 100
                                realStepSize: 0.25
                                realValue: appSettings.speed_limit
                                onRealValueModified: (newValue) => appSettings.speed_limit = newValue
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.videosConcurrencyHelp
                            }
                            Label {
                                text: qsTr("Videos Concurrency:")
                            }
                            SpinBox {
                                objectName: "videosConcurrencySpinBox"
                                Accessible.name: qsTr("Videos Concurrency")
                                Accessible.description: AppStrings.videosConcurrencyHelp
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
                                text: qsTr("Pages concurrency:")
                            }
                            SpinBox {
                                objectName: "pagesConcurrencySpinBox"
                                Accessible.name: qsTr("Pages Concurrency")
                                Accessible.description: AppStrings.pagesConcurrencyHelp
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: appSettings.pages_concurrency
                                onValueModified: appSettings.pages_concurrency = value
                            }

                            GridLayout {
                                columnSpacing: 15
                                Layout.columnSpan: 3
                                columns: window.compact ? 1 : 2
                                width: scrollviewPerformance.availableWidth
                                Layout.fillWidth: true
                                rowSpacing: 15

                                RowLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        Layout.fillWidth: true
                                        wrapMode: Text.Wrap
                                        text: qsTr("Response cache size (MB)")
                                    }
                                    HelpButton { helpText: AppStrings.responseCacheSizeHelp }
                                }
                                SpinBox {
                                    objectName: "responseCacheSizeSpinBox"
                                    Accessible.name: qsTr("Response cache size (MB)")
                                    Accessible.description: AppStrings.responseCacheSizeHelp
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 2000
                                    value: appSettings.response_cache_size
                                    onValueModified: appSettings.response_cache_size = value
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        Layout.fillWidth: true
                                        wrapMode: Text.Wrap
                                        text: qsTr("Response cache lifetime (seconds)")
                                    }
                                    HelpButton { helpText: AppStrings.responseCacheTTLHelp }
                                }
                                SpinBox {
                                    objectName: "responseCacheTTLSpinBox"
                                    Accessible.name: qsTr("Response cache lifetime (seconds)")
                                    Accessible.description: AppStrings.responseCacheTTLHelp
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 20000
                                    value: appSettings.response_cache_ttl
                                    onValueModified: appSettings.response_cache_ttl = value
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        Layout.fillWidth: true
                                        wrapMode: Text.Wrap
                                        text: qsTr("Segment-list cache size (MB)")
                                    }
                                    HelpButton { helpText: AppStrings.segmentCacheSizeHelp }
                                }
                                SpinBox {
                                    objectName: "segmentCacheSizeSpinBox"
                                    Accessible.name: qsTr("Segment-list cache size (MB)")
                                    Accessible.description: AppStrings.segmentCacheSizeHelp
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 2000
                                    value: appSettings.segment_cache_size
                                    onValueModified: appSettings.segment_cache_size = value
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        Layout.fillWidth: true
                                        wrapMode: Text.Wrap
                                        text: qsTr("Segment-list cache lifetime (seconds)")
                                    }
                                    HelpButton { helpText: AppStrings.segmentCacheTTLHelp }
                                }
                                SpinBox {
                                    objectName: "segmentCacheTTLSpinBox"
                                    Accessible.name: qsTr("Segment-list cache lifetime (seconds)")
                                    Accessible.description: AppStrings.segmentCacheTTLHelp
                                    Layout.fillWidth: true
                                    editable: true
                                    to: 20000
                                    value: appSettings.segment_cache_ttl
                                    onValueModified: appSettings.segment_cache_ttl = value
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        Layout.fillWidth: true
                                        wrapMode: Text.Wrap
                                        text: qsTr("Initial retry wait (seconds)")
                                    }
                                    HelpButton { helpText: AppStrings.retryInitialDelayHelp }
                                }
                                DecimalSpinBox {
                                    objectName: "requestInitialRetryDelaySpinBox"
                                    Accessible.name: qsTr("Initial retry wait (seconds)")
                                    Accessible.description: AppStrings.retryInitialDelayHelp
                                    Layout.fillWidth: true
                                    realTo: 20000
                                    realValue: appSettings.request_initial_retry_delay
                                    onRealValueModified: (newValue) => appSettings.request_initial_retry_delay = newValue
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        Layout.fillWidth: true
                                        wrapMode: Text.Wrap
                                        text: qsTr("Maximum retry wait (seconds)")
                                    }
                                    HelpButton { helpText: AppStrings.retryMaxDelayHelp }
                                }
                                DecimalSpinBox {
                                    objectName: "requestRetryMaxDelaySpinBox"
                                    Accessible.name: qsTr("Maximum retry wait (seconds)")
                                    Accessible.description: AppStrings.retryMaxDelayHelp
                                    Layout.fillWidth: true
                                    realTo: 20000
                                    realValue: appSettings.request_retry_max_delay
                                    onRealValueModified: (newValue) => appSettings.request_retry_max_delay = newValue
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        Layout.fillWidth: true
                                        wrapMode: Text.Wrap
                                        text: qsTr("Retry wait multiplier")
                                    }
                                    HelpButton { helpText: AppStrings.retryMultiplierHelp }
                                }
                                DecimalSpinBox {
                                    objectName: "requestRetryMultiplierSpinBox"
                                    Accessible.name: qsTr("Retry wait multiplier")
                                    Accessible.description: AppStrings.retryMultiplierHelp
                                    Layout.fillWidth: true
                                    realTo: 20000
                                    realValue: appSettings.request_retry_multiplier
                                    onRealValueModified: (newValue) => appSettings.request_retry_multiplier = newValue
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        Layout.fillWidth: true
                                        wrapMode: Text.Wrap
                                        text: qsTr("Random extra retry wait (seconds)")
                                    }
                                    HelpButton { helpText: AppStrings.retryJitterHelp }
                                }
                                DecimalSpinBox {
                                    objectName: "requestRetryJitterSpinBox"
                                    Accessible.name: qsTr("Random extra retry wait (seconds)")
                                    Accessible.description: AppStrings.retryJitterHelp
                                    Layout.fillWidth: true
                                    realTo: 20000
                                    realValue: appSettings.request_retry_jitter
                                    onRealValueModified: (newValue) => appSettings.request_retry_jitter = newValue
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
                    SmoothScrollView {
                        clip: true
                        id: "scrollviewSettings"

                        GridLayout {
                            columnSpacing: 15
                            columns: 2
                            width: scrollviewSettings.availableWidth
                            Layout.fillWidth: true
                            rowSpacing: 15

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.updateChecks
                            }
                            CheckBox {
                                objectName: "updateChecksCheckBox"
                                Accessible.name: qsTr("Search for Updates")
                                Accessible.description: AppStrings.updateChecks
                                text: qsTr("Search for Updates")
                                Layout.fillWidth: true
                                checked: appSettings.update_checks
                                onToggled: appSettings.update_checks = checked
                            }
                            Button {
                                text: qsTr("Check for app updates")
                                Layout.columnSpan: 2
                                Layout.fillWidth: true
                                onClicked: backend.check_for_updates()
                            }
                            HelpButton {
                                helpText: AppStrings.systemNotificationsHelp
                            }
                            CheckBox {
                                Layout.fillWidth: true
                                text: qsTr("System notifications when the app is inactive")
                                objectName: "systemNotificationsCheckBox"
                                checked: appSettings.system_notifications
                                onToggled: appSettings.system_notifications = checked
                            }
                            Label {
                                Layout.fillWidth: true
                                Layout.columnSpan: 2
                                visible: text !== ""
                                text: typeof systemNotifier !== "undefined" ? systemNotifier.status : ""
                                textFormat: Text.PlainText
                                wrapMode: Text.Wrap
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.supressErrors
                            }
                            CheckBox {
                                objectName: "supressErrorsCheckBox"
                                Accessible.name: qsTr("Reduce repeated error announcements")
                                Accessible.description: AppStrings.supressErrors
                                text: qsTr("Reduce repeated error announcements")
                                Layout.fillWidth: true
                                checked: appSettings.supress_errors
                                onToggled: appSettings.supress_errors = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: backend.errorReportDisclosure
                            }
                            CheckBox {
                                objectName: "enableLoggingCheckBox"
                                Accessible.name: qsTr("Send tracebacks and video URLs")
                                Accessible.description: backend.errorReportDisclosure
                                // Use \n for multi-line text
                                text: qsTr("Send tracebacks and video URLs")
                                Layout.fillWidth: true
                                checked: appSettings.enable_logging
                                onToggled: appSettings.enable_logging  = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.trustEnvironmentHelp
                            }
                            CheckBox {
                                objectName: "trustEnvironmentCheckBox"
                                Accessible.name: qsTr("Trust Environment")
                                Accessible.description: AppStrings.trustEnvironmentHelp
                                // Use \n for multi-line text
                                text: qsTr("Trust Environment (Advanced)")
                                Layout.fillWidth: true
                                checked: appSettings.trust_environment
                                onToggled: appSettings.trust_environment  = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.debugModeHelp
                            }
                            CheckBox {
                                objectName: "debugModeCheckBox"
                                Accessible.name: qsTr("Enable Debug Mode")
                                Accessible.description: AppStrings.debugModeHelp
                                text: qsTr("Enable Debug Mode (Not recommended)")
                                Layout.fillWidth: true
                                checked: appSettings.debug_mode
                                onToggled: appSettings.debug_mode = checked
                            }

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.logLevel
                            }
                            ComboBox {
                                objectName: "logLevelComboBox"
                                Accessible.name: qsTr("Log Level")
                                Accessible.description: AppStrings.logLevel
                                Layout.fillWidth: true
                                model: ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                                currentIndex: appSettings.log_level
                                onActivated: appSettings.log_level = currentIndex
                            }
                                
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.httpVersionHelp
                            }
                            TextField {
                                id: "httpVersion"
                                objectName: "httpVersionInput"
                                Accessible.name: qsTr("HTTP Version")
                                Accessible.description: AppStrings.httpVersionHelp
                                placeholderText: qsTr("HTTP Version may be: v1; v2; v3")
                                Layout.fillWidth: true
                                text: appSettings.http_version
                                validator: RegularExpressionValidator {
                                    regularExpression: /^(v[1-3])?$/i
                                }
                                color: acceptableInput ? (window.materialStyle ? Material.foreground : palette.text) : "#ef4444"
                                onEditingFinished: {
                                    if (acceptableInput)
                                        appSettings.http_version = text
                                    else
                                        text = appSettings.http_version
                                }
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.impersonationHelp
                            }
                            TextField {
                                id: "impersonation"
                                objectName: "impersonationInput"
                                Accessible.name: qsTr("Browser Impersonation Target")
                                Accessible.description: AppStrings.impersonationHelp
                                placeholderText: qsTr("e.g., 'chrome', 'safari', 'edge'")
                                Layout.fillWidth: true
                                text: appSettings.impersonation
                                validator: RegularExpressionValidator {
                                    regularExpression: /^[a-zA-Z0-9_\-]*$/
                                }
                                color: acceptableInput ? (window.materialStyle ? Material.foreground : palette.text) : "#ef4444"
                                onEditingFinished: {
                                    if (acceptableInput)
                                        appSettings.impersonation = text
                                    else
                                        text = appSettings.impersonation
                                }
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.customJA3Help
                            }
                            TextField {
                                id: "customJA3"
                                objectName: "customJA3Input"
                                Accessible.name: qsTr("Custom JA3 String")
                                Accessible.description: AppStrings.customJA3Help
                                placeholderText: qsTr("Custom JA3 String")
                                Layout.fillWidth: true
                                text: appSettings.custom_ja3
                                validator: RegularExpressionValidator {
                                    regularExpression: /^[0-9,\-]*$/
                                }
                                color: acceptableInput ? (window.materialStyle ? Material.foreground : palette.text) : "#ef4444"
                                onEditingFinished: {
                                    if (acceptableInput)
                                        appSettings.custom_ja3 = text
                                    else
                                        text = appSettings.custom_ja3
                                }
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.interfaceHelp
                            }
                            TextField {
                                id: "interface"
                                objectName: "interfaceInput"
                                Accessible.name: qsTr("Network Interface or IP")
                                Accessible.description: AppStrings.interfaceHelp
                                placeholderText: qsTr("e.g., eth0, wlan0, tun0, 10.6.3.20")
                                Layout.fillWidth: true
                                text: appSettings.interface
                                validator: RegularExpressionValidator {
                                    regularExpression: /^[^\s]*$/
                                }
                                color: acceptableInput ? (window.materialStyle ? Material.foreground : palette.text) : "#ef4444"
                                onEditingFinished: {
                                    if (acceptableInput)
                                        appSettings.interface = text
                                    else
                                        text = appSettings.interface
                                }
                            }
                        }
                    }

                    // ===============
                    // TAB 4: Privacy Settings
                    // ===============

                    SmoothScrollView {
                        clip: true
                        id: "scrollviewPrivacy"

                        GridLayout {
                            columnSpacing: 15
                            columns: 2
                            width: scrollviewPrivacy.availableWidth
                            Layout.fillWidth: true
                            rowSpacing: 15

                            HelpButton {
                                Layout.fillWidth: false
                                Layout.alignment: Qt.AlignTop
                                helpText: AppStrings.anonymousModeHelp
                            }
                            CheckBox {
                                objectName: "anonymousModeCheckBox"
                                Accessible.name: qsTr("Anonymous Mode")
                                Accessible.description: AppStrings.anonymousModeHelp
                                text: qsTr("Anonymous Mode")
                                Layout.fillWidth: true
                                checked: appSettings.anonymous_mode
                                onToggled: appSettings.anonymous_mode = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                Layout.alignment: Qt.AlignTop
                                helpText: AppStrings.encryptedCHHelp
                            }
                            CheckBox {
                                objectName: "encryptedCHCheckBox"
                                Accessible.name: qsTr("Encrypted Client Hello")
                                Accessible.description: AppStrings.encryptedCHHelp
                                text: qsTr("Encrypted Client Hello")
                                Layout.fillWidth: true
                                checked: appSettings.encrypted_ch
                                onToggled: appSettings.encrypted_ch = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                Layout.alignment: Qt.AlignTop
                                helpText: AppStrings.dnsOverHTTPSHelp
                            }
                            CheckBox {
                                objectName: "dnsOverHTTPSCheckBox"
                                Accessible.name: qsTr("DNS over HTTPS")
                                Accessible.description: AppStrings.dnsOverHTTPSHelp
                                text: qsTr("DNS over HTTPS")
                                Layout.fillWidth: true
                                checked: appSettings.dns_over_https
                                onToggled: appSettings.dns_over_https = checked
                            }

                            TorRouting {
                                Layout.columnSpan: 2
                                Layout.fillWidth: true
                            }

                            HelpButton {
                                Layout.fillWidth: false
                                Layout.alignment: Qt.AlignTop
                                helpText: AppStrings.dnsPrimaryHelp
                            }
                            TextField {
                                id: "dnsPrimaryInput"
                                objectName: "dnsPrimaryInput"
                                Accessible.name: qsTr("Primary DNS over HTTPS Server")
                                Accessible.description: AppStrings.dnsPrimaryHelp
                                placeholderText: qsTr("Enter Primary DNS (Must support DNS over HTTPS)")
                                Layout.fillWidth: true
                                text: appSettings.dns_server
                                validator: RegularExpressionValidator {
                                    regularExpression: /^(https?:\/\/\S+|(\d{1,3}\.){3}\d{1,3}(:\d+)?|[a-zA-Z0-9.\-_]+|\[[0-9a-fA-F:]+\](:\d+)?)$/
                                }
                                color: acceptableInput ? (window.materialStyle ? Material.foreground : palette.text) : "#ef4444"
                                onEditingFinished: {
                                    if (acceptableInput)
                                        appSettings.dns_server = text
                                    else
                                        text = appSettings.dns_server
                                }
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                Layout.alignment: Qt.AlignTop
                                helpText: AppStrings.fallbackDNSHelp
                            }
                            TextField {
                                id: "dnsFallbackInput"
                                objectName: "dnsFallbackInput"
                                Accessible.name: qsTr("Fallback DNS over HTTPS Server")
                                Accessible.description: AppStrings.fallbackDNSHelp
                                placeholderText: qsTr("Enter Fallback DNS (Must support DNS over HTTPS)")
                                Layout.fillWidth: true
                                text: appSettings.fallback_dns
                                validator: RegularExpressionValidator {
                                    regularExpression: /^(https?:\/\/\S+|(\d{1,3}\.){3}\d{1,3}(:\d+)?|[a-zA-Z0-9.\-_]+|\[[0-9a-fA-F:]+\](:\d+)?)$/
                                }
                                color: acceptableInput ? (window.materialStyle ? Material.foreground : palette.text) : "#ef4444"
                                onEditingFinished: {
                                    if (acceptableInput)
                                        appSettings.fallback_dns = text
                                    else
                                        text = appSettings.fallback_dns
                                }
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                Layout.alignment: Qt.AlignTop
                                helpText: AppStrings.sniObfuscationHelp
                            }
                            CheckBox {
                                    objectName: "sniObfuscationCheckBox"
                                    Accessible.name: qsTr("SNI Obfuscation")
                                    Accessible.description: AppStrings.sniObfuscationHelp
                                    text: qsTr("SNI Obfuscation")
                                    Layout.fillWidth: true
                                    checked: appSettings.sni_obfuscation
                                    onToggled: appSettings.sni_obfuscation = checked
                                }

                            GridLayout {
                                Layout.columnSpan: 2
                                Layout.fillWidth: true
                                columns: window.compact ? 1 : 2
                                columnSpacing: 15
                                rowSpacing: 15

                                ButtonGroup {
                                    id: sniModeGroup
                                }

                                RadioButton {
                                    objectName: "sniLiteRadio"
                                    Accessible.name: qsTr("Lite SNI Obfuscation")
                                    text: qsTr("Lite SNI Obfuscation")
                                    Layout.fillWidth: false
                                    enabled: appSettings.sni_obfuscation
                                    ButtonGroup.group: sniModeGroup
                                    checked: appSettings.sni_obfuscation_lite
                                    onClicked: appSettings.set_sni_obfuscation_mode("lite")
                                }
                                RadioButton {
                                    objectName: "sniStrictRadio"
                                    Accessible.name: qsTr("Strict SNI Obfuscation")
                                    text: qsTr("Strict SNI Obfuscation (Requires Admin / root rights)")
                                    Layout.fillWidth: false
                                    visible: !window.androidLayoutMode
                                    enabled: appSettings.sni_obfuscation
                                    ButtonGroup.group: sniModeGroup
                                    checked: appSettings.sni_obfuscation_strict
                                    onClicked: appSettings.set_sni_obfuscation_mode("strict")
                                }
                                ComboBox {
                                    id: strictProfileCombo
                                    objectName: "strictProfileCombo"
                                    Accessible.name: qsTr("Strict SNI Obfuscation Profile")
                                    Layout.fillWidth: true
                                    visible: !window.androidLayoutMode && appSettings.sni_obfuscation && appSettings.sni_obfuscation_strict
                                    enabled: appSettings.sni_obfuscation && appSettings.sni_obfuscation_strict
                                    model: ["Strict Fragmentation", "Strict Reverse", "Strict Desync"]
                                    currentIndex: Math.max(0, model.indexOf(appSettings.sni_obfuscation_strict_profile))
                                    onActivated: {
                                        appSettings.sni_obfuscation_strict_profile = currentText
                                    }
                                }
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                Layout.alignment: Qt.AlignTop
                                helpText: AppStrings.proxySetupHelp
                            }
                            Button {
                                Accessible.name: qsTr("Proxy Configuration")
                                Accessible.description: AppStrings.proxySetupHelp
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
                    SmoothScrollView {
                        id: "scrollviewUI"
                        clip: true

                        GridLayout {
                            width: scrollviewUI.availableWidth
                            columnSpacing: 15
                            columns: window.compact ? 1 : 3
                            rowSpacing: 15
                            Layout.fillWidth: true

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.guiLanguageHelp
                            }
                            Label {
                                text: qsTr("Graphical User Interface language:")
                            }
                            ComboBox {
                                objectName: "guiLanguageComboBox"
                                Accessible.name: qsTr("Graphical User Interface Language")
                                Accessible.description: AppStrings.guiLanguageHelp
                                Layout.fillWidth: true
                                model: ["English"]
                                currentIndex: 0
                                enabled: false
                            }
                            Label {
                                Layout.columnSpan: 3
                                Layout.fillWidth: true
                                wrapMode: Text.WordWrap
                                text: qsTr("Porn Fetch is English-only. Translations are not available yet.")
                            }
                            Label { text: qsTr("Accessibility") }
                            CheckBox {
                                text: qsTr("Reduce motion")
                                checked: appSettings.reduced_motion
                                onToggled: appSettings.reduced_motion = checked
                            }
                            CheckBox {
                                text: qsTr("High contrast")
                                checked: appSettings.high_contrast
                                onToggled: appSettings.high_contrast = checked
                            }
                            HelpButton {
                                Layout.fillWidth: false
                                helpText: AppStrings.fontSizeHelp
                            }
                            Label {
                                text: qsTr("Font Size:")
                            }
                            SpinBox {
                                objectName: "fontSizeSpinBox"
                                Accessible.name: qsTr("Font Size")
                                Accessible.description: AppStrings.fontSizeHelp
                                Layout.fillWidth: true
                                from: 5
                                to: 72
                                value: appSettings.font_size
                                onValueModified: appSettings.font_size = value
                            }
                            HelpButton { Layout.fillWidth: false; helpText: AppStrings.appStyleHelp }
                            Label { text: qsTr("Application Style (Requires Restart):") }
                            ComboBox {
                                objectName: "coreStyleComboBox"
                                Accessible.name: qsTr("Application Style")
                                Accessible.description: AppStrings.appStyleHelp
                                Layout.fillWidth: true
                                model: ["Material", "Fusion", "Universal", "Windows"]
                                currentIndex: Math.max(0, find(appSettings.core_style))
                                onActivated: appSettings.core_style = currentText
                            }

                            // 2. Dark/Light Mode
                            HelpButton { Layout.fillWidth: false; helpText: AppStrings.darkModeHelp }
                            Label { text: qsTr("Dark Mode:") }
                            Switch {
                                objectName: "darkModeSwitch"
                                Accessible.name: qsTr("Dark Mode")
                                Accessible.description: AppStrings.darkModeHelp
                                Layout.alignment: Qt.AlignLeft
                                checked: appSettings.dark_mode
                                onToggled: appSettings.dark_mode = checked
                            }

                            HelpButton {
                                Layout.fillWidth: false
                                helpText: qsTr("Show a glowing border while the app is busy.")
                            }
                            Label { text: qsTr("Activity glow") }
                            Switch {
                                objectName: "activityGlowSwitch"
                                Accessible.name: qsTr("Activity glow")
                                Accessible.description: qsTr("Show a glowing border while the app is busy.")
                                Layout.alignment: Qt.AlignLeft
                                checked: appSettings.activity_glow_enabled
                                onToggled: appSettings.activity_glow_enabled = checked
                            }

                            // 3. Accent Color
                            HelpButton { Layout.fillWidth: false; helpText: AppStrings.accentColorHelp }
                            Label { text: qsTr("Accent Color:") }
                            ComboBox {
                                objectName: "accentColorComboBox"
                                Accessible.name: qsTr("Application Accent Color")
                                Accessible.description: AppStrings.accentColorHelp
                                Layout.fillWidth: true
                                textRole: "text"
                                valueRole: "value"
                                model: ListModel {
                                    ListElement { text: qsTr("Indigo"); value: "#6366f1" }
                                    ListElement { text: qsTr("Red"); value: "#f44336" }
                                    ListElement { text: qsTr("Green"); value: "#4caf50" }
                                    ListElement { text: qsTr("Orange"); value: "#ff9800" }
                                    ListElement { text: qsTr("Purple"); value: "#9c27b0" }
                                }
                                currentIndex: Math.max(0, indexOfValue(appSettings.accent_color))
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
            visible: !window.compact
            Layout.fillWidth: true
            height: 1
        }

        // ---------------------------------------------------------
        // BOTTOM GLOBAL ACTION BUTTONS
        // ---------------------------------------------------------
        // A ColumnLayout containing 3 RowLayouts to perfectly align the buttons in a grid structure
        ColumnLayout {
            visible: !window.compact
            Layout.fillWidth: true
            spacing: 10 // Space between rows of buttons

            // Row 1
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Button {
                    Accessible.name: qsTr("Purchase / renew license")
                    Layout.fillWidth: true
                    // Material styling overrides for specific buttons to make them stand out
                    Material.background: "#6366f1" // Premium Indigo color
                    Material.foreground: "white"   // White text
                    font.bold: true // Make text bold
                    text: qsTr("Purchase / renew license")

                    onClicked: {
                        Qt.openUrlExternally("https://pornfetch.to/")
                    }

                }
                Button {
                    Accessible.name: qsTr("Import License File")
                    Layout.fillWidth: true
                    text: qsTr("Import License File")
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
                    objectName: "resetSettingsButton"
                    Accessible.name: qsTr("Reset Porn Fetch to default settings")
                    Accessible.description: qsTr("Restores all application settings to their default values")
                    Layout.fillWidth: true
                    Material.background: "#ef4444" // Danger Red color
                    Material.foreground: "white"
                    text: qsTr("Reset Porn Fetch to default settings")
                    onClicked: {backend.reset_pornfetch()}
                }
                Button {
                    Accessible.name: qsTr("Clear Temporary Files")
                    Layout.fillWidth: true
                    text: qsTr("Clear Temporary Files")
                    onClicked: {backend.clear_temporary_files()}
                }

            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                visible: backend.maintenance_available
                Button {
                    objectName: "manageInstallationButton"
                    Layout.fillWidth: true
                    text: qsTr("Manage installation")
                    Accessible.name: text
                    onClicked: backend.open_maintenance("components")
                }
                Button {
                    objectName: "uninstallButton"
                    Layout.fillWidth: true
                    text: qsTr("Uninstall Porn Fetch")
                    Accessible.name: text
                    onClicked: backend.open_maintenance("uninstall")
                }
            }
        }
    }
}
