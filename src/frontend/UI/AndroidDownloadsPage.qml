import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Dialogs as Dialogs
import QtQuick.Layouts

Pane {
    id: root
    padding: 12
    property bool showFilters: false
    readonly property color pageColor: appSettings.dark_mode ? "#101319" : "#f7f8fc"
    readonly property color cardColor: appSettings.dark_mode ? "#1b202a" : "#ffffff"
    readonly property color textColor: appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    background: Rectangle { color: root.pageColor }

    function outputFolderName() {
        if (!appSettings.android_output_folder) return qsTr("App storage")
        var path = decodeURIComponent(appSettings.android_output_folder.split("/").pop())
        return path.split(":").pop() || qsTr("Selected folder")
    }

    Dialogs.FolderDialog {
        id: outputFolderDialog
        title: qsTr("Choose where to save videos")
        onAccepted: backend.set_android_output_folder(selectedFolder.toString())
    }

    function filterValue(field) {
        return field.text.trim() === "" ? null : field.text.trim()
    }

    function filters() {
        return {
            "duration_minimum": minDuration.value || null,
            "duration_maximum": maxDuration.value || null,
            "author_regex": filterValue(authorRegex),
            "tags_regex": filterValue(tagsRegex),
            "title_regex": filterValue(titleRegex),
            "quality_minimum": minQuality.currentText === "Any" ? null : minQuality.currentText,
            "quality_maximum": maxQuality.currentText === "Any" ? null : maxQuality.currentText,
            "published_after": filterValue(afterDate),
            "published_before": filterValue(beforeDate)
        }
    }

    function licensedQuality(quality) {
        var normalized = String(quality || "").trim().toLowerCase()
        if (["best", "half", "4k", "uhd", "2k", "qhd", "fullhd", "fhd"].indexOf(normalized) !== -1)
            return true
        var resolution = parseInt(normalized)
        return !isNaN(resolution) && resolution > 720
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 8

        Rectangle {
            Layout.fillWidth: true
            implicitHeight: fetchContent.implicitHeight + 28
            radius: 22
            color: root.cardColor

            ColumnLayout {
                id: fetchContent
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.margins: 14
                spacing: 8

                Label {
                    Layout.fillWidth: true
                    text: qsTr("Add videos")
                    color: root.textColor
                    font.pixelSize: 18
                    font.bold: true
                }

                ComboBox {
                    id: sourceType
                    Layout.fillWidth: true
                    model: [qsTr("Video URL"), qsTr("Model URL"), qsTr("Playlist URL")]
                }
                TextField {
                    id: urlField
                    Layout.fillWidth: true
                    placeholderText: qsTr("Paste a video, model or playlist URL")
                    inputMethodHints: Qt.ImhUrlCharactersOnly | Qt.ImhNoPredictiveText
                    onAccepted: fetchButton.clicked()
                }
                Button {
                    id: fetchButton
                    Layout.fillWidth: true
                    text: sourceType.currentIndex === 0 ? qsTr("Get Video") : qsTr("Get Videos")
                    enabled: urlField.text.trim().length > 0 && !backend.busy
                    onClicked: {
                        var url = urlField.text.trim()
                        if (sourceType.currentIndex === 0)
                            backend.process_single_url(url, customOptions.text, root.filters())
                        else if (sourceType.currentIndex === 1)
                            backend.process_model_url(url, customOptions.text, root.filters())
                        else
                            backend.process_playlist_url(url, customOptions.text, root.filters())
                        urlField.clear()
                    }
                }
                RowLayout {
                    Layout.fillWidth: true
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Save to: %1").arg(root.outputFolderName())
                        color: root.mutedColor
                        elide: Text.ElideRight
                    }
                    Button {
                        text: qsTr("Choose folder")
                        flat: true
                        onClicked: outputFolderDialog.open()
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Button {
                Layout.fillWidth: true
                text: root.showFilters ? qsTr("Downloads") : qsTr("Filters and options")
                onClicked: root.showFilters = !root.showFilters
            }
            Button {
                text: qsTr("Cancel fetch")
                onClicked: backend.cancel_fetching()
            }
        }

        ColumnLayout {
            visible: !root.showFilters
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 4

            RowLayout {
                Layout.fillWidth: true
                Button { text: qsTr("All"); onClicked: backend.select_all_videos(true) }
                Button { text: qsTr("None"); onClicked: backend.select_all_videos(false) }
                Item { Layout.fillWidth: true }
                Button {
                    text: qsTr("Download selected")
                    enabled: downloadList.count > 0
                    onClicked: backend.download_selected_videos(cleanupStop.checked)
                }
            }

            ListView {
                id: downloadList
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                spacing: 8
                model: backend.downloads

                delegate: Frame {
                    id: card
                    required property string jobId
                    required property string title
                    required property string author
                    required property string duration
                    required property var availableQualities
                    required property string selectedQuality
                    required property int progress
                    required property bool selected
                    required property string status
                    readonly property bool active: status === "queued" || status === "downloading" || status === "stopping"
                    readonly property bool resumable: status === "cancelled" || status === "failed"
                    width: ListView.view.width
                    padding: 14
                    background: Rectangle { color: root.cardColor; radius: 18 }

                    Dialogs.FileDialog {
                        id: exportDialog
                        title: qsTr("Save downloaded video")
                        fileMode: Dialogs.FileDialog.SaveFile
                        onAccepted: backend.export_download(card.jobId, selectedFile.toString())
                    }

                    contentItem: ColumnLayout {
                        id: cardContent
                        spacing: 4

                        Label {
                            Layout.fillWidth: true
                            text: appSettings.anonymous_mode ? qsTr("[redacted]") : card.title
                            font.bold: true
                            color: root.textColor
                            wrapMode: Text.Wrap
                            maximumLineCount: 2
                            elide: Text.ElideRight
                        }
                        Label {
                            Layout.fillWidth: true
                            text: (appSettings.anonymous_mode ? qsTr("[redacted]") : card.author)
                                  + " · " + card.duration + " · " + card.status
                            elide: Text.ElideRight
                            color: root.mutedColor
                        }
                        ProgressBar {
                            Layout.fillWidth: true
                            from: 0
                            to: 100
                            value: card.progress
                        }
                        RowLayout {
                            Layout.fillWidth: true
                            CheckBox {
                                checked: card.selected
                                enabled: !card.active
                                Accessible.name: qsTr("Select download")
                                onToggled: backend.set_video_selected(card.jobId, checked)
                            }
                            ComboBox {
                                id: qualityCombo
                                Layout.fillWidth: true
                                model: card.availableQualities
                                currentIndex: {
                                    var options = card.availableQualities || []
                                    for (var i = 0; i < options.length; i++)
                                        if (String(options[i]) === String(card.selectedQuality)) return i
                                    return -1
                                }
                                delegate: ItemDelegate {
                                    required property var modelData
                                    width: qualityCombo.width
                                    text: String(modelData)
                                    enabled: !root.licensedQuality(modelData) || bridge.isPremium
                                }
                                onActivated: {
                                    if (!root.licensedQuality(currentValue) || bridge.isPremium)
                                        backend.update_video_quality(card.jobId, currentValue)
                                }
                            }
                            Label { text: Math.round(card.progress) + "%" }
                        }
                        RowLayout {
                            Layout.fillWidth: true
                            Button {
                                Layout.fillWidth: true
                                text: qsTr("Download")
                                enabled: !card.active
                                onClicked: backend.download_video(card.jobId, cleanupStop.checked)
                            }
                            Button {
                                Layout.fillWidth: true
                                text: card.active ? qsTr("Stop") : qsTr("Resume")
                                enabled: card.active || card.resumable
                                onClicked: {
                                    if (card.active) backend.stop_download(card.jobId)
                                    else backend.resume_download(card.jobId, cleanupStop.checked)
                                }
                            }
                        }
                        Button {
                            Layout.fillWidth: true
                            text: qsTr("Save elsewhere")
                            visible: card.status === "completed"
                            onClicked: exportDialog.open()
                        }
                    }
                }

                Label {
                    anchors.centerIn: parent
                    visible: downloadList.count === 0
                    text: qsTr("No downloads yet\nAdd a video URL to get started")
                    horizontalAlignment: Text.AlignHCenter
                    color: root.mutedColor
                }
            }
        }

        ScrollView {
            visible: root.showFilters
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            contentWidth: availableWidth

            ColumnLayout {
                width: parent.width
                spacing: 8

                CheckBox { id: cleanupStop; text: qsTr("Cleanup on stop (disables HLS resume)") }
                Label { text: qsTr("Duration in minutes") }
                RowLayout {
                    Layout.fillWidth: true
                    SpinBox { id: minDuration; Layout.fillWidth: true; from: 0; to: 9999; editable: true }
                    Label { text: "–" }
                    SpinBox { id: maxDuration; Layout.fillWidth: true; from: 0; to: 9999; editable: true }
                }
                TextField { id: titleRegex; Layout.fillWidth: true; placeholderText: qsTr("Title regex") }
                TextField { id: authorRegex; Layout.fillWidth: true; placeholderText: qsTr("Author regex") }
                TextField { id: tagsRegex; Layout.fillWidth: true; placeholderText: qsTr("Tags regex") }
                Label { text: qsTr("Quality range") }
                RowLayout {
                    Layout.fillWidth: true
                    ComboBox { id: minQuality; Layout.fillWidth: true; model: ["Any", "240", "360", "480", "720", "1080", "1440", "2160"] }
                    ComboBox { id: maxQuality; Layout.fillWidth: true; model: ["Any", "240", "360", "480", "720", "1080", "1440", "2160"] }
                }
                TextField { id: afterDate; Layout.fillWidth: true; placeholderText: qsTr("Published after (YYYY-MM-DD)") }
                TextField { id: beforeDate; Layout.fillWidth: true; placeholderText: qsTr("Published before (YYYY-MM-DD)") }
                TextField { id: customOptions; Layout.fillWidth: true; placeholderText: qsTr("Custom options") }
            }
        }
    }
}
