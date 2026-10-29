import QtQuick
import QtQuick.Window
Window {
    id: root
    width: 390
    height: 700
    visible: true
    color: "#14202b"
    property string results: "Testing native dependencies…"
    Text {
        anchors.centerIn: parent
        text: root.results
        color: "white"
        font.pixelSize: 22
    }
}
