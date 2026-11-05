// qml/Main.qml

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

ApplicationWindow {
    id: window
    LayoutMirroring.enabled: Qt.application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true
    palette.window: Theme.background
    palette.windowText: Theme.ink
    palette.text: Theme.ink
    palette.base: Theme.background
    palette.button: Theme.surface
    palette.buttonText: Theme.ink
    palette.placeholderText: Theme.muted
    palette.highlight: Theme.accent
    palette.highlightedText: Theme.selectionInk
    palette.mid: Theme.outline
    palette.disabled.text: Theme.disabledInk
    palette.disabled.buttonText: Theme.disabledInk
    font.pointSize: appSettings.font_size
    Material.theme: appSettings.dark_mode ? Material.Dark : Material.Light
    Material.accent: Theme.accent
    Material.foreground: Theme.ink
    Material.background: Theme.background

    background: Rectangle { color: Theme.background }

    width: 1350
    height: 720
    minimumWidth: 900
    minimumHeight: 600

    visible: true
    title: qsTr("Video Downloader")
    property alias safeToClose: shutdownController.safeToClose
    property bool startupContinued: false

    ServiceTorFailureDialog { presentationBlocked: !appSettings.license_offer_seen || licenseOfferDialog.visible || !appSettings.ukraine_message_seen || ukraineMessageDialog.visible || !appSettings.error_reporting_decided }

    ActivityEdge {
        objectName: "activityEdge"
        parent: Overlay.overlay
        anchors.fill: parent
        z: 100
        enabled: appSettings.activity_glow_enabled && !appSettings.reduced_motion
        active: backend.activityActive
        accentColor: appSettings.accent_color || "#6366f1"
        animationAllowed: window.visibility !== Window.Minimized && window.visibility !== Window.Hidden
    }

    function continueStartup() {
        if (startupContinued)
            return
        startupContinued = true
        if (appSettings.update_checks)
            backend.check_for_updates_background()
    }

    function beginOnboarding() {
        if (!licenseOfferDialog.presentOnce())
            continueAfterLicenseOffer()
    }

    function continueAfterLicenseOffer() {
        if (!ukraineMessageDialog.presentOnce())
            continueAfterPersonalMessage()
    }

    function continueAfterPersonalMessage() {
        if (appSettings.error_reporting_decided)
            continueStartup()
        else
            Qt.callLater(function() { errorReportingDialog.open() })
    }

    Component.onCompleted: Qt.callLater(window.beginOnboarding)

    LicenseOfferDialog {
        id: licenseOfferDialog
        settings: appSettings
        onDismissed: window.continueAfterLicenseOffer()
    }

    UkraineMessageDialog {
        id: ukraineMessageDialog
        settings: appSettings
        onDismissed: window.continueAfterPersonalMessage()
    }

    ApplicationShutdown {
        id: shutdownController
        targetWindow: window
        backendController: backend
    }

    Connections {
        target: typeof systemNotifier !== "undefined" ? systemNotifier : null
        function onActivated() { navigation.currentIndex = 0; window.show(); window.raise(); window.requestActivate() }
    }

    Connections {
        target: backend

        function onUpdateAvailable(details) {
            updateDialog.version = details.version || ""
            updateDialog.installAllowed = details.install_allowed === true
            updateDialog.entitlementMessage = details.entitlement_message || ""
            updateDialog.releaseUrl = details.release_url || ""
            updateDialog.importantInfo = details.important_info || ""
            // Clear old notes before switching between HTML and Markdown.
            updateDialog.changelog = ""
            updateDialog.changelogFormat = details.changelog_format || "html"
            updateDialog.changelog = details.changelog || ""
            updateDialog.updateInProgress = false
            updateDialog.statusMessage = ""
            updateDialog.downloadedBytes = 0
            updateDialog.totalBytes = 0
            if (!details.automatic || appSettings.update_prompts)
                updateDialog.open()
        }

        function onUpdateProgress(current, total) {
            updateDialog.downloadedBytes = current
            updateDialog.totalBytes = total
        }

        function onUpdateStatus(status) {
            updateDialog.statusMessage = status
        }

        function onUpdateFinished() {
            updateDialog.updateInProgress = false
        }

    }

    Dialog {
        id: errorReportingDialog
        ContrastPopupBackground { popup: errorReportingDialog }

        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.min(window.width - 48, 900)
        height: Math.min(window.height - 48, 680)
        modal: true
        padding: 20
        closePolicy: Popup.NoAutoClose

        background: Rectangle {
            radius: 12
            color: Theme.surface
            border.color: Theme.outline
            border.width: 1
        }

        contentItem: ColumnLayout {
            spacing: 14

            Label {
                Layout.fillWidth: true
                text: qsTr("Help improve Porn Fetch after errors?")
                color: Theme.accent
                font.pixelSize: 24 * appSettings.font_size / 12
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }

            Label {
                Layout.fillWidth: true
                text: qsTr("Reports include full Python tracebacks and video URLs. Reporting stays off until you choose to enable it.")
                color: Theme.ink
                font.bold: true
                wrapMode: Text.Wrap
            }

            SmoothScrollView {
                id: consentScroll
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                contentWidth: availableWidth
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                ColumnLayout {
                    width: consentScroll.availableWidth
                    spacing: 12

                    Label {
                        Layout.fillWidth: true
                        text: backend.errorReportDisclosure
                        textFormat: Text.PlainText
                        color: Theme.ink
                        wrapMode: Text.Wrap
                    }

                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Synthetic example of a stored report:")
                        color: Theme.accent
                        font.bold: true
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: exampleText.contentHeight + 24
                        radius: 6
                        color: Theme.surface
                        border.color: Theme.outline

                        TextEdit {
                            id: exampleText
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.margins: 12
                            height: contentHeight
                            text: backend.errorReportExample
                            textFormat: TextEdit.PlainText
                            color: Theme.ink
                            font.family: "monospace"
                            font.pixelSize: 12 * appSettings.font_size / 12
                            readOnly: true
                            selectByMouse: true
                            wrapMode: TextEdit.Wrap
                        }
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Item { Layout.fillWidth: true }

                AppButton {
                    text: qsTr("No, keep disabled")
                    onClicked: {
                        appSettings.set_error_reporting_consent(false)
                        errorReportingDialog.close()
                        window.continueStartup()
                    }
                }

                AppButton {
                    text: qsTr("Yes, enable reports")
                    onClicked: {
                        appSettings.set_error_reporting_consent(true)
                        errorReportingDialog.close()
                        window.continueStartup()
                    }
                }
            }
        }
    }

    Dialog {
        id: updateDialog
        ContrastPopupBackground { popup: updateDialog }
        objectName: "updateDialog"

        property bool installAllowed: false
        property string entitlementMessage: ""
        property string version: ""
        property string releaseUrl: ""
        property string importantInfo: ""
        property string changelog: ""
        property string changelogFormat: "html"
        property string statusMessage: ""
        property real downloadedBytes: 0
        property real totalBytes: 0
        property bool updateInProgress: false

        function formatBytes(bytes) {
            if (!bytes || bytes <= 0)
                return "0 B"
            var units = ["B", "KiB", "MiB", "GiB"]
            var unit = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1)
            return (bytes / Math.pow(1024, unit)).toFixed(unit === 0 ? 0 : 1) + " " + units[unit]
        }

        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.min(window.width - 48, 820)
        height: Math.min(window.height - 48, 640)
        modal: true
        focus: true
        padding: 20
        closePolicy: Popup.NoAutoClose

        background: Rectangle {
            radius: 12
            color: Theme.surface
            border.color: Theme.outline
            border.width: 1
        }

        contentItem: ColumnLayout {
            spacing: 14

            Label {
                Layout.fillWidth: true
                text: qsTr("Update available")
                color: Theme.accent
                font.pixelSize: 26 * appSettings.font_size / 12
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }

            Label {
                Layout.fillWidth: true
                text: updateDialog.entitlementMessage
                wrapMode: Text.WordWrap
                color: Theme.ink
            }
            SmoothScrollView {
                id: updateScroll
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                // Keep wrapping stable when the scrollbar appears.
                rightPadding: ScrollBar.vertical.width + 6
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                ColumnLayout {
                    width: Math.max(1, updateScroll.availableWidth)
                    spacing: 14

                    RowLayout {
                        Layout.fillWidth: true

                        Label {
                            text: qsTr("Version:")
                            color: Theme.accent
                            font.bold: true
                        }

                        Label {
                            Layout.fillWidth: true
                            text: updateDialog.version
                            color: Theme.ink
                        }
                    }

                    Label {
                        visible: updateDialog.importantInfo !== ""
                        text: qsTr("Important Info:")
                        color: Theme.accent
                        font.bold: true
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: updateDialog.importantInfo !== ""
                        text: updateDialog.importantInfo
                        color: Theme.ink
                        textFormat: Text.RichText
                        wrapMode: Text.Wrap
                        onLinkActivated: (link) => Qt.openUrlExternally(link)
                    }

                    Label {
                        text: qsTr("Changelog:")
                        color: Theme.accent
                        font.bold: true
                    }

                    TextArea {
                        id: changelogText
                        objectName: "updateChangelogText"
                        Layout.fillWidth: true
                        // A bounded plain-text reader avoids the Qt Quick batch
                        // renderer crash with long rich-text release notes.
                        text: backend.release_notes_text(updateDialog.changelog, updateDialog.changelogFormat)
                        color: Theme.ink
                        textFormat: Text.PlainText
                        readOnly: true
                        selectByMouse: true
                        wrapMode: Text.Wrap
                        background: null
                    }
                }
            }

            ProgressBar {
                Layout.fillWidth: true
                visible: updateDialog.updateInProgress || updateDialog.downloadedBytes > 0
                from: 0
                to: updateDialog.totalBytes > 0 ? updateDialog.totalBytes : 1
                value: updateDialog.downloadedBytes
                indeterminate: updateDialog.updateInProgress && updateDialog.totalBytes <= 0
            }

            Label {
                Layout.fillWidth: true
                visible: text !== ""
                text: updateDialog.statusMessage
                color: Theme.ink
                wrapMode: Text.Wrap
            }

            Label {
                Layout.fillWidth: true
                visible: updateDialog.totalBytes > 0
                text: updateDialog.formatBytes(updateDialog.downloadedBytes)
                      + " / " + updateDialog.formatBytes(updateDialog.totalBytes)
                color: Theme.ink
                horizontalAlignment: Text.AlignRight
            }

            CheckBox {
                objectName: "hideUpdatePromptsCheckBox"
                Layout.fillWidth: true
                text: qsTr("Don't show update dialogs again")
                checked: !appSettings.update_prompts
                enabled: !updateDialog.updateInProgress
                onToggled: appSettings.update_prompts = !checked
            }

            RowLayout {
                Layout.fillWidth: true

                Item { Layout.fillWidth: true }

                AppButton {
                    text: qsTr("Later")
                    enabled: !updateDialog.updateInProgress
                    onClicked: updateDialog.close()
                }

                AppButton {
                    objectName: "installUpdateButton"
                    text: updateDialog.updateInProgress ? qsTr("Preparing update…")
                          : updateDialog.installAllowed ? qsTr("Update now") : qsTr("Open downloads")
                    enabled: !updateDialog.updateInProgress
                    highlighted: true
                    onClicked: {
                        if (!updateDialog.installAllowed) {
                            Qt.openUrlExternally(updateDialog.releaseUrl)
                            return
                        }
                        updateDialog.updateInProgress = true
                        updateDialog.statusMessage = qsTr("Starting update…")
                        backend.auto_update()
                    }
                }
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 6

        RowLayout {
            Layout.fillWidth: true
            TabBar {
                id: navigation
                objectName: "mainNavigation"

                Layout.fillWidth: true

                TabButton {
                    Accessible.name: qsTr("Downloads")
                    icon.source: "qrc:/images/graphics/download.svg"
                    icon.width: 24
                    icon.height: 24
                    icon.color: "transparent"
                    display: AbstractButton.IconOnly
                }

                TabButton {
                    Accessible.name: qsTr("Account")
                    icon.source: "qrc:/images/graphics/account.svg"
                    icon.width: 24
                    icon.height: 24
                    icon.color: "transparent"
                    display: AbstractButton.IconOnly
                }

                TabButton {
                    Accessible.name: qsTr("Statistics")
                    icon.source: "qrc:/images/graphics/database.svg"
                    icon.width: 24
                    icon.height: 24
                    icon.color: "transparent"
                    display: AbstractButton.IconOnly
                }

                TabButton {
                    Accessible.name: qsTr("Settings")
                    icon.source: "qrc:/images/graphics/settings.svg"
                    icon.width: 24
                    icon.height: 24
                    icon.color: "transparent"
                    display: AbstractButton.IconOnly
                }

                TabButton {
                    Accessible.name: qsTr("Information")
                    icon.source: "qrc:/images/graphics/information.svg"
                    icon.width: 24
                    icon.height: 24
                    icon.color: "transparent"
                    display: AbstractButton.IconOnly
                }

            }
            NotificationPanel {
                blocked: !appSettings.license_offer_seen || licenseOfferDialog.visible || !appSettings.ukraine_message_seen || ukraineMessageDialog.visible || !appSettings.error_reporting_decided
            }
            AppButton {
                text: qsTr("SUPPORTED WEBSITES")
                onClicked: Qt.openUrlExternally("https://pornfetch.to/#websites")
            }
        }

        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true

            currentIndex: navigation.currentIndex

            DownloadsPage {
            }

            AccountPage {
                backendController: backend
            }

            StatisticsPage {
            }

            SettingsPage {
                // Pass a settings controller here when necessary.
            }

            Item {
                InfoPage {
                    anchors.fill: parent
                    visible: !appSettings.anonymous_mode
                }

                Label {
                    anchors.centerIn: parent
                    text: qsTr("Widget is hidden due to your privacy settings...")
                    font.pixelSize: appSettings.font_size
                    visible: appSettings.anonymous_mode
                }

            }
        }
    }
}
