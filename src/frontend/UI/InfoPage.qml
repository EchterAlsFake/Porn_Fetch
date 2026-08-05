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
        anchors.fill: parent
        contentWidth: width
        contentHeight: contentColumn.height + 60
        clip: true
        boundsBehavior: Flickable.StopAtBounds

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
                        text: "Version 3.8"
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

            // Development Card
            CreditCard {
                title: "Development Stack"
                icon: "💻"
                content: "Language: Python\nIDE: JetBrains PyCharm Professional\nPlatform: GitHub\nGUI: PySide6\n\nHUGE Thanks to Qt for giving us, Open-Source devs, a way to work with such a beautiful high-level frontend AND backend development toolkit for free."
            }

            // Contributors Card
            CreditCard {
                title: "Amazing Contributors"
                icon: "👥"
                content: "Egsagon (PHUB API & French)\nRSDCFGVHBJNKML\nJoshua-auhsoj (Chinese 3.0)\nRonLar1132\nxxIndirect\nefraxs\nomar-st\nSShattered\njourneym\nJoly0\nFatalPuppet (Italian)\nHeathenSkwerl"
            }

            // Open Source Libraries
            CreditCard {
                title: "Open Source Libraries"
                icon: "📚"
                content: "PHUB, requests, hqporner_api, hue_shift, PySide6, colorama, markdown, rich, tqdm, EPorner API, XNXX API, XVideos_API, eaf_base_api, pypresence, spankbang_api, ffmpeg-progress-yield, Mutagen, xhamster_api, missav_api, httpx, pywin32, pyav, porntrex_api, porngo_api, python-dateutil."
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
