import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    objectName: "websiteSupportContent"
    property color cardColor: "#1e293b"
    property color textColor: "#f0f2f8"
    property color mutedColor: "#aeb6c5"
    property int frontendIndex: 0
    readonly property bool compact: width < 760
    readonly property var columnWidths: [140, 75, 170, 170, 75, 75, 75, 100]

    WebsiteSupportData { id: support }

    ScrollView {
        id: scroll
        anchors.fill: parent
        contentWidth: availableWidth
        clip: true

        ColumnLayout {
            width: scroll.availableWidth
            spacing: 16

            Label {
                Layout.fillWidth: true
                text: qsTr("Supported websites and features")
                color: root.textColor
                font.bold: true
                font.pixelSize: root.compact ? 22 : 26
                wrapMode: Text.Wrap
            }
            Label {
                Layout.fillWidth: true
                text: support.notes[0]
                color: root.mutedColor
                wrapMode: Text.Wrap
            }
            ComboBox {
                objectName: "websiteFrontendSelector"
                Layout.fillWidth: root.compact
                Layout.preferredWidth: Math.min(360, scroll.availableWidth)
                model: [qsTr("GUI (desktop and Android)"), qsTr("CLI (interactive and batch)")]
                currentIndex: root.frontendIndex
                onActivated: root.frontendIndex = currentIndex
                Accessible.name: qsTr("Feature matrix frontend")
            }
            Label {
                Layout.fillWidth: true
                visible: !root.compact
                text: qsTr("Scroll horizontally to see every feature.")
                color: root.mutedColor
                wrapMode: Text.Wrap
            }

            Flickable {
                Layout.fillWidth: true
                Layout.preferredHeight: visible ? table.implicitHeight + 16 : 0
                visible: !root.compact
                clip: true
                contentWidth: table.width
                contentHeight: table.implicitHeight
                flickableDirection: Flickable.HorizontalFlick
                boundsBehavior: Flickable.StopAtBounds
                ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AsNeeded }

                Column {
                    id: table
                    width: root.columnWidths.reduce(function(total, value) { return total + value }, 0) + 7
                    spacing: 1
                    RowLayout {
                        width: table.width
                        spacing: 1
                        Repeater {
                            model: support.headers
                            delegate: Label {
                                required property int index
                                required property string modelData
                                Layout.preferredWidth: root.columnWidths[index]
                                Layout.fillHeight: true
                                padding: 10
                                text: modelData
                                color: root.textColor
                                font.bold: true
                                wrapMode: Text.Wrap
                                background: Rectangle { color: root.cardColor }
                            }
                        }
                    }
                    Repeater {
                        model: root.compact ? [] : support.sites
                        delegate: RowLayout {
                            required property var modelData
                            width: table.width
                            spacing: 1
                            Repeater {
                                model: support.rowFor(modelData, root.frontendIndex === 1)
                                delegate: Label {
                                    required property int index
                                    required property string modelData
                                    Layout.preferredWidth: root.columnWidths[index]
                                    Layout.fillHeight: true
                                    padding: 10
                                    text: modelData
                                    textFormat: Text.PlainText
                                    color: root.textColor
                                    font.bold: index === 0
                                    wrapMode: Text.Wrap
                                    background: Rectangle { color: root.cardColor }
                                }
                            }
                        }
                    }
                }
            }

            Repeater {
                model: root.compact ? support.sites : []
                delegate: Frame {
                    id: card
                    required property var modelData
                    readonly property var values: support.rowFor(modelData, root.frontendIndex === 1)
                    Layout.fillWidth: true
                    padding: 14
                    background: Rectangle { color: root.cardColor; radius: 12 }
                    contentItem: ColumnLayout {
                        Label {
                            Layout.fillWidth: true
                            text: card.modelData.name
                            color: root.textColor
                            font.bold: true
                            font.pixelSize: 19
                        }
                        Repeater {
                            model: card.values.slice(1)
                            delegate: RowLayout {
                                required property int index
                                required property string modelData
                                Layout.fillWidth: true
                                spacing: 12
                                Label {
                                    Layout.preferredWidth: 100
                                    Layout.alignment: Qt.AlignTop
                                    text: support.headers[index + 1]
                                    color: root.mutedColor
                                    wrapMode: Text.Wrap
                                }
                                Label {
                                    Layout.fillWidth: true
                                    text: modelData
                                    textFormat: Text.PlainText
                                    color: root.textColor
                                    wrapMode: Text.Wrap
                                }
                            }
                        }
                    }
                }
            }

            Repeater {
                model: support.notes.slice(1)
                delegate: Label {
                    required property string modelData
                    Layout.fillWidth: true
                    text: modelData
                    color: root.mutedColor
                    wrapMode: Text.Wrap
                }
            }
        }
    }
}
