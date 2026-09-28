import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    padding: 8
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
                    contentItem: ColumnLayout {
                        Label { text: modelData.title; font.bold: true }
                        Label { Layout.fillWidth: true; text: String(modelData.value); wrapMode: Text.Wrap }
                    }
                }
            }

            Label { text: qsTr("Sources"); font.bold: true }
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
