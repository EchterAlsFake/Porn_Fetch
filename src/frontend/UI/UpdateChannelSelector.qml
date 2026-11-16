import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    Layout.fillWidth: true
    Label { text: qsTr("Update channel"); wrapMode: Text.Wrap; Layout.fillWidth: true }
    AppComboBox {
        id: selector
        objectName: "updateChannelSelector"
        Layout.fillWidth: true
        implicitHeight: 48
        model: [qsTr("Stable"), qsTr("Beta")]
        currentIndex: appSettings.update_channel === "beta" ? 1 : 0
        Accessible.name: qsTr("Update channel")
        focusPolicy: Qt.StrongFocus
        property bool closingWithBack: false
        function moveFocus(forward) {
            const target = nextItemInFocusChain(forward)
            if (target) target.forceActiveFocus(Qt.TabFocusReason)
        }
        Keys.onUpPressed: function(event) {
            if (popup.visible) event.accepted = false
            else moveFocus(false)
        }
        Keys.onDownPressed: function(event) {
            if (popup.visible) event.accepted = false
            else moveFocus(true)
        }
        Keys.onLeftPressed: function(event) {
            if (popup.visible) event.accepted = false
            else moveFocus(false)
        }
        Keys.onRightPressed: function(event) {
            if (popup.visible) event.accepted = false
            else moveFocus(true)
        }
        Keys.onReturnPressed: function(event) {
            if (popup.visible) event.accepted = false
            else popup.open()
        }
        Keys.onEnterPressed: function(event) {
            if (popup.visible) event.accepted = false
            else popup.open()
        }
        Keys.onPressed: function(event) {
            if (event.key === Qt.Key_Select) {
                if (popup.visible) {
                    if (highlightedIndex >= 0) {
                        activated(highlightedIndex)
                    }
                    popup.close()
                    forceActiveFocus()
                } else popup.open()
                event.accepted = true
            } else if ((event.key === Qt.Key_Back || event.key === Qt.Key_Escape) && popup.visible) {
                closingWithBack = true
                popup.close()
                forceActiveFocus()
                event.accepted = true
            }
        }
        Keys.onReleased: function(event) {
            if (closingWithBack && (event.key === Qt.Key_Back || event.key === Qt.Key_Escape)) {
                closingWithBack = false
                event.accepted = true
            }
        }
        onActivated: function(index) {
            const channel = index === 1 ? "beta" : "stable"
            if (appSettings.update_channel !== channel) {
                appSettings.update_channel = channel
                backend.check_for_updates()
            }
        }
        onActiveFocusChanged: {
            if (activeFocus) {
                let item = parent
                while (item && !(item instanceof Flickable)) item = item.parent
                if (item) {
                    const point = mapToItem(item.contentItem, 0, 0)
                    item.contentY = Math.max(0, Math.min(point.y, item.contentHeight - item.height))
                }
            }
        }
        Rectangle {
            anchors.fill: parent
            color: "transparent"
            visible: selector.activeFocus
            border.width: 3
            border.color: Theme.accent
            radius: 4
        }
    }
    Label {
        Layout.fillWidth: true
        wrapMode: Text.Wrap
        text: qsTr("Stable receives Stable releases only. Beta receives the newest Beta or Stable release. Switching never downgrades your installation.")
    }
    Label {
        Layout.fillWidth: true
        wrapMode: Text.Wrap
        text: qsTr("Installed: %1").arg(backend.installed_release)
    }
}
