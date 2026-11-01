import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt5Compat.GraphicalEffects 1.0

Rectangle {
    id: root
    width: 800
    height: 600
    color: "transparent"

    // Background Gradient
    LinearGradient {
        anchors.fill: parent
        start: Qt.point(0, 0)
        end: Qt.point(width, height)
        gradient: Gradient {
            GradientStop { position: 0.0; color: (appSettings.high_contrast ? "#000000" : "#1a1a2e") }
            GradientStop { position: 1.0; color: (appSettings.high_contrast ? "#000000" : "#16213e") }
        }
    }

    Flickable {
        id: infoFlickable
        anchors.fill: parent
        contentWidth: width
        contentHeight: contentColumn.height + 60
        clip: true
        boundsBehavior: Flickable.StopAtBounds

        SmoothWheelHandler {
            id: infoWheelHandler
            flickable: infoFlickable
        }

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AsNeeded
            active: size < 1.0 || hovered || pressed
                    || infoWheelHandler.scrolling
        }

        ColumnLayout {
            id: contentColumn
            width: infoFlickable.width - 40
            x: 20
            y: 30
            spacing: 25

            Button {
                text: qsTr("Help translate")
                Layout.fillWidth: true
                implicitHeight: Math.max(48, contentItem.implicitHeight + topPadding + bottomPadding)
                onClicked: Qt.openUrlExternally(appSettings.translation_help_url)
            }
            // Header Section
            Item {
                Layout.fillWidth: true
                implicitHeight: Math.max(140, headerColumn.implicitHeight + 40)
                
                Rectangle {
                    anchors.fill: parent
                    radius: 16
                    color: (appSettings.high_contrast ? "#000000" : "#2a2a4a")
                    opacity: 0.8
                    border.color: (appSettings.high_contrast ? "#ffffff" : "#3a3a6a")
                    border.width: 1
                }

                Column {
                    id: headerColumn
                    anchors.centerIn: parent
                    width: parent.width - 40
                    spacing: 8
                    
                    Text {
                        text: qsTr("Porn Fetch")
                        font.pixelSize: 36 * appSettings.font_size / 12
                        font.bold: true
                        font.family: "Inter, sans-serif"
                        color: (appSettings.high_contrast ? "#ffffff" : "#ffffff")
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                    }
                    
                    Text {
                        text: qsTr("Version %1").arg(Qt.application.version)
                        font.pixelSize: 18 * appSettings.font_size / 12
                        font.family: "Inter, sans-serif"
                        color: (appSettings.high_contrast ? "#ffffff" : "#00f2fe")
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                    }
                    
                    Text {
                        text: qsTr("Copyright © 2023-2026 Johannes Habel (EchterAlsFake)")
                        font.pixelSize: 14 * appSettings.font_size / 12
                        font.family: "Inter, sans-serif"
                        color: (appSettings.high_contrast ? "#ffffff" : "#a0a0c0")
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                    }
                }
            }

            // Notice Card
            CreditCard {
                title: qsTr("Special Notice")
                icon: "⭐"
                content: qsTr("This project was only possible because Egsagon made the PHUB API that interacts with PornHub and which Porn Fetch uses. Although I now have ownership, without him, this project wouldn't be possible in the first place.")
            }

            CreditCard {
                title: qsTr("Application License")
                icon: "📄"
                content: qsTr("Porn Fetch Source-Available License 1.0. You may inspect and modify the code and share builds privately. Public forks must keep premium licensing operational. Older GPL copies keep their GPL rights. See the full license below.")
            }

            Button {
                text: qsTr("Show application license")
                onClicked: {
                    legalDialog.showNotices = false
                    legalDialog.open()
                }
            }

            Button {
                text: qsTr("Show third-party notices")
                onClicked: {
                    legalDialog.showNotices = true
                    legalDialog.open()
                }
            }

            // Development Card
            CreditCard {
                title: qsTr("Development Stack")
                icon: "💻"
                content: qsTr("Language: Python\nIDE: JetBrains PyCharm Professional\nPlatform: GitHub\nGUI: PySide6\n\nThanks to Qt for the Python GUI toolkit used by this project. Qt components have their own license terms.")
            }

            // Contributors Card
            CreditCard {
                title: qsTr("Amazing Contributors")
                icon: "👥"
                content: qsTr("Egsagon (PHUB API & French)\nRSDCFGVHBJNKML\nJoshua-auhsoj (Chinese 3.0)\nRonLar1132\nxxIndirect\nefraxs\nomar-st\nSShattered\njourneym\nJoly0\nFatalPuppet (Italian)\nHeathenSkwerl")
            }

            // Third-party components
            CreditCard {
                title: qsTr("Third-party components")
                icon: "📚"
                content: qsTr("Porn Fetch uses independently licensed provider APIs, PySide6/Qt, PocketBase, and Python packages. Use the third-party notices button for the current inventory and license information.")
            }

            // Other Tech
            GridLayout {
                Layout.fillWidth: true
                columns: width < 700 ? 1 : 2
                columnSpacing: 20
                rowSpacing: 20
                
                CreditCard {
                    Layout.preferredWidth: 1
                    title: qsTr("Android")
                    icon: "📱"
                    content: qsTr("Buildozer\nCython\nChaquopy")
                }

                CreditCard {
                    Layout.preferredWidth: 1
                    title: qsTr("Applications")
                    icon: "⚙️"
                    content: qsTr("FFMPEG (via pyav)\n\nUsed for processing\nmedia streams.")
                }

                CreditCard {
                    Layout.preferredWidth: 1
                    title: qsTr("macOS Build")
                    icon: "🍎"
                    content: qsTr("OneClick-macOS-Simple-KVM\n\nMakes macOS builds possible.")
                }

                CreditCard {
                    Layout.preferredWidth: 1
                    title: qsTr("iOS Testing")
                    icon: "📱"
                    content: qsTr("palera1n\nKitty-XZ\n\nJailbreak testing.")
                }
            }
        }
    }

    Dialog {
        id: legalDialog
        property bool showNotices: false
        title: showNotices ? "Third-party notices" : "Porn Fetch application license"
        modal: true
        anchors.centerIn: parent
        width: Math.min(root.width - 40, 720)
        height: Math.min(root.height - 40, 520)
        standardButtons: Dialog.Close

        contentItem: ScrollView {
            TextArea {
                readOnly: true
                selectByMouse: true
                wrapMode: TextArea.Wrap
                text: legalDialog.showNotices ? thirdPartyNoticesText : applicationLicenseText
            }
        }
    }

    component CreditCard: Rectangle {
        id: card
        objectName: "creditCard"
        property string title: ""
        property string content: qsTr("")
        property string icon: ""

        Layout.fillWidth: true
        Layout.minimumWidth: 0
        Layout.alignment: Qt.AlignTop
        implicitWidth: 320
        implicitHeight: cardColumn.implicitHeight + 40
        radius: 12
        color: (appSettings.high_contrast ? "#000000" : "#252545")
        opacity: 0.9
        border.color: (appSettings.high_contrast ? "#ffffff" : "#3a3a6a")
        border.width: 1

        ColumnLayout {
            id: cardColumn
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 20
            spacing: 10

            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Text {
                    text: card.icon
                    font.pixelSize: 24 * appSettings.font_size / 12
                }

                Text {
                    Layout.fillWidth: true
                    Layout.minimumWidth: 0
                    text: card.title
                    font.pixelSize: 20 * appSettings.font_size / 12
                    font.bold: true
                    font.family: "Inter, sans-serif"
                    color: (appSettings.high_contrast ? "#ffffff" : "#ffffff")
                    wrapMode: Text.Wrap
                }
            }

            Rectangle {
                Layout.fillWidth: true
                implicitHeight: 1
                color: (appSettings.high_contrast ? "#000000" : "#3a3a6a")
            }

            Text {
                Layout.fillWidth: true
                Layout.minimumWidth: 0
                text: card.content
                font.pixelSize: 14 * appSettings.font_size / 12
                font.family: "Inter, sans-serif"
                color: (appSettings.high_contrast ? "#ffffff" : "#c0c0d0")
                textFormat: Text.PlainText
                wrapMode: Text.Wrap
                lineHeight: 1.4
            }
        }
    }
}
