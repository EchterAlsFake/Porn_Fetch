import QtQuick
import QtQuick.Controls
import QtQuick.Controls.impl
import QtQuick.Layouts

Button {
    id: control
    property string helpText: ""

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

    Dialog {
        id: helpDialog

        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.min(520, Math.max(320, (parent ? parent.width : 568) - 48))
        height: Math.min(Math.max(180, (parent ? parent.height : 568) - 48),
                         Math.max(180, helpMessage.implicitHeight + 140))

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

        contentItem: ScrollView {
            id: helpScroll
            clip: true

            Label {
                id: helpMessage
                width: helpScroll.availableWidth
                text: control.helpText
                font: helpDialog.font
                wrapMode: Text.Wrap
            }
        }
    }
}
