import QtQuick

Rectangle {
    objectName: "contrastControlOutline"
    required property var control
    parent: control ? control.background : null
    anchors.fill: parent
    visible: Theme.highContrast
    color: "transparent"
    radius: 4
    border.width: control && control.activeFocus ? 3 : 2
    border.color: !control || !control.enabled ? Theme.disabledInk : control.activeFocus ? Theme.accent : Theme.outline
}
