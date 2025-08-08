import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    visibility: Window.FullScreen
    title: qsTr("Video Downloader")
    Material.theme: Material.Dark
    Material.accent: Material.Blue

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12
        clip: true

        Label {
            text: qsTr("Enter Video URL →")
            font.pointSize: 16
            color: "white"
        }

        TextField {
            id: urlInput
            placeholderText: qsTr("Paste video URL here")
            Layout.fillWidth: true
            Material.background: Material.Dense
        }

        GroupBox {
            title: qsTr("Quality")
            Layout.fillWidth: true
            Material.background: Material.Dense

            Flow {
                Layout.fillWidth: true
                spacing: 12

                RadioButton {
                    id: bestQuality; text: qsTr("Best"); checked: true
                }
                RadioButton {
                    id: halfQuality; text: qsTr("Half")
                }
                RadioButton {
                    id: worstQuality; text: qsTr("Worst")
                }
            }
        }

        Button {
            text: qsTr("Download")
            Layout.fillWidth: true
            onClicked: {
                var quality = bestQuality.checked ? "best"
                    : halfQuality.checked ? "half"
                        : "worst";
                progressBar.value = 0;
                downloadLabel.text = "";
                backend.downloadVideo(urlInput.text, quality);
            }
        }

        Label {
            id: downloadLocation
            text: "Videos are downloaded to: /storage/emulated/0/Download/"
            font.pointSize: 14
            color: "lightgray"
            Layout.fillWidth: true
            wrapMode: text.Wrap
            elide: Text.ElideRight
        }

        Label {
            id: downloadLabel
            text: ""
            font.pointSize: 14
            color: "lightgray"
            // make sure it never forces the layout wider than the screen
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            elide: Text.ElideRight
        }

        StackLayout {
            Layout.fillWidth: true
            height: 28

            ProgressBar {
                id: progressBar
                anchors.fill: parent
                from: 0;
                to: 100; value: 0
                height: parent.height
            }

            Label {
                text: qsTr("%1%").arg(Math.round(progressBar.value))
                anchors.centerIn: parent
                font.bold: true
                color: "white"
            }
        }

        Connections {
            target: backend

            function onTitleChanged(title) {
                // now this long text will wrap or elide, not push everything wider
                downloadLabel.text = qsTr("Downloading: %1").arg(title)
            }

            function onProgressChanged(current, total) {
                var percent = total > 0 ? (current / total) * 100 : 0
                progressBar.value = percent
            }
        }
    }
}