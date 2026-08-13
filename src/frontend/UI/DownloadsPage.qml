// qml/pages/DownloadsPage.qml

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    padding: 0

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
        radius: 10
    }

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
            "published_before": beforeDateField.text === "" ? null : beforeDateField.text
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

            TextField {
                id: videoUrlField
                focus: true // This automatically focuses the element when the app starts cuz you probably gotta download a video xD
                Layout.fillWidth: true

                placeholderText: qsTr("Enter a video URL")
                selectByMouse: true

                onAccepted: {
                    backend.process_single_url(videoUrlField.text, customOptions.text, root.getFilters())
                    videoUrlField.text = ""
                }
            }

            Button {
                text: qsTr("Get Video")

                enabled: videoUrlField.text.trim().length > 0
                         && !backend.busy

                onClicked: {
                    backend.process_single_url(videoUrlField.text, customOptions.text, getFilters())
                    videoUrlField.text = ""
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
                    backend.process_model_url(text, customOptions.text, getFilters())
                    modelUrlField.text = ""
                }
            }

            Button {
                text: qsTr("Get Videos")

                enabled: modelUrlField.text.trim().length > 0
                         && !backend.busy

                onClicked: {
                    backend.process_model_url(modelUrlField.text, customOptions.text, getFilters())
                    modelUrlField.text = ""
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
                    backend.process_playlist_url(text, customOptions.text, getFilters())
                    playlistUrlField.text = ""
                }
            }

            Button {
                text: qsTr("Get Videos")

                enabled: playlistUrlField.text.trim().length > 0
                         && !backend.busy

                onClicked: {
                    backend.process_playlist_url(playlistUrlField.text, customOptions.text, getFilters())
                    playlistUrlField.text = ""
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

                text: qsTr("Downloads")
                highlighted: contentStack.currentIndex === 0

                onClicked: {
                    contentStack.currentIndex = 0
                }
            }

            Button {
                Layout.fillWidth: true

                text: qsTr("Advanced Configuration")
                highlighted: contentStack.currentIndex === 1

                onClicked: {
                    contentStack.currentIndex = 1
                }
            }

            Button {
                Layout.fillWidth: true

                text: qsTr("Cancel Loading")

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
                                Layout.preferredWidth: 90
                                text: qsTr("Download?")
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
                                Layout.preferredWidth: 90
                                text: qsTr("Duration")
                            }

                            Label {
                                Layout.preferredWidth: 100
                                text: qsTr("Quality")
                            }

                            Label {
                                Layout.preferredWidth: 65
                                text: qsTr("STOP")
                            }

                            Label {
                                Layout.preferredWidth: 180
                                text: qsTr("Progress")
                            }
                        }
                    }

                    ListView {
                        id: downloadList

                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        clip: true
                        spacing: 1

                        model: backend.downloads

                        delegate: Rectangle {
                            id: downloadRow

                            required property string jobId
                            required property string title
                            required property string author
                            required property string duration
                            required property var availableQualities
                            required property string selectedQuality
                            required property int progress

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

                                CheckBox {
                                    Layout.preferredWidth: 90
                                }

                                Label {
                                    Layout.fillWidth: true
                                    Layout.preferredWidth: 60
                                    Layout.minimumWidth: 100
                                    text: (appSettings.anonymous_mode === true || appSettings.anonymous_mode === "true" || appSettings.anonymous_mode === 1) ? "[redacted]" : downloadRow.title
                                    wrapMode: Text.Wrap
                                }

                                Label {
                                    Layout.fillWidth: true
                                    Layout.preferredWidth: 40
                                    Layout.minimumWidth: 80
                                    text: (appSettings.anonymous_mode === true || appSettings.anonymous_mode === "true" || appSettings.anonymous_mode === 1) ? "[redacted]" : downloadRow.author
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideRight
                                }

                                Label {
                                    Layout.preferredWidth: 90
                                    text: downloadRow.duration
                                }

                                ComboBox {
                                    id: qualityCombo
                                    Layout.preferredWidth: 100

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
                                        color: "white"
                                        font: qualityCombo.font
                                        verticalAlignment: Text.AlignVCenter
                                        horizontalAlignment: Text.AlignHCenter
                                        elide: Text.ElideRight
                                    }

                                    // 4. Custom look for the dropdown items (Freemium logic)
                                    delegate: ItemDelegate {
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
                                                color: parent.enabled ? "white" : "gray"
                                                verticalAlignment: Text.AlignVCenter
                                            }

                                            // Show a padlock icon for locked qualities
                                            Text {
                                                text: "🔒"
                                                visible: isPremiumRes && !(bridge && bridge.isPremium)
                                                verticalAlignment: Text.AlignVCenter
                                            }
                                        }
                                    }
                                }

                                Button {
                                    Layout.preferredWidth: 65

                                    text: "■"

                                    onClicked: {
                                        backend.stop_download(
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

            // --------------------------------------
            // Advanced configuration
            // --------------------------------------

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                contentWidth: availableWidth

                ScrollBar.vertical: ScrollBar {
                    policy: ScrollBar.AsNeeded
                }

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

                            CheckBox {
                                id: doNotClearCheck
                                text: qsTr("Do not clear videos")
                                Layout.fillWidth: true
                            }

                            CheckBox {
                                id: cleanupStopCheck
                                text: qsTr("Cleanup on stop (disables resume for HLS)")
                                Layout.fillWidth: true
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                Label { text: qsTr("Start:") }
                                SpinBox {
                                    id: startSpin
                                    value: 0
                                    editable: true
                                    Layout.fillWidth: true
                                }
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                Label { text: qsTr("End:") }
                                SpinBox {
                                    id: endSpin
                                    value: 0
                                    editable: true
                                    Layout.fillWidth: true
                                }
                            }
                        }
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

                                SpinBox {
                                    id: minDurationSpin
                                    from: 0; to: 9999
                                    value: 0
                                    editable: true
                                    Layout.fillWidth: true
                                    // Shows "Any" when 0, otherwise "X min"
                                    textFromValue: function(value) { return value === 0 ? qsTr("Any") : value + qsTr(" min") }
                                }
                                Label { text: "-" }
                                SpinBox {
                                    id: maxDurationSpin
                                    from: 0; to: 9999
                                    value: 0
                                    editable: true
                                    Layout.fillWidth: true
                                    textFromValue: function(value) { return value === 0 ? qsTr("Any") : value + qsTr(" min") }
                                }
                            }

                            // Regex Filters
                            Label { text: qsTr("Title Regex:") }
                            TextField {
                                id: titleRegexField
                                Layout.fillWidth: true
                                placeholderText: qsTr("e.g., ^Step.*")
                            }

                            Label { text: qsTr("Author Regex:") }
                            TextField {
                                id: authorRegexField
                                Layout.fillWidth: true
                                placeholderText: qsTr("e.g., .*Studio$")
                            }

                            Label { text: qsTr("Tags Regex:") }
                            TextField {
                                id: tagsRegexField
                                Layout.fillWidth: true
                                placeholderText: qsTr("e.g., pov|amateur")
                            }

                            // Quality Range
                            Label { text: qsTr("Quality Range:") }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 10

                                ComboBox {
                                    id: minQualityCombo
                                    Layout.fillWidth: true
                                    model: ["Any", "240p", "360p", "480p", "720p", "1080p", "1440p", "4k"]
                                }
                                Label { text: qsTr("to") }
                                ComboBox {
                                    id: maxQualityCombo
                                    Layout.fillWidth: true
                                    model: ["Any", "240p", "360p", "480p", "720p", "1080p", "1440p", "4k"]
                                }
                            }

                            // Dates
                            Label { text: qsTr("Publish Date:") }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 10

                                TextField {
                                    id: afterDateField
                                    Layout.fillWidth: true
                                    placeholderText: qsTr("After (YYYY-MM-DD)")
                                    // Forces the user to type a valid date format
                                    validator: RegularExpressionValidator { regularExpression: /^\d{4}-\d{2}-\d{2}$/ }
                                }
                                Label { text: "-" }
                                TextField {
                                    id: beforeDateField
                                    Layout.fillWidth: true
                                    placeholderText: qsTr("Before (YYYY-MM-DD)")
                                    validator: RegularExpressionValidator { regularExpression: /^\d{4}-\d{2}-\d{2}$/ }
                                }
                            }
                        }
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
                                TextField {
                                    id: customOptions
                                    placeholderText: "$title"
                                    Layout.fillWidth: true
                                }
                                Button {
                                    text: qsTr("Options")
                                }
                            }
                        }
                    }

                    Button {
                        text: qsTr("Keyboard shortcuts")
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
