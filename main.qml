import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 360
    height: 640
    title: qsTr("Video Downloader")
    Material.theme: Material.Dark
    Material.accent: Material.Blue

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        Label {
            text: qsTr("Enter Video URL ->:")
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

            RowLayout {
                spacing: 20
                RadioButton { id: bestQuality; text: qsTr("Best"); checked: true }
                RadioButton { id: halfQuality; text: qsTr("Half") }
                RadioButton { id: worstQuality; text: qsTr("Worst") }
            }
        }

        Button {
            text: qsTr("Download")
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                var quality = bestQuality.checked ? "best"
                              : halfQuality.checked ? "half"
                              : "worst"
                progressBar.value = 0
                downloadLabel.text = ""
                backend.downloadVideo(urlInput.text, quality)
            }
        }

        Label {
            id: downloadLabel
            text: ""
            font.pointSize: 14
            color: "lightgray"
        }

        ProgressBar {
            id: progressBar
            Layout.fillWidth: true
            from: 0
            to: 100
            value: 0
        }

        Connections {
            target: backend
            function onTitleChanged(title) {
                downloadLabel.text = qsTr("Downloading: %1").arg(title)
            }
            function onProgressChanged(current, total) {
                var percent = total > 0 ? (current / total) * 100 : 0
                progressBar.value = percent
            }
        }
    }
}
