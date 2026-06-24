import QtQuick
import QtQuick.Controls

Item {
    id: root

    // Default dimensions
    width: 350
    height: 60

    // Exposed properties for easy customization
    property string text: inputField.text
    property string placeholderText: "Enter Video URL..."
    property color primaryColor: "#00e5ff" // Cyan accent for modern look
    property color textColor: "#ffffff"
    property color inactiveColor: "#808080"

    signal accepted()

    Rectangle {
        anchors.fill: parent
        color: "transparent"

        // Floating Placeholder Label
        Text {
            id: floatingLabel
            text: root.placeholderText

            // Color logic: Primary color when focused, otherwise inactive color
            color: inputField.activeFocus ? root.primaryColor : root.inactiveColor

            // Size logic: Shrink when focused or when text exists
            font.pixelSize: (inputField.activeFocus || inputField.text !== "") ? 12 : 16

            // Position logic: Move to the top when focused or populated
            y: (inputField.activeFocus || inputField.text !== "") ? 5 : 25

            anchors.left: parent.left
            anchors.leftMargin: 5

            // Smooth animations for size and position changes
            Behavior on y {
                NumberAnimation { duration: 200; easing.type: Easing.OutQuad }
            }

        }

        // The actual text input field
        TextInput {
            id: inputField
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 8
            anchors.leftMargin: 5

            font.pixelSize: 16
            color: root.textColor
            clip: true
            selectByMouse: true
            verticalAlignment: TextInput.AlignBottom

            // Trigger the exposed signal when the user presses Enter
            onAccepted: root.accepted()
        }

        // Inactive background line
        Rectangle {
            id: backgroundLine
            height: 1
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            color: root.inactiveColor
            opacity: 0.5
        }

        // Animated active underline
        Rectangle {
            id: activeLine
            height: 2
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter

            // Expand width to 100% when focused, collapse to 0 when unfocused
            width: inputField.activeFocus ? parent.width : 0
            color: root.primaryColor

            Behavior on width {
                NumberAnimation { duration: 250; easing.type: Easing.OutCubic }
            }
        }
    }
}