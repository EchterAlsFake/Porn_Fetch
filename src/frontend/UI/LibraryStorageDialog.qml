import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Dialogs as Dialogs
import QtQuick.Layouts

Dialog {
    id: root
    objectName: "libraryStorageDialog"
    property var storageBridge: typeof creatorBridge !== "undefined" ? creatorBridge : null
    property var returnFocusItem
    readonly property bool busy: storageBridge && storageBridge.transferBusy
    readonly property bool supported: storageBridge && storageBridge.transferSupported
    property bool migrationOnly: false
    property string migrationAction: ""
    readonly property real progress: storageBridge && typeof storageBridge.transferProgress === "number" ? storageBridge.transferProgress : -1
    property string pendingKind: ""
    property var pendingDetails: ({})
    property string statusText: ""
    parent: Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(680, parent ? parent.width - 24 : 680)
    height: Math.min(migrationOnly ? 360 : 760, parent ? parent.height - 24 : 760)
    modal: true; focus: true
    enter: Transition {}
    exit: Transition {}
    title: migrationOnly ? (migrationAction === "export" ? qsTr("Export library") : qsTr("Import library")) : qsTr("Move or locate downloaded videos")
    closePolicy: Popup.NoAutoClose
    function handleBack(event, released, popup) {
        if (event.key !== Qt.Key_Escape && event.key !== Qt.Key_Back) return false
        event.accepted = true
        if (released && !root.busy) popup.close()
        return true
    }
    background: Rectangle { color: Theme.surface; radius: 12; border.width: 1; border.color: Theme.outline }
    header: ColumnLayout {
        spacing: 8
        Label { text: root.title; color: Theme.ink; padding: 20; font.pixelSize: 21; font.bold: true; Layout.fillWidth: true; wrapMode: Text.WordWrap }
        ProgressBar {
            objectName: "storageProgressBar"
            Layout.fillWidth: true; Layout.leftMargin: 20; Layout.rightMargin: 20
            visible: root.busy || root.statusText !== ""; from: 0; to: 1
            value: Math.max(0, root.progress); indeterminate: root.busy && root.progress < 0
            Accessible.name: qsTr("Library storage operation in progress")
        }
        Label {
            objectName: "storageProgressLabel"
            Layout.fillWidth: true; Layout.leftMargin: 20; Layout.rightMargin: 20
            visible: root.busy || root.statusText !== ""
            text: (root.storageBridge && root.storageBridge.transferStage ? root.storageBridge.transferStage : qsTr("Working…"))
                + (root.progress >= 0 ? " " + Math.round(root.progress * 100) + "%" : "")
            color: Theme.ink; wrapMode: Text.WordWrap
        }
        Label {
            objectName: "storageStatus"
            Layout.fillWidth: true; Layout.leftMargin: 20; Layout.rightMargin: 20
            visible: root.statusText !== ""; text: root.statusText
            textFormat: Text.PlainText; color: Theme.ink; wrapMode: Text.WrapAnywhere
            Accessible.role: Accessible.AlertMessage
        }
    }
    function restoreFocus() {
        Qt.callLater(function() {
            if (!root.returnFocusItem || !root.returnFocusItem.visible) return
            var window = root.returnFocusItem.Window.window
            if (window) window.requestActivate()
            root.returnFocusItem.forceActiveFocus(Qt.TabFocusReason)
        })
    }
    function prepareOperation(item) {
        returnFocusItem = item
        pendingKind = ""; statusText = ""
    }
    function presentMigration(action, item) {
        if (action !== "import" && action !== "export") return
        migrationOnly = true
        migrationAction = action
        prepareOperation(item)
        if (!root.supported) { open(); return }
        if (action === "export") exportPicker.open()
        else importPicker.open()
    }
    function startMigration(filename) {
        open()
        if (migrationAction === "export") storageBridge.exportLibrary(filename)
        else storageBridge.previewImport(filename)
    }
    function present(folder, item) {
        migrationOnly = false
        migrationAction = ""
        prepareOperation(item)
        oldFolder.text = folder || ""
        newFolder.text = ""
        open()
    }
    function reveal(item) {
        if (!item || !item.activeFocus) return
        var ancestor = item
        while (ancestor && ancestor !== form.contentItem) ancestor = ancestor.parent
        if (!ancestor) return
        var point = item.mapToItem(form.contentItem, 0, 0)
        form.contentItem.contentY = Math.max(0, Math.min(form.contentItem.contentHeight - form.availableHeight,
            Math.min(point.y - 8, Math.max(form.contentItem.contentY, point.y + item.height + 8 - form.availableHeight))))
    }
    onOpened: Qt.callLater(function() {
        (root.supported && !root.migrationOnly ? oldFolder : closeButton).forceActiveFocus(Qt.TabFocusReason)
    })
    onClosed: {
        if (storageBridge) storageBridge.cancelTransfer()
        restoreFocus()
    }
    Connections {
        target: root.parent ? root.parent.Window.window : null
        function onActiveFocusItemChanged() { if (root.opened) root.reveal(root.parent.Window.window.activeFocusItem) }
    }
    Connections {
        target: root.storageBridge
        function onTransferPreview(kind, details) {
            if (!root.opened) return
            root.pendingKind = kind; root.pendingDetails = details
            confirmDialog.open()
        }
        function onTransferFinished(message) {
            if (!root.opened) return
            root.statusText = message
            Qt.callLater(function() { closeButton.forceActiveFocus(Qt.TabFocusReason) })
        }
    }
    Dialogs.FolderDialog {
        id: folderPicker
        property var field
        title: qsTr("Choose a video folder")
        onAccepted: { field.text = appSettings.local_path_from_url(selectedFolder); field.forceActiveFocus() }
        onRejected: if (field) field.forceActiveFocus()
    }
    Dialogs.FileDialog {
        id: exportPicker
        objectName: "storageExportPicker"
        parentWindow: root.parent ? root.parent.Window.window : null
        fileMode: Dialogs.FileDialog.SaveFile
        title: qsTr("Export PocketBase library")
        nameFilters: [qsTr("Porn Fetch library (*.zip)")]
        defaultSuffix: "zip"
        onAccepted: root.startMigration(appSettings.local_path_from_url(selectedFile))
        onRejected: root.restoreFocus()
    }
    Dialogs.FileDialog {
        id: importPicker
        objectName: "storageImportPicker"
        parentWindow: root.parent ? root.parent.Window.window : null
        fileMode: Dialogs.FileDialog.OpenFile
        title: qsTr("Import PocketBase library")
        nameFilters: [qsTr("Porn Fetch library (*.zip)")]
        onAccepted: root.startMigration(appSettings.local_path_from_url(selectedFile))
        onRejected: root.restoreFocus()
    }
    contentItem: SmoothScrollView {
        id: form
        clip: true
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        Keys.priority: Keys.AfterItem
        Keys.onReleased: function(event) { root.handleBack(event, true, root) }
        Keys.onPressed: function(event) {
            if (root.handleBack(event, false, root)) return
            if ([Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right].indexOf(event.key) < 0) return
            var item = root.parent.Window.window.activeFocusItem
            if (!item) return
            var next = item.nextItemInFocusChain(event.key === Qt.Key_Down || event.key === Qt.Key_Right)
            var count = 0
            while (next && (!next.visible || !next.enabled || !next.activeFocusOnTab) && count++ < 100)
                next = next.nextItemInFocusChain(event.key === Qt.Key_Down || event.key === Qt.Key_Right)
            if (next) { next.forceActiveFocus(Qt.TabFocusReason); event.accepted = true }
        }
        ColumnLayout {
            width: form.availableWidth; spacing: 12
            Label { Layout.fillWidth: true; visible: !root.supported; text: qsTr("Moving files and library migration currently require the desktop app and local filesystem folders."); color: Theme.ink; wrapMode: Text.WordWrap }
            Label { Layout.fillWidth: true; visible: !root.migrationOnly; text: qsTr("Stop scans and pause downloads before continuing."); color: Theme.muted; wrapMode: Text.WordWrap }
            ColumnLayout {
                objectName: "storageRelocationSection"
                Layout.fillWidth: true; spacing: 12; visible: !root.migrationOnly
                Label { text: qsTr("Move or locate downloaded videos"); color: Theme.ink; font.bold: true }
                Label { Layout.fillWidth: true; text: qsTr("Keep filenames and subfolders unchanged. This updates all completed records and subscription destinations under the old folder, including shared history. Paused downloads keep their original locations."); color: Theme.muted; wrapMode: Text.WordWrap }
                Label { text: qsTr("Old folder"); color: Theme.ink }
                AppTextField { id: oldFolder; objectName: "storageOldFolder"; Layout.fillWidth: true; enabled: root.supported && !root.busy; selectByMouse: true; Accessible.name: qsTr("Old video folder") }
                CreatorButton { text: qsTr("Choose old folder"); enabled: root.supported && !root.busy; onClicked: { folderPicker.field = oldFolder; folderPicker.open() } }
                Label { text: qsTr("New folder"); color: Theme.ink }
                AppTextField { id: newFolder; objectName: "storageNewFolder"; Layout.fillWidth: true; enabled: root.supported && !root.busy; selectByMouse: true; Accessible.name: qsTr("New video folder") }
                CreatorButton { text: qsTr("Choose new folder"); enabled: root.supported && !root.busy; onClicked: { folderPicker.field = newFolder; folderPicker.open() } }
                Flow {
                    Layout.fillWidth: true; spacing: 8
                    CreatorButton { objectName: "storageMoveButton"; text: qsTr("Move files"); enabled: root.supported && !root.busy && oldFolder.text.trim() !== "" && newFolder.text.trim() !== ""; onClicked: root.storageBridge.previewRelocation(oldFolder.text, newFolder.text, "move") }
                    CreatorButton { objectName: "storageLocateButton"; text: qsTr("Locate moved files"); enabled: root.supported && !root.busy && oldFolder.text.trim() !== "" && newFolder.text.trim() !== ""; onClicked: root.storageBridge.previewRelocation(oldFolder.text, newFolder.text, "locate") }
                }
                Label { Layout.fillWidth: true; text: qsTr("Move files copies completed videos and known metadata/artwork, saves the new paths, then removes the originals. Existing destination files are never overwritten. Locate moved files only verifies and updates paths."); color: Theme.muted; wrapMode: Text.WordWrap }
            }
            ColumnLayout {
                objectName: "storageMigrationSection"
                Layout.fillWidth: true; spacing: 12; visible: root.migrationOnly
                Label {
                    Layout.fillWidth: true
                    text: root.migrationAction === "export"
                        ? qsTr("The archive includes your library and download history, without video files. Keep it private.")
                        : qsTr("Review the import preview before continuing. A safety backup is created before changes are applied.")
                    color: Theme.muted; wrapMode: Text.WordWrap
                }
            }
        }
    }
    footer: Item {
        Keys.onPressed: function(event) { root.handleBack(event, false, root) }
        Keys.onReleased: function(event) { root.handleBack(event, true, root) }
        implicitHeight: 76
        CreatorButton { id: closeButton; objectName: "storageCloseButton"; anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter; anchors.margins: 14; text: qsTr("Close"); enabled: !root.busy; onClicked: root.close() }
    }
    Dialog {
        id: confirmDialog
        objectName: "storageConfirmDialog"
        parent: Overlay.overlay; anchors.centerIn: parent
        width: Math.min(540, parent ? parent.width - 24 : 540)
        height: Math.min(440, parent ? parent.height - 24 : 440)
        modal: true; focus: true
        enter: Transition {}
        exit: Transition {}
        closePolicy: Popup.NoAutoClose
        title: root.pendingKind === "import" ? qsTr("Import this library?") : qsTr("Update video locations?")
        background: Rectangle { color: Theme.surface; radius: 12; border.width: 1; border.color: Theme.outline }
        onOpened: Qt.callLater(function() { confirmCancel.forceActiveFocus(Qt.TabFocusReason) })
        onClosed: {
            if (root.storageBridge) root.storageBridge.cancelTransfer()
            Qt.callLater(function() { closeButton.forceActiveFocus(Qt.TabFocusReason) })
        }
        contentItem: SmoothScrollView {
            id: confirmScroll
            Keys.onPressed: function(event) { root.handleBack(event, false, confirmDialog) }
            Keys.onReleased: function(event) { root.handleBack(event, true, confirmDialog) }
            clip: true
            TextArea {
                width: confirmScroll.availableWidth
                readOnly: true; selectByMouse: true; activeFocusOnTab: true
                textFormat: TextEdit.PlainText; renderType: TextEdit.NativeRendering
                Accessible.name: confirmDialog.title
                ContrastOutline { control: parent }
                text: root.pendingKind === "import"
                    ? qsTr("The export contains %1 subscriptions and %2 creator videos. This device has %3 subscriptions and %4 history records. Choose how to import. Replace removes current library records and history; video files are kept.").arg(root.pendingDetails.subscriptions || 0).arg(root.pendingDetails.videos || 0).arg(root.pendingDetails.existing || 0).arg(root.pendingDetails.history || 0)
                    : qsTr("Update %1 completed video records and %2 subscription destinations? %3").arg(root.pendingDetails.videos || 0).arg(root.pendingDetails.folders || 0).arg(root.pendingDetails.mode === "move" ? qsTr("Files will be moved after copying them safely.") : qsTr("Files are already at the new location; only saved paths will change."))
                        + (root.pendingKind === "relocate" && root.pendingDetails.missing > 0
                            ? "\n\n" + qsTr("%1 recorded files could not be found at either location. They will be skipped and marked for retry. Available files will move and the destination will update. Choose Download all videos afterward to fetch the missing videos again.").arg(root.pendingDetails.missing) : "")
                color: Theme.ink; wrapMode: TextEdit.Wrap
            }
        }
        footer: Flow {
            Keys.onPressed: function(event) { root.handleBack(event, false, confirmDialog) }
            Keys.onReleased: function(event) { root.handleBack(event, true, confirmDialog) }
            padding: 12; spacing: 8
            CreatorButton { id: confirmCancel; objectName: "storageConfirmCancel"; text: qsTr("Cancel"); onClicked: { root.storageBridge.cancelTransfer(); confirmDialog.close() } }
            CreatorButton { objectName: "storageConfirmMerge"; visible: root.pendingKind === "import"; text: root.pendingDetails.existing || root.pendingDetails.history ? qsTr("Merge") : qsTr("Import"); onClicked: { root.storageBridge.confirmTransfer("merge"); confirmDialog.close() } }
            CreatorButton { objectName: "storageConfirmReplace"; visible: root.pendingKind === "import" && (root.pendingDetails.existing > 0 || root.pendingDetails.history > 0); text: qsTr("Replace"); onClicked: { root.storageBridge.confirmTransfer("replace"); confirmDialog.close() } }
            CreatorButton { objectName: "storageConfirmRelocate"; visible: root.pendingKind === "relocate"; text: root.pendingDetails.missing > 0 ? qsTr("Move available files") : qsTr("Apply"); onClicked: { root.storageBridge.confirmTransfer(""); confirmDialog.close() } }
        }
    }
}
