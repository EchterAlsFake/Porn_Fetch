// qml/pages/DownloadsPage.qml

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Pane {
    id: root
    objectName: "downloadsPage"
    padding: 0
    readonly property bool materialStyle: (typeof appSettings !== "undefined" && appSettings)
                                          && appSettings.core_style === "Material"
    FontMetrics { id: tableFont; font: root.font }
    readonly property real downloadButtonMaximumWidth: Math.max(140, tableFont.advanceWidth(qsTr("Download")) + 48)
    readonly property real actionColumnWidth: downloadButtonMaximumWidth + 56
    readonly property real stopColumnWidth: Math.max(120, tableFont.advanceWidth(qsTr("Stop / Resume")) + 16)
    readonly property real removeColumnWidth: Math.max(80, tableFont.advanceWidth(qsTr("Remove")) + 16)
    readonly property real minimumTableWidth: actionColumnWidth + 100 + 80 + 130 + 100
                                                   + stopColumnWidth + 180 + removeColumnWidth + 72

    ScrollableMessageDialog {
        id: titleOptionsDialog
        objectName: "titleOptionsDialog"
        title: qsTr("Title formatting options")
        message: AppStrings.titleFormattingHelp
        modal: true
    }

    ScrollableMessageDialog {
        id: keyboardShortcutsDialog
        objectName: "downloadKeyboardDialog"
        title: qsTr("Keyboard shortcuts")
        message: qsTr("Enter in a video, model or playlist URL field starts that fetch.\n\nTab and Shift+Tab move between controls.\nSpace activates a focused button or checkbox.\nArrow keys change a focused quality selection or number input.")
        modal: true
    }

    Connections {
        target: backend.downloads
        function onRowsAboutToBeRemoved(parentIndex, first, last) {
            var item = downloadList.Window.window.activeFocusItem
            while (item && item !== downloadList) {
                if (item.objectName === "downloadRow" && item.index >= first && item.index <= last) {
                    videoUrlField.forceActiveFocus()
                    return
                }
                item = item.parent
            }
        }
    }

    ScrollableMessageDialog { id: downloadErrorDialog; title: qsTr("Download failed"); modal: true }
    Connections {
        target: appSettings
        function onAnonymousModeChanged() {
            if (appSettings.anonymous_mode) {
                downloadErrorDialog.close()
                downloadErrorDialog.message = ""
            }
        }
    }

    function qualityRequiresLicense(quality) {
        var normalized = String(quality || "").trim().toLowerCase()
        if (["best", "half", "4k", "uhd", "2k", "qhd", "fullhd", "fhd"]
                .indexOf(normalized) !== -1)
            return true
        var resolution = parseInt(normalized)
        return !isNaN(resolution) && resolution > 720
    }

    background: Rectangle {
        color: "transparent"
        border.width: 2
        border.color: Theme.outline
        radius: 10
    }

    readonly property var inputErrors: backend.inputErrors || ({})

    function getFilters() {
        return {
            "duration_minimum": minDurationSpin.value === 0 ? null : minDurationSpin.value,
            "duration_maximum": maxDurationSpin.value === 0 ? null : maxDurationSpin.value,
            "author_regex": authorRegexField.text === "" ? null : authorRegexField.text,
            "tags_regex": tagsRegexField.text === "" ? null : tagsRegexField.text,
            "title_regex": titleRegexField.text === "" ? null : titleRegexField.text,
            "quality_minimum": minQualityCombo.currentText === "Any" ? null : minQualityCombo.currentText,
            "quality_maximum": maxQualityCombo.currentText === "Any" ? null : maxQualityCombo.currentText,
            "published_after": afterDateField.text === "" ? null : afterDateField.text,
            "published_before": beforeDateField.text === "" ? null : beforeDateField.text,
            "start_index": startSpin.value,
            "end_index": endSpin.value
        }
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

            AppTextField {
                id: videoUrlField
                Accessible.description: root.inputErrors.video || ""
                onTextEdited: backend.clear_input_error("video")
                objectName: "videoUrlInput"
                focus: true // This automatically focuses the element when the app starts cuz you probably gotta download a video xD
                Layout.fillWidth: true

                Accessible.name: placeholderText
                placeholderText: qsTr("Enter a video URL")
                selectByMouse: true

                onAccepted: {
                    if (backend.busy || !text.trim()) return
                    if (backend.process_single_url(videoUrlField.text, customOptions.text, root.getFilters()))
                        videoUrlField.text = ""
                }
            }

            AppButton {
                objectName: "getVideoButton"
                text: qsTr("Get Video")

                enabled: videoUrlField.text.trim().length > 0
                         && !backend.busy

                onClicked: {
                    if (backend.process_single_url(videoUrlField.text, customOptions.text, getFilters()))
                        videoUrlField.text = ""
                }
            }

            Label {
                Layout.columnSpan: 3
                Layout.fillWidth: true
                visible: text !== ""
                text: root.inputErrors.video || ""
                textFormat: Text.PlainText
                wrapMode: Text.Wrap
            }

            Label {
                text: qsTr("Model URL:")
            }

            AppTextField {
                id: modelUrlField
                Accessible.description: root.inputErrors.model || ""
                onTextEdited: backend.clear_input_error("model")
                objectName: "modelUrlInput"

                Layout.fillWidth: true

                Accessible.name: placeholderText
                placeholderText: qsTr("Enter a model or channel URL")
                selectByMouse: true

                onAccepted: {
                    if (backend.busy || !text.trim()) return
                    if (backend.process_model_url(text, customOptions.text, getFilters()))
                        modelUrlField.text = ""
                }
            }

            AppButton {
                objectName: "getModelVideosButton"
                text: qsTr("Get Videos")

                enabled: modelUrlField.text.trim().length > 0
                         && !backend.busy

                onClicked: {
                    if (backend.process_model_url(modelUrlField.text, customOptions.text, getFilters()))
                        modelUrlField.text = ""
                }
            }


            Label {
                Layout.columnSpan: 3
                Layout.fillWidth: true
                visible: text !== ""
                text: root.inputErrors.model || ""
                textFormat: Text.PlainText
                wrapMode: Text.Wrap
            }

            Label {
                text: qsTr("Playlist URL:")
            }

            AppTextField {
                id: playlistUrlField
                Accessible.description: root.inputErrors.playlist || ""
                onTextEdited: backend.clear_input_error("playlist")
                objectName: "playlistUrlInput"

                Layout.fillWidth: true

                Accessible.name: placeholderText
                placeholderText: qsTr("Enter a playlist URL")
                selectByMouse: true

                onAccepted: {
                    if (backend.busy || !text.trim()) return
                    if (backend.process_playlist_url(text, customOptions.text, getFilters()))
                        playlistUrlField.text = ""
                }
            }

            AppButton {
                objectName: "getPlaylistVideosButton"
                text: qsTr("Get Videos")

                enabled: playlistUrlField.text.trim().length > 0
                         && !backend.busy

                onClicked: {
                    if (backend.process_playlist_url(playlistUrlField.text, customOptions.text, getFilters()))
                        playlistUrlField.text = ""
                }
            }

        }

        Label {
            Layout.fillWidth: true
            visible: text !== ""
            text: root.inputErrors.playlist || root.inputErrors.filters || ""
            textFormat: Text.PlainText
            wrapMode: Text.Wrap
        }

        Label {
            Layout.fillWidth: true
            visible: !bridge.isPremium
            text: qsTr("Free preview: model, channel and playlist URLs show their first 5 videos. Activate a premium license for bulk downloading.")
            wrapMode: Text.Wrap
        }

        // ------------------------------------------
        // Sub-page controls
        // ------------------------------------------

        RowLayout {
            Layout.fillWidth: true
            spacing: 2

            AppButton {
                Layout.fillWidth: true

                text: qsTr("Downloads")
                objectName: "downloadListButton"
                highlighted: contentStack.currentIndex === 0

                onClicked: {
                    contentStack.currentIndex = 0
                }
            }

            AppButton {
                Layout.fillWidth: true

                text: qsTr("Advanced Configuration")
                objectName: "downloadAdvancedButton"
                highlighted: contentStack.currentIndex === 1

                onClicked: {
                    contentStack.currentIndex = 1
                }
            }

            AppButton {
                Layout.fillWidth: true

                text: qsTr("Cancel Loading")
                objectName: "cancelLoadingButton"
                enabled: backend.busy

                onClicked: {
                    backend.cancel_fetching()
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

                    RowLayout {
                        Layout.fillWidth: true
                        Layout.leftMargin: 8
                        Layout.rightMargin: 8
                        Layout.topMargin: 4
                        Layout.bottomMargin: 4
                        spacing: 8

                        AppButton {
                            text: qsTr("Select All")
                            objectName: "downloadSelectAllButton"
                            enabled: downloadList.count > 0
                            onClicked: backend.select_all_videos(true)
                        }

                        AppButton {
                            text: qsTr("Clear Selection")
                            objectName: "downloadClearSelectionButton"
                            enabled: downloadList.count > 0
                            onClicked: backend.select_all_videos(false)
                        }

                        AppButton {
                            objectName: "clearDownloadListButton"
                            text: qsTr("Clear list")
                            enabled: downloadList.count > 0 || backend.busy
                            Accessible.description: qsTr("Remove all video rows. Downloaded files and history are kept.")
                            ToolTip.visible: hovered
                            ToolTip.text: Accessible.description
                            onClicked: backend.clear_download_list()
                        }

                        Item {
                            Layout.fillWidth: true
                        }

                        AppButton {
                            objectName: "downloadSelectedButton"
                            text: qsTr("Download Selected")
                            enabled: downloadList.count > 0
                            onClicked: backend.download_selected_videos(cleanupStopCheck.checked)
                        }
                    }

                    Flickable {
                        id: tableViewport
                        objectName: "downloadTableViewport"
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        contentWidth: Math.max(width, root.minimumTableWidth)
                        contentHeight: height
                        flickableDirection: Flickable.HorizontalFlick
                        boundsBehavior: Flickable.StopAtBounds
                        ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AsNeeded }

                        ColumnLayout {
                            width: tableViewport.contentWidth
                            height: tableViewport.height - (tableViewport.contentWidth > tableViewport.width ? 16 : 0)
                            spacing: 0
                            Rectangle {
                                Layout.fillWidth: true
                                implicitHeight: headerLayout.implicitHeight + 16
                                color: "transparent"

                                RowLayout {
                                    id: headerLayout
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.leftMargin: 8
                                    anchors.rightMargin: 8
                                    spacing: 8

                                    Label {
                                        Layout.minimumWidth: root.actionColumnWidth
                                        Layout.preferredWidth: root.actionColumnWidth
                                        Layout.maximumWidth: root.actionColumnWidth
                                        text: qsTr("Select / Download")
                                    }

                                    Label {
                                        Layout.fillWidth: true
                                        Layout.preferredWidth: 60
                                        Layout.minimumWidth: 100
                                        text: qsTr("Title")
                                    }

                                    Label {
                                        Layout.fillWidth: true
                                        Layout.preferredWidth: 40
                                        Layout.minimumWidth: 80
                                        text: qsTr("Author")
                                    }

                                    Label {
                                        Layout.preferredWidth: 130
                                        Layout.minimumWidth: 130
                                        Layout.maximumWidth: 130
                                        text: qsTr("Duration")
                                    }

                                    Label {
                                        Layout.preferredWidth: 100
                                        Layout.minimumWidth: 100
                                        Layout.maximumWidth: 100
                                        text: qsTr("Quality")
                                    }

                                    Label {
                                        Layout.preferredWidth: root.stopColumnWidth
                                        Layout.minimumWidth: root.stopColumnWidth
                                        Layout.maximumWidth: root.stopColumnWidth
                                        text: qsTr("Stop / Resume")
                                    }

                                    Label {
                                        Layout.preferredWidth: 180
                                        Layout.minimumWidth: 180
                                        Layout.maximumWidth: 180
                                        text: qsTr("Progress")
                                    }
                                    Label {
                                        Layout.preferredWidth: root.removeColumnWidth
                                        Layout.minimumWidth: root.removeColumnWidth
                                        Layout.maximumWidth: root.removeColumnWidth
                                        text: qsTr("Remove")
                                    }
                                }
                            }

                            ListView {
                                id: downloadList
                                objectName: "downloadList"

                                Layout.fillWidth: true
                                Layout.fillHeight: true

                                clip: true
                                spacing: 1

                                model: backend.downloads

                                SmoothWheelHandler {
                                    id: downloadWheelHandler
                                    flickable: downloadList
                                }

                                delegate: Rectangle {
                                    id: downloadRow
                                    objectName: "downloadRow"

                                    required property int index
                                    required property string errorId
                                    required property string jobId
                                    required property string title
                                    required property string author
                                    required property string duration
                                    required property var availableQualities
                                    required property string selectedQuality
                                    required property int progress
                                    required property bool selected
                                    required property string status

                                    readonly property string stateText: ({pending: qsTr("Ready"), queued: qsTr("Queued"), downloading: qsTr("Downloading"), stopping: qsTr("Stopping"), cancelled: qsTr("Stopped"), failed: qsTr("Failed"), completed: qsTr("Completed")})[status] || status
                                    readonly property bool downloadActive: status === "queued"
                                                                           || status === "downloading"
                                                                           || status === "stopping"
                                    readonly property bool canResume: status === "cancelled"
                                                                      || status === "failed"

                                    width: ListView.view.width
                                    implicitHeight: Math.max(48, rowLayout.implicitHeight + 16)
                                    color: "transparent"
                                    RowLayout {
                                        id: rowLayout
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.leftMargin: 8
                                        anchors.rightMargin: 8
                                        spacing: 8

                                        RowLayout {
                                            Layout.minimumWidth: root.actionColumnWidth
                                            Layout.preferredWidth: root.actionColumnWidth
                                            Layout.maximumWidth: root.actionColumnWidth
                                            spacing: 4

                                            CheckBox {
                                                objectName: "downloadSelectCheck"
                                                Accessible.name: qsTr("Select video")
                                                checked: downloadRow.selected
                                                enabled: !downloadRow.downloadActive
                                                onToggled: backend.set_video_selected(
                                                               downloadRow.jobId, checked)
                                            }

                                            AppButton {
                                                objectName: "downloadStartButton"
                                                Layout.fillWidth: true
                                                Layout.maximumWidth: root.downloadButtonMaximumWidth
                                                text: downloadRow.status === "failed" ? qsTr("Retry") : downloadRow.status === "cancelled" ? qsTr("Resume") : qsTr("Download")
                                                Accessible.name: qsTr("Download %1: %2").arg(downloadRow.index + 1).arg(text)
                                                enabled: !downloadRow.downloadActive
                                                onClicked: backend.download_video(
                                                               downloadRow.jobId,
                                                               cleanupStopCheck.checked)
                                            }
                                        }

                                        Label {
                                            id: titleLabel
                                            objectName: "downloadTitleLabel"
                                            Layout.fillWidth: true
                                            Layout.preferredWidth: 60
                                            Layout.minimumWidth: 100
                                            text: (appSettings.anonymous_mode === true || appSettings.anonymous_mode === "true" || appSettings.anonymous_mode === 1) ? qsTr("[redacted]") : downloadRow.title
                                            textFormat: Text.PlainText
                                            clip: true
                                            maximumLineCount: 1
                                            wrapMode: Text.NoWrap
                                            elide: Text.ElideRight

                                            ToolTip.visible: titleHover.hovered
                                                                 && titleLabel.truncated
                                            ToolTip.delay: 500
                                            ToolTip.text: titleLabel.text

                                            HoverHandler {
                                                id: titleHover
                                            }
                                        }

                                        Label {
                                            id: authorLabel
                                            objectName: "downloadAuthorLabel"
                                            Layout.fillWidth: true
                                            Layout.preferredWidth: 40
                                            Layout.minimumWidth: 80
                                            text: (appSettings.anonymous_mode === true || appSettings.anonymous_mode === "true" || appSettings.anonymous_mode === 1) ? qsTr("[redacted]") : downloadRow.author
                                            textFormat: Text.PlainText
                                            clip: true
                                            maximumLineCount: 1
                                            wrapMode: Text.NoWrap
                                            elide: Text.ElideRight

                                            ToolTip.visible: authorHover.hovered
                                                                 && authorLabel.truncated
                                            ToolTip.delay: 500
                                            ToolTip.text: authorLabel.text

                                            HoverHandler {
                                                id: authorHover
                                            }
                                        }

                                        Label {
                                            Layout.preferredWidth: 130
                                            Layout.minimumWidth: 130
                                            Layout.maximumWidth: 130
                                            text: downloadRow.duration
                                        }

                                        AppComboBox {
                                            id: qualityCombo
                                            Accessible.name: qsTr("Video quality")
                                            objectName: "downloadQualityCombo"
                                            Layout.preferredWidth: 100
                                            Layout.minimumWidth: 100
                                            Layout.maximumWidth: 100

                                            // 1. Feed the list of qualities from Python to the dropdown
                                            model: availableQualities

                                            // 2. Set the currently displayed item
                                            function findQualityIndex() {
                                                var qs = availableQualities || [];
                                                for (var i = 0; i < qs.length; i++) {
                                                    if (String(qs[i]) === String(selectedQuality)) return i;
                                                }
                                                return -1;
                                            }
                                            currentIndex: findQualityIndex()

                                            // 3. Send the change back to Python when the user picks a new option
                                            onActivated: {
                                                if (!root.qualityRequiresLicense(currentValue)
                                                        || (bridge && bridge.isPremium))
                                                    backend.update_video_quality(jobId, currentValue)
                                            }

                                            contentItem: Text {
                                                text: qualityCombo.currentIndex >= 0
                                                      ? availableQualities[qualityCombo.currentIndex]
                                                      : qsTr("License required")
                                                color: root.materialStyle
                                                       ? qualityCombo.Material.foreground
                                                       : qualityCombo.palette.buttonText
                                                font: qualityCombo.font
                                                verticalAlignment: Text.AlignVCenter
                                                horizontalAlignment: Text.AlignHCenter
                                                elide: Text.ElideRight
                                            }

                                            // 4. Custom look for the dropdown items (Freemium logic)
                                            delegate: ItemDelegate {
                                                id: qualityDelegate
                                                width: parent.width

                                                readonly property bool isPremiumRes: root.qualityRequiresLicense(modelData)

                                                // Disable the row entirely if it's premium AND the user isn't premium
                                                enabled: !isPremiumRes || (bridge && bridge.isPremium)

                                                contentItem: RowLayout {
                                                    spacing: 5

                                                    Text {
                                                        Layout.fillWidth: true
                                                        text: modelData
                                                        // Gray out the text if it's disabled
                                                        color: root.materialStyle
                                                               ? (qualityDelegate.enabled
                                                                  ? qualityDelegate.Material.foreground
                                                                  : qualityDelegate.Material.hintTextColor)
                                                               : (qualityDelegate.enabled
                                                                  ? qualityDelegate.palette.text
                                                                  : qualityDelegate.palette.mid)
                                                        verticalAlignment: Text.AlignVCenter
                                                    }

                                                    // Show a padlock icon for locked qualities
                                                    Image {
                                                        source: "qrc:/images/graphics/lock.png"
                                                        visible: isPremiumRes && !(bridge && bridge.isPremium)
                                                        Layout.preferredWidth: 16
                                                        Layout.preferredHeight: 16
                                                        fillMode: Image.PreserveAspectFit
                                                        Layout.alignment: Qt.AlignVCenter
                                                    }
                                                }
                                            }
                                        }

                                        AppButton {
                                            objectName: "downloadStopResumeButton"
                                            Layout.preferredWidth: root.stopColumnWidth
                                            Layout.minimumWidth: root.stopColumnWidth
                                            Layout.maximumWidth: root.stopColumnWidth

                                            text: downloadRow.downloadActive ? qsTr("Stop") : downloadRow.status === "failed" ? qsTr("Retry") : qsTr("Resume")
                                            Accessible.name: qsTr("Download %1: %2").arg(downloadRow.index + 1).arg(text)
                                            enabled: downloadRow.downloadActive
                                                     || downloadRow.canResume
                                            ToolTip.visible: hovered
                                            ToolTip.text: downloadRow.downloadActive
                                                          ? qsTr("Stop download")
                                                          : qsTr("Resume download")

                                            onClicked: {
                                                if (downloadRow.downloadActive) {
                                                    backend.stop_download(downloadRow.jobId)
                                                } else {
                                                    backend.resume_download(
                                                        downloadRow.jobId,
                                                        cleanupStopCheck.checked)
                                                }
                                            }
                                        }

                                        ColumnLayout {
                                            Layout.preferredWidth: 180
                                            Layout.minimumWidth: 180
                                            Layout.maximumWidth: 180
                                            spacing: 4
                                            Label {
                                                objectName: "downloadStatusLabel"
                                                Layout.fillWidth: true
                                                text: downloadRow.stateText + (downloadRow.status === "downloading" ? " · " + qsTr("%1%").arg(downloadRow.progress) : "")
                                                textFormat: Text.PlainText
                                                wrapMode: Text.Wrap
                                            }
                                            ProgressBar {
                                                id: rowProgress
                                                objectName: "downloadProgressBar"
                                                Layout.fillWidth: true
                                                Accessible.name: qsTr("Download %1 progress").arg(downloadRow.index + 1)
                                                Accessible.description: downloadRow.stateText
                                                from: 0
                                                to: 100
                                                value: downloadRow.progress
                                                indeterminate: downloadRow.status === "queued"
                                            }
                                            AppButton {
                                                visible: downloadRow.status === "failed" && downloadRow.errorId !== ""
                                                text: qsTr("Error details")
                                                onClicked: {
                                                    downloadErrorDialog.message = backend.download_error_details(downloadRow.jobId)
                                                    downloadErrorDialog.open()
                                                }
                                            }
                                        }
                                        AppButton {
                                            objectName: "downloadRemoveButton"
                                            Layout.preferredWidth: root.removeColumnWidth
                                            Layout.minimumWidth: root.removeColumnWidth
                                            Layout.maximumWidth: root.removeColumnWidth
                                            icon.source: "qrc:/images/graphics/settings/trash.svg"
                                            display: AbstractButton.IconOnly
                                            Accessible.name: qsTr("Remove video from list")
                                            ToolTip.visible: hovered
                                            ToolTip.text: qsTr("Remove from list. An active download will stop first.")
                                            onClicked: {
                                                videoUrlField.forceActiveFocus()
                                                backend.remove_video(downloadRow.jobId)
                                            }
                                        }
                                    }
                                }

                                ScrollBar.vertical: ScrollBar {
                                    policy: ScrollBar.AsNeeded
                                    active: size < 1.0 || hovered || pressed
                                            || downloadWheelHandler.scrolling
                                }

                                Label {
                                    anchors.centerIn: parent

                                    visible: downloadList.count === 0

                                    text: qsTr("No downloads")
                                }
                            }
                        }
                    }
                }
            }

            // --------------------------------------
            // Advanced configuration
            // --------------------------------------

            // --------------------------------------
            // Advanced configuration
            // --------------------------------------

            SmoothScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                contentWidth: availableWidth

                ColumnLayout {
                    width: parent.width
                    spacing: 15

                    // --- 1. GENERAL OPERATIONS ---
                    GroupBox {
                        title: qsTr("General Operations")
                        Layout.fillWidth: true

                        GridLayout {
                            anchors.fill: parent
                            columns: 2
                            columnSpacing: 15
                            rowSpacing: 10

                            RowLayout {
                                Layout.fillWidth: true
                                Layout.columnSpan: 2
                                CheckBox {
                                    id: cleanupStopCheck
                                    objectName: "cleanupStopCheck"
                                    text: qsTr("Cleanup on stop")
                                }
                                HelpButton { helpText: AppStrings.cleanupOnStopHelp }
                                Item { Layout.fillWidth: true }
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                Label { text: qsTr("Start video:") }
                                AppSpinBox {
                                    id: startSpin
                                    objectName: "downloadStartIndex"
                                    from: 0; to: 1000000
                                    value: 0
                                    editable: true
                                    Layout.fillWidth: true
                                }
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                Label { text: qsTr("End video:") }
                                AppSpinBox {
                                    id: endSpin
                                    objectName: "downloadEndIndex"
                                    from: 0; to: 1000000
                                    value: 0
                                    editable: true
                                    Layout.fillWidth: true
                                }
                            }
                        }
                    }

                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Video positions are inclusive and start at 1. Use 0 for the first video or no end limit. Positions are applied before filters.")
                        wrapMode: Text.WordWrap
                    }

                    // --- 2. VIDEO FILTERS ---
                    GroupBox {
                        title: qsTr("Video Filters (Applied during fetch)")
                        Layout.fillWidth: true

                        GridLayout {
                            anchors.fill: parent
                            columns: 2
                            columnSpacing: 15
                            rowSpacing: 10

                            // Duration
                            Label { text: qsTr("Duration (Minutes):") }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 10

                                AppSpinBox {
                                    id: minDurationSpin
                                    objectName: "downloadMinimumDuration"
                                    from: 0; to: 9999
                                    value: 0
                                    editable: true
                                    Layout.fillWidth: true
                                    // Shows "Any" when 0, otherwise "X min"
                                    textFromValue: function(value) { return value === 0 ? qsTr("Any") : value + qsTr(" min") }
                                }
                                Label { text: "-" }
                                AppSpinBox {
                                    id: maxDurationSpin
                                    objectName: "downloadMaximumDuration"
                                    from: 0; to: 9999
                                    value: 0
                                    editable: true
                                    Layout.fillWidth: true
                                    textFromValue: function(value) { return value === 0 ? qsTr("Any") : value + qsTr(" min") }
                                }
                            }

                            // Regex Filters
                            Label { text: qsTr("Title Regex:") }
                            AppTextField {
                                id: titleRegexField
                                objectName: "downloadTitleRegex"
                                Layout.fillWidth: true
                                Accessible.name: placeholderText
                                placeholderText: qsTr("e.g., ^Step.*")
                            }

                            Label { text: qsTr("Author Regex:") }
                            AppTextField {
                                id: authorRegexField
                                objectName: "downloadAuthorRegex"
                                Layout.fillWidth: true
                                placeholderText: qsTr("e.g., .*Studio$")
                            }

                            Label { text: qsTr("Tags Regex:") }
                            AppTextField {
                                id: tagsRegexField
                                objectName: "downloadTagsRegex"
                                Layout.fillWidth: true
                                Accessible.name: placeholderText
                                placeholderText: qsTr("e.g., pov|amateur")
                            }

                            // Quality Range
                            Label { text: qsTr("Quality Range:") }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 10

                                AppComboBox {
                                    id: minQualityCombo
                                    objectName: "downloadMinimumQuality"
                                    Layout.fillWidth: true
                                    model: ["Any", "144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "4k"]
                                }
                                Label { text: qsTr("to") }
                                AppComboBox {
                                    id: maxQualityCombo
                                    objectName: "downloadMaximumQuality"
                                    Layout.fillWidth: true
                                    model: ["Any", "144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "4k"]
                                }
                            }

                            // Dates
                            Label { text: qsTr("Publish Date:") }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 10

                                AppTextField {
                                    id: afterDateField
                                    objectName: "downloadAfterDate"
                                    Layout.fillWidth: true
                                    Accessible.name: placeholderText
                                    placeholderText: qsTr("After (YYYY-MM-DD)")
                                    // Forces the user to type a valid date format
                                    validator: RegularExpressionValidator { regularExpression: /^\d{4}-\d{2}-\d{2}$/ }
                                }
                                Label { text: "-" }
                                AppTextField {
                                    id: beforeDateField
                                    objectName: "downloadBeforeDate"
                                    Layout.fillWidth: true
                                    placeholderText: qsTr("Before (YYYY-MM-DD)")
                                    validator: RegularExpressionValidator { regularExpression: /^\d{4}-\d{2}-\d{2}$/ }
                                }
                            }
                        }
                    }

                    Label {
                        Layout.fillWidth: true
                        text: qsTr("All filters must match. Regexes ignore case; a tag regex may match any single tag. Quality range checks the highest available resolution. Date limits include the whole selected day.")
                        wrapMode: Text.WordWrap
                    }

                    // --- 3. FORMATTING & SHORTCUTS ---
                    GroupBox {
                        title: qsTr("Output")
                        Layout.fillWidth: true

                        GridLayout {
                            anchors.fill: parent
                            columns: 2
                            columnSpacing: 15

                            Label { text: qsTr("Custom Title formatting:") }
                            RowLayout {
                                Layout.fillWidth: true
                                AppTextField {
                                    id: customOptions
                                    objectName: "downloadTitlePattern"
                                    Accessible.name: placeholderText
                                    placeholderText: qsTr("$title")
                                    Layout.fillWidth: true
                                }
                                AppButton {
                                    objectName: "downloadTitleOptionsButton"
                                    text: qsTr("Options")
                                    onClicked: titleOptionsDialog.open()
                                }
                            }
                        }
                    }

                    AppButton {
                        objectName: "downloadKeyboardButton"
                        text: qsTr("Keyboard shortcuts")
                        onClicked: keyboardShortcutsDialog.open()
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                    }

                    // Spacer item to push everything up
                    Item {
                        Layout.fillHeight: true
                    }
                }
            }
        }

        // ------------------------------------------
        // Status and total area
        // ------------------------------------------

    }
}
