import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Dialogs as Dialogs
import QtQuick.Layouts

Dialog {
    id: root
    objectName: "firstRunSetup"
    required property var settings
    required property string licenseText
    required property string reportDisclosure
    property bool fullScreen: false
    property bool requireOutputFolder: Qt.platform.os === "android"
    property var steps: []
    property int currentIndex: 0
    property int reportingChoice: -1
    readonly property string step: steps.length ? steps[currentIndex] : ""
    readonly property bool active: !settings.smoke_test && (!settings.setup_completed || visible)
    readonly property bool compactHeight: height < 480
    readonly property real textScale: Math.max(1, settings.font_size / 12)
    readonly property string stepTitle: step === "license" ? qsTr("Review the license")
        : step === "offer" ? qsTr("Choose how you use Porn Fetch")
        : step === "reporting" ? qsTr("Make error reporting your choice")
        : step === "ukraine" ? qsTr("A personal message from me") : qsTr("Choose where your videos are saved")
    readonly property bool canContinue: step === "license" ? acceptLicense.checked
        : step === "reporting" ? reportingChoice >= 0
        : step === "folder" ? !!settings.android_output_folder : true
    signal finished()
    signal quitRequested()

    function begin() {
        if (settings.smoke_test || settings.setup_completed) return false
        var pending = []
        if (!settings.license_accepted) pending.push("license")
        if (!settings.license_offer_seen) pending.push("offer")
        if (!settings.error_reporting_decided) pending.push("reporting")
        if (!settings.ukraine_message_seen) pending.push("ukraine")
        if (requireOutputFolder && !settings.android_output_folder) pending.push("folder")
        steps = pending
        currentIndex = 0
        if (!steps.length) {
            if (settings.finish_setup(requireOutputFolder)) finished()
            return false
        }
        open()
        return true
    }

    function advance() {
        if (!canContinue) return
        if (step === "license") settings.accept_application_license(licenseText)
        else if (step === "offer") settings.mark_license_offer_seen()
        else if (step === "reporting") settings.set_error_reporting_options(reportingChoice !== 0, reportingChoice === 2)
        else if (step === "ukraine") settings.mark_ukraine_message_seen()
        if (currentIndex + 1 < steps.length) {
            currentIndex += 1
        } else if (settings.finish_setup(requireOutputFolder)) {
            close()
            finished()
        }
    }

    function resetScroll() {
        Qt.callLater(function() {
            pageScroll.contentItem.contentY = 0
            pageScroll.forceActiveFocus(Qt.TabFocusReason)
        })
    }
    onCurrentIndexChanged: resetScroll()
    onOpened: resetScroll()
    font.pointSize: settings.font_size
    Material.theme: settings.dark_mode ? Material.Dark : Material.Light
    Material.accent: Theme.accent
    Material.foreground: Theme.ink
    palette.text: Theme.ink
    palette.buttonText: Theme.ink
    palette.windowText: Theme.ink
    palette.highlight: Theme.accent
    palette.highlightedText: Theme.selectionInk
    palette.disabled.text: Theme.disabledInk
    palette.disabled.buttonText: Theme.disabledInk
    parent: Overlay.overlay
    anchors.centerIn: parent
    width: fullScreen ? parent.width : Math.min(900, parent.width - 32)
    height: fullScreen ? parent.height : Math.min(820, parent.height - 32)
    margins: 0
    topInset: 0; bottomInset: 0; leftInset: 0; rightInset: 0
    padding: compactHeight ? 14 : width < 480 ? 20 : 32
    leftPadding: padding + (fullScreen ? parent.SafeArea.margins.left : 0)
    rightPadding: padding + (fullScreen ? parent.SafeArea.margins.right : 0)
    topPadding: padding + (fullScreen ? parent.SafeArea.margins.top : 0)
    bottomPadding: 12 + (fullScreen ? parent.SafeArea.margins.bottom : 0)
    modal: true
    focus: true
    closePolicy: Popup.NoAutoClose
    title: qsTr("Set up Porn Fetch")
    z: 1000
    background: Rectangle {
        color: Theme.background
        radius: root.fullScreen ? 0 : 18
        border.width: root.fullScreen ? 0 : root.settings.high_contrast ? 2 : 1
        border.color: root.settings.high_contrast ? Theme.ink : Theme.outline
    }

    header: ColumnLayout {
        spacing: root.compactHeight ? 6 : 10
        RowLayout {
            Layout.fillWidth: true
            Layout.leftMargin: root.leftPadding
            Layout.rightMargin: root.rightPadding
            Layout.topMargin: root.topPadding
            Label {
                text: qsTr("PORN FETCH")
                color: Theme.accent
                font.bold: true
                font.letterSpacing: 2
                font.pixelSize: 12 * root.textScale
            }
            Item { Layout.fillWidth: true }
            Label {
                objectName: "setupStepCounter"
                text: qsTr("Setup %1 of %2").arg(root.currentIndex + 1).arg(root.steps.length)
                color: Theme.muted
                font.pixelSize: 12 * root.textScale
            }
            ToolButton {
                id: discoveryButton
                objectName: "ukraineDiscoveryButton"
                visible: root.step === "ukraine"
                Layout.preferredWidth: 44
                Layout.preferredHeight: 44
                hoverEnabled: true
                text: "✦"
                Accessible.name: qsTr("A small surprise")
                Accessible.description: qsTr("Open a surprise in your browser.")
                ToolTip.visible: hovered || activeFocus
                ToolTip.text: qsTr("Curious?")
                HoverHandler { cursorShape: Qt.PointingHandCursor }
                contentItem: Label {
                    text: discoveryButton.text
                    color: Theme.accent
                    font.pixelSize: 24
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Accessible.ignored: true
                }
                background: Rectangle {
                    color: discoveryButton.down ? Qt.rgba(Theme.accent.r, Theme.accent.g, Theme.accent.b, 0.24)
                        : discoveryButton.hovered ? Qt.rgba(Theme.accent.r, Theme.accent.g, Theme.accent.b, 0.12) : Theme.surface
                    radius: 12
                    border.width: discoveryButton.activeFocus ? 2 : 1
                    border.color: discoveryButton.activeFocus || discoveryButton.hovered ? Theme.accent : Theme.outline
                }
                onClicked: Qt.openUrlExternally("https://www.youtube.com/watch?v=lV9q901vS6o")
            }
        }
        ProgressBar {
            Layout.fillWidth: true
            Layout.leftMargin: root.leftPadding
            Layout.rightMargin: root.rightPadding
            from: 0; to: Math.max(1, root.steps.length)
            value: root.currentIndex + 1
            Accessible.name: qsTr("Setup progress")
        }
        Label {
            Layout.fillWidth: true
            Layout.leftMargin: root.leftPadding
            Layout.rightMargin: root.rightPadding
            text: root.stepTitle
            color: Theme.ink
            font.pixelSize: (root.width < 480 || root.compactHeight ? 23 : 30) * root.textScale
            font.weight: Font.DemiBold
            wrapMode: Text.Wrap
            Accessible.role: Accessible.Heading
        }
        Label {
            Layout.fillWidth: true
            Layout.leftMargin: root.leftPadding
            Layout.rightMargin: root.rightPadding
            Layout.bottomMargin: 8
            text: root.compactHeight ? qsTr("One-time setup. Your choices are saved on this device.")
                : qsTr("A one-time setup for this device. Your choices are saved, and this setup will not appear again after you finish. You can change reporting and storage in Settings.")
            color: Theme.muted
            font.pixelSize: 13 * root.textScale
            wrapMode: Text.Wrap
        }
    }

    contentItem: ColumnLayout {
        spacing: 12
        SmoothScrollView {
            id: pageScroll
            objectName: "setupPageScroll"
            Layout.fillWidth: true
            Layout.fillHeight: true
            contentWidth: availableWidth
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
            ColumnLayout {
                width: pageScroll.availableWidth
                spacing: 18
                Rectangle {
                    visible: root.step === "license"
                    Layout.fillWidth: true
                    implicitHeight: licenseBody.contentHeight + 32
                    color: Theme.surface
                    radius: 10
                    border.color: Theme.outline
                    TextEdit {
                        id: licenseBody
                        objectName: "setupLicenseText"
                        anchors { left: parent.left; right: parent.right; top: parent.top; margins: 16 }
                        height: contentHeight
                        text: root.licenseText
                        textFormat: TextEdit.PlainText
                        readOnly: true
                        selectByMouse: true
                        wrapMode: TextEdit.Wrap
                        color: Theme.ink
                        font.pixelSize: 14 * root.textScale
                        Accessible.name: qsTr("Full application license")
                    }
                }
                LicenseOfferContent {
                    settings: root.settings
                    visible: root.step === "offer"
                    Layout.fillWidth: true
                }
                AppButton {
                    objectName: "setupBuyLicenseButton"
                    visible: root.step === "offer"
                    Layout.fillWidth: true
                    text: qsTr("Get a license")
                    onClicked: Qt.openUrlExternally("https://pornfetch.to")
                }
                ColumnLayout {
                    visible: root.step === "reporting"
                    Layout.fillWidth: true
                    spacing: 12
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Your reports stay private with me. I never publish them or share them with anyone.")
                        color: Theme.ink
                        font.bold: true
                        wrapMode: Text.Wrap
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("I am not interested in what you watch or download. I do not go through reported video URLs to see what you watched. These reports help me reproduce failures and improve the app.")
                        color: Theme.muted
                        wrapMode: Text.Wrap
                    }
                    ButtonGroup { id: reportOptions }
                    ReportOption {
                        objectName: "setupReportsOff"
                        Layout.fillWidth: true
                        text: qsTr("Off: no error reports")
                        ButtonGroup.group: reportOptions
                        checked: root.reportingChoice === 0
                        onClicked: root.reportingChoice = 0
                    }
                    ReportOption {
                        objectName: "setupReportsBasic"
                        Layout.fillWidth: true
                        text: qsTr("Basic reports")
                        ButtonGroup.group: reportOptions
                        checked: root.reportingChoice === 1
                        onClicked: root.reportingChoice = 1
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("App/OS information, error type, operation and provider or quality. No video URLs, exception messages, local paths or Python tracebacks.")
                        color: Theme.muted
                        wrapMode: Text.Wrap
                    }
                    ReportOption {
                        objectName: "setupReportsFull"
                        Layout.fillWidth: true
                        text: qsTr("Full Python tracebacks and video URLs")
                        ButtonGroup.group: reportOptions
                        checked: root.reportingChoice === 2
                        onClicked: root.reportingChoice = 2
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Full error reports make a significant difference: they often give me the details I need to identify an issue immediately and fix it much faster. Each fix benefits everyone using Porn Fetch.")
                        color: Theme.ink
                        font.bold: true
                        wrapMode: Text.Wrap
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Includes complete exception chains and diagnostic context. Video URLs, query strings, messages and paths can reveal sensitive information. These reports are not anonymous.")
                        color: Theme.muted
                        wrapMode: Text.Wrap
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("All choices let you use the app. You can change your choice later in Settings.")
                        color: Theme.ink
                        wrapMode: Text.Wrap
                    }
                    AppButton {
                        id: disclosureToggle
                        Layout.fillWidth: true
                        checkable: true
                        text: checked ? qsTr("Hide full reporting disclosure") : qsTr("How reports are sent, stored and deleted")
                        Accessible.description: qsTr("Expand the full error-reporting disclosure")
                    }
                    Label {
                        visible: disclosureToggle.checked
                        Layout.fillWidth: true
                        text: root.reportDisclosure
                        textFormat: Text.PlainText
                        color: Theme.muted
                        wrapMode: Text.Wrap
                    }
                }
                ColumnLayout {
                    visible: root.step === "ukraine"
                    Layout.fillWidth: true
                    spacing: 16
                    RowLayout {
                        Layout.fillWidth: true
                        Image {
                            source: "qrc:/images/graphics/ukraine_flag.svg"
                            Layout.preferredWidth: 48
                            Layout.preferredHeight: 32
                        }
                        Label {
                            Layout.fillWidth: true
                            text: qsTr("I stand with Ukraine.")
                            color: Theme.ink
                            font.bold: true
                            font.pixelSize: 22 * root.textScale
                            wrapMode: Text.Wrap
                        }
                    }
                    UkraineMessageContent { settings: root.settings; Layout.fillWidth: true }
                }
                ColumnLayout {
                    visible: root.step === "folder"
                    Layout.fillWidth: true
                    spacing: 18
                    Image { source: "qrc:/images/graphics/download.png"; Layout.preferredWidth: 56; Layout.preferredHeight: 56 }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Choose a shared folder so you can open your completed videos in a player or file manager.")
                        color: Theme.ink
                        font.bold: true
                        wrapMode: Text.Wrap
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Without an output folder, videos stay in Android's private app directory. Your normal file manager and other apps cannot open them there; accessing that directory generally requires root. You need to choose a different folder before using the downloader.")
                        color: Theme.muted
                        wrapMode: Text.Wrap
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("In the system picker, open or create a folder and allow Porn Fetch to use it. The permission is saved for future launches. Cancelling keeps you on this page.")
                        color: Theme.muted
                        wrapMode: Text.Wrap
                    }
                    Label {
                        objectName: "setupFolderStatus"
                        Layout.fillWidth: true
                        text: root.settings.android_output_folder
                            ? qsTr("Folder selected. Completed videos will be saved there automatically.")
                            : qsTr("Choose an output folder to finish setup.")
                        color: root.settings.android_output_folder ? Theme.accent : Theme.ink
                        wrapMode: Text.Wrap
                    }
                }
            }
        }
        AppButton {
            objectName: "setupChooseFolderButton"
            visible: root.step === "folder"
            Layout.fillWidth: true
            text: root.settings.android_output_folder ? qsTr("Choose another folder") : qsTr("Choose output folder")
            onClicked: folderPicker.open()
        }
        CheckBox {
            id: acceptLicense
            objectName: "setupAcceptLicenseCheckBox"
            visible: root.step === "license"
            Layout.fillWidth: true
            text: qsTr("I have read and accept the Porn Fetch Source-Available License 1.0.")
            contentItem: Label {
                text: acceptLicense.text
                leftPadding: acceptLicense.indicator.width + acceptLicense.spacing
                color: Theme.ink
                wrapMode: Text.Wrap
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    component ReportOption: RadioButton {
        id: control
        contentItem: Label {
            text: control.text
            font: control.font
            color: Theme.ink
            leftPadding: control.indicator.width + control.spacing
            wrapMode: Text.Wrap
            verticalAlignment: Text.AlignVCenter
        }
    }

    Dialogs.FolderDialog {
        id: folderPicker
        objectName: "setupFolderPicker"
        title: qsTr("Choose where to save videos")
        onAccepted: backend.set_android_output_folder(selectedFolder.toString())
    }

    footer: ColumnLayout {
        spacing: 8
        RowLayout {
            Layout.fillWidth: true
            Layout.leftMargin: root.leftPadding
            Layout.rightMargin: root.rightPadding
            Layout.topMargin: 10
            Layout.bottomMargin: root.bottomPadding
            AppButton {
                objectName: "setupBackButton"
                text: root.currentIndex ? qsTr("Back") : root.step === "license" ? qsTr("Decline and exit") : qsTr("Exit setup")
                onClicked: root.currentIndex ? root.currentIndex -= 1 : root.quitRequested()
            }
            Item { Layout.fillWidth: true }
            AppButton {
                objectName: "setupContinueButton"
                text: root.currentIndex === root.steps.length - 1 ? qsTr("Finish setup")
                    : root.step === "offer" ? qsTr("Continue free") : qsTr("Continue")
                enabled: root.canContinue
                highlighted: true
                onClicked: root.advance()
            }
        }
    }
}
