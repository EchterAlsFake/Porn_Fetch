import QtQuick
import QtQuick.Window

Window {
    width: 390
    height: 700
    visible: true
    title: "Python on iOS"
    color: "#14202b"
    Text {
        anchors.centerIn: parent
        text: "Hello World!\nPython + PySide6 + QML"
        color: "white"
        font.pixelSize: 24
        horizontalAlignment: Text.AlignHCenter
    }
}
