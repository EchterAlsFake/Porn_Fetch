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
    implicitHeight: 64
    padding: 12
    Accessible.role: Accessible.Indicator
    Accessible.name: qsTr("Processing videos")

    background: Rectangle {
        radius: 12
        color: Qt.rgba(control.accentColor.r, control.accentColor.g,
                       control.accentColor.b, 0.09)
        border.color: Qt.rgba(control.accentColor.r, control.accentColor.g,
                              control.accentColor.b, 0.25)
    }

    RowLayout {
        anchors.fill: parent
        spacing: 14

        Item {
            Layout.preferredWidth: 52
            Layout.preferredHeight: 34

            Repeater {
                model: 5

                Rectangle {
                    id: bar
                    required property int index
                    x: index * 11
                    anchors.verticalCenter: parent.verticalCenter
                    width: 6
                    height: 10
                    radius: 3
                    color: control.accentColor
                    opacity: 0.5 + height / 64

                    SequentialAnimation on height {
                        running: control.running && control.visible
                        loops: Animation.Infinite
                        PauseAnimation { duration: bar.index * 90 }
                        NumberAnimation {
                            to: 32
                            duration: 360
                            easing.type: Easing.InOutSine
                        }
                        NumberAnimation {
                            to: 10
                            duration: 360
                            easing.type: Easing.InOutSine
                        }
                        PauseAnimation { duration: (4 - bar.index) * 90 }
                    }
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
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
}
