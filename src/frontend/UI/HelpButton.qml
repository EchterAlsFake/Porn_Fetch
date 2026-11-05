import QtQuick
import QtQuick.Controls
import QtQuick.Controls.impl

AppButton {
    id: control
    property string helpText: ""

    Accessible.name: qsTr("Help")
    Accessible.description: helpText

    implicitWidth: Math.max(48, contentItem.implicitWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(48, contentItem.implicitHeight + topPadding + bottomPadding)
    clip: true
    icon.source: "qrc:/images/graphics/information.svg"
    icon.width: 22
    icon.height: 22

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
        color: control.palette.buttonText
    }

    ScrollableMessageDialog {
        id: helpDialog
        objectName: "helpDialog"

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
