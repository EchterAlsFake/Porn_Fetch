import QtQuick
import QtQuick.Controls
import QtQuick.Window

Window {
    id: licenseWin
    width: 500
    height: 560
    minimumWidth: 320
    minimumHeight: 240
    title: qsTr("Manage License")

    color: appSettings.high_contrast ? Theme.background : appSettings.dark_mode ? "#1f1f21" : "#f5f6f8"

    ScrollView {
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth
        LicenseWidget {
            width: parent.width
            height: implicitHeight
        }
    }
}