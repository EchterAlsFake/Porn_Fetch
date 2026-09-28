import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    padding: 12
    readonly property color pageColor: appSettings.dark_mode ? "#101319" : "#f7f8fc"
    readonly property color cardColor: appSettings.dark_mode ? "#1b202a" : "#ffffff"
    readonly property color textColor: appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    background: Rectangle { color: root.pageColor }
    property var statistics: ({})

    function refresh() { statistics = databaseBridge.getDashboardStats() }
    Component.onCompleted: refresh()
    Connections {
        target: databaseBridge
        function onStatisticsChanged() { root.refresh() }
    }

    ScrollView {
        anchors.fill: parent
        contentWidth: availableWidth
        clip: true

        ColumnLayout {
            width: parent.width
            spacing: 12
            Label {
                Layout.fillWidth: true
                text: root.statistics.enabled
                      ? qsTr("Local download history")
                      : qsTr("Download tracking is disabled. Enable it in Settings and restart the app.")
                font.bold: true
                color: root.textColor
                wrapMode: Text.Wrap
            }
            Button { text: qsTr("Refresh"); onClicked: root.refresh() }

            Repeater {
                model: [
                    { title: qsTr("Tracked videos"), value: root.statistics.total || 0 },
                    { title: qsTr("Successful"), value: root.statistics.successful || 0 },
                    { title: qsTr("Failed"), value: root.statistics.failed || 0 },
                    { title: qsTr("Success rate"), value: (root.statistics.successRate || 0) + "%" },
                    { title: qsTr("Total downloaded"), value: (root.statistics.totalSizeMb || 0) + " MiB" },
                    { title: qsTr("Last downloaded"), value: root.statistics.lastDownloaded || qsTr("None") }
                ]
                delegate: Frame {
                    required property var modelData
                    Layout.fillWidth: true
                    padding: 16
                    background: Rectangle { color: root.cardColor; radius: 18 }
                    contentItem: ColumnLayout {
                        Label { text: modelData.title; color: root.mutedColor }
                        Label { Layout.fillWidth: true; text: String(modelData.value); color: root.textColor; font.pixelSize: 22; font.bold: true; wrapMode: Text.Wrap }
                    }
                }
            }

            Label { text: qsTr("Sources"); color: root.textColor; font.bold: true; font.pixelSize: 18 }
            Repeater {
                model: root.statistics.sources || []
                delegate: Label {
                    required property var modelData
                    Layout.fillWidth: true
                    text: (modelData.source || modelData.name || qsTr("Unknown"))
                          + ": " + (modelData.total || 0)
                    wrapMode: Text.Wrap
                }
            }
        }
    }
}
