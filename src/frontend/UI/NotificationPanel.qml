import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: root
    property var controller: typeof noticeCenter !== "undefined" ? noticeCenter : null
    property bool blocked: false
    readonly property int entryCount: controller ? controller.entries.length : 0
    readonly property var decision: controller ? controller.pendingDecision : ({})
    property string pendingAnnouncement: ""
    property bool pendingUrgent: false
    property var pendingFeedback: null
    function showFeedback() {
        if (!blocked && pendingFeedback) {
            feedbackDialog.title = pendingFeedback.title;
            feedbackDialog.message = pendingFeedback.message;
            pendingFeedback = null;
            feedbackDialog.open();
        }
    }
    function openActivity() { activityDialog.open() }
    spacing: 0
    Accessible.role: Accessible.Grouping
    Accessible.name: qsTr("Application notifications")
    function showDecision() {
        if (!blocked && decision.action && !decisionDialog.visible) {
            decisionDialog.action = decision.action;
            decisionDialog.title = decision.title;
            decisionDialog.message = decision.message;
            decisionDialog.open();
        }
    }
    onDecisionChanged: Qt.callLater(showDecision)

    Connections {
        target: appSettings
        function onAnonymousModeChanged() {
            activityDialog.close();
            activityDialog.displayedEntries = root.controller ? root.controller.entries : [];
            root.pendingAnnouncement = "";
            root.pendingFeedback = null;
            feedbackDialog.close();
            announcementTimer.stop();
        }
    }

    function performAction(action) {
        activityDialog.pendingAction = action;
        activityDialog.close();
    }

    function dispatchAction(action) {
        if (action === "retry")
            backend.retry_failed_downloads();
        else if (action === "output")
            backend.open_output_folder();
        else if (action === "updates")
            backend.review_update();
    }

    Connections {
        target: root.controller
        function onDirectRequested(title, message) {
            root.pendingFeedback = {title: title, message: message};
            root.showFeedback();
        }
        function onAnnounced(message, urgent) {
            root.pendingAnnouncement = message;
            root.pendingUrgent = urgent;
            announcementTimer.restart();
        }
    }
    Timer {
        id: announcementTimer
        interval: 650
        onTriggered: {
            if (!root.blocked) {
                root.Accessible.announce(root.pendingAnnouncement, root.pendingUrgent ? Accessible.Assertive : Accessible.Polite);
                root.pendingAnnouncement = "";
            }
        }
    }
    onBlockedChanged: {
        if (!blocked && pendingAnnouncement)
            announcementTimer.restart();
        Qt.callLater(showDecision);
        Qt.callLater(showFeedback);
    }

    RowLayout {
        AppButton {
            id: activityButton
            objectName: "recentActivityButton"
            Layout.minimumWidth: 0
            text: root.controller && root.controller.restartRequired ? qsTr("Restart required")
                  : qsTr("Activity (%1)").arg(root.entryCount)
            Accessible.name: qsTr("Recent activity (%1)").arg(root.entryCount)
            ToolTip.visible: hovered
            ToolTip.text: qsTr("View messages and errors")
            implicitHeight: Math.max(48, contentItem.implicitHeight + topPadding + bottomPadding)
            enabled: !root.blocked
            onClicked: activityDialog.open()
        }
    }

    ScrollableMessageDialog {
        id: feedbackDialog
        objectName: "directFeedbackDialog"
        modal: true
    }

    ScrollableMessageDialog {
        id: decisionDialog
        property string action: ""
        modal: true
        standardButtons: Dialog.Yes | Dialog.No
        onAccepted: root.controller.resolve_decision(action, true)
        onRejected: root.controller.resolve_decision(action, false)
        onClosed: Qt.callLater(root.showDecision)
    }

    Dialog {
        id: activityDialog
        ContrastPopupBackground { popup: activityDialog }
        objectName: "recentActivityDialog"
        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.max(1, Math.min(680, parent.width - 32))
        height: Math.max(1, Math.min(640, parent.height - 32))
        modal: true
        closePolicy: Popup.CloseOnEscape
        title: qsTr("Recent activity")
        property var previousFocus: null
        property var displayedEntries: []
        property string pendingAction: ""
        onAboutToShow: {
            previousFocus = root.Window.window.activeFocusItem;
            displayedEntries = root.controller ? root.controller.entries : [];
        }
        onOpened: activityList.forceActiveFocus()
        onClosed: {
            var item = previousFocus;
            var action = pendingAction;
            pendingAction = "";
            Qt.callLater(function () {
                // Finish closing Activity before opening another modal dialog.
                if (action) {
                    root.dispatchAction(action);
                    return;
                }
                if (item) {
                    item.focus = false;
                    item.forceActiveFocus(Qt.TabFocusReason);
                }
            });
        }
        standardButtons: Dialog.Close
        contentItem: ColumnLayout {
            spacing: 8
            Label {
                Layout.fillWidth: true
                text: qsTr("Messages are kept for this session only. Downloaded videos use the output folder in Settings.")
                textFormat: Text.PlainText
                wrapMode: Text.Wrap
            }
            ListView {
                id: activityList
                objectName: "recentActivityList"
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                spacing: 12
                // Keep reading position and keyboard focus stable when background
                // tasks publish messages. Refresh is an explicit user action.
                model: activityDialog.displayedEntries
                Accessible.role: Accessible.List
                Accessible.name: qsTr("Recent application messages")
                ScrollBar.vertical: ScrollBar {}
                delegate: Pane {
                    required property var modelData
                    width: ListView.view.width
                    padding: 8
                    contentItem: ColumnLayout {
                        spacing: 4
                        Label {
                            Layout.fillWidth: true
                            font.bold: true
                            text: modelData.title + (modelData.count > 1 ? qsTr(" (%1 occurrences)").arg(modelData.count) : "")
                            textFormat: Text.PlainText
                            wrapMode: Text.Wrap
                        }
                        Label {
                            Layout.fillWidth: true
                            text: modelData.message
                            textFormat: Text.PlainText
                            wrapMode: Text.Wrap
                        }
                        Label {
                            Layout.fillWidth: true
                            text: modelData.details
                            visible: text !== ""
                            textFormat: Text.PlainText
                            wrapMode: Text.Wrap
                        }
                        Flow {
                            Layout.fillWidth: true
                            spacing: 8
                            AppButton {
                                id: copyMessageButton
                                property bool copied: false
                                text: copied ? qsTr("Copied") : qsTr("Copy message")
                                Accessible.name: qsTr("Copy message")
                                implicitHeight: 48
                                onClicked: {
                                    root.controller.copy(modelData.id);
                                    copied = true;
                                    copiedTimer.restart();
                                }
                                Timer {
                                    id: copiedTimer
                                    interval: 3000
                                    onTriggered: copyMessageButton.copied = false
                                }
                            }
                            AppButton {
                                visible: modelData.action !== ""
                                text: modelData.action === "retry" ? qsTr("Retry failed downloads") : modelData.action === "updates" ? qsTr("Review update") : qsTr("Open output folder")
                                implicitHeight: 48
                                onClicked: root.performAction(modelData.action)
                            }
                        }
                    }
                }
            }
            Label {
                visible: activityDialog.displayedEntries.length === 0
                text: qsTr("No messages yet.")
            }
            Flow {
                Layout.fillWidth: true
                spacing: 8
                AppButton {
                    id: refreshButton
                    text: qsTr("Refresh messages")
                    implicitHeight: 48
                    onClicked: activityDialog.displayedEntries = root.controller ? root.controller.entries : []
                }
                AppButton {
                    text: qsTr("Clear messages")
                    enabled: root.entryCount > 0
                    implicitHeight: 48
                    onClicked: {
                        refreshButton.forceActiveFocus();
                        root.controller.clear();
                        activityDialog.displayedEntries = [];
                    }
                }
            }
        }
    }

    Popup {
        id: shutdownPopup
        ContrastPopupBackground { popup: shutdownPopup }
        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.max(1, Math.min(480, parent.width - 32))
        modal: true
        focus: true
        visible: root.controller && root.controller.shuttingDown
        closePolicy: Popup.NoAutoClose
        contentItem: Label {
            text: qsTr("Closing…\nStopping downloads and saving application state.")
            textFormat: Text.PlainText
            wrapMode: Text.Wrap
        }
    }
}
