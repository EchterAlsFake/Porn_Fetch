import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Dialogs as Dialogs
import QtQuick.Layouts

Pane {
    id: root
    padding: 0
    property int section: -1
    readonly property bool tablet: width >= 740
    readonly property int activeSection: section < 0 ? 0 : section
    readonly property color pageColor: appSettings.dark_mode ? "#101319" : "#f7f8fc"
    readonly property color cardColor: appSettings.dark_mode ? "#1b202a" : "#ffffff"
    readonly property color textColor: appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    readonly property color accentColor: appSettings.accent_color
    readonly property var titles: [qsTr("Downloads"), qsTr("Performance"), qsTr("Privacy & network"),
                                   qsTr("Appearance"), qsTr("System & data"), qsTr("License")]
    readonly property var subtitles: [qsTr("Quality, sources and files"), qsTr("Speed and reliability"),
                                      qsTr("Privacy and connections"), qsTr("Theme and language"),
                                      qsTr("App behavior and maintenance"), qsTr("Premium access")]

    function goBack() {
        if (!tablet && section >= 0) {
            section = -1
            return true
        }
        return false
    }

    background: Rectangle { color: root.pageColor }

    component SettingCard: Rectangle {
        id: card
        property string heading: ""
        property string description: ""
        default property alias controls: cardBody.data
        Layout.fillWidth: true
        implicitHeight: cardBody.implicitHeight + 32
        radius: 20
        color: root.cardColor
        ColumnLayout {
            id: cardBody
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 16
            spacing: 10
            Label {
                Layout.fillWidth: true
                text: card.heading
                color: root.textColor
                font.pixelSize: 17
                font.bold: true
                wrapMode: Text.Wrap
            }
            Label {
                Layout.fillWidth: true
                visible: card.description !== ""
                text: card.description
                color: root.mutedColor
                font.pixelSize: 13
                wrapMode: Text.Wrap
            }
        }
    }

    component ToggleRow: RowLayout {
        id: row
        property string label: ""
        property string detail: ""
        property bool value: false
        signal changed(bool selected)
        Layout.fillWidth: true
        spacing: 12
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 2
            Label {
                Layout.fillWidth: true
                text: row.label
                color: root.textColor
                wrapMode: Text.Wrap
            }
            Label {
                Layout.fillWidth: true
                visible: row.detail !== ""
                text: row.detail
                color: root.mutedColor
                font.pixelSize: 12
                wrapMode: Text.Wrap
            }
        }
        Switch {
            checked: row.value
            Accessible.name: row.label
            onToggled: row.changed(checked)
        }
    }

    component NumberRow: RowLayout {
        id: row
        property string label: ""
        property int number: 0
        property int minimum: 0
        property int maximum: 9999
        signal changed(int number)
        Layout.fillWidth: true
        spacing: 8
        Label {
            Layout.fillWidth: true
            text: row.label
            color: root.textColor
            wrapMode: Text.Wrap
        }
        SpinBox {
            Layout.preferredWidth: 130
            from: row.minimum
            to: row.maximum
            value: row.number
            editable: true
            Accessible.name: row.label
            onValueModified: row.changed(value)
        }
    }

    component ChoiceRow: ColumnLayout {
        id: row
        property string label: ""
        property var choices: []
        property int selected: 0
        property var allowed: null
        signal chosen(int index)
        Layout.fillWidth: true
        spacing: 4
        Label { text: row.label; color: root.textColor }
        ComboBox {
            Layout.fillWidth: true
            model: row.choices
            currentIndex: row.selected
            Accessible.name: row.label
            onActivated: {
                if (row.allowed && !row.allowed(currentIndex)) {
                    currentIndex = Qt.binding(function() { return row.selected })
                    return
                }
                row.chosen(currentIndex)
            }
        }
    }

    component TextRow: ColumnLayout {
        id: row
        property string label: ""
        property string value: ""
        property bool locked: false
        signal submitted(string value)
        Layout.fillWidth: true
        spacing: 4
        Label { text: row.label; color: root.textColor }
        TextField {
            Layout.fillWidth: true
            text: row.value
            readOnly: row.locked
            Accessible.name: row.label
            onEditingFinished: {
                if (!row.locked && text.trim() !== "") row.submitted(text.trim())
            }
        }
    }

    ProxyWindow {
        id: proxyWindow
        onProxyTestRequested: function(proxyUrl, verifySsl) { backend.testProxy(proxyUrl, verifySsl) }
        onProxyAccepted: function(proxyUrl, verifySsl) { backend.applyProxy(proxyUrl, verifySsl) }
        onProxyDisabled: backend.applyProxy("", true)
    }
    Connections {
        target: backend
        function onProxyTestSucceeded(proxyUrl, stats) { proxyWindow.showTestSuccess(proxyUrl, stats) }
        function onProxyTestFailed(proxyUrl, message) { proxyWindow.showTestFailure(proxyUrl, message) }
        function onProxySslError(proxyUrl, message) { proxyWindow.showSslWarning(proxyUrl, message) }
    }

    Dialogs.FileDialog {
        id: licenseFileDialog
        title: qsTr("Import license file")
        nameFilters: [qsTr("License files (*.license)"), qsTr("All files (*)")]
        onAccepted: bridge.installFromPath(selectedFile.toString())
    }

    Dialogs.FolderDialog {
        id: outputFolderDialog
        title: qsTr("Choose where to save videos")
        onAccepted: backend.set_android_output_folder(selectedFolder.toString())
    }

    function outputFolderName() {
        if (!appSettings.android_output_folder) return qsTr("App storage")
        var path = decodeURIComponent(appSettings.android_output_folder.split("/").pop())
        return path.split(":").pop() || qsTr("Selected folder")
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: root.tablet ? 18 : 12
        anchors.rightMargin: root.tablet ? 24 : 12
        spacing: root.tablet ? 18 : 0

        ScrollView {
            id: categoryScroll
            visible: root.tablet || root.section < 0
            Layout.preferredWidth: root.tablet ? 260 : root.width - 24
            Layout.fillHeight: true
            contentWidth: availableWidth
            clip: true

            ColumnLayout {
                width: categoryScroll.availableWidth
                spacing: 8
                Item { Layout.preferredHeight: 6 }
                Label {
                    text: qsTr("PREFERENCES")
                    color: root.accentColor
                    font.pixelSize: 12
                    font.bold: true
                    leftPadding: 12
                }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Choose what matters to you")
                    color: root.mutedColor
                    font.pixelSize: 13
                    wrapMode: Text.Wrap
                    leftPadding: 12
                    bottomPadding: 8
                }

                Repeater {
                    model: root.titles
                    delegate: ItemDelegate {
                        id: categoryDelegate
                        required property int index
                        required property string modelData
                        Layout.fillWidth: true
                        Layout.preferredHeight: 72
                        onClicked: root.section = index
                        scale: pressed ? 0.98 : hovered ? 1.015 : 1
                        Behavior on scale { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
                        background: Rectangle {
                            radius: 18
                            color: root.activeSection === index && root.tablet
                                   ? Qt.rgba(root.accentColor.r, root.accentColor.g, root.accentColor.b, 0.18)
                                   : categoryDelegate.hovered
                                     ? Qt.rgba(root.accentColor.r, root.accentColor.g, root.accentColor.b, 0.10)
                                   : root.cardColor
                            Behavior on color { ColorAnimation { duration: 150 } }
                        }
                        contentItem: RowLayout {
                            spacing: 12
                            Rectangle {
                                Layout.preferredWidth: 40
                                Layout.preferredHeight: 40
                                radius: 13
                                color: Qt.rgba(root.accentColor.r, root.accentColor.g, root.accentColor.b, 0.16)
                                Label {
                                    anchors.centerIn: parent
                                    text: String(index + 1)
                                    color: root.accentColor
                                    font.bold: true
                                }
                            }
                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 1
                                Label {
                                    Layout.fillWidth: true
                                    text: modelData
                                    color: root.textColor
                                    font.bold: true
                                    elide: Text.ElideRight
                                }
                                Label {
                                    Layout.fillWidth: true
                                    text: root.subtitles[index]
                                    color: root.mutedColor
                                    font.pixelSize: 11
                                    elide: Text.ElideRight
                                }
                            }
                            Label {
                                visible: !root.tablet
                                text: "›"
                                color: root.mutedColor
                                font.pixelSize: 26
                            }
                        }
                    }
                }
                Item { Layout.preferredHeight: 12 }
            }
        }

        ColumnLayout {
            visible: root.tablet || root.section >= 0
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8

            RowLayout {
                visible: root.tablet
                Layout.fillWidth: true
                Layout.preferredHeight: visible ? 52 : 0
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 0
                    Label {
                        Layout.fillWidth: true
                        text: root.titles[root.activeSection]
                        color: root.textColor
                        font.pixelSize: 21
                        font.bold: true
                        elide: Text.ElideRight
                    }
                    Label {
                        Layout.fillWidth: true
                        text: root.subtitles[root.activeSection]
                        color: root.mutedColor
                        font.pixelSize: 12
                        elide: Text.ElideRight
                    }
                }
            }

            ScrollView {
                id: detailScroll
                Layout.fillWidth: true
                Layout.fillHeight: true
                contentWidth: availableWidth
                clip: true
                Loader {
                    id: sectionLoader
                    width: detailScroll.availableWidth
                    sourceComponent: [downloadsSection, performanceSection, privacySection,
                                      appearanceSection, systemSection, licenseSection][root.activeSection]
                }
            }
        }
    }

    Component {
        id: downloadsSection
        ColumnLayout {
            width: sectionLoader.width
            spacing: 14
            SettingCard {
                heading: qsTr("Video preferences")
                description: qsTr("Choose how links and model pages are processed.")
                ChoiceRow {
                    label: qsTr("Default quality")
                    choices: ["Best", "Half", "Worst", "2160p", "1440p", "1080p", "720p",
                              "540p", "480p", "360p", "250p", "240p", "144p"]
                    selected: appSettings.quality
                    allowed: function(index) {
                        return bridge.isPremium || [0, 1, 3, 4, 5].indexOf(index) === -1
                    }
                    onChosen: function(index) { backend.set_default_quality(index) }
                }
                ChoiceRow {
                    label: qsTr("Model videos")
                    choices: [qsTr("Both"), qsTr("Uploaded"), qsTr("Featured")]
                    selected: appSettings.model_videos
                    onChosen: function(index) { appSettings.model_videos = index }
                }
                NumberRow {
                    label: qsTr("Maximum results")
                    number: appSettings.result_limit
                    maximum: 5000
                    onChanged: function(number) { appSettings.result_limit = number }
                }
                ToggleRow {
                    label: qsTr("Strict quality selection")
                    detail: qsTr("Use only the quality you selected when available.")
                    value: appSettings.strict_enforcement
                    onChanged: function(selected) { appSettings.strict_enforcement = selected }
                }
            }
            SettingCard {
                heading: qsTr("Files & history")
                ToggleRow {
                    label: qsTr("Write metadata")
                    value: appSettings.write_metadata
                    onChanged: function(selected) { appSettings.write_metadata = selected }
                }
                ToggleRow {
                    label: qsTr("Skip existing files")
                    value: appSettings.skip_existing_files
                    onChanged: function(selected) { appSettings.skip_existing_files = selected }
                }
                ToggleRow {
                    label: qsTr("Track downloads")
                    detail: qsTr("Build a private history on this device. Restart required.")
                    value: appSettings.track_videos
                    onChanged: function(selected) { appSettings.track_videos = selected }
                }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Save completed videos to")
                    color: root.textColor
                    font.bold: true
                }
                Label {
                    Layout.fillWidth: true
                    text: root.outputFolderName()
                    color: root.mutedColor
                    wrapMode: Text.Wrap
                }
                Button {
                    Layout.fillWidth: true
                    text: qsTr("Choose folder")
                    onClicked: outputFolderDialog.open()
                }
                Button {
                    Layout.fillWidth: true
                    visible: appSettings.android_output_folder !== ""
                    text: qsTr("Use app storage")
                    flat: true
                    onClicked: appSettings.android_output_folder = ""
                }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Completed videos are saved to this folder automatically.")
                    color: root.mutedColor
                    wrapMode: Text.Wrap
                    font.pixelSize: 12
                }
            }
            Item { Layout.preferredHeight: 14 }
        }
    }

    Component {
        id: performanceSection
        ColumnLayout {
            width: sectionLoader.width
            spacing: 14
            SettingCard {
                heading: qsTr("Download speed")
                NumberRow { label: qsTr("Parallel downloads"); number: appSettings.parallel_downloads; minimum: 1; maximum: 20; onChanged: function(n) { appSettings.parallel_downloads = n } }
                NumberRow { label: qsTr("Download workers"); number: appSettings.download_workers; minimum: 1; maximum: 64; onChanged: function(n) { appSettings.download_workers = n } }
                TextRow {
                    label: qsTr("Speed limit (MB/s, 0 for unlimited)")
                    value: String(appSettings.speed_limit)
                    onSubmitted: function(value) {
                        var speed = Number(value)
                        if (isFinite(speed) && speed >= 0 && speed <= 100) appSettings.speed_limit = speed
                    }
                }
            }
            SettingCard {
                heading: qsTr("Requests")
                NumberRow { label: qsTr("Retries"); number: appSettings.retries; maximum: 30; onChanged: function(n) { appSettings.retries = n } }
                NumberRow { label: qsTr("Timeout in seconds"); number: appSettings.timeout; minimum: 1; maximum: 600; onChanged: function(n) { appSettings.timeout = n } }
                NumberRow { label: qsTr("Delay between requests"); number: appSettings.network_delay; maximum: 120; onChanged: function(n) { appSettings.network_delay = n } }
                NumberRow { label: qsTr("Processing delay"); number: appSettings.processing_delay; maximum: 100; onChanged: function(n) { appSettings.processing_delay = n } }
                NumberRow { label: qsTr("Video requests at once"); number: appSettings.videos_concurrency; minimum: 1; maximum: 100; onChanged: function(n) { appSettings.videos_concurrency = n } }
                NumberRow { label: qsTr("Page requests at once"); number: appSettings.pages_concurrency; minimum: 1; maximum: 100; onChanged: function(n) { appSettings.pages_concurrency = n } }
            }
            Item { Layout.preferredHeight: 14 }
        }
    }

    Component {
        id: privacySection
        ColumnLayout {
            width: sectionLoader.width
            spacing: 14
            SettingCard {
                heading: qsTr("Privacy")
                ToggleRow {
                    label: qsTr("Anonymous mode")
                    detail: qsTr("Hide titles and private information in the app.")
                    value: appSettings.anonymous_mode
                    onChanged: function(selected) { appSettings.anonymous_mode = selected }
                }
                ToggleRow {
                    label: qsTr("Automatic error reports")
                    value: appSettings.enable_logging
                    onChanged: function(selected) { appSettings.set_error_reporting_consent(selected) }
                }
            }
            SettingCard {
                heading: qsTr("Connection protection")
                ToggleRow { label: qsTr("DNS over HTTPS"); value: appSettings.dns_over_https; onChanged: function(v) { appSettings.dns_over_https = v } }
                ToggleRow { label: qsTr("Encrypted Client Hello"); value: appSettings.encrypted_ch; onChanged: function(v) { appSettings.encrypted_ch = v } }
                ToggleRow { label: qsTr("Use Tor"); value: appSettings.enable_tor; onChanged: function(v) { appSettings.enable_tor = v } }
                ToggleRow { label: qsTr("Route license requests through Tor"); value: appSettings.enable_tor_server_routing; onChanged: function(v) { appSettings.enable_tor_server_routing = v } }
                Button {
                    Layout.fillWidth: true
                    text: appSettings.proxy ? qsTr("Configure proxy") : qsTr("Set up proxy")
                    onClicked: proxyWindow.openWithProxy(appSettings.proxy)
                }
            }
            Item { Layout.preferredHeight: 14 }
        }
    }

    Component {
        id: appearanceSection
        ColumnLayout {
            width: sectionLoader.width
            spacing: 14
            SettingCard {
                heading: qsTr("Theme")
                description: qsTr("A Material look designed for your phone and tablet.")
                ToggleRow { label: qsTr("Dark mode"); value: appSettings.dark_mode; onChanged: function(v) { appSettings.dark_mode = v } }
                NumberRow { label: qsTr("Text size"); number: appSettings.font_size; minimum: 8; maximum: 32; onChanged: function(n) { appSettings.font_size = n } }
                ChoiceRow {
                    label: qsTr("Accent color")
                    choices: [qsTr("Indigo"), qsTr("Red"), qsTr("Green"), qsTr("Orange"), qsTr("Purple")]
                    selected: Math.max(0, ["#6366f1", "#f44336", "#4caf50", "#ff9800", "#9c27b0"].indexOf(appSettings.accent_color))
                    onChosen: function(index) { appSettings.accent_color = ["#6366f1", "#f44336", "#4caf50", "#ff9800", "#9c27b0"][index] }
                }
            }
            SettingCard {
                heading: qsTr("Language")
                ChoiceRow {
                    label: qsTr("Interface language")
                    choices: [qsTr("System"), qsTr("English"), qsTr("German"), qsTr("Chinese"), qsTr("French")]
                    selected: appSettings.language
                    onChosen: function(index) { appSettings.language = index }
                }
                ChoiceRow {
                    label: qsTr("Content language")
                    choices: ["English", "Deutsch", "Français", "Italiano", "Español", "中文"]
                    selected: Math.max(0, ["en-US", "de-DE", "fr-FR", "it-IT", "es-ES", "zh-CN"].indexOf(appSettings.locale))
                    onChosen: function(index) { appSettings.locale = ["en-US", "de-DE", "fr-FR", "it-IT", "es-ES", "zh-CN"][index] }
                }
            }
            Item { Layout.preferredHeight: 14 }
        }
    }

    Component {
        id: systemSection
        ColumnLayout {
            width: sectionLoader.width
            spacing: 14
            SettingCard {
                heading: qsTr("App behavior")
                ToggleRow { label: qsTr("Suppress error dialogs"); value: appSettings.supress_errors; onChanged: function(v) { appSettings.supress_errors = v } }
                ToggleRow { label: qsTr("Use system proxy settings"); value: appSettings.trust_environment; onChanged: function(v) { appSettings.trust_environment = v } }
                ToggleRow { label: qsTr("Debug mode"); value: appSettings.debug_mode; onChanged: function(v) { appSettings.debug_mode = v } }
            }
            SettingCard {
                heading: qsTr("Maintenance")
                Button { Layout.fillWidth: true; text: qsTr("Clear temporary files"); onClicked: backend.clear_temporary_files() }
                Button { Layout.fillWidth: true; text: qsTr("Reset settings"); onClicked: backend.reset_pornfetch() }
            }
            Item { Layout.preferredHeight: 14 }
        }
    }

    Component {
        id: licenseSection
        ColumnLayout {
            width: sectionLoader.width
            spacing: 14
            SettingCard {
                heading: bridge.isValid ? qsTr("Premium active") : qsTr("No active license")
                description: bridge.reason
                Label {
                    Layout.fillWidth: true
                    visible: bridge.expiresAt !== ""
                    text: qsTr("Expires %1").arg(bridge.expiresAt)
                    color: root.mutedColor
                    wrapMode: Text.Wrap
                }
                Button {
                    Layout.fillWidth: true
                    text: qsTr("Import license file")
                    onClicked: licenseFileDialog.open()
                }
                Button {
                    Layout.fillWidth: true
                    text: qsTr("Refresh license")
                    enabled: !bridge.busy
                    onClicked: bridge.refresh()
                }
                Button {
                    Layout.fillWidth: true
                    visible: bridge.isValid
                    text: qsTr("Deactivate license")
                    enabled: !bridge.busy
                    onClicked: bridge.deactivate()
                }
            }
            SettingCard {
                heading: qsTr("Beta test license")
                description: qsTr("The beta checkout is a test. No real transaction takes place.")
                Button {
                    Layout.fillWidth: true
                    text: qsTr("Get beta test license")
                    onClicked: Qt.openUrlExternally("https://echteralsfake.me/")
                }
            }
            Item { Layout.preferredHeight: 14 }
        }
    }
}
