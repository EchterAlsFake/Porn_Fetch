import QtQuick
import QtQuick.Controls

CheckBox {
    id: root
    implicitHeight: Math.max(44, contentItem.implicitHeight + 16)
    spacing: 10
    Keys.onReturnPressed: toggle()
    Keys.onEnterPressed: toggle()
    indicator: Rectangle {
        x: 4; y: (root.height - height) / 2
        width: 22; height: 22; radius: 4
        color: root.checked ? Theme.accent : Theme.surface
        border.width: root.visualFocus ? 3 : 1
        border.color: root.visualFocus ? Theme.accent : Theme.outline
        Label { anchors.centerIn: parent; text: "✓"; visible: root.checked; font.pixelSize: 17; font.bold: true; color: Theme.highContrast ? Theme.selectionInk : Theme.dark ? "#171329" : "#ffffff" }
    }
    contentItem: Label {
        text: root.text; textFormat: Text.PlainText
        leftPadding: 36; rightPadding: 4; wrapMode: Text.WordWrap
        verticalAlignment: Text.AlignVCenter; color: Theme.ink
    }
    background: Rectangle { radius: 5; color: "transparent"; border.width: root.visualFocus ? 2 : 0; border.color: Theme.accent }
}
