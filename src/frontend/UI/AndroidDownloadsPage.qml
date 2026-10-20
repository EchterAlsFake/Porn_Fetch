import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Dialogs as Dialogs
import QtQuick.Layouts

Pane {
    id: root
    padding: width >= 840 ? 24 : 12
    property bool showFilters: false
    property bool selectionMode: false
    property string expandedJob: ""
    readonly property color pageColor: appSettings.dark_mode ? "#101319" : "#f7f8fc"
    readonly property color cardColor: appSettings.dark_mode ? "#1b202a" : "#ffffff"
    readonly property color textColor: appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    background: Rectangle {
        color: root.pageColor
    }

    readonly property string currentOutputFolderName: {
        var folder = appSettings.android_output_folder;
        if (!folder || folder.trim() === "")
            return qsTr("App storage");
        var decoded = decodeURIComponent(folder).replace(/\/+$/, "");
        if (decoded.indexOf("/storage/emulated/0/") !== -1) {
            return decoded.substring(decoded.indexOf("/storage/emulated/0/") + 20);
        }
        if (decoded.indexOf(":") !== -1) {
            var afterColon = decoded.substring(decoded.lastIndexOf(":") + 1);
            if (afterColon.length > 0)
                return afterColon;
        }
        var parts = decoded.split("/");
        return parts[parts.length - 1] || qsTr("Selected folder");
    }

    function outputFolderName() {
        return root.currentOutputFolderName;
    }

    Dialogs.FolderDialog {
        id: outputFolderDialog
        title: qsTr("Choose where to save videos")
        onAccepted: backend.set_android_output_folder(selectedFolder.toString())
    }

    function filterValue(field) {
        return field.text.trim() === "" ? null : field.text.trim();
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
        };
    }

    function licensedQuality(quality) {
        var normalized = String(quality || "").trim().toLowerCase();
        if (["best", "half", "4k", "uhd", "2k", "qhd", "fullhd", "fhd"].indexOf(normalized) !== -1)
            return true;
        var resolution = parseInt(normalized);
        return !isNaN(resolution) && resolution > 720;
    }

    // Keep the queue visible; entry and advanced options are a separate task.
    Drawer {
        id: addSheet
        objectName: "mobileAddSheet"
        edge: Qt.BottomEdge
        parent: Overlay.overlay
        width: Math.min(parent.width, 640)
        x: (parent.width - width) / 2
        height: Math.min(parent.height, 720)
        modal: true
        dragMargin: 0
        padding: 16
        background: Rectangle {
            color: root.cardColor
            radius: 24
        }
        ColumnLayout {
            anchors.fill: parent
            RowLayout {
                Layout.fillWidth: true
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Add videos")
                    font.bold: true
                    font.pixelSize: 22
                }
                ToolButton {
                    text: qsTr("Close")
                    implicitHeight: 48
                    onClicked: addSheet.close()
                }
            }
            ScrollView {
                id: entryScroll
                Layout.fillWidth: true
                Layout.fillHeight: true
                contentWidth: availableWidth
                clip: true
                ColumnLayout {
                    width: entryScroll.availableWidth
                    spacing: 8
                    ComboBox {
                        id: sourceType
                        implicitHeight: 48
                        Layout.fillWidth: true
                        model: [qsTr("Video URL"), qsTr("Model URL"), qsTr("Playlist URL")]
                    }
                    TextField {
                        id: urlField
                        implicitHeight: 56
                        Layout.fillWidth: true
                        placeholderText: qsTr("Paste a video, model or playlist URL")
                        inputMethodHints: Qt.ImhUrlCharactersOnly | Qt.ImhNoPredictiveText
                        onAccepted: fetchButton.clicked()
                    }
                    Button {
                        id: fetchButton
                        implicitHeight: 48
                        highlighted: true
                        background: Rectangle {
                            radius: 24
                            color: Material.accent
                            opacity: parent.enabled ? 1 : 0.38
                        }
                        Layout.fillWidth: true
                        text: sourceType.currentIndex === 0 ? qsTr("Get Video") : qsTr("Get Videos")
                        enabled: urlField.text.trim().length > 0 && !backend.busy
                        onClicked: {
                            if (!enabled)
                                return;
                            var url = urlField.text.trim();
                            if (sourceType.currentIndex === 0)
                                backend.process_single_url(url, customOptions.text, root.filters());
                            else if (sourceType.currentIndex === 1)
                                backend.process_model_url(url, customOptions.text, root.filters());
                            else if (sourceType.currentIndex === 2)
                                backend.process_playlist_url(url, customOptions.text, root.filters());
                            urlField.clear();
                            Qt.inputMethod.hide();
                            addSheet.close();
                        }
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        visible: true
                        Label {
                            Layout.fillWidth: true
                            text: qsTr("Save to: %1").arg(root.currentOutputFolderName)
                            color: root.mutedColor
                            elide: Text.ElideRight
                        }
                        Button {
                            text: qsTr("Choose folder")
                            flat: true
                            onClicked: outputFolderDialog.open()
                        }
                    }

                    Button {
                        Layout.fillWidth: true
                        implicitHeight: 48
                        text: root.showFilters ? qsTr("Hide filters and options") : qsTr("Filters and options")
                        flat: true
                        onClicked: root.showFilters = !root.showFilters
                    }
                    ColumnLayout {
                        visible: root.showFilters
                        Layout.fillWidth: true
                        CheckBox {
                            id: cleanupStop
                            Layout.fillWidth: true
                            text: qsTr("Delete partial files on stop")
                            implicitHeight: 48
                        }
                        Label {
                            text: qsTr("Duration in minutes")
                        }
                        RowLayout {
                            Layout.fillWidth: true
                            SpinBox {
                                id: minDuration
                                Layout.fillWidth: true
                                from: 0
                                to: 9999
                                editable: true
                            }
                            Label {
                                text: "–"
                            }
                            SpinBox {
                                id: maxDuration
                                Layout.fillWidth: true
                                from: 0
                                to: 9999
                                editable: true
                            }
                        }
                        TextField {
                            id: titleRegex
                            Layout.fillWidth: true
                            placeholderText: qsTr("Title regex")
                        }
                        TextField {
                            id: authorRegex
                            Layout.fillWidth: true
                            placeholderText: qsTr("Author regex")
                        }
                        TextField {
                            id: tagsRegex
                            Layout.fillWidth: true
                            placeholderText: qsTr("Tags regex")
                        }
                        Label {
                            text: qsTr("Quality range")
                        }
                        RowLayout {
                            Layout.fillWidth: true
                            ComboBox {
                                id: minQuality
                                Layout.fillWidth: true
                                model: ["Any", "240", "360", "480", "720", "1080", "1440", "2160"]
                            }
                            ComboBox {
                                id: maxQuality
                                Layout.fillWidth: true
                                model: ["Any", "240", "360", "480", "720", "1080", "1440", "2160"]
                            }
                        }
                        TextField {
                            id: afterDate
                            Layout.fillWidth: true
                            placeholderText: qsTr("Published after (YYYY-MM-DD)")
                        }
                        TextField {
                            id: beforeDate
                            Layout.fillWidth: true
                            placeholderText: qsTr("Published before (YYYY-MM-DD)")
                        }
                        TextField {
                            id: customOptions
                            Layout.fillWidth: true
                            placeholderText: qsTr("Custom options")
                        }
                    }
                }
            }
        }
    }

    ColumnLayout {
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        width: Math.min(parent.width, 960)
        spacing: 8
        RowLayout {
            Layout.fillWidth: true
            Label {
                Layout.fillWidth: true
                text: qsTr("Downloads")
                font.pixelSize: 24
                font.bold: true
                elide: Text.ElideRight
            }
            Button {
                text: qsTr("Add videos")
                highlighted: true
                background: Rectangle {
                    radius: 24
                    color: Material.accent
                    opacity: parent.enabled ? 1 : 0.38
                }
                implicitHeight: 48
                onClicked: addSheet.open()
            }
        }
        RowLayout {
            Layout.fillWidth: true
            Label {
                Layout.fillWidth: true
                text: qsTr("%1 videos").arg(downloadList.count)
                color: root.mutedColor
                elide: Text.ElideRight
            }
            ToolButton {
                text: root.selectionMode ? qsTr("Done") : qsTr("Select")
                implicitHeight: 48
                enabled: downloadList.count > 0
                onClicked: root.selectionMode = !root.selectionMode
            }
        }
        RowLayout {
            visible: backend.busy
            Layout.fillWidth: true
            ProcessingIndicator {
                Layout.fillWidth: true
                running: backend.busy
            }
            ToolButton {
                text: qsTr("Cancel")
                implicitHeight: 48
                onClicked: backend.cancel_fetching()
            }
        }
        ListView {
            id: downloadList
            objectName: "mobileDownloadList"
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 0
            clip: true
            spacing: 8
            boundsBehavior: Flickable.StopAtBounds
            model: backend.downloads
            ScrollBar.vertical: ScrollBar {}
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
                padding: 12
                background: Rectangle {
                    color: root.cardColor
                    radius: 16
                    border.width: card.selected && root.selectionMode ? 2 : 0
                    border.color: Material.accent
                }
                Dialogs.FileDialog {
                    id: exportDialog
                    title: qsTr("Save downloaded video")
                    fileMode: Dialogs.FileDialog.SaveFile
                    onAccepted: backend.export_download(card.jobId, selectedFile.toString())
                }
                contentItem: ColumnLayout {
                    spacing: 4
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 4
                        CheckBox {
                            visible: root.selectionMode
                            implicitWidth: 48
                            implicitHeight: 48
                            checked: card.selected
                            enabled: !card.active
                            Accessible.name: qsTr("Select %1").arg(appSettings.anonymous_mode ? qsTr("video") : card.title)
                            onToggled: backend.set_video_selected(card.jobId, checked)
                        }
                        ItemDelegate {
                            Layout.fillWidth: true
                            implicitHeight: Math.max(64, rowText.implicitHeight + 12)
                            padding: 4
                            Accessible.name: qsTr("Video details")
                            Accessible.description: appSettings.anonymous_mode ? qsTr("Video") : card.title
                            onClicked: root.expandedJob = root.expandedJob === card.jobId ? "" : card.jobId
                            contentItem: ColumnLayout {
                                id: rowText
                                spacing: 4
                                Label {
                                    Layout.fillWidth: true
                                    text: appSettings.anonymous_mode ? qsTr("[redacted]") : card.title
                                    color: root.textColor
                                    font.bold: true
                                    wrapMode: Text.Wrap
                                    maximumLineCount: root.expandedJob === card.jobId ? 20 : 2
                                    elide: Text.ElideRight
                                }
                                Label {
                                    Layout.fillWidth: true
                                    text: (appSettings.anonymous_mode ? qsTr("[redacted]") : card.author) + " · " + card.duration
                                    color: root.mutedColor
                                    elide: Text.ElideRight
                                }
                            }
                        }
                        ToolButton {
                            implicitWidth: 48
                            implicitHeight: 48
                            contentItem: Item {
                                // Geometry avoids depending on the device font's symbol coverage.
                                Item {
                                    anchors.centerIn: parent
                                    width: 14
                                    height: 14
                                    rotation: root.expandedJob === card.jobId ? 180 : 0
                                    Rectangle { x: 1; y: 5; width: 9; height: 2; radius: 1; rotation: 45; color: root.textColor }
                                    Rectangle { x: 6; y: 5; width: 9; height: 2; radius: 1; rotation: -45; color: root.textColor }
                                }
                            }
                            Accessible.name: root.expandedJob === card.jobId ? qsTr("Hide details") : qsTr("Show details")
                            onClicked: root.expandedJob = root.expandedJob === card.jobId ? "" : card.jobId
                        }
                    }
                    ProgressBar {
                        visible: card.active
                        Layout.fillWidth: true
                        from: 0
                        to: 100
                        value: card.progress
                        indeterminate: card.status === "queued"
                        Accessible.name: qsTr("Download progress")
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        Label {
                            Layout.fillWidth: true
                            color: root.mutedColor
                            elide: Text.ElideRight
                            text: {
                                var labels = {
                                    pending: qsTr("Ready"),
                                    queued: qsTr("Queued"),
                                    downloading: qsTr("Downloading"),
                                    stopping: qsTr("Stopping"),
                                    cancelled: qsTr("Stopped"),
                                    failed: qsTr("Failed"),
                                    completed: qsTr("Completed")
                                };
                                return (labels[card.status] || card.status) + (card.status === "downloading" ? " · " + card.progress + "%" : "") + (card.selectedQuality ? " · " + card.selectedQuality : "");
                            }
                        }
                        Button {
                            implicitHeight: 48
                            flat: true
                            text: card.active ? qsTr("Stop") : card.resumable ? qsTr("Resume") : card.status === "completed" ? qsTr("Save") : qsTr("Download")
                            enabled: card.status !== "stopping"
                            onClicked: {
                                if (card.active)
                                    backend.stop_download(card.jobId);
                                else if (card.resumable)
                                    backend.resume_download(card.jobId, cleanupStop.checked);
                                else if (card.status === "completed") {
                                    exportDialog.selectedFile = backend.download_file_url(card.jobId);
                                    exportDialog.open();
                                } else
                                    backend.download_video(card.jobId, cleanupStop.checked);
                            }
                        }
                    }
                    RowLayout {
                        visible: root.expandedJob === card.jobId
                        Layout.fillWidth: true
                        Label {
                            text: qsTr("Quality")
                            color: root.mutedColor
                        }
                        ComboBox {
                            id: qualityCombo
                            Layout.fillWidth: true
                            implicitHeight: 48
                            enabled: !card.active && card.status !== "completed"
                            Accessible.name: qsTr("Video quality")
                            model: card.availableQualities
                            currentIndex: {
                                var options = card.availableQualities || [];
                                for (var i = 0; i < options.length; i++)
                                    if (String(options[i]) === String(card.selectedQuality))
                                        return i;
                                return -1;
                            }
                            delegate: ItemDelegate {
                                id: qualityDelegateItem
                                required property var modelData
                                width: qualityCombo.width
                                enabled: !root.licensedQuality(modelData) || bridge.isPremium
                                contentItem: RowLayout {
                                    spacing: 8
                                    Label {
                                        Layout.fillWidth: true
                                        text: String(qualityDelegateItem.modelData)
                                        color: qualityDelegateItem.enabled ? root.textColor : root.mutedColor
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    Image {
                                        source: "qrc:/images/graphics/lock.png"
                                        visible: root.licensedQuality(qualityDelegateItem.modelData) && !bridge.isPremium
                                        Layout.preferredWidth: 16
                                        Layout.preferredHeight: 16
                                        fillMode: Image.PreserveAspectFit
                                        Layout.alignment: Qt.AlignVCenter
                                    }
                                }
                            }
                            onActivated: {
                                if (!root.licensedQuality(currentValue) || bridge.isPremium)
                                    backend.update_video_quality(card.jobId, currentValue);
                            }
                        }
                    }
                }
            }
            ColumnLayout {
                anchors.centerIn: parent
                width: Math.min(parent.width - 32, 360)
                visible: downloadList.count === 0
                spacing: 12
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Your downloads start here")
                    font.bold: true
                    wrapMode: Text.Wrap
                    horizontalAlignment: Text.AlignHCenter
                }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Add a video, model or playlist link. Choose a quality, then download when you’re ready.")
                    color: root.mutedColor
                    wrapMode: Text.Wrap
                    horizontalAlignment: Text.AlignHCenter
                }
                Button {
                    Layout.alignment: Qt.AlignHCenter
                    text: qsTr("Add videos")
                    implicitHeight: 48
                    onClicked: addSheet.open()
                }
            }
        }
        ColumnLayout {
            visible: root.selectionMode
            Layout.fillWidth: true
            spacing: 0
            RowLayout {
                Layout.fillWidth: true
                Button {
                    Layout.fillWidth: true
                    implicitHeight: 48
                    text: qsTr("Select all")
                    onClicked: backend.select_all_videos(true)
                }
                Button {
                    Layout.fillWidth: true
                    implicitHeight: 48
                    text: qsTr("Clear selection")
                    onClicked: backend.select_all_videos(false)
                }
            }
            Button {
                Layout.fillWidth: true
                implicitHeight: 48
                highlighted: true
                background: Rectangle {
                    radius: 24
                    color: Material.accent
                    opacity: parent.enabled ? 1 : 0.38
                }
                text: qsTr("Download selected")
                onClicked: backend.download_selected_videos(cleanupStop.checked)
            }
        }
    }
}
