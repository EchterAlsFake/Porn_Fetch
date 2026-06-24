import QtQuick
import QtQuick.Controls

Button {
    id: control

    // Exposed properties for easy theming
    property color primaryColor: "#00e5ff" // Matches the cyan input line
    property color hoverColor: "#4dffff"   // Slightly lighter for hover state
    property color pressedColor: "#00b3cc" // Slightly darker for pressed state
    property color textColor: "#121212"    // Dark text pops nicely against the bright cyan
    property int borderRadius: 8
    Layout.botto

    // Enable hover states
    hoverEnabled: true

    // Customizing the text label
    contentItem: Text {
        text: control.text
        font.pixelSize: 16
        font.bold: true
        color: control.textColor
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    // Customizing the background shape and animations
    background: Rectangle {
        id: bgRect
        radius: control.borderRadius

        // Dynamic color based on interaction state
        color: control.down ? control.pressedColor : control.hovered ? control.hoverColor : control.primaryColor

        // Tactile scale effect (shrinks slightly when clicked)
        scale: control.down ? 0.96 : 1.0

        // Smooth color transitions
        Behavior on color {
            ColorAnimation { duration: 150; easing.type: Easing.OutQuad }
        }

        // Springy scale animations
        Behavior on scale {
            NumberAnimation { duration: 100; easing.type: Easing.OutQuad }
        }
    }
}