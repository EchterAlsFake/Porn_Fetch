import QtQuick
import QtQuick.Controls

Pane {
    id: root
    padding: 12
    background: Rectangle { color: appSettings.dark_mode ? "#101319" : "#f7f8fc" }

    WebsiteSupportContent {
        anchors.fill: parent
        cardColor: appSettings.dark_mode ? "#1b202a" : "#ffffff"
        textColor: appSettings.dark_mode ? "#f0f2f8" : "#202431"
        mutedColor: appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    }
}
