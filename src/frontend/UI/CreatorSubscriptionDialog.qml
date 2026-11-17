import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root
    readonly property real fontScale: typeof appSettings !== "undefined" && appSettings ? Math.max(1, appSettings.font_size / 12) : 1
    objectName: "creatorSubscriptionDialog"
    property var preview
    property string editingId: ""
    property var returnFocusItem
    readonly property var qualityValues: ["best", "half", "worst", "2160", "1440", "1080", "720", "540", "480", "360", "250", "240", "144"]
    property string errorText: ""
    readonly property string detectedProvider: {
        if (preview && !preview.isPreview) return preview.providerForUrl(urlField.text.trim())
        var match = urlField.text.trim().match(/^https?:\/\/(?:[a-z0-9-]+\.)*(pornhub\.com|bellesa\.co|redgifs\.com|tube8\.com|pornhat\.com|porndoe\.com|eporner\.com|xvideos\d*\.com|xnxx\d*\.com|xhamster\d*\.com|spankbang\.com|youporn\.com|porn\.com|youjizz\.com|thumbzilla\.com|redtube\.com|porntrex\.com|tnaflix\.com|empflix\.com)\/.+/i)
        return match ? match[1].replace(/\.(com|co)$/, "") : ""
    }
    signal saved()
    parent: Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(540, parent ? parent.width - 24 : 540)
    height: Math.min(690, parent ? parent.height - 24 : 690)
    enter: Transition {}
    exit: Transition {}
    modal: true
    focus: true
    title: editingId ? qsTr("Subscription settings") : qsTr("Add a subscription")
    background: Rectangle { color: Theme.surface; radius: 12; border.width: 1; border.color: Theme.outline }
    Overlay.modal: Rectangle { color: "#99000000" }
    header: Label { text: root.title; color: Theme.ink; font.pixelSize: 22 * root.fontScale; font.bold: true; padding: 20; wrapMode: Text.WordWrap }
    closePolicy: Popup.CloseOnEscape
    function present(id, focusItem) {
        editingId = id || ""; returnFocusItem = focusItem; errorText = ""
        var s = id ? preview.source(id) : null
        urlField.text = s ? s.url : ""; nameField.text = s ? s.name : ""
        startup.checked = s ? s.startup : true; automatic.checked = s ? s.automatic : false
        folder.text = s ? s.folder : preview.defaultFolder
        quality.currentIndex = Math.max(0, qualityValues.indexOf(s ? s.quality.replace(/p$/, "") : preview.defaultQuality))
        kind.currentIndex = s ? Math.max(0, kind.model.indexOf(s.kind)) : 0
        open()
    }
    function save() {
        if (!detectedProvider) { errorText = qsTr("Enter a full profile or collection URL from a supported provider."); urlField.forceActiveFocus(); return }
        if (!nameField.text.trim()) { errorText = qsTr("Give this subscription a name."); nameField.forceActiveFocus(); return }
        if (!folder.text.trim()) { errorText = qsTr("Enter a destination for these videos."); folder.forceActiveFocus(); return }
        if (!editingId && preview.sources.some(function(s) { return s.url.replace(/\/$/, "") === urlField.text.trim().replace(/\/$/, "") })) {
            errorText = qsTr("That URL is already in your subscriptions."); urlField.forceActiveFocus(); return
        }
        preview.save(editingId, {url: urlField.text.trim(), name: nameField.text.trim(), provider: detectedProvider,
            kind: kind.currentText, startup: startup.checked, automatic: automatic.checked,
            quality: qualityValues[quality.currentIndex], folder: folder.text.trim()})
        if (preview.isPreview) { close(); saved() }
    }
    Connections {
        target: root.preview
        ignoreUnknownSignals: true
        function onSaveFinished(id, error) {
            if (!root.opened) return
            if (error) root.errorText = error
            else { root.close(); root.saved() }
        }
    }
    Connections {
        target: root.parent ? root.parent.Window.window : null
        function onActiveFocusItemChanged() {
            if (!root.opened) return
            var item = root.parent.Window.window.activeFocusItem
            var ancestor = item
            while (ancestor && ancestor !== formScroll.contentItem) ancestor = ancestor.parent
            if (!ancestor) return
            var point = item.mapToItem(formScroll.contentItem, 0, 0)
            formScroll.contentItem.contentY = Math.max(0, Math.min(formScroll.contentItem.contentHeight - formScroll.availableHeight,
                Math.min(point.y - 8, Math.max(formScroll.contentItem.contentY, point.y + item.height + 8 - formScroll.availableHeight))))
        }
    }
    onOpened: urlField.forceActiveFocus(Qt.TabFocusReason)
    onClosed: if (returnFocusItem) returnFocusItem.forceActiveFocus(Qt.TabFocusReason)
    contentItem: SmoothScrollView {
        id: formScroll
        clip: true
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        Keys.priority: Keys.AfterItem
        Keys.onPressed: function(event) {
            if (event.key !== Qt.Key_Down && event.key !== Qt.Key_Up) return
            var item = root.parent.Window.window.activeFocusItem
            if (!item) return
            var next = item.nextItemInFocusChain(event.key === Qt.Key_Down)
            var count = 0
            while (next && (!next.activeFocusOnTab || !next.visible || !next.enabled) && count++ < 100)
                next = next.nextItemInFocusChain(event.key === Qt.Key_Down)
            if (next) { next.forceActiveFocus(Qt.TabFocusReason); event.accepted = true }
        }
        ColumnLayout {
            width: formScroll.availableWidth
            spacing: 12
            Label { Layout.fillWidth: true; text: qsTr("Follow a creator, channel, playlist or collection."); wrapMode: Text.WordWrap; color: Theme.muted }
            Label { Layout.fillWidth: true; text: qsTr("Premium unlocks full creator archives, higher resolutions and automatic downloads. Try five videos per subscription free at up to 720p."); wrapMode: Text.WordWrap; color: Theme.ink; font.bold: true }
            Label { text: qsTr("Source URL"); font.bold: true }
            AppTextField { id: urlField; KeyNavigation.priority: KeyNavigation.BeforeItem; KeyNavigation.down: nameField; objectName: "creatorUrlInput"; readOnly: !root.preview.isPreview && root.editingId.length > 0; Layout.fillWidth: true; placeholderText: "https://…"; inputMethodHints: Qt.ImhUrlCharactersOnly | Qt.ImhNoAutoUppercase; selectByMouse: true; Accessible.name: qsTr("Source URL"); onTextEdited: root.errorText = "" }
            Label { Layout.fillWidth: true; text: root.detectedProvider ? (root.preview.isPreview ? qsTr("Provider: %1 · sample resolution") : qsTr("Provider: %1")).arg(root.detectedProvider) : qsTr("Paste an individual source URL, rather than a video link."); color: Theme.muted; font.pixelSize: 12 * root.fontScale; wrapMode: Text.WordWrap }
            Label { text: qsTr("Display name"); font.bold: true }
            AppTextField { id: nameField; KeyNavigation.priority: KeyNavigation.BeforeItem; KeyNavigation.up: urlField; KeyNavigation.down: kind; objectName: "creatorNameInput"; Layout.fillWidth: true; placeholderText: qsTr("e.g. My favourite studio"); selectByMouse: true; Accessible.name: qsTr("Display name") }
            RowLayout {
                Layout.fillWidth: true
                ColumnLayout {
                    Layout.fillWidth: true
                    Label { text: qsTr("Source type"); font.bold: true }
                    AppComboBox { id: kind; enabled: root.preview.isPreview; KeyNavigation.priority: KeyNavigation.BeforeItem; KeyNavigation.up: nameField; KeyNavigation.down: folder; KeyNavigation.right: quality; Layout.fillWidth: true; model: root.preview.isPreview || root.editingId ? [qsTr("Creator"), qsTr("Channel"), qsTr("Performer"), qsTr("Playlist"), qsTr("Collection")] : [qsTr("Automatic")]; Accessible.name: qsTr("Source type") }
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    Label { text: qsTr("Quality"); font.bold: true }
                    AppComboBox { id: quality; KeyNavigation.priority: KeyNavigation.BeforeItem; KeyNavigation.up: nameField; KeyNavigation.down: folder; KeyNavigation.left: kind; Layout.fillWidth: true; model: [qsTr("Best available"), qsTr("Middle quality"), qsTr("Lowest quality"), "2160p", "1440p", "1080p", "720p", "540p", "480p", "360p", "250p", "240p", "144p"]; Accessible.name: qsTr("Quality") }
                }
            }
            Label { text: qsTr("Save videos to"); font.bold: true }
            AppTextField { id: folder; readOnly: root.preview.mobileStorage; KeyNavigation.priority: KeyNavigation.BeforeItem; KeyNavigation.up: kind; KeyNavigation.down: root.preview.mobileStorage ? useAppFolderButton : startup; Layout.fillWidth: true; selectByMouse: true; Accessible.name: qsTr("Download destination") }
            CreatorButton { id: useAppFolderButton; visible: root.preview.mobileStorage; text: qsTr("Use current app download folder"); Keys.onUpPressed: folder.forceActiveFocus(); Keys.onDownPressed: startup.forceActiveFocus(); onClicked: folder.text = root.preview.defaultFolder }
            Label { visible: root.preview.mobileStorage; Layout.fillWidth: true; text: qsTr("Choose a shared download folder in app Settings. This subscription keeps its destination when you resume it."); color: Theme.muted; wrapMode: Text.WordWrap; font.pixelSize: 12 * root.fontScale }
            CreatorCheckBox { id: startup; KeyNavigation.up: root.preview.mobileStorage ? useAppFolderButton : folder; KeyNavigation.down: automatic; text: qsTr("Scan when Porn Fetch starts"); Layout.fillWidth: true }
            CreatorCheckBox { id: automatic; enabled: root.preview.premium || checked; KeyNavigation.up: startup; KeyNavigation.down: saveButton; text: qsTr("Automatically download new videos (Premium)"); Layout.fillWidth: true }
            Label { Layout.fillWidth: true; text: qsTr("The first scan builds your library. Choose Download all videos to download existing videos. New uploads can be downloaded after future startup or manual scans."); wrapMode: Text.WordWrap; color: Theme.muted; font.pixelSize: 12 * root.fontScale }
            Label { Layout.fillWidth: true; visible: root.errorText.length > 0; text: root.errorText; wrapMode: Text.WordWrap; color: Theme.ink; font.bold: true; Accessible.role: Accessible.AlertMessage }
        }
    }
    footer: Item {
        implicitHeight: 70
        RowLayout {
            anchors.fill: parent; anchors.margins: 14; spacing: 10
            Item { Layout.fillWidth: true }
            CreatorButton { id: cancelButton; text: qsTr("Cancel"); Keys.onDownPressed: urlField.forceActiveFocus(); Keys.onUpPressed: (automatic.enabled ? automatic : startup).forceActiveFocus(); Keys.onRightPressed: saveButton.forceActiveFocus(); Keys.onLeftPressed: saveButton.forceActiveFocus(); onClicked: root.close() }
            CreatorButton { id: saveButton; Keys.onDownPressed: urlField.forceActiveFocus(); Keys.onUpPressed: (automatic.enabled ? automatic : startup).forceActiveFocus(); Keys.onLeftPressed: cancelButton.forceActiveFocus(); Keys.onRightPressed: cancelButton.forceActiveFocus(); objectName: "creatorSaveButton"; enabled: !root.preview.saving; text: root.preview.saving ? qsTr("Saving…") : root.editingId ? qsTr("Save changes") : qsTr("Add and scan"); highlighted: true; onClicked: root.save() }
        }
    }
}
