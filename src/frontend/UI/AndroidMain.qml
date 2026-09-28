import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 400
    height: 800
    title: qsTr("Porn Fetch")
    font.pointSize: Math.max(12, appSettings.font_size)

    property bool safeToClose: false
    property int pageIndex: 0
    readonly property bool tablet: contentItem.width >= 700
    readonly property var pageNames: [qsTr("Downloads"), qsTr("Account"), qsTr("Statistics"),
                                      qsTr("Settings"), qsTr("Info"), qsTr("Supported websites")]

    onClosing: function(event) {
        if (!safeToClose) {
            event.accepted = false
            backend.initiate_shutdown()
        }
    }

    Connections {
        target: backend
        function onMobileNotice(title, message) {
            noticeDialog.title = title
            noticeText.text = message
            noticeDialog.open()
        }
        function onShutdown_complete() {
            window.safeToClose = true
            window.close()
        }
    }

    Connections {
        target: appSettings
        function onAnonymousModeChanged() {
            if (appSettings.anonymous_mode && window.pageIndex > 3)
                window.pageIndex = 0
        }
    }

    Dialog {
        id: noticeDialog
        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.min(window.width - 24, 540)
        height: Math.min(window.height - 24, 400)
        modal: true
        standardButtons: Dialog.Ok
        contentItem: ScrollView {
            Label {
                id: noticeText
                width: parent.width
                wrapMode: Text.Wrap
            }
        }
    }

    Component.onCompleted: {
        if (!appSettings.error_reporting_decided)
            Qt.callLater(function() { consentDialog.open() })
    }

    Dialog {
        id: consentDialog
        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.min(window.width - 32, 560)
        height: Math.min(window.height - 32, 620)
        modal: true
        closePolicy: Popup.NoAutoClose
        title: qsTr("Help improve Porn Fetch after errors?")

        contentItem: ColumnLayout {
            spacing: 12
            Label {
                Layout.fillWidth: true
                text: qsTr("Automatic error reporting is disabled until you choose to enable it.")
                wrapMode: Text.Wrap
            }
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Label {
                    width: parent.width
                    text: backend.errorReportDisclosure
                    wrapMode: Text.Wrap
                }
            }
            Button {
                Layout.fillWidth: true
                text: qsTr("No, keep disabled")
                onClicked: {
                    appSettings.set_error_reporting_consent(false)
                    consentDialog.close()
                }
            }
            Button {
                Layout.fillWidth: true
                text: qsTr("Yes, enable reports")
                onClicked: {
                    appSettings.set_error_reporting_consent(true)
                    consentDialog.close()
                }
            }
        }
    }

    Item {
        anchors.fill: parent
        focus: true
        Keys.onReleased: function(event) {
            if (event.key === Qt.Key_Back || event.key === Qt.Key_Escape) {
                if (window.pageIndex !== 0) {
                    window.pageIndex = 0
                    event.accepted = true
                }
            }
        }

        RowLayout {
            anchors.fill: parent
            spacing: 0

            Rectangle {
                visible: window.tablet
                Layout.preferredWidth: visible ? 180 : 0
                Layout.fillHeight: true
                color: window.palette.window

                ListView {
                    anchors.fill: parent
                    model: window.pageNames
                    currentIndex: window.pageIndex
                    delegate: ItemDelegate {
                        required property int index
                        required property string modelData
                        width: ListView.view.width
                        height: 56
                        text: modelData
                        highlighted: window.pageIndex === index
                        enabled: !appSettings.anonymous_mode || index < 4
                        onClicked: window.pageIndex = index
                    }
                }
            }

            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 0

                ToolBar {
                    Layout.fillWidth: true
                    contentItem: Label {
                        leftPadding: 16
                        text: window.pageNames[window.pageIndex]
                        font.bold: true
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                }

                StackLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    currentIndex: window.pageIndex

                    AndroidDownloadsPage {}
                    AccountPage { backendController: backend }
                    AndroidStatisticsPage {}
                    SettingsPage {}
                    AndroidInfoPage { visible: !appSettings.anonymous_mode }
                    AndroidSupportedWebsitesPage { visible: !appSettings.anonymous_mode }
                }

                TabBar {
                    visible: !window.tablet
                    Layout.fillWidth: true
                    currentIndex: window.pageIndex < 4 ? window.pageIndex : 4

                    TabButton { text: qsTr("Downloads"); onClicked: window.pageIndex = 0 }
                    TabButton { text: qsTr("Account"); onClicked: window.pageIndex = 1 }
                    TabButton { text: qsTr("Stats"); onClicked: window.pageIndex = 2 }
                    TabButton { text: qsTr("Settings"); onClicked: window.pageIndex = 3 }
                    TabButton {
                        text: qsTr("More")
                        onClicked: moreMenu.open()
                        Menu {
                            id: moreMenu
                            y: -height
                            MenuItem {
                                text: qsTr("Info")
                                enabled: !appSettings.anonymous_mode
                                onTriggered: window.pageIndex = 4
                            }
                            MenuItem {
                                text: qsTr("Supported websites")
                                enabled: !appSettings.anonymous_mode
                                onTriggered: window.pageIndex = 5
                            }
                        }
                    }
                }
            }
        }
    }
}
