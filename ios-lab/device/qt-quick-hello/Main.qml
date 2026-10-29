import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 375
    height: 667
    title: "Qt Quick on iPhone 7"
    Material.theme: Material.Dark
    Material.accent: Material.Teal
    property int taps: 0
    ColumnLayout {
        anchors.centerIn: parent
        width: parent.width - 48
        spacing: 20
        Label {
            text: "Hello Qt Quick!"
            font.pixelSize: 28
            Layout.alignment: Qt.AlignHCenter
        }
        Label {
            text: "Qt " + Qt.application.version + " on iOS 15\nRunning on your iPhone 7."
            horizontalAlignment: Text.AlignHCenter
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
        }
        Button {
            text: "Tapped " + taps + " times"
            Layout.alignment: Qt.AlignHCenter
            onClicked: taps++
        }
    }
}
