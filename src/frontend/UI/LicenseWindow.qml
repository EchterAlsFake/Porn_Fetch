import QtQuick
import QtQuick.Controls
import QtQuick.Window

Window {
    id: licenseWin
    width: 500
    height: 560
    minimumWidth: 460
    minimumHeight: 520
    title: qsTr("Manage License")

    // Use the dark background to match the widget
    color: (appSettings.high_contrast ? "#000000" : "#1f1f21")

    // Instantiate your hyper-modern widget inside this window!
    LicenseWidget {
        anchors.fill: parent
    }
}