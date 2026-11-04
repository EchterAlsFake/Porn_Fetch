import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ScrollableMessageDialog {
    id: root
    objectName: "serviceTorFailureDialog"
    parent: Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(parent.width - 32, 540)
    height: Math.min(parent.height - 32, implicitHeight)
    z: 200
    modal: true
    title: qsTr("Porn Fetch over Tor")
    property bool presentationBlocked: false
    property bool pendingNotice: false
    function showPending() {
        if (pendingNotice && !presentationBlocked && appSettings.service_transport !== "direct") {
            pendingNotice = false
            open()
        }
    }
    onPresentationBlockedChanged: showPending()

    Connections {
        target: torStatus
        function onFailure(message) {
            if (appSettings.service_transport !== "direct") {
                root.message = message
                root.pendingNotice = true
                root.showPending()
            }
        }
    }
    Connections {
        target: appSettings
        function onServiceTransportChanged(mode) {
            torStatus.resetFailureNotice()
            if (mode === "direct") root.close()
        }
    }
    footer: ColumnLayout {
        spacing: 8
        Button {
            Layout.fillWidth: true
            objectName: "disableServiceTorButton"
            text: qsTr("Turn off Tor for Porn Fetch")
            onClicked: { appSettings.service_transport = "direct"; root.close() }
        }
        Button {
            Layout.fillWidth: true
            text: qsTr("Keep Tor enabled")
            onClicked: root.close()
        }
    }
}
