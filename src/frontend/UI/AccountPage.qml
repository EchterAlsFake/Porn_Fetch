// qml/pages/AccountPage.qml

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root

    required property var backend

    property string selectedProvider:
        providerTabs.currentIndex === 0 ? "Provider A" : "Provider B"

    padding: 8

    background: Rectangle {
        border.width: 2
        radius: 10
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 6

        TabBar {
            id: providerTabs

            Layout.fillWidth: true

            TabButton {
                text: qsTr("PROVIDER A")
            }

            TabButton {
                text: qsTr("PROVIDER B")
            }
        }

        GridLayout {
            Layout.fillWidth: true

            columns: 2

            Label {
                text: qsTr("Email:")
            }

            TextField {
                id: emailField

                Layout.fillWidth: true

                inputMethodHints: Qt.ImhEmailCharactersOnly
                selectByMouse: true
            }

            Label {
                text: qsTr("Password:")
            }

            TextField {
                id: passwordField

                Layout.fillWidth: true

                echoMode: TextInput.Password
                selectByMouse: true
            }
        }

        RowLayout {
            Layout.fillWidth: true

            Button {
                Layout.fillWidth: true
                text: qsTr("GET CALLED VIDEOS")

                onClicked: {
                    // root.backend.fetch_called_videos(...)
                }
            }

            Button {
                Layout.fillWidth: true
                text: qsTr("GET RECOMMENDED VIDEOS")

                onClicked: {
                    // root.backend.fetch_recommended_videos(...)
                }
            }

            Button {
                Layout.fillWidth: true
                text: qsTr("GET LIKED VIDEOS")

                onClicked: {
                    // root.backend.fetch_liked_videos(...)
                }
            }
        }

        Button {
            Layout.fillWidth: true

            text: qsTr("LOGIN")

            enabled: emailField.text.trim().length > 0
                     && passwordField.text.length > 0
                     && !root.backend.busy

            onClicked: {
                root.backend.login(
                    root.selectedProvider,
                    emailField.text,
                    passwordField.text
                )
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Label {
                anchors.centerIn: parent

                text: qsTr("Retrieved videos will appear here")
            }
        }
    }
}