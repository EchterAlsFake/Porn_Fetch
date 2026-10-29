import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: control
    spacing: 15
    readonly property var modes: ["direct", "tor", "tor_all"]

    HelpButton { helpText: AppStrings.torIntegrationHelp }

    ColumnLayout {
        Layout.fillWidth: true
        Layout.minimumWidth: 0
        Label {
            Layout.fillWidth: true
            text: qsTr("Route connections through the Tor network")
            font.bold: true
            wrapMode: Text.Wrap
        }
        ComboBox {
            id: scopeCombo
            objectName: "torRoutingComboBox"
            Accessible.name: qsTr("Tor routing")
            Accessible.description: AppStrings.torIntegrationHelp
            Layout.fillWidth: true
            Layout.minimumWidth: 0
            enabled: !(backend.activityActive === true)
            model: [qsTr("Off — connect directly"), qsTr("Tor — updates and licensing only"), qsTr("Tor — all app traffic, including downloads")]
            currentIndex: Math.max(0, control.modes.indexOf(appSettings.service_transport))
            onActivated: function(index) {
                // Keep the current route until the warning is acknowledged.
                currentIndex = Qt.binding(function() { return Math.max(0, control.modes.indexOf(appSettings.service_transport)) })
                if (index === 2 && appSettings.service_transport !== "tor_all")
                    allTrafficWarning.open()
                else
                    appSettings.service_transport = control.modes[index]
            }
        }
        Label {
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            text: qsTr("Finish active work before changing Tor routing.")
            visible: !scopeCombo.enabled
        }
        Label {
            objectName: "torStatusLabel"
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            text: torStatus.text
            visible: appSettings.service_transport !== "direct"
        }
    }

    ScrollableMessageDialog {
        id: allTrafficWarning
        objectName: "torAllTrafficWarning"
        title: qsTr("Using Tor for video downloads")
        message: AppStrings.torAllTrafficNotice
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        onAccepted: appSettings.service_transport = "tor_all"
    }
}
