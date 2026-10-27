import QtQuick
import QtQuick.Controls
import QtQuick.Controls.impl

Button {
    id: control
    property string helpText: ""

    Accessible.name: qsTr("Help")
    Accessible.description: helpText

    clip: true
    icon.source: "qrc:/images/graphics/information.svg"
    palette.buttonText: "white"

    onClicked: {
        helpDialog.open()
    }

    contentItem: IconLabel {
        clip: control.clip
        display: control.display
        font: control.font
        icon: control.icon
        mirrored: control.mirrored
        spacing: control.spacing
        text: control.text
    }

    ScrollableMessageDialog {
        id: helpDialog

        // Keep the settings page interactive so an open help message reflects
        // font changes immediately.
        modal: false
        focus: true
        closePolicy: Popup.CloseOnEscape
        standardButtons: Dialog.Ok
        title: qsTr("Help")

        // HelpButton inherits its font from the containing page/application.
        // Keeping this as a binding also updates an already-open dialog.
        font: control.font

        message: control.helpText
    }
}
