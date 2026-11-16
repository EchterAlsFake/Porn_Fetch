import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    readonly property real fontScale: typeof appSettings !== "undefined" && appSettings ? Math.max(1, appSettings.font_size / 12) : 1
    property string status: "complete"
    readonly property color tone: Theme.highContrast ? Theme.ink
        : ["failed", "incomplete"].indexOf(status) >= 0 ? (Theme.dark ? "#ffba85" : "#8a3c00")
        : ["complete", "completed"].indexOf(status) >= 0 ? (Theme.dark ? "#8cdeb5" : "#16633f")
        : Theme.accent
    readonly property string label: ({complete: qsTr("Up to date"), preview: qsTr("Five-video preview"), scanning: qsTr("Scanning"), incomplete: qsTr("Scan incomplete"), stopped: qsTr("Scan stopped"),
        new: qsTr("New"), pending: qsTr("Queued"), downloading: qsTr("Downloading"), paused: qsTr("Paused"), failed: qsTr("Needs attention"), completed: qsTr("Downloaded"), ignored: qsTr("Ignored")})[status] || status
    implicitWidth: badge.implicitWidth + 20
    implicitHeight: badge.implicitHeight + 10
    radius: 5
    color: Theme.highContrast ? Theme.background : Qt.rgba(tone.r, tone.g, tone.b, 0.10)
    border.width: Theme.highContrast ? 1 : 0
    border.color: tone
    Label { id: badge; anchors.centerIn: parent; text: root.label; color: root.tone; font.pixelSize: 12 * root.fontScale; font.weight: Font.DemiBold }
}
