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
            GradientStop { position: 0.0; color: "#1a1a2e" }
            GradientStop { position: 1.0; color: "#16213e" }
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

            // Header Section
            Item {
                Layout.fillWidth: true
                implicitHeight: Math.max(140, headerColumn.implicitHeight + 40)
                
                Rectangle {
                    anchors.fill: parent
                    radius: 16
                    color: "#2a2a4a"
                    opacity: 0.8
                    border.color: "#3a3a6a"
                    border.width: 1
                }

                Column {
                    id: headerColumn
                    anchors.centerIn: parent
                    width: parent.width - 40
                    spacing: 8
                    
                    Text {
                        text: "Porn Fetch"
                        font.pixelSize: 36
                        font.bold: true
                        font.family: "Inter, sans-serif"
                        color: "#ffffff"
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                    }
                    
                    Text {
                        text: "Version " + Qt.application.version
                        font.pixelSize: 18
                        font.family: "Inter, sans-serif"
                        color: "#00f2fe"
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                    }
                    
                    Text {
                        text: "Copyright © 2023-2026 Johannes Habel (EchterAlsFake)"
                        font.pixelSize: 14
                        font.family: "Inter, sans-serif"
                        color: "#a0a0c0"
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                    }
                }
            }

            // Notice Card
            CreditCard {
                title: "Special Notice"
                icon: "⭐"
                content: "This project was only possible because Egsagon made the PHUB API that interacts with PornHub and which Porn Fetch uses. Although I now have ownership, without him, this project wouldn't be possible in the first place."
            }

            CreditCard {
                title: "Application License"
                icon: "📄"
                content: "Porn Fetch Source-Available License 1.0. You may inspect and modify the code and share builds privately. Public forks must keep premium licensing operational. Older GPL copies keep their GPL rights. See the full license below."
            }

            Button {
                text: "Show application license"
                onClicked: {
                    legalDialog.showNotices = false
                    legalDialog.open()
                }
            }

            Button {
                text: "Show third-party notices"
                onClicked: {
                    legalDialog.showNotices = true
                    legalDialog.open()
                }
            }

            // Development Card
            CreditCard {
                title: "Development Stack"
                icon: "💻"
                content: "Language: Python\nIDE: JetBrains PyCharm Professional\nPlatform: GitHub\nGUI: PySide6\n\nThanks to Qt for the Python GUI toolkit used by this project. Qt components have their own license terms."
            }

            // Contributors Card
            CreditCard {
                title: "Amazing Contributors"
                icon: "👥"
                content: "Egsagon (PHUB API & French)\nRSDCFGVHBJNKML\nJoshua-auhsoj (Chinese 3.0)\nRonLar1132\nxxIndirect\nefraxs\nomar-st\nSShattered\njourneym\nJoly0\nFatalPuppet (Italian)\nHeathenSkwerl"
            }

            // Third-party components
            CreditCard {
                title: "Third-party components"
                icon: "📚"
                content: "Porn Fetch uses independently licensed provider APIs, PySide6/Qt, PocketBase, and Python packages. Use the third-party notices button for the current inventory and license information."
            }

            // Other Tech
            GridLayout {
                Layout.fillWidth: true
                columns: width < 700 ? 1 : 2
                columnSpacing: 20
                rowSpacing: 20
                
                CreditCard {
                    Layout.preferredWidth: 1
                    title: "Android"
                    icon: "📱"
                    content: "Buildozer\nCython\nChaquopy"
                }

                CreditCard {
                    Layout.preferredWidth: 1
                    title: "Applications"
                    icon: "⚙️"
                    content: "FFMPEG (via pyav)\n\nUsed for processing\nmedia streams."
                }

                CreditCard {
                    Layout.preferredWidth: 1
                    title: "macOS Build"
                    icon: "🍎"
                    content: "OneClick-macOS-Simple-KVM\n\nMakes macOS builds possible."
                }

                CreditCard {
                    Layout.preferredWidth: 1
                    title: "iOS Testing"
                    icon: "📱"
                    content: "palera1n\nKitty-XZ\n\nJailbreak testing."
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
        property string content: ""
        property string icon: ""

        Layout.fillWidth: true
        Layout.minimumWidth: 0
        Layout.alignment: Qt.AlignTop
        implicitWidth: 320
        implicitHeight: cardColumn.implicitHeight + 40
        radius: 12
        color: "#252545"
        opacity: 0.9
        border.color: "#3a3a6a"
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
                    font.pixelSize: 24
                }

                Text {
                    Layout.fillWidth: true
                    Layout.minimumWidth: 0
                    text: card.title
                    font.pixelSize: 20
                    font.bold: true
                    font.family: "Inter, sans-serif"
                    color: "#ffffff"
                    wrapMode: Text.Wrap
                }
            }

            Rectangle {
                Layout.fillWidth: true
                implicitHeight: 1
                color: "#3a3a6a"
            }

            Text {
                Layout.fillWidth: true
                Layout.minimumWidth: 0
                text: card.content
                font.pixelSize: 14
                font.family: "Inter, sans-serif"
                color: "#c0c0d0"
                textFormat: Text.PlainText
                wrapMode: Text.Wrap
                lineHeight: 1.4
            }
        }
    }
}
