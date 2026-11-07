import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    objectName: "downloadManagerPage"
    padding: 12
    background: Rectangle { color: Theme.background }

    ColumnLayout {
        anchors.fill: parent
        spacing: 12
        Label {
            Layout.fillWidth: true
            text: qsTr("Download manager")
            font.bold: true
            font.pointSize: appSettings.font_size + 4
            wrapMode: Text.WordWrap
        }
        Label {
            Layout.fillWidth: true
            text: qsTr("Downloads from this session stay here when the main list is cleared. This list resets when you close Porn Fetch.")
            color: Theme.muted
            wrapMode: Text.WordWrap
        }
        AppButton {
            text: qsTr("Open output folder")
            onClicked: backend.open_output_folder()
        }
        Label {
            Layout.fillWidth: true
            text: qsTr("%1 downloads this session").arg(sessionList.count)
            color: Theme.muted
            wrapMode: Text.WordWrap
        }
        ListView {
            id: sessionList
            objectName: "sessionDownloadList"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            spacing: 8
            boundsBehavior: Flickable.StopAtBounds
            model: backend.sessionDownloads
            ScrollBar.vertical: ScrollBar {}
            SmoothWheelHandler { flickable: sessionList }

            delegate: Rectangle {
                id: entry
                objectName: "sessionDownloadRow"
                required property string title
                required property string author
                required property string selectedQuality
                required property int progress
                required property string status
                readonly property string stateText: ({queued: qsTr("Queued"), downloading: qsTr("Downloading"),
                    stopping: qsTr("Stopping"), cancelled: qsTr("Stopped"), failed: qsTr("Failed"),
                    completed: qsTr("Completed")})[status] || status
                width: sessionList.width
                implicitHeight: entryContent.implicitHeight + 24
                radius: 10
                color: Theme.surface
                border.color: Theme.outline
                border.width: Theme.highContrast ? 2 : 1

                ColumnLayout {
                    id: entryContent
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.margins: 12
                    spacing: 6
                    Label {
                        Layout.fillWidth: true
                        text: appSettings.anonymous_mode ? qsTr("[redacted]") : entry.title
                        textFormat: Text.PlainText
                        font.bold: true
                        wrapMode: Text.WordWrap
                        color: Theme.ink
                    }
                    Label {
                        Layout.fillWidth: true
                        visible: !appSettings.anonymous_mode && entry.author.length > 0
                        text: entry.author
                        textFormat: Text.PlainText
                        color: Theme.muted
                        wrapMode: Text.WordWrap
                    }
                    Label {
                        Layout.fillWidth: true
                        text: entry.stateText + " · " + entry.progress + "%"
                              + (entry.selectedQuality ? " · " + entry.selectedQuality
                                 + (/^\d+$/.test(entry.selectedQuality) ? "p" : "") : "")
                        color: Theme.ink
                        wrapMode: Text.WordWrap
                    }
                    ProgressBar {
                        Layout.fillWidth: true
                        from: 0
                        to: 100
                        value: entry.progress
                        indeterminate: entry.status === "queued"
                        Accessible.name: qsTr("Download progress")
                        Accessible.description: entry.stateText
                    }
                }
            }

            Label {
                anchors.centerIn: parent
                width: parent.width
                visible: sessionList.count === 0
                text: qsTr("No downloads started this session.")
                color: Theme.muted
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
}
