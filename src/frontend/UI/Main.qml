// qml/Main.qml

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    font.pointSize: appSettings.font_size

    width: 1350
    height: 720
    minimumWidth: 900
    minimumHeight: 600

    visible: true
    title: qsTr("Video Downloader")
    property bool safeToClose: false
    onClosing: (closeEvent) => {
        if (!safeToClose) {
            closeEvent.accepted = false
            backend.initiate_shutdown()
        }
    }

    Connections {
        target: backend
        function onShutdown_complete() {
            window.safeToClose = true
            window.close()
        }
    }

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
                icon.source: "qrc:/images/graphics/database.svg"
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
            }

            AccountPage {
            }

            StatisticsPage {
            }

            SettingsPage {
                // Pass a settings controller here when necessary.
            }

            Item {
                InfoPage {
                    anchors.fill: parent
                    visible: !appSettings.anonymous_mode
                }

                Label {
                    anchors.centerIn: parent
                    text: qsTr("Widget is hidden due to your privacy settings...")
                    font.pixelSize: appSettings.font_size
                    visible: appSettings.anonymous_mode
                }

            }


            Item {
                SupportedWebsitesPage {
                    anchors.fill: parent
                    visible: !appSettings.anonymous_mode
                }

                Label {
                    anchors.centerIn: parent
                    text: qsTr("Widget is hidden due to your privacy settings...")
                    font.pixelSize: appSettings.font_size
                    visible: appSettings.anonymous_mode
                }

            }

        }
    }
}
