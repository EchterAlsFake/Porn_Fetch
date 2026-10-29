import QtQuick
import QtQuick.Controls
import QtQuick.Layouts



Dialog {
    id: inputDialog
    title: "User Input"
    modal: true
    anchors.centerIn: Overlay.overlay
    width: 320
    standardButtons: Dialog.Ok | Dialog.Cancel

    signal acceptedInput(string text)

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Label {
            text: "App Name:"
        }

        TextField {
            id: appNameInput
            Layout.fillWidth: true
            placeholderText: "Leave empty for 'Porn Fetch'"
            focus: true
        }
    }

    onAccepted: {
        backend.install_pornfetch(appNameInput.text)
        appNameInput.clear()
    }

    onRejected: {
        backend.handle_abort()
        appNameInput.clear()
    }
}

