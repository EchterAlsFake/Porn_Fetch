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
            GradientStop { position: 0.0; color: "#0f2027" }
            GradientStop { position: 0.5; color: "#203a43" }
            GradientStop { position: 1.0; color: "#2c5364" }
        }
    }

    ListModel {
        id: sitesModel
        ListElement { category: "Videos"; sites: "PornHub, HQporner, Eporner, xnxx, xvideos, missav, Xhamster, Spankbang, YouPorn"; icon: "🎬" }
        ListElement { category: "Searching"; sites: "PornHub, HQporner, Eporner, xnxx, xvideos, missav, Xhamster, Spankbang"; icon: "🔍" }
        ListElement { category: "Models / Pornstars / Creators"; sites: "PornHub, HQporner, xnxx, Xhamster, Spankbang"; icon: "💃" }
        ListElement { category: "Pornstars"; sites: "PornHub, Eporner, xvideos, Xhamster, Spankbang"; icon: "⭐" }
        ListElement { category: "Channels"; sites: "PornHub, Xhamster, Spankbang"; icon: "📺" }
        ListElement { category: "Playlists"; sites: "PornHub, xvideos, youporn"; icon: "📑" }
        ListElement { category: "Shorts"; sites: "Xhamster"; icon: "📱" }
        ListElement { category: "Account Login"; sites: "PornHub, XVideos"; icon: "🔑" }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        // Header
        Rectangle {
            Layout.fillWidth: true
            height: 80
            radius: 16
            color: "#1a1a2e"
            opacity: 0.85
            border.color: "#4a4a8a"
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15

                Text {
                    text: "🌐"
                    font.pixelSize: 32
                }

                Column {
                    Layout.fillWidth: true
                    Text {
                        text: "Supported Websites & Features"
                        font.pixelSize: 24
                        font.bold: true
                        font.family: "Inter, sans-serif"
                        color: "#ffffff"
                    }
                    Text {
                        text: "A comprehensive list of supported platforms and their capabilities."
                        font.pixelSize: 14
                        font.family: "Inter, sans-serif"
                        color: "#4facfe"
                    }
                }
            }
        }

        // Grid View of Categories
        GridView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            cellWidth: parent.width / 2
            cellHeight: 120
            model: sitesModel
            boundsBehavior: Flickable.StopAtBounds

            delegate: Item {
                width: GridView.view.cellWidth
                height: GridView.view.cellHeight

                Rectangle {
                    anchors.fill: parent
                    anchors.margins: 8
                    radius: 12
                    color: "#1e293b"
                    opacity: 0.8
                    border.color: "#334155"
                    border.width: 1

                    // Hover effect
                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                    }

                    states: State {
                        name: "hovered"
                        when: mouseArea.containsMouse
                        PropertyChanges { target: delegateBackground; color: "#2d3748"; border.color: "#4fd1c5" }
                    }

                    transitions: Transition {
                        ColorAnimation { duration: 200 }
                    }

                    id: delegateBackground

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 15
                        spacing: 5

                        RowLayout {
                            spacing: 8
                            Text {
                                text: model.icon
                                font.pixelSize: 18
                            }
                            Text {
                                Layout.fillWidth: true
                                text: model.category
                                font.pixelSize: 16
                                font.bold: true
                                font.family: "Inter, sans-serif"
                                color: "#ffffff"
                            }
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            height: 1
                            color: "#334155"
                        }

                        Text {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            text: model.sites
                            font.pixelSize: 13
                            font.family: "Inter, sans-serif"
                            color: "#cbd5e1"
                            wrapMode: Text.WordWrap
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
            }
        }
    }
}
