// qml/Main.qml

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Universal
import "pages"

ApplicationWindow {
    id: window
    required property var backend

    width: 1350
    height: 720
    minimumWidth: 900
    minimumHeight: 600

    visible: true
    title: qsTr("Video Downloader")

    color: "#172023"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 6

        TabBar {
            id: navigation

            Layout.fillWidth: true

            TabButton {
                icon.source: "qrc:/images/graphics/download.svg"
                icon.width: 24
                icon.height: 24
                icon.color: "transparent"
                display: AbstractButton.IconOnly
            }

            TabButton {
                icon.source: "qrc:/images/graphics/account.svg"
                icon.width: 24
                icon.height: 24
                icon.color: "transparent"
                display: AbstractButton.IconOnly
            }

            TabButton {
                icon.source: "qrc:/images/graphics/settings.svg"
                icon.width: 24
                icon.height: 24
                icon.color: "transparent"
                display: AbstractButton.IconOnly
            }

            TabButton {
                icon.source: "qrc:/images/graphics/information.svg"
                icon.width: 24
                icon.height: 24
                icon.color: "transparent"
                display: AbstractButton.IconOnly
            }

            TabButton {
                text: qsTr("SUPPORTED WEBSITES")
            }
        }

        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true

            currentIndex: navigation.currentIndex

            DownloadsPage {
                backend: window.backend
            }

            AccountPage {
                backend: window.backend
            }

            SettingsPage {
                // Pass a settings controller here when necessary.
            }

            InfoPage {
            }

            SupportedWebsitesPage {
            }
        }
    }
}