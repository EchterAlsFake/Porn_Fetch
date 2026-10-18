import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root
    objectName: "betaDisclaimerDialog"

    required property var disclaimer
    property color surfaceColor: "#1e1e24"
    property color textColor: "#f1f5f9"
    property color borderColor: "#383b48"
    signal confirmed()
    signal exitRequested()

    parent: Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(parent.width - 32, 760)
    height: Math.min(parent.height - 32, 720)
    modal: true
    focus: true
    z: 1000
    padding: 20
    closePolicy: Popup.NoAutoClose
    title: qsTr("Porn Fetch v3.9 BETA disclaimer")

    // Begin only after the opening transition, when the notice is visible.
    onOpened: disclaimer.startReading()
    onClosed: disclaimer.stopReading()

    background: Rectangle {
        color: root.surfaceColor
        radius: 12
        border.color: root.borderColor
    }

    contentItem: ColumnLayout {
        spacing: 16

        ScrollView {
            id: noticeScroll
            objectName: "betaDisclaimerScroll"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            contentWidth: availableWidth
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

            Label {
                width: noticeScroll.availableWidth
                text: root.disclaimer.text
                textFormat: Text.PlainText
                color: root.textColor
                wrapMode: Text.Wrap
                font.pixelSize: 15
            }
        }

        Label {
            Layout.fillWidth: true
            text: root.disclaimer.remainingSeconds > 0
                  ? qsTr("Please read the disclaimer. OK will be available in %1 seconds.").arg(root.disclaimer.remainingSeconds)
                  : qsTr("Click OK to consent and continue, or Exit to close Porn Fetch.")
            color: root.textColor
            wrapMode: Text.Wrap
        }

        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }

            Button {
                text: qsTr("Exit")
                onClicked: root.exitRequested()
            }

            Button {
                objectName: "betaDisclaimerOkButton"
                enabled: root.disclaimer.remainingSeconds === 0
                text: enabled ? qsTr("OK") : qsTr("OK (%1 s)").arg(root.disclaimer.remainingSeconds)
                onClicked: {
                    if (root.disclaimer.accept()) {
                        root.close()
                        root.confirmed()
                    }
                }
            }
        }
    }
}
