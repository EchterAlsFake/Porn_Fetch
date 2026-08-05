// qml/pages/DownloadsPage.qml

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root

    required property var backend

    padding: 0

    background: Rectangle {
        border.width: 2
        radius: 10
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 5

        // ------------------------------------------
        // URL input area
        // ------------------------------------------

        GridLayout {
            Layout.fillWidth: true

            columns: 3
            columnSpacing: 4
            rowSpacing: 5

            Label {
                text: qsTr("Video URL:")
            }

            TextField {
                id: videoUrlField

                Layout.fillWidth: true

                placeholderText: qsTr("Enter a video URL")
                selectByMouse: true

                onAccepted: {
                    root.backend.fetch_video(text)
                }
            }

            Button {
                text: qsTr("FETCH VIDEOS")

                enabled: videoUrlField.text.trim().length > 0
                         && !root.backend.busy

                onClicked: {
                    root.backend.fetch_video(videoUrlField.text)
                }
            }

            Label {
                text: qsTr("Playlist URL:")
            }

            TextField {
                id: playlistUrlField

                Layout.fillWidth: true

                placeholderText: qsTr("Enter a playlist URL")
                selectByMouse: true

                onAccepted: {
                    root.backend.fetch_playlist(text)
                }
            }

            Button {
                text: qsTr("FETCH VIDEOS")

                enabled: playlistUrlField.text.trim().length > 0
                         && !root.backend.busy

                onClicked: {
                    root.backend.fetch_playlist(playlistUrlField.text)
                }
            }

            Label {
                text: qsTr("Model URL:")
            }

            TextField {
                id: modelUrlField

                Layout.fillWidth: true

                placeholderText: qsTr("Enter a model or channel URL")
                selectByMouse: true

                onAccepted: {
                    root.backend.fetch_model(text)
                }
            }

            Button {
                text: qsTr("FETCH VIDEOS")

                enabled: modelUrlField.text.trim().length > 0
                         && !root.backend.busy

                onClicked: {
                    root.backend.fetch_model(modelUrlField.text)
                }
            }
        }

        // ------------------------------------------
        // Sub-page controls
        // ------------------------------------------

        RowLayout {
            Layout.fillWidth: true
            spacing: 2

            Button {
                Layout.fillWidth: true

                text: qsTr("DOWNLOADS")
                highlighted: contentStack.currentIndex === 0

                onClicked: {
                    contentStack.currentIndex = 0
                }
            }

            Button {
                Layout.fillWidth: true

                text: qsTr("ADVANCED CONFIGURATION")
                highlighted: contentStack.currentIndex === 1

                onClicked: {
                    contentStack.currentIndex = 1
                }
            }

            Button {
                Layout.fillWidth: true

                text: qsTr("CANCEL LOADING")

                enabled: root.backend.busy

                onClicked: {
                    root.backend.cancel_fetching()
                }
            }
        }

        StackLayout {
            id: contentStack

            Layout.fillWidth: true
            Layout.fillHeight: true

            currentIndex: 0

            // --------------------------------------
            // Download list
            // --------------------------------------

            Item {
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 0

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: 40

                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 8
                            anchors.rightMargin: 8
                            spacing: 8

                            Label {
                                Layout.preferredWidth: 70
                                text: qsTr("DOWNLOAD")
                            }

                            Label {
                                Layout.fillWidth: true
                                text: qsTr("TITLE")
                            }

                            Label {
                                Layout.preferredWidth: 160
                                text: qsTr("AUTHOR")
                            }

                            Label {
                                Layout.preferredWidth: 75
                                text: qsTr("LENGTH")
                            }

                            Label {
                                Layout.preferredWidth: 80
                                text: qsTr("QUALITY")
                            }

                            Label {
                                Layout.preferredWidth: 65
                                text: qsTr("STOP")
                            }

                            Label {
                                Layout.preferredWidth: 180
                                text: qsTr("PROGRESS")
                            }
                        }
                    }

                    ListView {
                        id: downloadList

                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        clip: true
                        spacing: 1

                        model: root.backend.downloads

                        delegate: Rectangle {
                            id: downloadRow

                            required property string jobId
                            required property string title
                            required property string author
                            required property string duration
                            required property string quality
                            required property int progress

                            width: ListView.view.width
                            height: 48

                            RowLayout {
                                anchors.fill: parent
                                anchors.leftMargin: 8
                                anchors.rightMargin: 8
                                spacing: 8

                                CheckBox {
                                    Layout.preferredWidth: 70
                                }

                                Label {
                                    Layout.fillWidth: true

                                    text: downloadRow.title

                                    elide: Text.ElideRight
                                }

                                Label {
                                    Layout.preferredWidth: 160

                                    text: downloadRow.author

                                    elide: Text.ElideRight
                                }

                                Label {
                                    Layout.preferredWidth: 75

                                    text: downloadRow.duration
                                }

                                Label {
                                    Layout.preferredWidth: 80

                                    text: downloadRow.quality
                                }

                                Button {
                                    Layout.preferredWidth: 65

                                    text: "■"

                                    onClicked: {
                                        root.backend.stop_download(
                                            downloadRow.jobId
                                        )
                                    }
                                }

                                ProgressBar {
                                    Layout.preferredWidth: 180

                                    from: 0
                                    to: 100
                                    value: downloadRow.progress
                                }
                            }
                        }

                        ScrollBar.vertical: ScrollBar {
                        }

                        Label {
                            anchors.centerIn: parent

                            visible: downloadList.count === 0

                            text: qsTr("No downloads")
                        }
                    }
                }
            }

            // --------------------------------------
            // Advanced configuration
            // --------------------------------------

            Rectangle {

                Label {
                    anchors.centerIn: parent

                    text: qsTr("Advanced configuration")
                }
            }
        }

        // ------------------------------------------
        // Status and total area
        // ------------------------------------------

        Label {
            Layout.fillWidth: true

            visible: text.length > 0

            text: root.backend.statusMessage
        }

        RowLayout {
            Layout.fillWidth: true

            Label {
                text: qsTr("Total (HLS):")
            }

            Rectangle {
                Layout.fillWidth: true
                implicitHeight: 24

                Label {
                    anchors.centerIn: parent

                    text: root.backend.totalHls
                }
            }
        }
    }
}