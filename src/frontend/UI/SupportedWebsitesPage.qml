import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    // The parent supplies the actual width. Deriving its size hint from the
    // responsive content feeds that width back into StackLayout/Pane sizing.
    implicitWidth: 640
    objectName: "supportedWebsitesPage"
    signal backRequested()
    property bool showBackButton: true
    property var websites: backend.supportedWebsites
    readonly property real scale: appSettings.font_size / 12
    readonly property var filteredWebsites: {
        const query = search.text.trim().toLowerCase()
        return websites.filter(site => (!query || (site.name + " " + site.domain).toLowerCase().includes(query))
                               && (typeFilter.currentIndex !== 1 || site.profiles)
                               && (typeFilter.currentIndex !== 2 || site.collections))
    }
    padding: width < 600 ? 12 : 24
    background: Rectangle { color: Theme.background }

    function focusInitial() { search.forceActiveFocus(Qt.TabFocusReason) }
    function focusCard(index) {
        const card = cards.itemAt(Math.max(0, Math.min(cards.count - 1, index)))
        if (card) card.forceActiveFocus(Qt.TabFocusReason)
    }
    function reveal(card) {
        Qt.callLater(function() {
            const y = card.mapToItem(scroller.contentItem, 0, 0).y
            scroller.contentY = Math.max(0, Math.min(scroller.contentHeight - scroller.height,
                y < scroller.contentY ? y : Math.max(scroller.contentY, y + card.height - scroller.height)))
        })
    }
    // Navigate on release so Android's window-level Back handler cannot act
    // on the same key after focus has already returned to the previous page.
    Keys.onEscapePressed: event => { event.accepted = true }
    Keys.onBackPressed: event => { event.accepted = true }
    Keys.onReleased: event => {
        if (event.key === Qt.Key_Back || event.key === Qt.Key_Escape) {
            event.accepted = true
            root.backRequested()
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 12
        RowLayout {
            Layout.fillWidth: true
            AppButton {
                id: back
                visible: root.showBackButton
                Layout.minimumHeight: 48
                objectName: "websitesBackButton"
                text: qsTr("Back")
                Accessible.name: qsTr("Back from supported websites")
                onClicked: root.backRequested()
                KeyNavigation.right: search
                KeyNavigation.down: search
            }
            Label {
                Layout.fillWidth: true
                text: qsTr("Supported websites")
                font.pixelSize: 25 * root.scale
                font.bold: true
                color: Theme.ink
                wrapMode: Text.WordWrap
            }
        }
        Label {
            Layout.fillWidth: true
            text: qsTr("Find your website. See which links you can use.")
            color: Theme.muted
            wrapMode: Text.WordWrap
        }
        GridLayout {
            Layout.fillWidth: true
            columns: root.width < 600 ? 1 : 2
            columnSpacing: 12
            rowSpacing: 4
            AppTextField {
                id: search
                objectName: "websiteSearch"
                Layout.fillWidth: true
                Layout.minimumHeight: 48
                placeholderText: qsTr("Filter by website name or domain")
                Accessible.name: placeholderText
                selectByMouse: true
                inputMethodHints: Qt.ImhNoAutoUppercase | Qt.ImhNoPredictiveText
                KeyNavigation.up: back
                Keys.onDownPressed: typeFilter.forceActiveFocus(Qt.TabFocusReason)
                onAccepted: root.focusCard(0)
            }
            AppComboBox {
                id: typeFilter
                objectName: "websiteTypeFilter"
                Layout.fillWidth: true
                Layout.minimumHeight: 48
                model: [qsTr("All websites"), qsTr("Profiles and channels"), qsTr("Playlists and collections")]
                Accessible.name: qsTr("Filter by supported link type")
                KeyNavigation.up: search
                Keys.onDownPressed: event => {
                    if (!popup.visible) { root.focusCard(0); event.accepted = true }
                    else event.accepted = false
                }
            }
        }
        Label {
            Layout.fillWidth: true
            text: qsTr("%1 of %2 websites · Select a card for link guidance").arg(root.filteredWebsites.length).arg(root.websites.length)
            color: Theme.muted
            wrapMode: Text.WordWrap
            font.pixelSize: 12 * root.scale
        }
        ScrollView {
            id: scroll
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            contentWidth: availableWidth
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
            Flickable {
                id: scroller
                objectName: "websitesScroller"
                boundsBehavior: Flickable.StopAtBounds
                contentWidth: width
                contentHeight: content.implicitHeight
                ColumnLayout {
                    id: content
                    width: scroller.width
                    spacing: 12
                    Label {
                        Layout.fillWidth: true
                        visible: root.filteredWebsites.length === 0
                        text: qsTr("No matching websites. Try another name or choose All websites.")
                        color: Theme.ink
                        wrapMode: Text.WordWrap
                        padding: 24
                    }
                    GridLayout {
                        id: grid
                        Layout.fillWidth: true
                        columns: Math.max(1, Math.min(3, Math.floor(scroller.width / (290 * root.scale))))
                        columnSpacing: 12
                        rowSpacing: 12
                        Repeater {
                            id: cards
                            model: root.filteredWebsites
                            delegate: AbstractButton {
                                id: card
                                required property var modelData
                                required property int index
                                objectName: "websiteCard-" + modelData.id
                                Layout.fillWidth: true
                                Layout.preferredWidth: 1
                                Layout.alignment: Qt.AlignTop
                                implicitHeight: cardContent.implicitHeight + 32
                                padding: 16
                                checkable: true
                                activeFocusOnTab: true
                                Accessible.name: modelData.name + ". " + capabilities.text
                                Accessible.description: checked ? modelData.details : qsTr("Activate to show supported link guidance")
                                onActiveFocusChanged: if (activeFocus) root.reveal(card)
                                onCheckedChanged: if (activeFocus) root.reveal(card)
                                Keys.onReturnPressed: toggle()
                                Keys.onEnterPressed: toggle()
                                Keys.onSelectPressed: toggle()
                                onClicked: if (activeFocus) root.reveal(card)
                                Keys.onLeftPressed: root.focusCard(index - 1)
                                Keys.onRightPressed: root.focusCard(index + 1)
                                Keys.onUpPressed: {
                                    if (index < grid.columns) typeFilter.forceActiveFocus(Qt.TabFocusReason)
                                    else root.focusCard(index - grid.columns)
                                }
                                Keys.onDownPressed: root.focusCard(index + grid.columns)
                                background: Rectangle {
                                    radius: 16
                                    color: card.down ? Theme.background : Theme.surface
                                    border.width: card.visualFocus ? 3 : 1
                                    border.color: card.visualFocus || card.hovered || card.checked ? Theme.accent : Theme.outline
                                }
                                contentItem: ColumnLayout {
                                    id: cardContent
                                    spacing: 10
                                    RowLayout {
                                        Layout.fillWidth: true
                                        Rectangle {
                                            Layout.preferredWidth: 42
                                            Layout.preferredHeight: 42
                                            radius: 12
                                            color: Theme.accent
                                            Label {
                                                anchors.centerIn: parent
                                                text: card.modelData.name.substring(0, 1)
                                                font.pixelSize: 21 * root.scale
                                                font.bold: true
                                                color: Theme.selectionInk
                                            }
                                        }
                                        ColumnLayout {
                                            Layout.fillWidth: true
                                            spacing: 2
                                            Label {
                                                Layout.fillWidth: true
                                                text: card.modelData.name
                                                color: Theme.ink
                                                font.pixelSize: 18 * root.scale
                                                font.bold: true
                                                wrapMode: Text.WordWrap
                                            }
                                            Label {
                                                Layout.fillWidth: true
                                                text: card.modelData.domain
                                                color: Theme.muted
                                                font.pixelSize: 12 * root.scale
                                                wrapMode: Text.WrapAnywhere
                                            }
                                        }
                                        Label {
                                            text: card.checked ? "−" : "+"
                                            color: Theme.accent
                                            font.pixelSize: 22 * root.scale
                                        }
                                    }
                                    Label {
                                        id: capabilities
                                        Layout.fillWidth: true
                                        text: [qsTr("Videos"), card.modelData.profiles ? qsTr("Profiles / channels") : "",
                                               card.modelData.collections ? qsTr("Playlists / collections") : ""].filter(Boolean).join(" · ")
                                        color: Theme.ink
                                        font.pixelSize: 13 * root.scale
                                        wrapMode: Text.WordWrap
                                    }
                                    Label {
                                        Layout.fillWidth: true
                                        visible: card.checked
                                        text: card.modelData.details
                                        textFormat: Text.PlainText
                                        color: Theme.muted
                                        font.pixelSize: 13 * root.scale
                                        wrapMode: Text.Wrap
                                    }
                                }
                            }
                        }
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Use Video URL for individual videos, Model URL for profiles or channels, and Playlist/Collection URL for supported lists. Website homepages and keyword search are not download sources.")
                        color: Theme.muted
                        wrapMode: Text.WordWrap
                        font.pixelSize: 13 * root.scale
                        topPadding: 8
                        bottomPadding: 16
                    }
                }
            }
        }
    }
}
