import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 400
    height: 800
    title: qsTr("Porn Fetch")
    font.pointSize: Math.max(12, appSettings.font_size)
    Material.theme: appSettings.dark_mode ? Material.Dark : Material.Light
    Material.accent: appSettings.accent_color
    Material.primary: appSettings.accent_color

    readonly property color backgroundColor: appSettings.dark_mode ? "#101319" : "#f7f8fc"
    readonly property color surfaceColor: appSettings.dark_mode ? "#1b202a" : "#ffffff"
    readonly property color navigationColor: appSettings.dark_mode ? "#171b23" : "#eef0f7"
    readonly property color primaryTextColor: appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color secondaryTextColor: appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    readonly property color accentColor: appSettings.accent_color
    background: Rectangle { color: window.backgroundColor }

    property bool safeToClose: false
    property int pageIndex: 0
    readonly property bool tablet: contentItem.width >= 960
    readonly property var pageNames: [qsTr("Downloads"), qsTr("Account"), qsTr("Statistics"),
                                      qsTr("Settings"), qsTr("Info"), qsTr("Supported websites")]
    readonly property var pageDescriptions: [qsTr("Collect and save videos"), qsTr("Your connected accounts"),
                                             qsTr("Your download activity"), qsTr("Make it yours"),
                                             qsTr("About this app"), qsTr("Available sources")]
    readonly property var pageIcons: ["qrc:/images/graphics/download.svg", "qrc:/images/graphics/account.svg",
                                      "qrc:/images/graphics/database.svg", "qrc:/images/graphics/settings.svg",
                                      "qrc:/images/graphics/information.svg", "qrc:/images/graphics/information.svg"]

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
                if (window.pageIndex === 3 && settingsPage.goBack()) {
                    event.accepted = true
                } else if (window.pageIndex !== 0) {
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
                Layout.preferredWidth: visible ? 204 : 0
                Layout.fillHeight: true
                color: window.navigationColor

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 12
                    spacing: 8

                    RowLayout {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 76
                        spacing: 10
                        Rectangle {
                            Layout.preferredWidth: 38
                            Layout.preferredHeight: 38
                            radius: 13
                            color: window.accentColor
                            Label {
                                anchors.centerIn: parent
                                text: "P"
                                color: "white"
                                font.pixelSize: 22
                                font.bold: true
                            }
                        }
                        Label {
                            text: qsTr("Porn Fetch")
                            color: window.primaryTextColor
                            font.pixelSize: 18
                            font.bold: true
                        }
                    }

                    Repeater {
                        model: window.pageNames
                        delegate: ItemDelegate {
                            required property int index
                            required property string modelData
                            Layout.fillWidth: true
                            Layout.preferredHeight: 54
                            enabled: !appSettings.anonymous_mode || index < 4
                            onClicked: window.pageIndex = index
                            background: Rectangle {
                                radius: 18
                                color: window.pageIndex === index
                                       ? Qt.rgba(window.accentColor.r, window.accentColor.g,
                                                 window.accentColor.b, 0.20)
                                       : "transparent"
                            }
                            contentItem: RowLayout {
                                spacing: 12
                                Image {
                                    source: window.pageIcons[index]
                                    Layout.preferredWidth: 28
                                    Layout.preferredHeight: 28
                                    fillMode: Image.PreserveAspectFit
                                }
                                Label {
                                    Layout.fillWidth: true
                                    text: modelData
                                    color: window.pageIndex === index
                                           ? window.accentColor : window.primaryTextColor
                                    font.bold: window.pageIndex === index
                                    elide: Text.ElideRight
                                }
                            }
                        }
                    }
                    Item { Layout.fillHeight: true }
                }
            }

            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 0

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: window.tablet ? 92 : 82
                    color: window.backgroundColor

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.leftMargin: window.tablet ? 28 : 20
                        anchors.rightMargin: 16
                        spacing: 1
                        Item { Layout.fillHeight: true }
                        Label {
                            text: window.pageNames[window.pageIndex]
                            color: window.primaryTextColor
                            font.pixelSize: window.tablet ? 29 : 25
                            font.bold: true
                            elide: Text.ElideRight
                            Layout.fillWidth: true
                        }
                        Label {
                            text: window.pageDescriptions[window.pageIndex]
                            color: window.secondaryTextColor
                            font.pixelSize: 13
                            Layout.fillWidth: true
                            elide: Text.ElideRight
                        }
                        Item { Layout.fillHeight: true }
                    }
                }

                StackLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    currentIndex: window.pageIndex

                    AndroidDownloadsPage {}
                    AndroidAccountPage {}
                    AndroidStatisticsPage {}
                    AndroidSettingsPage { id: settingsPage; objectName: "androidSettingsPage" }
                    AndroidInfoPage { visible: !appSettings.anonymous_mode }
                    AndroidSupportedWebsitesPage { visible: !appSettings.anonymous_mode }
                }

                Rectangle {
                    visible: !window.tablet
                    Layout.fillWidth: true
                    Layout.preferredHeight: visible ? 74 : 0
                    color: window.navigationColor

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 4
                        anchors.rightMargin: 4
                        spacing: 0
                        Repeater {
                            model: [qsTr("Downloads"), qsTr("Account"), qsTr("Stats"),
                                    qsTr("Settings"), qsTr("More")]
                            delegate: AbstractButton {
                                required property int index
                                required property string modelData
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                onClicked: {
                                    if (index === 4) moreMenu.open()
                                    else window.pageIndex = index
                                }
                                background: Rectangle {
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    anchors.top: parent.top
                                    anchors.topMargin: 7
                                    width: 56
                                    height: 34
                                    radius: 17
                                    color: (window.pageIndex === index || (index === 4 && window.pageIndex > 3))
                                           ? Qt.rgba(window.accentColor.r, window.accentColor.g,
                                                     window.accentColor.b, 0.22) : "transparent"
                                }
                                contentItem: ColumnLayout {
                                    spacing: 0
                                    Image {
                                        Layout.alignment: Qt.AlignHCenter
                                        Layout.preferredWidth: 28
                                        Layout.preferredHeight: 28
                                        source: window.pageIcons[Math.min(index, 4)]
                                        fillMode: Image.PreserveAspectFit
                                    }
                                    Label {
                                        Layout.alignment: Qt.AlignHCenter
                                        text: modelData
                                        color: (window.pageIndex === index || (index === 4 && window.pageIndex > 3))
                                               ? window.accentColor : window.secondaryTextColor
                                        font.pixelSize: 11
                                        font.bold: window.pageIndex === index
                                    }
                                }
                            }
                        }
                    }

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
