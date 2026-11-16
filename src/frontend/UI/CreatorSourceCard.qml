import QtQuick
import "CreatorFocus.js" as CreatorFocus
import QtQuick.Controls
import QtQuick.Layouts

ItemDelegate {
    id: root
    readonly property real fontScale: typeof appSettings !== "undefined" && appSettings ? Math.max(1, appSettings.font_size / 12) : 1
    required property var sourceData
    required property var counts
    property bool privateMode: false
    readonly property color tint: Theme.highContrast ? Theme.accent : sourceData.provider === "Bellesa" ? (Theme.dark ? "#b5a6ff" : "#6752ba") : Theme.accent
    padding: 20
    implicitHeight: cardContent.implicitHeight + 40
    hoverEnabled: true
    Accessible.name: (privateMode ? qsTr("Subscription") : sourceData.name) + ", " + state.label
    Keys.onDownPressed: CreatorFocus.move(root, true)
    Keys.onUpPressed: CreatorFocus.move(root, false)
    Keys.onRightPressed: CreatorFocus.move(root, true)
    Keys.onLeftPressed: CreatorFocus.move(root, false)
    Keys.onReturnPressed: clicked()
    Keys.onEnterPressed: clicked()
    background: Rectangle {
        radius: 12
        color: root.hovered || root.highlighted ? Qt.tint(Theme.surface, Qt.rgba(root.tint.r, root.tint.g, root.tint.b, 0.07)) : Theme.surface
        border.width: root.visualFocus ? 3 : 1
        border.color: root.visualFocus ? Theme.accent : Qt.rgba(Theme.outline.r, Theme.outline.g, Theme.outline.b, Theme.highContrast ? 1 : 0.4)
    }
    contentItem: ColumnLayout {
        id: cardContent
        spacing: 16
        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            Rectangle {
                Layout.preferredWidth: 44; Layout.preferredHeight: 44; radius: 12
                color: Qt.rgba(root.tint.r, root.tint.g, root.tint.b, 0.13)
                Label { anchors.centerIn: parent; text: root.privateMode ? "•" : root.sourceData.initials; color: root.tint; font.pixelSize: 17 * root.fontScale; font.bold: true }
            }
            ColumnLayout {
                Layout.fillWidth: true; spacing: 3
                Label { Layout.fillWidth: true; text: root.privateMode ? qsTr("Hidden subscription") : root.sourceData.name; textFormat: Text.PlainText; color: Theme.ink; font.pixelSize: 18 * root.fontScale; font.bold: true; elide: Text.ElideRight }
                Label { Layout.fillWidth: true; text: root.sourceData.provider + " · " + root.sourceData.kind; color: Theme.muted; font.pixelSize: 12 * root.fontScale; elide: Text.ElideRight }
            }
            Label { text: "›"; font.pixelSize: 26 * root.fontScale; color: Theme.muted }
        }
        RowLayout {
            Layout.fillWidth: true
            CreatorStatus { id: state; status: root.sourceData.scan }
            Item { Layout.fillWidth: true }
            Label { text: qsTr("%1 videos").arg(root.counts.total); color: Theme.muted; font.pixelSize: 12 * root.fontScale }
        }
        ProgressBar {
            Layout.fillWidth: true; from: 0; to: Math.max(1, root.counts.total); value: root.counts.completed
            Accessible.name: qsTr("%1 of %2 downloaded").arg(root.counts.completed).arg(root.counts.total)
        }
        RowLayout {
            Layout.fillWidth: true
            Label { text: qsTr("%1 downloaded").arg(root.counts.completed); color: Theme.muted; font.pixelSize: 12 * root.fontScale }
            Item { Layout.fillWidth: true }
            Label { text: qsTr("%1 new").arg(root.counts.newCount); color: root.counts.newCount ? root.tint : Theme.muted; font.pixelSize: 12 * root.fontScale; font.bold: root.counts.newCount > 0 }
        }
        Rectangle { Layout.fillWidth: true; implicitHeight: 1; color: Theme.outline; opacity: Theme.highContrast ? 1 : 0.25 }
        Label {
            Layout.fillWidth: true; color: Theme.muted; font.pixelSize: 12 * root.fontScale; elide: Text.ElideRight
            text: root.sourceData.scan === "scanning" ? qsTr("Scanning · %1 videos found").arg(root.sourceData.scan_discovered || 0) + (root.sourceData.scan_pages > 0 ? qsTr(" · %1 pages reached").arg(root.sourceData.scan_pages) : "")
                : root.sourceData.scan === "incomplete" ? qsTr("Some pages could not be reached")
                : root.sourceData.automatic ? qsTr("Auto-download new videos is on") : qsTr("Last scan: %1").arg(root.sourceData.lastScan)
        }
    }
}
