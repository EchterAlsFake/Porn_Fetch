import QtQuick
import QtQuick.Controls
import QtQuick.Controls.impl

Button {
    id: control
    clip: true
    icon.source: "qrc:/images/graphics/tooltip.svg"
    palette.buttonText: "white"
    text: "Help"

    contentItem: IconLabel {
        clip: control.clip
        color: control.palette.buttonText
        display: control.display
        font: control.font
        icon: control.icon
        mirrored: control.mirrored
        spacing: control.spacing
        text: control.text
    }
}
