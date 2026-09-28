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

        Column {
            id: contentColumn
            width: parent.width - 40
            anchors.horizontalCenter: parent.horizontalCenter
            y: 30
            spacing: 25

            // Header Section
            Item {
                width: parent.width
                height: 140
                
                Rectangle {
                    anchors.fill: parent
                    radius: 16
                    color: "#2a2a4a"
                    opacity: 0.8
                    border.color: "#3a3a6a"
                    border.width: 1
                }

                Column {
                    anchors.centerIn: parent
                    spacing: 8
                    
                    Text {
                        text: "Porn Fetch"
                        font.pixelSize: 36
                        font.bold: true
                        font.family: "Inter, sans-serif"
                        color: "#ffffff"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    
                    Text {
                        text: "Version " + Qt.application.version
                        font.pixelSize: 18
                        font.family: "Inter, sans-serif"
                        color: "#00f2fe"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    
                    Text {
                        text: "Copyright © 2023-2026 Johannes Habel (EchterAlsFake)"
                        font.pixelSize: 14
                        font.family: "Inter, sans-serif"
                        color: "#a0a0c0"
                        anchors.horizontalCenter: parent.horizontalCenter
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
                content: "Porn Fetch uses independently licensed provider APIs, PySide6/Qt, PocketBase, Sparkle on macOS, and Python packages. Use the third-party notices button for the current inventory and license information."
            }

            // Other Tech
            RowLayout {
                width: parent.width
                spacing: 20
                
                CreditCard {
                    Layout.fillWidth: true
                    title: "Android"
                    icon: "📱"
                    content: "Buildozer\nCython\nChaquopy"
                }

                CreditCard {
                    Layout.fillWidth: true
                    title: "Applications"
                    icon: "⚙️"
                    content: "FFMPEG (via pyav)\n\nUsed for processing\nmedia streams."
                }
            }
            
            RowLayout {
                width: parent.width
                spacing: 20
                
                CreditCard {
                    Layout.fillWidth: true
                    title: "macOS Build"
                    icon: "🍎"
                    content: "OneClick-macOS-Simple-KVM\n\nMakes macOS builds possible."
                }

                CreditCard {
                    Layout.fillWidth: true
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

    // Custom Component for Cards
    component CreditCard: Rectangle {
        property string title: ""
        property string content: ""
        property string icon: ""
        
        width: parent ? parent.width : 0
        height: cardColumn.height + 40
        radius: 12
        color: "#252545"
        opacity: 0.9
        border.color: "#3a3a6a"
        border.width: 1

        Column {
            id: cardColumn
            width: parent.width - 40
            anchors.centerIn: parent
            spacing: 10

            RowLayout {
                width: parent.width
                spacing: 10
                
                Text {
                    text: parent.parent.parent.icon
                    font.pixelSize: 24
                }
                
                Text {
                    text: parent.parent.parent.title
                    font.pixelSize: 20
                    font.bold: true
                    font.family: "Inter, sans-serif"
                    color: "#ffffff"
                    Layout.fillWidth: true
                }
            }
            
            Rectangle {
                width: parent.width
                height: 1
                color: "#3a3a6a"
            }

            Text {
                width: parent.width
                text: parent.parent.content
                font.pixelSize: 14
                font.family: "Inter, sans-serif"
                color: "#c0c0d0"
                wrapMode: Text.WordWrap
                lineHeight: 1.4
            }
        }
    }
}
