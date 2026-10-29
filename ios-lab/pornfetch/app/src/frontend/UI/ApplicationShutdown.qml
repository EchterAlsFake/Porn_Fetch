import QtQuick

QtObject {
    id: root
    required property var targetWindow
    required property var backendController
    property bool active: true
    property bool safeToClose: false

    property Connections closeConnection: Connections {
        target: root.targetWindow
        enabled: root.active
        function onClosing(closeEvent) {
            if (!root.safeToClose) {
                closeEvent.accepted = false
                root.backendController.initiate_shutdown()
            }
        }
    }
    property Connections completionConnection: Connections {
        target: root.backendController
        enabled: root.active
        function onShutdown_complete() {
            root.safeToClose = true
            root.targetWindow.close()
        }
    }
}
