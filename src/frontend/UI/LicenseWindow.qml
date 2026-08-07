import QtQuick
import QtQuick.Controls
import QtQuick.Window

Window {
    id: licenseWin
    width: 500
    height: 480
    minimumWidth: 460
    minimumHeight: 450
    title: qsTr("Manage License")

    // Use the dark background to match the widget
    color: "#1f1f21"

    // Instantiate your hyper-modern widget inside this window!
    LicenseWidget {
        anchors.fill: parent
    }
}