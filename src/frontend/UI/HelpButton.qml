import QtQuick
import QtQuick.Controls
import QtQuick.Controls.impl

Button {
    id: control
    property string helpText: ""

    clip: true
    icon.source: "qrc:/images/graphics/information.svg"
    palette.buttonText: "white"

    onClicked: {
        backend.handle_message(helpText)
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
}
