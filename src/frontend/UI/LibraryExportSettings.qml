import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs as Dialogs
import QtQuick.Layouts

Frame {
    id: root
    objectName: "libraryExportSettings"
    property var scrollView: null
    readonly property bool premium: typeof bridge !== "undefined" && bridge.isPremium
    readonly property bool busy: typeof backend.libraryExportBusy !== "undefined" && backend.libraryExportBusy
    property bool hasPreview: false
    Layout.fillWidth: true

    function reveal(control, force) {
        if ((!control.activeFocus && !force) || !scrollView) return;
        var flick = scrollView.contentItem;
        var position = control.mapToItem(flick.contentItem, 0, 0);
        var target = flick.contentY;
        if (position.y < target) target = position.y;
        else if (position.y + control.height > target + flick.height)
            target = position.y + control.height - flick.height;
        flick.contentY = Math.max(0, Math.min(target, flick.contentHeight - flick.height));
    }
    function navigate(event, control) {
        if (event.key !== Qt.Key_Up && event.key !== Qt.Key_Down) return;
        var fields = [mode, layoutChoice, genres, studios, server, localRoot, remoteRoot,
                        apiKey, saveKey, videoFile, chooseFile, source, preview, previewText, exportButton, retry];
        var controls = [];
        for (var j = 0; j < fields.length; ++j) {
            if (fields[j].helpButton) controls.push(fields[j].helpButton);
            controls.push(fields[j]);
        }
        var step = event.key === Qt.Key_Down ? 1 : -1;
        for (var i = controls.indexOf(control) + step; i >= 0 && i < controls.length; i += step) {
            if (controls[i].enabled && controls[i].visible) {
                controls[i].forceActiveFocus(Qt.TabFocusReason);
                event.accepted = true;
                break;
            }
        }
    }
    function invalidate() {
        root.hasPreview = false;
        previewText.text = "";
        if (typeof backend.clear_library_preview === "function") backend.clear_library_preview();
    }
    component ExportField: AppTextField {
        Layout.fillWidth: true
        enabled: !root.busy
        onActiveFocusChanged: root.reveal(this)
        Keys.onPressed: function(event) { root.navigate(event, this); }
    }
    component ExportButton: AppButton {
        onActiveFocusChanged: root.reveal(this)
        Keys.onPressed: function(event) { root.navigate(event, this); }
    }
    component ExportCheck: CheckBox {
        Layout.fillWidth: true
        activeFocusOnTab: true
        ContrastOutline { control: parent }
        onActiveFocusChanged: root.reveal(this)
        Keys.onPressed: function(event) {
            if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter || event.key === Qt.Key_Select) {
                toggle(); toggled(); event.accepted = true;
            } else root.navigate(event, this);
        }
    }

    Connections {
        target: backend
        ignoreUnknownSignals: true
        function onLibraryPreviewReady(summary) {
            if (appSettings.anonymous_mode) { previewText.text = ""; root.hasPreview = false; return; }
            previewText.text = summary;
            root.hasPreview = summary.length > 0;
            if (root.hasPreview) { status.text = qsTr("Preview ready. Review the available metadata before exporting."); Qt.callLater(function() { preview.forceActiveFocus(); }); }
        }
        function onLibraryExportFinished(message) {
            status.text = appSettings.anonymous_mode ? qsTr("Metadata operation finished. Details are hidden in Anonymous Mode.") : message;
            Qt.callLater(function() { preview.forceActiveFocus(); });
        }
    }
    Connections {
        target: appSettings
        function onAnonymousModeChanged() { root.invalidate(); status.text = ""; }
    }
    Dialogs.FileDialog {
        id: picker
        title: qsTr("Choose a completed video")
        nameFilters: [qsTr("Videos (*.mp4 *.mkv *.webm *.mov *.m4v *.ts)")]
        onAccepted: { videoFile.text = appSettings.local_path_from_url(selectedFile); root.invalidate(); chooseFile.forceActiveFocus(); }
        onRejected: chooseFile.forceActiveFocus()
    }
    contentItem: ColumnLayout {
        spacing: 10
        Label { text: qsTr("Media Library Export · Premium"); font.bold: true; Layout.fillWidth: true; wrapMode: Text.Wrap }
        Label {
            text: root.premium ? qsTr("Export available metadata and artwork for Jellyfin. Unknown fields stay empty; uploaders and studios remain separate.")
                               : qsTr("Activate Premium to export library metadata. Existing embedded MP4 tags remain available.")
            Layout.fillWidth: true; wrapMode: Text.Wrap
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: modeHelp
                objectName: "modeLibraryHelp"
                helpText: AppStrings.libraryExportHelp
                Accessible.name: qsTr("Help: %1").arg(mode.Accessible.name || mode.text || mode.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: mode
                Keys.onPressed: function(event) { root.navigate(event, modeHelp); }
            }
            AppComboBox {
                property string helpText: AppStrings.libraryExportHelp
                property var helpButton: modeHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: mode; objectName: "metadataExportMode"; Layout.fillWidth: true
                Accessible.name: qsTr("Automatic library export")
                model: [qsTr("Automatic export off"), qsTr("Export for Jellyfin")]
                currentIndex: appSettings.metadata_export === "jellyfin" ? 1 : 0
                enabled: !root.busy
                onActivated: function(index) { appSettings.metadata_export = index === 1 && root.premium ? "jellyfin" : "off"; currentIndex = appSettings.metadata_export === "jellyfin" ? 1 : 0; }
                onActiveFocusChanged: root.reveal(this)
                Keys.onPressed: function(event) { if (!popup.visible && (event.key === Qt.Key_Up || event.key === Qt.Key_Down)) root.navigate(event, this); }
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: layoutChoiceHelp
                objectName: "layoutChoiceLibraryHelp"
                helpText: AppStrings.libraryLayoutHelp
                Accessible.name: qsTr("Help: %1").arg(layoutChoice.Accessible.name || layoutChoice.text || layoutChoice.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: layoutChoice
                Keys.onPressed: function(event) { root.navigate(event, layoutChoiceHelp); }
            }
            AppComboBox {
                property string helpText: AppStrings.libraryLayoutHelp
                property var helpButton: layoutChoiceHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: layoutChoice; objectName: "metadataExportLayout"; Layout.fillWidth: true
                Accessible.name: qsTr("New download library layout")
                model: [qsTr("Sidecars beside each video"), qsTr("One folder per new video")]
                currentIndex: appSettings.metadata_layout === "scene-folder" ? 1 : 0
                enabled: root.premium && !root.busy
                onActivated: function(index) { appSettings.metadata_layout = index === 1 ? "scene-folder" : "alongside"; }
                onActiveFocusChanged: root.reveal(this)
                Keys.onPressed: function(event) { if (!popup.visible) root.navigate(event, this); }
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: genresHelp
                objectName: "genresLibraryHelp"
                helpText: AppStrings.libraryGenresHelp
                Accessible.name: qsTr("Help: %1").arg(genres.Accessible.name || genres.text || genres.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: genres
                Keys.onPressed: function(event) { root.navigate(event, genresHelp); }
            }
            ExportCheck {
                property string helpText: AppStrings.libraryGenresHelp
                property var helpButton: genresHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: genres; objectName: "metadataExportGenres"; text: qsTr("Use source categories as genres")
                checked: appSettings.metadata_genres; enabled: root.premium && !root.busy
                onToggled: { appSettings.metadata_genres = checked; root.invalidate(); }
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: studiosHelp
                objectName: "studiosLibraryHelp"
                helpText: AppStrings.libraryStudiosHelp
                Accessible.name: qsTr("Help: %1").arg(studios.Accessible.name || studios.text || studios.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: studios
                Keys.onPressed: function(event) { root.navigate(event, studiosHelp); }
            }
            ExportCheck {
                property string helpText: AppStrings.libraryStudiosHelp
                property var helpButton: studiosHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: studios; objectName: "metadataExportStudioFallback"; text: qsTr("Use credited providers, publishers and channels as studios")
                checked: appSettings.metadata_studio_fallback; enabled: root.premium && !root.busy
                onToggled: { appSettings.metadata_studio_fallback = checked; root.invalidate(); }
            }
        }
        Label { text: qsTr("Optional Jellyfin connection"); font.bold: true }
        Label { text: qsTr("Jellyfin must already have access to these files. This connection sends scan notifications; it does not transfer videos. All app traffic mode routes these requests through Tor too."); wrapMode: Text.Wrap; Layout.fillWidth: true }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: serverHelp
                objectName: "serverLibraryHelp"
                helpText: AppStrings.jellyfinServerHelp
                Accessible.name: qsTr("Help: %1").arg(server.Accessible.name || server.text || server.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: server
                Keys.onPressed: function(event) { root.navigate(event, serverHelp); }
            }
            ExportField {
                property string helpText: AppStrings.jellyfinServerHelp
                property var helpButton: serverHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: server; objectName: "jellyfinUrl"; Accessible.name: qsTr("Jellyfin server URL")
                placeholderText: qsTr("Server URL, for example http://localhost:8096")
                text: appSettings.jellyfin_url; onEditingFinished: appSettings.jellyfin_url = text.trim()
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: localRootHelp
                objectName: "localRootLibraryHelp"
                helpText: AppStrings.jellyfinLocalRootHelp
                Accessible.name: qsTr("Help: %1").arg(localRoot.Accessible.name || localRoot.text || localRoot.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: localRoot
                Keys.onPressed: function(event) { root.navigate(event, localRootHelp); }
            }
            ExportField {
                property string helpText: AppStrings.jellyfinLocalRootHelp
                property var helpButton: localRootHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: localRoot; objectName: "jellyfinLocalRoot"; Accessible.name: qsTr("Local media root")
                placeholderText: qsTr("Local media root, for example /mnt/media")
                text: appSettings.jellyfin_local_root; onEditingFinished: appSettings.jellyfin_local_root = text.trim()
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: remoteRootHelp
                objectName: "remoteRootLibraryHelp"
                helpText: AppStrings.jellyfinServerRootHelp
                Accessible.name: qsTr("Help: %1").arg(remoteRoot.Accessible.name || remoteRoot.text || remoteRoot.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: remoteRoot
                Keys.onPressed: function(event) { root.navigate(event, remoteRootHelp); }
            }
            ExportField {
                property string helpText: AppStrings.jellyfinServerRootHelp
                property var helpButton: remoteRootHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: remoteRoot; objectName: "jellyfinServerRoot"; Accessible.name: qsTr("Media root inside Jellyfin")
                placeholderText: qsTr("Jellyfin media root, for example /media")
                text: appSettings.jellyfin_server_root; onEditingFinished: appSettings.jellyfin_server_root = text.trim()
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: apiKeyHelp
                objectName: "apiKeyLibraryHelp"
                helpText: AppStrings.jellyfinApiKeyHelp
                Accessible.name: qsTr("Help: %1").arg(apiKey.Accessible.name || apiKey.text || apiKey.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: apiKey
                Keys.onPressed: function(event) { root.navigate(event, apiKeyHelp); }
            }
            ExportField {
                property string helpText: AppStrings.jellyfinApiKeyHelp
                property var helpButton: apiKeyHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: apiKey; objectName: "jellyfinApiKey"; Accessible.name: qsTr("Jellyfin API key")
                placeholderText: qsTr("API key (stored locally; leave blank to clear)"); echoMode: TextInput.Password
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: saveKeyHelp
                objectName: "saveKeyLibraryHelp"
                helpText: AppStrings.jellyfinSaveKeyHelp
                Accessible.name: qsTr("Help: %1").arg(saveKey.Accessible.name || saveKey.text || saveKey.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: saveKey
                Keys.onPressed: function(event) { root.navigate(event, saveKeyHelp); }
            }
            ExportButton {
                property string helpText: AppStrings.jellyfinSaveKeyHelp
                property var helpButton: saveKeyHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: saveKey; text: qsTr("Save API key"); enabled: root.premium && !root.busy
                onClicked: { if (backend.save_jellyfin_api_key(apiKey.text)) apiKey.clear(); }
            }
        }
        Label { text: qsTr("Export or repair an existing video"); font.bold: true }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: videoFileHelp
                objectName: "videoFileLibraryHelp"
                helpText: AppStrings.libraryExistingFileHelp
                Accessible.name: qsTr("Help: %1").arg(videoFile.Accessible.name || videoFile.text || videoFile.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: videoFile
                Keys.onPressed: function(event) { root.navigate(event, videoFileHelp); }
            }
            ExportField {
                property string helpText: AppStrings.libraryExistingFileHelp
                property var helpButton: videoFileHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: videoFile; objectName: "metadataVideoFile"; Accessible.name: qsTr("Completed video file")
                echoMode: appSettings.anonymous_mode ? TextInput.Password : TextInput.Normal
                placeholderText: qsTr("Completed video file")
                onTextEdited: root.invalidate()
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: chooseFileHelp
                objectName: "chooseFileLibraryHelp"
                helpText: AppStrings.libraryChooseFileHelp
                Accessible.name: qsTr("Help: %1").arg(chooseFile.Accessible.name || chooseFile.text || chooseFile.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: chooseFile
                Keys.onPressed: function(event) { root.navigate(event, chooseFileHelp); }
            }
            ExportButton {
                property string helpText: AppStrings.libraryChooseFileHelp
                property var helpButton: chooseFileHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700
                id: chooseFile; text: qsTr("Choose video"); enabled: !root.busy; onClicked: picker.open()
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: sourceHelp
                objectName: "sourceLibraryHelp"
                helpText: AppStrings.librarySourceUrlHelp
                Accessible.name: qsTr("Help: %1").arg(source.Accessible.name || source.text || source.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: source
                Keys.onPressed: function(event) { root.navigate(event, sourceHelp); }
            }
            ExportField {
                property string helpText: AppStrings.librarySourceUrlHelp
                property var helpButton: sourceHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true
                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: source; objectName: "metadataSourceUrl"; Accessible.name: qsTr("Original video URL")
                echoMode: appSettings.anonymous_mode ? TextInput.Password : TextInput.Normal
                placeholderText: qsTr("Original URL (optional when Porn Fetch metadata is saved)")
                onTextEdited: root.invalidate()
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: previewHelp
                objectName: "previewLibraryHelp"
                helpText: AppStrings.libraryPreviewHelp
                Accessible.name: qsTr("Help: %1").arg(preview.Accessible.name || preview.text || preview.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: preview
                Keys.onPressed: function(event) { root.navigate(event, previewHelp); }
            }
            ExportButton {
                property string helpText: AppStrings.libraryPreviewHelp
                property var helpButton: previewHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true

                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: preview; objectName: "metadataPreviewButton"; text: qsTr("Preview metadata")
                enabled: root.premium && !root.busy && !appSettings.anonymous_mode && videoFile.text.trim().length > 0
                onClicked: { status.text = qsTr("Reading metadata…"); backend.preview_library_export(videoFile.text, source.text); }
            }
        }
        ScrollView {
            id: previewScroll
            visible: root.hasPreview && !appSettings.anonymous_mode; Layout.fillWidth: true; Layout.preferredHeight: visible ? 240 : 0
            TextArea {
                id: previewText; objectName: "metadataPreviewText"; readOnly: true; selectByMouse: true
                activeFocusOnTab: true
                Accessible.name: qsTr("Library metadata preview")
                textFormat: TextEdit.PlainText; renderType: TextEdit.NativeRendering; wrapMode: TextEdit.Wrap
                ContrastOutline { control: previewText }
                onActiveFocusChanged: { if (activeFocus) root.reveal(previewScroll, true); }
                Keys.onPressed: function(event) {
                    if (event.key === Qt.Key_Up || event.key === Qt.Key_Down) {
                        var flick = previewScroll.contentItem;
                        var next = Math.max(0, Math.min(flick.contentY + (event.key === Qt.Key_Down ? 36 : -36), flick.contentHeight - flick.height));
                        if (Math.abs(next - flick.contentY) > 0.5) { flick.contentY = next; event.accepted = true; }
                        else root.navigate(event, this);
                    }
                }
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: exportButtonHelp
                objectName: "exportButtonLibraryHelp"
                helpText: AppStrings.libraryWriteHelp
                Accessible.name: qsTr("Help: %1").arg(exportButton.Accessible.name || exportButton.text || exportButton.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: exportButton
                Keys.onPressed: function(event) { root.navigate(event, exportButtonHelp); }
            }
            ExportButton {
                property string helpText: AppStrings.libraryWriteHelp
                property var helpButton: exportButtonHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true
                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: exportButton; objectName: "metadataExportButton"; text: qsTr("Export metadata")
                enabled: root.premium && !root.busy && root.hasPreview
                onClicked: backend.export_library_metadata()
            }
        }
        RowLayout {
            Layout.fillWidth: true
            HelpButton {
                id: retryHelp
                objectName: "retryLibraryHelp"
                helpText: AppStrings.libraryRetryHelp
                Accessible.name: qsTr("Help: %1").arg(retry.Accessible.name || retry.text || retry.placeholderText)
                onActiveFocusChanged: root.reveal(this)
                KeyNavigation.right: retry
                Keys.onPressed: function(event) { root.navigate(event, retryHelp); }
            }
            ExportButton {
                property string helpText: AppStrings.libraryRetryHelp
                property var helpButton: retryHelp
                KeyNavigation.left: helpButton
                hoverEnabled: true
                Accessible.description: helpText
                ToolTip.text: helpText
                ToolTip.visible: hovered
                ToolTip.delay: 700

                id: retry; text: qsTr("Retry pending exports and notifications")
                enabled: root.premium && !root.busy; onClicked: backend.retry_library_exports()
            }
        }
        Label { id: status; objectName: "metadataExportStatus"; Layout.fillWidth: true; wrapMode: Text.Wrap; textFormat: Text.PlainText }
    }
}
