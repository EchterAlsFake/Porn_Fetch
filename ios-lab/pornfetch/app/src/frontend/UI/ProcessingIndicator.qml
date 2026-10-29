pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Pane {
    id: control
    property bool running: false
    readonly property color accentColor: appSettings.core_style === "Material"
                                         ? Material.accent : palette.highlight
    visible: running
    implicitHeight: 56
    padding: 10
    Accessible.role: Accessible.Indicator
    Accessible.name: qsTr("Processing videos")

    background: Rectangle {
        radius: 12
        color: Qt.rgba(control.accentColor.r, control.accentColor.g,
                       control.accentColor.b, 0.09)
        border.color: Qt.rgba(control.accentColor.r, control.accentColor.g,
                              control.accentColor.b, 0.25)
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 2

        Label {
            Layout.fillWidth: true
            text: qsTr("Processing videos")
            font.bold: true
            elide: Text.ElideRight
        }
        Label {
            Layout.fillWidth: true
            text: qsTr("Preparing your download list…")
            opacity: 0.7
            elide: Text.ElideRight
        }
    }
}
