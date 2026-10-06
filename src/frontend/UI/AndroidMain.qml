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
    readonly property bool settingsDetail: pageIndex === 3 && !settingsPage.tablet && settingsPage.section >= 0
    readonly property bool moreDetail: !tablet && (pageIndex === 4 || pageIndex === 5)
    readonly property var pageNames: [qsTr("Downloads"), qsTr("Account"), qsTr("Statistics"),
                                      qsTr("Settings"), qsTr("Info"), qsTr("Supported websites"), qsTr("More")]
    readonly property var pageDescriptions: [qsTr("Collect and save videos"), qsTr("Your connected accounts"),
                                             qsTr("Your download activity"), qsTr("Make it yours"),
                                             qsTr("About this app"), qsTr("Available sources"), qsTr("Explore the app")]
    readonly property var pageIcons: ["qrc:/images/graphics/download.png", "qrc:/images/graphics/account.png",
                                      "qrc:/images/graphics/database.png", "qrc:/images/graphics/settings.png",
                                      "qrc:/images/graphics/information.png", "qrc:/images/graphics/information.png",
                                      "qrc:/images/graphics/information.png"]

    function goBack() {
        if (settingsDetail) settingsPage.goBack()
        else if (moreDetail) pageIndex = 6
        else if (pageIndex !== 0) pageIndex = 0
    }

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
        target: bridge
        function onLicenseRejected(message) {
            noticeDialog.title = qsTr("License rejected")
            noticeText.text = message
            noticeDialog.open()
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
                if (window.pageIndex !== 0 || window.settingsDetail) {
                    window.goBack()
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
                        Image {
                            Layout.preferredWidth: 38
                            Layout.preferredHeight: 38
                            source: "qrc:/images/graphics/logo.png"
                            fillMode: Image.PreserveAspectFit
                        }
                        Label {
                            text: qsTr("Porn Fetch")
                            color: window.primaryTextColor
                            font.pixelSize: 18
                            font.bold: true
                        }
                    }

                    Repeater {
                        model: window.pageNames.slice(0, 6)
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

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: window.tablet ? 28 : 20
                        anchors.rightMargin: 16
                        spacing: 12
                        Button {
                            visible: window.settingsDetail || window.moreDetail
                            Layout.preferredWidth: visible ? 48 : 0
                            Layout.preferredHeight: 48
                            text: "←"
                            font.pixelSize: 25
                            Accessible.name: qsTr("Back")
                            onClicked: window.goBack()
                            contentItem: Label {
                                text: "←"
                                color: window.accentColor
                                font.pixelSize: 28
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                            background: Rectangle {
                                radius: 24
                                color: Qt.rgba(window.accentColor.r, window.accentColor.g,
                                               window.accentColor.b, 0.18)
                            }
                        }
                        Image {
                            visible: !window.tablet && window.pageIndex === 0
                            Layout.preferredWidth: visible ? 36 : 0
                            Layout.preferredHeight: 36
                            source: "qrc:/images/graphics/logo.png"
                            fillMode: Image.PreserveAspectFit
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 1
                            Label {
                                text: window.settingsDetail ? settingsPage.titles[settingsPage.section]
                                      : window.pageNames[window.pageIndex]
                                color: window.primaryTextColor
                                font.pixelSize: window.tablet ? 29 : 25
                                font.bold: true
                                elide: Text.ElideRight
                                Layout.fillWidth: true
                            }
                            Label {
                                text: window.settingsDetail ? settingsPage.subtitles[settingsPage.section]
                                      : window.pageDescriptions[window.pageIndex]
                                color: window.secondaryTextColor
                                font.pixelSize: 13
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }
                        }
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
                    AndroidMorePage {
                        visible: !appSettings.anonymous_mode
                        onOpenPage: function(index) { window.pageIndex = index }
                    }
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
                                enabled: index !== 4 || !appSettings.anonymous_mode
                                onClicked: {
                                    if (index === 4) window.pageIndex = 6
                                    else window.pageIndex = index
                                }
                                background: Rectangle {
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    anchors.top: parent.top
                                    anchors.topMargin: 7
                                    width: 56
                                    height: 34
                                    radius: 17
                                    color: (window.pageIndex === index || (index === 4 && window.pageIndex >= 4))
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
                                        color: (window.pageIndex === index || (index === 4 && window.pageIndex >= 4))
                                               ? window.accentColor : window.secondaryTextColor
                                        font.pixelSize: 11
                                        font.bold: window.pageIndex === index
                                    }
                                }
                            }
                        }
                    }

                }
            }
        }
    }
}
