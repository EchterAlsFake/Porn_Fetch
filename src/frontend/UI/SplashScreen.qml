import QtQuick
import QtQuick.Window

Window {
    id: splashWindow
    width: 600
    height: 400
    title: qsTr("PornFetch-Splash")
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
        width: parent.width - 48
        spacing: 15

        // 4. Logo Widget
        Image {
            id: logoImage
            // In QML, you pass a file path/URL instead of a QPixmap
            source: "qrc:/images/graphics/logo_transparent.png"
            width: parent.width
            height: Math.min(240, splashWindow.height - statusText.implicitHeight - 80)
            anchors.horizontalCenter: parent.horizontalCenter
            fillMode: Image.PreserveAspectFit

            // Optional: Constrain maximum size to respect margins
            sourceSize.width: width * Screen.devicePixelRatio
            sourceSize.height: height * Screen.devicePixelRatio
        }

        // 5. Text Widget (Status)
        Text {
            id: statusText
            text: qsTr("Initializing...")
            color: "#ffffff"
            font.pointSize: 10
            width: parent.width
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
