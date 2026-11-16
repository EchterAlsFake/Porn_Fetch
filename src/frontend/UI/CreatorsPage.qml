import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    property bool showBackButton: true
    readonly property real fontScale: typeof appSettings !== "undefined" && appSettings ? Math.max(1, appSettings.font_size / 12) : 1
    objectName: "creatorsPage"
    padding: width < 600 ? 12 : 24
    background: Rectangle { color: Theme.background }
    property alias previewModel: mockData
    property var dataSource: typeof creatorBridge !== "undefined" ? liveData : mockData
    CreatorController { id: liveData; bridge: typeof creatorBridge !== "undefined" ? creatorBridge : null }
    property string selectedId: ""
    property int sourceFilter: 0
    property int videoFilter: 0
    property int videoPage: 0
    property string pendingFocusName: ""
    property bool historyOpen: false
    property bool availabilityDetailsOpen: false
    property bool waitingForAvailabilityFocus: false
    readonly property color successTone: Theme.highContrast ? Theme.ink : Theme.dark ? "#8cdeb5" : "#16633f"
    readonly property color infoTone: Theme.highContrast ? Theme.ink : Theme.dark ? "#a9ceff" : "#254c98"
    readonly property color waitingTone: Theme.highContrast ? Theme.ink : Theme.dark ? "#f1cb88" : "#815000"
    readonly property color newTone: Theme.highContrast ? Theme.ink : Theme.dark ? "#d6b7ff" : "#6736a1"
    function qualityText(value) {
        if (value === "best") return qsTr("Best available")
        if (value === "half") return qsTr("Middle quality")
        if (value === "worst") return qsTr("Lowest quality")
        return /^\d+$/.test(value) ? value + "p" : value
    }
    component DetailTile: Rectangle {
        property string caption
        property string value
        property string note: ""
        property color tone: Theme.ink
        property string valueName: ""
        Layout.fillWidth: true; Layout.fillHeight: true
        implicitHeight: tileContent.implicitHeight + 28
        radius: 9; color: Theme.surface
        border.width: 1; border.color: Qt.rgba(Theme.outline.r, Theme.outline.g, Theme.outline.b, Theme.highContrast ? 1 : 0.5)
        ColumnLayout {
            id: tileContent
            anchors.left: parent.left; anchors.right: parent.right; anchors.top: parent.top; anchors.margins: 14
            spacing: 6
            Label { Layout.fillWidth: true; text: caption; color: Theme.muted; font.pixelSize: 12 * root.fontScale; wrapMode: Text.WordWrap }
            Label { objectName: valueName; Layout.fillWidth: true; text: value; textFormat: Text.PlainText; color: tone; font.pixelSize: 15 * root.fontScale; font.bold: true; wrapMode: Text.WrapAnywhere }
            Label { Layout.fillWidth: true; visible: note.length > 0; text: note; color: Theme.muted; font.pixelSize: 12 * root.fontScale; wrapMode: Text.WordWrap }
        }
    }
    function dateText(value) {
        if (!value) return qsTr("Not yet")
        var date = new Date(String(value).replace(/^(\d{4}-\d\d-\d\d) /, "$1T"))
        return isNaN(date.getTime()) ? value : date.toLocaleString(Qt.locale(), Locale.ShortFormat)
    }
    readonly property bool compact: width < 760
    readonly property bool privateMode: typeof appSettings !== "undefined" && appSettings && appSettings.anonymous_mode === true
    readonly property var selectedSource: { var all = dataSource.sources; return dataSource.source(selectedId) }
    readonly property var selectedCounts: dataSource.counts(selectedSource)
    readonly property bool detailOpen: selectedSource !== null
    readonly property var visibleSources: dataSource.sources.filter(function(s) {
        if (sourceFilter === 1) return dataSource.counts(s).newCount > 0
        if (sourceFilter === 2) return ["incomplete", "stopped"].indexOf(s.scan) >= 0 || dataSource.counts(s).failed > 0
        if (sourceFilter === 3) return s.automatic
        return true
    })
    readonly property var filteredVideos: !dataSource.isPreview ? dataSource.videos : selectedSource ? selectedSource.videos.filter(function(v) {
        return videoFilter === 0 || v.status === ["", "new", "pending", "downloading", "paused", "completed", "failed", "ignored"][videoFilter]
    }) : []
    readonly property int pageCount: Math.max(1, Math.ceil((dataSource.isPreview ? filteredVideos.length : dataSource.videoTotal) / 12))
    readonly property var pageVideos: !dataSource.isPreview ? dataSource.videos : filteredVideos.slice(videoPage * 12, (videoPage + 1) * 12)
    function requestVideoPage() { if (!dataSource.isPreview) dataSource.select(selectedId, videoFilter, videoPage) }
    onSelectedIdChanged: { historyOpen = false; requestVideoPage() }
    onVideoFilterChanged: requestVideoPage()
    onVideoPageChanged: requestVideoPage()
    onPageCountChanged: videoPage = Math.min(videoPage, pageCount - 1)
    function focusInitial() {
        if (root.dataSource.available) addButton.forceActiveFocus(Qt.TabFocusReason)
        else if (root.dataSource.availability === "unavailable") availabilityCheckButton.forceActiveFocus(Qt.TabFocusReason)
        else {
            waitingForAvailabilityFocus = root.dataSource.availability === "checking"
            availabilityHeading.forceActiveFocus(Qt.TabFocusReason)
        }
    }
    function openSource(id, focusItem) {
        selectedId = id; videoFilter = 0; videoPage = 0
        scroll.contentItem.contentY = 0
        Qt.callLater(function() {
            if (root.showBackButton) backButton.forceActiveFocus(Qt.TabFocusReason)
            else videoStatusFilter.forceActiveFocus(Qt.TabFocusReason)
        })
    }
    function goBack() {
        if (!detailOpen) return false
        var previousId = selectedId
        selectedId = ""; scroll.contentItem.contentY = 0
        Qt.callLater(function() {
            var card = root.findControl(root, "creatorSource-" + previousId)
            if (card && card.visible) card.forceActiveFocus(Qt.TabFocusReason)
            else addButton.forceActiveFocus(Qt.TabFocusReason)
        })
        return true
    }
    function reveal(item) {
        if (!item || !item.activeFocus || !root.visible) return
        var ancestor = item
        while (ancestor && ancestor !== scroll.contentItem) ancestor = ancestor.parent
        if (!ancestor) return
        var point = item.mapToItem(scroll.contentItem, 0, 0)
        scroll.contentItem.contentY = Math.max(0, Math.min(scroll.contentItem.contentHeight - scroll.availableHeight,
            Math.min(point.y - 12, Math.max(scroll.contentItem.contentY, point.y + item.height + 12 - scroll.availableHeight))))
    }
    // Retain native text editing and ComboBox navigation; handle unconsumed D-pad keys.
    Keys.priority: Keys.AfterItem
    Keys.onPressed: function(event) {
        if (event.key === Qt.Key_Escape || event.key === Qt.Key_Back) { event.accepted = detailOpen; return }
        if ([Qt.Key_Down, Qt.Key_Up, Qt.Key_Left, Qt.Key_Right].indexOf(event.key) >= 0) {
            var current = root.Window.window.activeFocusItem
            if (!current) return
            var next = current.nextItemInFocusChain((event.key === Qt.Key_Down || event.key === Qt.Key_Right))
            var guard = 0
            while (next && (!next.activeFocusOnTab || !next.visible || !next.enabled) && guard++ < 300) next = next.nextItemInFocusChain((event.key === Qt.Key_Down || event.key === Qt.Key_Right))
            if (next) { next.forceActiveFocus(Qt.TabFocusReason); event.accepted = true }
        }
    }
    Keys.onReleased: function(event) {
        if (event.key === Qt.Key_Escape || event.key === Qt.Key_Back) event.accepted = goBack()
    }
    Connections {
        target: root.Window.window
        function onActiveFocusItemChanged() { Qt.callLater(function() { root.reveal(root.Window.window.activeFocusItem) }) }
    }
    function findControl(item, name) {
        if (item.objectName === name) return item
        for (var i = 0; i < item.children.length; ++i) {
            var found = findControl(item.children[i], name)
            if (found) return found
        }
        return null
    }
    Connections {
        target: root.dataSource
        function onAvailabilityChanged() {
            if (!root.visible || !root.waitingForAvailabilityFocus) return
            Qt.callLater(function() {
                root.focusInitial()
                if (root.dataSource.availability !== "checking") root.waitingForAvailabilityFocus = false
            })
        }
        function onAboutToChange() {
            var item = root.Window.window.activeFocusItem
            root.pendingFocusName = item && item.objectName ? item.objectName : ""
        }
        function onSourcesChanged() {
            var name = root.pendingFocusName
            root.pendingFocusName = ""
            if (!name) return
            Qt.callLater(function() {
                var current = root.Window.window.activeFocusItem
                if (current && current.objectName && current.objectName !== name) return
                var item = root.findControl(root, name)
                if (item && item.visible && item.enabled) item.forceActiveFocus(Qt.TabFocusReason)
                else if (name.indexOf("creatorVideoAction-") === 0) videoStatusFilter.forceActiveFocus(Qt.TabFocusReason)
            })
        }
    }
    CreatorPreviewModel { id: mockData; active: root.visible && root.dataSource.isPreview }
    CreatorSubscriptionDialog { id: subscriptionDialog; preview: root.dataSource }
    Dialog {
        id: removeDialog
        property var returnFocusItem
        parent: Overlay.overlay; anchors.centerIn: parent
        width: Math.min(440, parent ? parent.width - 24 : 440)
        height: Math.min(260, parent ? parent.height - 24 : 260)
        enter: Transition {}
        exit: Transition {}
        modal: true; focus: true; title: qsTr("Remove subscription?")
        background: Rectangle { color: Theme.surface; radius: 12; border.width: 1; border.color: Theme.outline }
        Overlay.modal: Rectangle { color: "#99000000" }
        standardButtons: Dialog.Cancel | Dialog.Ok
        onOpened: standardButton(Dialog.Ok).text = qsTr("Remove subscription")
        contentItem: Label { text: qsTr("This removes the subscription from your library. Downloaded files and history are kept."); wrapMode: Text.WordWrap; color: Theme.ink }
        onAccepted: { var id = root.selectedId; root.goBack(); dataSource.remove(id); Qt.callLater(function() { addButton.forceActiveFocus() }) }
        onRejected: if (returnFocusItem) returnFocusItem.forceActiveFocus()
    }

    SmoothScrollView {
        id: scroll
        anchors.fill: parent; clip: true
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        ColumnLayout {
            width: scroll.availableWidth
            spacing: 20
            RowLayout {
                Layout.fillWidth: true; spacing: 12
                ColumnLayout {
                    Layout.fillWidth: true; spacing: 5
                    Label { text: qsTr("Your creator library"); color: Theme.ink; font.pixelSize: (root.compact ? 26 : 32) * root.fontScale; font.weight: Font.DemiBold; Layout.fillWidth: true; wrapMode: Text.WordWrap }
                    Label { text: qsTr("Follow once. Keep your collection up to date."); color: Theme.muted; Layout.fillWidth: true; wrapMode: Text.WordWrap }
                }
                CreatorButton { id: addButton; objectName: "creatorAddButton"; enabled: root.dataSource.available; text: root.compact ? qsTr("+ Add") : qsTr("+ Add subscription"); highlighted: true; onClicked: subscriptionDialog.present("", this) }
            }
            Rectangle {
                Layout.fillWidth: true; implicitHeight: premiumNotice.implicitHeight + 32
                color: Theme.surface; radius: 10; border.width: Theme.highContrast ? 2 : 1; border.color: root.newTone
                ColumnLayout {
                    id: premiumNotice
                    anchors.left: parent.left; anchors.right: parent.right; anchors.top: parent.top; anchors.margins: 16
                    spacing: 10
                    Label { objectName: "creatorPremiumNotice"; Layout.fillWidth: true; text: root.dataSource.premium ? qsTr("Premium creator archives") : qsTr("Creator archives are a Premium feature"); color: root.newTone; font.pixelSize: 18 * root.fontScale; font.bold: true; wrapMode: Text.WordWrap }
                    Label { Layout.fillWidth: true; text: root.dataSource.premium ? qsTr("Full scans, the highest available quality and automatic downloads are unlocked.") : qsTr("Try it free: download and resume five videos per subscription at up to 720p. Premium unlocks full creator scans, higher resolutions and automatic downloads."); color: Theme.ink; wrapMode: Text.WordWrap }
                    CreatorButton { visible: !root.dataSource.premium; text: qsTr("Get Premium ↗"); onClicked: Qt.openUrlExternally("https://pornfetch.to"); Accessible.description: qsTr("Open pornfetch.to in your browser. Activate your license in Settings.") }
                }
            }
            Rectangle {
                visible: root.dataSource.isPreview
                Layout.fillWidth: true; implicitHeight: previewNotice.implicitHeight + 24; radius: 8
                color: Qt.rgba(Theme.accent.r, Theme.accent.g, Theme.accent.b, Theme.highContrast ? 0 : 0.08)
                border.color: Theme.highContrast ? Theme.ink : Qt.rgba(Theme.accent.r, Theme.accent.g, Theme.accent.b, 0.35); border.width: 1
                Label { id: previewNotice; anchors.fill: parent; anchors.margins: 12; text: qsTr("INTERACTIVE PREVIEW  ·  Sample subscriptions and videos. Changes reset when the app closes; scans and downloads are simulated."); color: Theme.muted; wrapMode: Text.WordWrap; font.pixelSize: 12 * root.fontScale }
            }
            Label { Layout.fillWidth: true; visible: dataSource.message.length > 0; text: dataSource.message; color: Theme.ink; wrapMode: Text.WordWrap; Accessible.role: Accessible.AlertMessage }
            Rectangle {
                objectName: "creatorAvailabilityNotice"
                visible: root.dataSource.availability !== "ready"
                Layout.fillWidth: true; implicitHeight: availabilityContent.implicitHeight + 32
                radius: 10; color: Theme.surface; border.width: 1; border.color: Theme.accent
                ColumnLayout {
                    id: availabilityContent
                    anchors.left: parent.left; anchors.right: parent.right; anchors.top: parent.top; anchors.margins: 16
                    spacing: 12
                    Label {
                        id: availabilityHeading
                        objectName: "creatorAvailabilityTitle"; Layout.fillWidth: true
                        text: root.dataSource.availability === "checking" ? qsTr("Checking PocketBase…") : root.dataSource.availability === "unsupported" ? qsTr("Creator storage is not supported yet") : qsTr("PocketBase is unavailable")
                        color: Theme.ink; font.bold: true; font.pixelSize: 18 * root.fontScale; wrapMode: Text.WordWrap
                        Accessible.role: Accessible.AlertMessage
                    }
                    Label {
                        Layout.fillWidth: true; color: Theme.muted; wrapMode: Text.WordWrap
                        text: root.dataSource.availability === "checking" ? qsTr("Checking the local database before you add a subscription. This may take a moment.") : qsTr("Creator subscriptions need PocketBase. Follow these steps before adding a source.")
                    }
                    TextArea {
                        visible: root.dataSource.availability !== "checking"
                        Layout.fillWidth: true; text: root.dataSource.availabilityHelp
                        readOnly: true; selectByMouse: true; activeFocusOnTab: visible
                        textFormat: TextEdit.PlainText; renderType: Text.NativeRendering
                        wrapMode: TextEdit.Wrap; color: Theme.ink; padding: 0
                        font.pixelSize: 13 * root.fontScale
                        background: Rectangle { color: "transparent"; border.width: parent.activeFocus ? 2 : 0; border.color: Theme.accent; radius: 4 }
                        Accessible.name: qsTr("PocketBase setup instructions")
                    }
                    Flow {
                        visible: root.dataSource.availability === "unavailable"
                        Layout.fillWidth: true; spacing: 8
                        CreatorButton { visible: root.dataSource.canManageComponents; text: qsTr("Manage components"); onClicked: root.dataSource.manageComponents() }
                        CreatorButton { id: availabilityCheckButton; objectName: "creatorCheckAvailabilityButton"; text: qsTr("Check again"); highlighted: true; onClicked: { root.waitingForAvailabilityFocus = true; root.availabilityDetailsOpen = false; root.dataSource.checkAvailability() } }
                        CreatorButton { visible: root.dataSource.availabilityError.length > 0; text: root.availabilityDetailsOpen ? qsTr("Hide error details") : qsTr("Show error details"); flat: true; onClicked: root.availabilityDetailsOpen = !root.availabilityDetailsOpen }
                    }
                    TextArea {
                        visible: root.availabilityDetailsOpen && root.dataSource.availability === "unavailable"
                        Layout.fillWidth: true; text: root.dataSource.availabilityError
                        readOnly: true; selectByMouse: true; activeFocusOnTab: visible
                        textFormat: TextEdit.PlainText; renderType: Text.NativeRendering
                        wrapMode: TextEdit.Wrap; color: Theme.muted; padding: 4
                        background: Rectangle { color: Theme.background; border.width: parent.activeFocus ? 2 : 0; border.color: Theme.accent; radius: 4 }
                        Accessible.name: qsTr("PocketBase error details")
                    }
                }
            }

            // Overview
            GridLayout {
                visible: !root.detailOpen; Layout.fillWidth: true; columns: root.compact ? 2 : 4; columnSpacing: 12; rowSpacing: 12
                Repeater {
                    model: [{label: qsTr("Subscriptions"), value: dataSource.sources.length}, {label: qsTr("New videos"), value: dataSource.total("newCount")}, {label: qsTr("Downloaded"), value: dataSource.total("completed")}, {label: qsTr("Needs attention"), value: dataSource.total("failed")}]
                    delegate: Rectangle {
                        required property var modelData
                        Layout.fillWidth: true; Layout.preferredWidth: 1; implicitHeight: 96; radius: 10; color: Theme.surface
                        border.width: 1; border.color: Qt.rgba(Theme.outline.r, Theme.outline.g, Theme.outline.b, Theme.highContrast ? 1 : 0.3)
                        ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 4
                            Label { text: modelData.value; font.pixelSize: 28 * root.fontScale; font.weight: Font.DemiBold; color: Theme.ink }
                            Label { text: modelData.label; color: Theme.muted; font.pixelSize: 12 * root.fontScale; Layout.fillWidth: true; elide: Text.ElideRight }
                        }
                    }
                }
            }
            RowLayout {
                visible: !root.detailOpen; Layout.fillWidth: true
                Label { text: qsTr("Subscriptions"); font.pixelSize: 20 * root.fontScale; font.bold: true; color: Theme.ink; Layout.fillWidth: true }
                AppComboBox { objectName: "creatorSourceFilter"; Layout.preferredWidth: root.compact ? 170 : 210; model: [qsTr("All sources"), qsTr("With new videos"), qsTr("Needs attention"), qsTr("Auto-download on")]; Accessible.name: qsTr("Filter subscriptions"); onActivated: root.sourceFilter = currentIndex }
            }
            GridLayout {
                visible: !root.detailOpen; Layout.fillWidth: true
                columns: root.width >= 1250 ? 3 : root.width >= 760 ? 2 : 1
                columnSpacing: 16; rowSpacing: 16
                Repeater {
                    model: root.visibleSources
                    delegate: CreatorSourceCard {
                        required property var modelData
                        Layout.fillWidth: true; Layout.preferredWidth: 1
                        objectName: "creatorSource-" + modelData.id
                        sourceData: modelData; counts: dataSource.counts(modelData); privateMode: root.privateMode
                        onClicked: root.openSource(modelData.id, this)
                    }
                }
            }
            ColumnLayout {
                visible: !root.detailOpen && root.visibleSources.length === 0
                Layout.fillWidth: true; Layout.topMargin: 30; Layout.bottomMargin: 36; spacing: 12
                Label { Layout.alignment: Qt.AlignHCenter; text: dataSource.sources.length ? qsTr("No subscriptions match this filter") : qsTr("Your collection starts here"); font.pixelSize: 22 * root.fontScale; font.bold: true; color: Theme.ink; wrapMode: Text.WordWrap; Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter }
                Label { Layout.fillWidth: true; text: dataSource.sources.length ? qsTr("Choose another filter to see your sources.") : qsTr("Add a creator or collection URL to discover their videos in one place."); color: Theme.muted; wrapMode: Text.WordWrap; horizontalAlignment: Text.AlignHCenter }
                CreatorButton { Layout.alignment: Qt.AlignHCenter; enabled: root.dataSource.available; text: qsTr("Add subscription"); onClicked: subscriptionDialog.present("", this) }
            }

            // Source detail
            ColumnLayout {
                visible: root.detailOpen; Layout.fillWidth: true; spacing: 16
                CreatorButton { id: backButton; visible: root.showBackButton; objectName: "creatorBackButton"; text: qsTr("‹ All subscriptions"); flat: true; onClicked: root.goBack() }
                RowLayout {
                    Layout.fillWidth: true
                    ColumnLayout {
                        Layout.fillWidth: true
                        Label { Layout.fillWidth: true; text: root.privateMode ? qsTr("Hidden subscription") : root.selectedSource ? root.selectedSource.name : ""; textFormat: Text.PlainText; font.pixelSize: 28 * root.fontScale; font.bold: true; color: Theme.ink; wrapMode: Text.WordWrap }
                        Label { Layout.fillWidth: true; text: root.selectedSource ? root.selectedSource.provider + " · " + root.selectedSource.kind : ""; color: Theme.muted }
                    }
                    CreatorStatus { status: root.selectedSource ? root.selectedSource.scan : "complete" }
                }
                Label { Layout.fillWidth: true; visible: !root.privateMode; text: root.selectedSource ? root.selectedSource.url : ""; textFormat: Text.PlainText; color: Theme.muted; wrapMode: Text.WrapAnywhere; font.pixelSize: 12 * root.fontScale }
                Rectangle {
                    visible: root.selectedSource !== null && ["incomplete", "stopped", "scanning"].indexOf(root.selectedSource.scan) >= 0
                    Layout.fillWidth: true; radius: 8; color: Theme.surface
                    implicitHeight: scanInfo.implicitHeight + 24
                    border.width: 1; border.color: Theme.outline
                    ColumnLayout {
                        id: scanInfo; anchors.left: parent.left; anchors.right: parent.right; anchors.top: parent.top; anchors.margins: 12
                        Label { Layout.fillWidth: true; color: Theme.ink; wrapMode: Text.WordWrap
                            text: !root.selectedSource ? "" : root.selectedSource.scan === "incomplete" ? (root.selectedSource.error || qsTr("Scan incomplete. A page could not be reached. Your discovered videos are safe; scan again to retry.")) : root.selectedSource.scan === "stopped" ? qsTr("Scan stopped. Discovered videos are kept. Scan again whenever you are ready.") : qsTr("Discovering videos. You can browse and download the videos already found.") }
                        ProgressBar { visible: root.selectedSource !== null && root.selectedSource.scan === "scanning"; Layout.fillWidth: true; indeterminate: visible; Accessible.name: qsTr("Scanning source pages") }
                        Label { Layout.fillWidth: true; visible: root.selectedSource !== null && root.selectedSource.scan === "scanning"; text: root.selectedSource ? qsTr("%1 videos found").arg(root.selectedSource.scan_discovered || 0) + (root.selectedSource.scan_pages > 0 ? qsTr(" · %1 pages reached").arg(root.selectedSource.scan_pages) : "") : ""; color: Theme.muted; wrapMode: Text.WordWrap }
                        CreatorButton { visible: root.dataSource.isPreview && root.selectedSource !== null && root.selectedSource.scan === "scanning"; text: qsTr("Finish sample scan"); onClicked: dataSource.finishScan(root.selectedId) }
                    }
                }
                Flow {
                    Layout.fillWidth: true; spacing: 8
                    CreatorButton { objectName: "creatorDownloadButton"; text: !root.dataSource.premium ? (root.selectedCounts.paused > 0 ? qsTr("Resume free preview") : qsTr("Download free preview")) : root.selectedCounts.paused > 0 ? qsTr("Resume / download pending") : qsTr("Download pending"); highlighted: true; enabled: root.selectedCounts.newCount + root.selectedCounts.pending + root.selectedCounts.paused > 0; onClicked: dataSource.bulk(root.selectedId, "download") }
                    CreatorButton { text: qsTr("Pause downloads"); enabled: root.selectedCounts.pending + root.selectedCounts.downloading > 0; onClicked: dataSource.bulk(root.selectedId, "pause") }
                    CreatorButton { objectName: "creatorScanButton"; text: root.selectedSource && root.selectedSource.scan === "scanning" ? qsTr("Stop scan") : qsTr("Scan now"); onClicked: dataSource.scan(root.selectedId) }
                    CreatorButton { text: qsTr("Settings"); onClicked: subscriptionDialog.present(root.selectedId, this) }
                }
                Flow {
                    objectName: "creatorSummary"; Layout.fillWidth: true; spacing: 10
                    Repeater {
                        model: [
                            {caption: qsTr("Videos"), count: root.selectedCounts.total, tone: Theme.ink},
                            {caption: qsTr("Downloaded"), count: root.selectedCounts.completed, tone: root.successTone},
                            {caption: qsTr("Queued"), count: root.selectedCounts.pending, tone: root.infoTone},
                            {caption: qsTr("Paused"), count: root.selectedCounts.paused, tone: root.waitingTone},
                            {caption: qsTr("New"), count: root.selectedCounts.newCount, tone: root.newTone}]
                        delegate: Rectangle {
                            required property var modelData
                            width: Math.max(108, countLabel.implicitWidth + 32); height: metricColumn.implicitHeight + 24
                            radius: 9; color: Theme.highContrast ? Theme.surface : Qt.rgba(modelData.tone.r, modelData.tone.g, modelData.tone.b, 0.08)
                            border.width: 1; border.color: Qt.rgba(modelData.tone.r, modelData.tone.g, modelData.tone.b, Theme.highContrast ? 1 : 0.45)
                            Column { id: metricColumn; anchors.left: parent.left; anchors.top: parent.top; anchors.margins: 12; spacing: 5
                                Label { text: modelData.count; color: modelData.tone; font.pixelSize: 22 * root.fontScale; font.bold: true }
                                Label { id: countLabel; text: modelData.caption; color: Theme.ink; font.pixelSize: 13 * root.fontScale }
                            }
                        }
                    }
                }
                GridLayout {
                    Layout.fillWidth: true; columns: root.width < 600 ? 1 : 2; columnSpacing: 12; rowSpacing: 12
                    DetailTile { caption: qsTr("Quality"); valueName: "creatorQualityValue"; value: root.selectedSource ? root.qualityText(root.selectedSource.quality) : ""; tone: root.newTone; note: root.dataSource.premium ? "" : qsTr("Free preview downloads are limited to 720p.") }
                    DetailTile { caption: qsTr("Destination"); valueName: "creatorDestinationValue"; value: root.privateMode ? qsTr("Destination hidden") : root.selectedSource ? root.selectedSource.folder : "" }
                    DetailTile { caption: qsTr("Last attempt"); valueName: "creatorLastAttemptValue"; value: root.selectedSource ? root.dateText(root.selectedSource.last_scan || root.selectedSource.lastScan) : ""; tone: root.infoTone }
                    DetailTile { caption: qsTr("Last complete scan"); valueName: "creatorLastCompleteValue"; value: root.selectedSource ? root.dateText(root.selectedSource.last_success) : ""; tone: root.selectedSource && root.selectedSource.last_success ? root.successTone : root.waitingTone; note: root.dataSource.premium ? "" : qsTr("Full scans require Premium.") }
                }
                CreatorButton { objectName: "creatorScanHistoryButton"; text: root.historyOpen ? qsTr("Hide recent scans") : qsTr("Show recent scans"); flat: true; onClicked: root.historyOpen = !root.historyOpen }
                ColumnLayout {
                    visible: root.historyOpen; Layout.fillWidth: true; spacing: 10
                    Label { text: qsTr("Recent scans (latest 10)"); color: Theme.ink; font.bold: true }
                    Label { visible: root.dataSource.scanHistory.length === 0; text: qsTr("No scan attempts yet."); color: Theme.muted }
                    Repeater {
                        model: root.historyOpen ? root.dataSource.scanHistory : []
                        delegate: ColumnLayout {
                            required property var modelData
                            Layout.fillWidth: true; spacing: 4
                            Label { Layout.fillWidth: true; text: root.dateText(modelData.started) + " · " + (modelData.trigger === "startup" ? qsTr("Startup") : modelData.trigger === "initial" ? qsTr("First scan") : qsTr("Manual")); color: Theme.ink; wrapMode: Text.WordWrap }
                            CreatorStatus { status: modelData.status === "running" ? "scanning" : modelData.status === "cancelled" ? "stopped" : modelData.status }
                            Label { Layout.fillWidth: true; text: qsTr("%1 videos found").arg(modelData.discovered || 0) + (modelData.pages > 0 ? qsTr(" · %1 pages reached").arg(modelData.pages) : ""); color: Theme.muted; wrapMode: Text.WordWrap }
                            Label { Layout.fillWidth: true; visible: !!modelData.finished; text: qsTr("Finished: %1").arg(root.dateText(modelData.finished)); color: Theme.muted; wrapMode: Text.WordWrap }
                            Label { Layout.fillWidth: true; visible: !!modelData.error; text: modelData.error || ""; textFormat: Text.PlainText; color: Theme.muted; wrapMode: Text.WordWrap }
                        }
                    }
                }
                RowLayout {
                    Layout.fillWidth: true
                    Label { text: qsTr("Video library"); font.pixelSize: 20 * root.fontScale; font.bold: true; color: Theme.ink; Layout.fillWidth: true }
                    AppComboBox { id: videoStatusFilter; objectName: "creatorVideoFilter"; Layout.preferredWidth: root.compact ? 170 : 210; model: [qsTr("All videos"), qsTr("New"), qsTr("Queued"), qsTr("Downloading"), qsTr("Paused"), qsTr("Downloaded"), qsTr("Needs attention"), qsTr("Ignored")]; currentIndex: root.videoFilter; Accessible.name: qsTr("Filter videos"); onActivated: { root.videoFilter = currentIndex; root.videoPage = 0 } }
                }
                Repeater {
                    model: root.pageVideos
                    delegate: Rectangle {
                        id: videoRow
                        required property var modelData
                        Layout.fillWidth: true; implicitHeight: rowLayout.implicitHeight + 24; radius: 8; color: Theme.surface
                        border.width: 1; border.color: Qt.rgba(Theme.outline.r, Theme.outline.g, Theme.outline.b, Theme.highContrast ? 1 : 0.25)
                        GridLayout {
                            id: rowLayout; anchors.left: parent.left; anchors.right: parent.right; anchors.top: parent.top; anchors.margins: 12
                            columns: root.compact ? 1 : 3; columnSpacing: 18; rowSpacing: 10
                            ColumnLayout {
                                Layout.fillWidth: true; spacing: 4
                                Label { Layout.fillWidth: true; text: root.privateMode ? qsTr("Hidden video") : videoRow.modelData.title; textFormat: Text.PlainText; color: Theme.ink; font.bold: true; wrapMode: Text.WordWrap }
                                Label { text: [videoRow.modelData.duration, videoRow.modelData.quality, videoRow.modelData.published].filter(function(value) { return !!value }).join(" · ") || qsTr("Details load when downloading"); color: Theme.muted; font.pixelSize: 12 * root.fontScale }
                                ProgressBar { visible: ["downloading", "paused"].indexOf(videoRow.modelData.status) >= 0; Layout.fillWidth: true; from: 0; to: 100; value: videoRow.modelData.progress; Accessible.name: qsTr("Video progress"); Accessible.description: value + "%" }
                                Label { visible: videoRow.modelData.status === "failed" || (videoRow.modelData.status === "paused" && !!videoRow.modelData.error); text: videoRow.modelData.error || qsTr("Connection interrupted. Ready to retry."); color: Theme.muted; font.pixelSize: 12 * root.fontScale; Layout.fillWidth: true; wrapMode: Text.WordWrap }
                            }
                            CreatorStatus { status: videoRow.modelData.status }
                            RowLayout {
                                CreatorButton {
                                    objectName: "creatorVideoAction-" + videoRow.modelData.id
                                    text: videoRow.modelData.status === "downloading" ? qsTr("Pause") : videoRow.modelData.status === "failed" ? qsTr("Retry") : videoRow.modelData.status === "paused" ? qsTr("Resume") : videoRow.modelData.status === "ignored" ? qsTr("Restore") : qsTr("Download")
                                    visible: videoRow.modelData.status !== "completed"
                                    Accessible.name: text + " " + (root.privateMode ? qsTr("video") : videoRow.modelData.title)
                                    onClicked: { var focus = videoStatusFilter; dataSource.videoAction(root.selectedId, videoRow.modelData.id, videoRow.modelData.status === "downloading" ? "paused" : videoRow.modelData.status === "ignored" ? "new" : "downloading"); Qt.callLater(function() { focus.forceActiveFocus() }) }
                                }
                                CreatorButton {
                                    text: qsTr("Ignore"); flat: true; visible: ["new", "failed", "pending"].indexOf(videoRow.modelData.status) >= 0
                                    Accessible.name: qsTr("Ignore %1").arg(root.privateMode ? qsTr("video") : videoRow.modelData.title)
                                    onClicked: { dataSource.videoAction(root.selectedId, videoRow.modelData.id, "ignored"); Qt.callLater(function() { videoStatusFilter.forceActiveFocus() }) }
                                }
                            }
                        }
                    }
                }
                Label { visible: root.filteredVideos.length === 0; Layout.fillWidth: true; Layout.topMargin: 24; Layout.bottomMargin: 24; text: root.selectedCounts.total === 0 ? qsTr("Your first scan is getting started. Discovered videos will appear here.") : qsTr("No videos in this view. Choose another status to explore the library."); color: Theme.muted; wrapMode: Text.WordWrap; horizontalAlignment: Text.AlignHCenter }
                RowLayout {
                    Layout.fillWidth: true; visible: root.filteredVideos.length > 0
                    CreatorButton { id: previousPageButton; text: qsTr("Previous"); enabled: root.videoPage > 0; onClicked: { root.videoPage--; videoStatusFilter.forceActiveFocus() } }
                    Label { Layout.fillWidth: true; text: qsTr("Page %1 of %2").arg(root.videoPage + 1).arg(root.pageCount); color: Theme.muted; horizontalAlignment: Text.AlignHCenter }
                    CreatorButton { text: qsTr("Next"); enabled: root.videoPage + 1 < root.pageCount; onClicked: { root.videoPage++; videoStatusFilter.forceActiveFocus() } }
                }
                Rectangle { Layout.fillWidth: true; implicitHeight: 1; color: Theme.outline; opacity: 0.3 }
                RowLayout {
                    Layout.fillWidth: true
                    CreatorButton { text: qsTr("Retry failed"); enabled: root.selectedCounts.failed > 0; onClicked: dataSource.bulk(root.selectedId, "retry") }
                    Item { Layout.fillWidth: true }
                    CreatorButton { text: qsTr("Remove subscription"); flat: true; onClicked: { removeDialog.returnFocusItem = this; removeDialog.open() } }
                }
            }
            Label { Layout.fillWidth: true; text: qsTr("Checks run on startup and when you choose Scan now. Porn Fetch needs to be open to scan and download."); color: Theme.muted; wrapMode: Text.WordWrap; font.pixelSize: 12 * root.fontScale; Layout.topMargin: 8; Layout.bottomMargin: 8 }
        }
    }
}
