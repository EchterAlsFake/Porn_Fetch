import QtQuick
import QtQuick.Window

Window {
    id: splashWindow
    width: 600
    height: 400
    title: "PornFetch-Splash"
    visible: true
    // 1. Window Flags
    flags: Qt.SplashScreen | Qt.FramelessWindowHint

    // 2. Appearance (Dark Theme)
    color: "#1e1e1e"

    // Expose a property so Python can update the text
    property alias message: statusText.text

    // 3. Layout (Vertical, Centered)
    Column {
        anchors.centerIn: parent
        spacing: 15

        // 4. Logo Widget
        Image {
            id: logoImage
            // In QML, you pass a file path/URL instead of a QPixmap
            source: "qrc:/images/graphics/logo_transparent.png"
            anchors.horizontalCenter: parent.horizontalCenter
            fillMode: Image.PreserveAspectFit

            // Optional: Constrain maximum size to respect margins
            sourceSize.width: 560
            sourceSize.height: 300
        }

        // 5. Text Widget (Status)
        Text {
            id: statusText
            text: "Initializing..."
            color: "#ffffff"
            font.pointSize: 10
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}