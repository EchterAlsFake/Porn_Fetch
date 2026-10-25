import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root
    objectName: "serviceTorFailureDialog"
    parent: Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(parent.width - 32, 540)
    height: Math.min(parent.height - 32, implicitHeight)
    z: 200
    modal: true
    title: qsTr("Porn Fetch over Tor")
    property string message: ""

    Connections {
        target: torStatus
        function onFailure(message) {
            if (appSettings.service_transport === "tor") {
                root.message = message
                root.open()
            }
        }
    }
    Connections {
        target: appSettings
        function onServiceTransportChanged(mode) {
            torStatus.resetFailureNotice()
            if (mode !== "tor") root.close()
        }
    }
    contentItem: ScrollView {
        implicitHeight: notice.implicitHeight
        clip: true
        Label {
            id: notice
            objectName: "serviceTorFailureText"
            width: parent.width
            text: root.message
            textFormat: Text.PlainText
            wrapMode: Text.WordWrap
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
