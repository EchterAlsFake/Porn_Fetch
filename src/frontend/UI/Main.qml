// qml/Main.qml

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    font.pointSize: appSettings.font_size

    width: 1350
    height: 720
    minimumWidth: 900
    minimumHeight: 600

    visible: true
    title: qsTr("Video Downloader")
    property bool safeToClose: false
    property bool startupContinued: false

    function continueStartup() {
        if (startupContinued)
            return
        startupContinued = true
        if (appSettings.update_checks)
            backend.check_for_updates()
    }

    Component.onCompleted: {
        if (appSettings.error_reporting_decided)
            continueStartup()
        else
            Qt.callLater(function() { errorReportingDialog.open() })
    }

    onClosing: (closeEvent) => {
        if (!safeToClose) {
            closeEvent.accepted = false
            backend.initiate_shutdown()
        }
    }

    Connections {
        target: backend

        function onUpdateAvailable(details) {
            updateDialog.version = details.version || ""
            updateDialog.authenticatedUrl = details.url || ""
            updateDialog.anonymousUrl = details.anonymous_download || ""
            updateDialog.importantInfo = details.important_info || ""
            updateDialog.changelog = details.changelog || ""
            updateDialog.updateInProgress = false
            updateDialog.statusMessage = ""
            updateDialog.downloadedBytes = 0
            updateDialog.totalBytes = 0
            updateDialog.open()
        }

        function onUpdateProgress(current, total) {
            updateDialog.downloadedBytes = current
            updateDialog.totalBytes = total
        }

        function onUpdateStatus(status) {
            updateDialog.statusMessage = status
            var normalized = status.toLowerCase()
            if (normalized.indexOf("failed") !== -1
                    || normalized.indexOf("successful") !== -1)
                updateDialog.updateInProgress = false
        }

        function onShutdown_complete() {
            window.safeToClose = true
            window.close()
        }
    }

    Dialog {
        id: errorReportingDialog

        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.min(window.width - 48, 900)
        height: Math.min(window.height - 48, 680)
        modal: true
        padding: 20
        closePolicy: Popup.NoAutoClose

        background: Rectangle {
            radius: 12
            color: "#1e1e24"
            border.color: "#383b48"
            border.width: 1
        }

        contentItem: ColumnLayout {
            spacing: 14

            Label {
                Layout.fillWidth: true
                text: qsTr("Help improve Porn Fetch after errors?")
                color: "#4da6ff"
                font.pixelSize: 24
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }

            Label {
                Layout.fillWidth: true
                text: qsTr("This is a one-time choice. Automatic error reporting is disabled until you explicitly enable it.")
                color: "#f1f5f9"
                font.bold: true
                wrapMode: Text.Wrap
            }

            SmoothScrollView {
                id: consentScroll
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                contentWidth: availableWidth
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                ColumnLayout {
                    width: consentScroll.availableWidth
                    spacing: 12

                    Label {
                        Layout.fillWidth: true
                        text: backend.errorReportDisclosure
                        color: "#d7dce5"
                        wrapMode: Text.Wrap
                    }

                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Synthetic example of a stored report:")
                        color: "#5dade2"
                        font.bold: true
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: exampleText.contentHeight + 24
                        radius: 6
                        color: "#111318"
                        border.color: "#383b48"

                        TextEdit {
                            id: exampleText
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.margins: 12
                            height: contentHeight
                            text: backend.errorReportExample
                            color: "#d7dce5"
                            font.family: "monospace"
                            font.pixelSize: 12
                            readOnly: true
                            selectByMouse: true
                            wrapMode: TextEdit.Wrap
                        }
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Item { Layout.fillWidth: true }

                Button {
                    text: qsTr("No, keep disabled")
                    onClicked: {
                        appSettings.set_error_reporting_consent(false)
                        errorReportingDialog.close()
                        window.continueStartup()
                    }
                }

                Button {
                    text: qsTr("Yes, enable reports")
                    onClicked: {
                        appSettings.set_error_reporting_consent(true)
                        errorReportingDialog.close()
                        window.continueStartup()
                    }
                }
            }
        }
    }

    Dialog {
        id: updateDialog

        property string version: ""
        property string authenticatedUrl: ""
        property string anonymousUrl: ""
        property string importantInfo: ""
        property string changelog: ""
        property string statusMessage: ""
        property real downloadedBytes: 0
        property real totalBytes: 0
        property bool updateInProgress: false

        function formatBytes(bytes) {
            if (!bytes || bytes <= 0)
                return "0 B"
            var units = ["B", "KiB", "MiB", "GiB"]
            var unit = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1)
            return (bytes / Math.pow(1024, unit)).toFixed(unit === 0 ? 0 : 1) + " " + units[unit]
        }

        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.min(window.width - 48, 820)
        height: Math.min(window.height - 48, 640)
        modal: true
        padding: 20
        closePolicy: Popup.NoAutoClose

        background: Rectangle {
            radius: 12
            color: "#1e1e24"
            border.color: "#383b48"
            border.width: 1
        }

        contentItem: ColumnLayout {
            spacing: 14

            Label {
                Layout.fillWidth: true
                text: qsTr("🚀 New Update Available!")
                color: "#4da6ff"
                font.pixelSize: 26
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }

            SmoothScrollView {
                id: updateScroll
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                ColumnLayout {
                    width: updateScroll.availableWidth
                    spacing: 14

                    RowLayout {
                        Layout.fillWidth: true

                        Label {
                            text: qsTr("Version:")
                            color: "#5dade2"
                            font.bold: true
                        }

                        Label {
                            Layout.fillWidth: true
                            text: updateDialog.version
                            color: "#e0e0e0"
                        }
                    }

                    RowLayout {
                        Layout.fillWidth: true

                        Label {
                            text: qsTr("Download:")
                            color: "#5dade2"
                            font.bold: true
                        }

                        Button {
                            text: qsTr("Authenticated Link")
                            flat: true
                            enabled: updateDialog.authenticatedUrl !== ""
                            onClicked: Qt.openUrlExternally(updateDialog.authenticatedUrl)
                        }

                        Label {
                            text: "|"
                            color: "#94a3b8"
                        }

                        Button {
                            text: qsTr("Anonymous Link")
                            flat: true
                            enabled: updateDialog.anonymousUrl !== ""
                            onClicked: Qt.openUrlExternally(updateDialog.anonymousUrl)
                        }

                        Item { Layout.fillWidth: true }
                    }

                    Label {
                        text: qsTr("Important Info:")
                        color: "#5dade2"
                        font.bold: true
                    }

                    Text {
                        Layout.fillWidth: true
                        text: updateDialog.importantInfo
                        color: "#e0e0e0"
                        textFormat: Text.RichText
                        wrapMode: Text.Wrap
                        onLinkActivated: (link) => Qt.openUrlExternally(link)
                    }

                    Label {
                        text: qsTr("Changelog:")
                        color: "#5dade2"
                        font.bold: true
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: changelogText.implicitHeight + 20
                        radius: 6
                        color: "#2a2a2a"
                        border.color: "#444444"
                        border.width: 1

                        Text {
                            id: changelogText
                            anchors.fill: parent
                            anchors.margins: 10
                            text: updateDialog.changelog
                            color: "#e0e0e0"
                            textFormat: Text.RichText
                            wrapMode: Text.Wrap
                            onLinkActivated: (link) => Qt.openUrlExternally(link)
                        }
                    }
                }
            }

            ProgressBar {
                Layout.fillWidth: true
                visible: updateDialog.updateInProgress || updateDialog.downloadedBytes > 0
                from: 0
                to: updateDialog.totalBytes > 0 ? updateDialog.totalBytes : 1
                value: updateDialog.downloadedBytes
                indeterminate: updateDialog.updateInProgress && updateDialog.totalBytes <= 0
            }

            Label {
                Layout.fillWidth: true
                visible: text !== ""
                text: updateDialog.statusMessage
                color: text.toLowerCase().indexOf("failed") !== -1 ? "#ef4444" : "#e0e0e0"
                wrapMode: Text.Wrap
            }

            Label {
                Layout.fillWidth: true
                visible: updateDialog.totalBytes > 0
                text: updateDialog.formatBytes(updateDialog.downloadedBytes)
                      + " / " + updateDialog.formatBytes(updateDialog.totalBytes)
                color: "#94a3b8"
                horizontalAlignment: Text.AlignRight
            }

            RowLayout {
                Layout.fillWidth: true

                Item { Layout.fillWidth: true }

                Button {
                    text: qsTr("Later")
                    enabled: !updateDialog.updateInProgress
                    onClicked: updateDialog.close()
                }

                Button {
                    text: updateDialog.updateInProgress ? qsTr("Updating…") : qsTr("Auto Update")
                    enabled: !updateDialog.updateInProgress
                    highlighted: true
                    onClicked: {
                        updateDialog.updateInProgress = true
                        updateDialog.statusMessage = qsTr("Starting update…")
                        backend.auto_update()
                    }
                }
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 6

        TabBar {
            id: navigation

            Layout.fillWidth: true

            TabButton {
                icon.source: "qrc:/images/graphics/download.svg"
                icon.width: 24
                icon.height: 24
                icon.color: "transparent"
                display: AbstractButton.IconOnly
            }

            TabButton {
                icon.source: "qrc:/images/graphics/account.svg"
                icon.width: 24
                icon.height: 24
                icon.color: "transparent"
                display: AbstractButton.IconOnly
            }

            TabButton {
                icon.source: "qrc:/images/graphics/database.svg"
                icon.width: 24
                icon.height: 24
                icon.color: "transparent"
                display: AbstractButton.IconOnly
            }

            TabButton {
                icon.source: "qrc:/images/graphics/settings.svg"
                icon.width: 24
                icon.height: 24
                icon.color: "transparent"
                display: AbstractButton.IconOnly
            }

            TabButton {
                icon.source: "qrc:/images/graphics/information.svg"
                icon.width: 24
                icon.height: 24
                icon.color: "transparent"
                display: AbstractButton.IconOnly
            }

            TabButton {
                text: qsTr("SUPPORTED WEBSITES")
            }
        }

        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true

            currentIndex: navigation.currentIndex

            DownloadsPage {
            }

            AccountPage {
                backendController: backend
            }

            StatisticsPage {
            }

            SettingsPage {
                // Pass a settings controller here when necessary.
            }

            Item {
                InfoPage {
                    anchors.fill: parent
                    visible: !appSettings.anonymous_mode
                }

                Label {
                    anchors.centerIn: parent
                    text: qsTr("Widget is hidden due to your privacy settings...")
                    font.pixelSize: appSettings.font_size
                    visible: appSettings.anonymous_mode
                }

            }


            Item {
                SupportedWebsitesPage {
                    anchors.fill: parent
                    visible: !appSettings.anonymous_mode
                }

                Label {
                    anchors.centerIn: parent
                    text: qsTr("Widget is hidden due to your privacy settings...")
                    font.pixelSize: appSettings.font_size
                    visible: appSettings.anonymous_mode
                }

            }

        }
    }
}
