import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Dialog {
    id: root
    ContrastPopupBackground { popup: root }
    objectName: "licenseOfferDialog"
    required property var settings
    property bool fullScreen: false
    readonly property bool highContrast: settings.high_contrast
    readonly property real textScale: Math.max(1, settings.font_size / 12)
    readonly property color surface: highContrast ? Theme.background : "#101012"
    readonly property color ink: highContrast ? Theme.ink : "#f5f2f4"
    readonly property color muted: highContrast ? ink : "#b7b1ba"
    readonly property color accent: highContrast ? Theme.accent : "#ef88b2"
    readonly property color outline: highContrast ? Theme.ink : "#3b343e"
    Material.theme: highContrast && !settings.dark_mode ? Material.Light : Material.Dark
    Material.foreground: root.ink
    palette.buttonText: root.ink
    signal dismissed()

    function presentOnce() {
        if (visible)
            return true
        if (settings.license_offer_seen)
            return false
        open()
        return true
    }

    parent: Overlay.overlay
    anchors.centerIn: parent
    width: fullScreen ? parent.width : Math.min(parent.width - 24, 680)
    height: fullScreen ? parent.height : Math.min(parent.height - 24, offerScroll.contentHeight + topPadding + bottomPadding + footer.implicitHeight)
    margins: 0
    topInset: 0
    bottomInset: 0
    leftInset: 0
    rightInset: 0
    padding: width < 480 ? 20 : 32
    topPadding: padding + (fullScreen ? parent.SafeArea.margins.top : 0)
    leftPadding: padding + (fullScreen ? parent.SafeArea.margins.left : 0)
    rightPadding: padding + (fullScreen ? parent.SafeArea.margins.right : 0)
    modal: true
    focus: true
    z: 1000
    title: qsTr("Lifetime Premium")
    closePolicy: Popup.CloseOnEscape
    onOpened: {
        settings.mark_license_offer_seen()
        offerScroll.forceActiveFocus()
    }
    onClosed: dismissed()

    background: Rectangle {
        color: root.surface
        radius: root.fullScreen ? 0 : 18
        border.width: root.highContrast ? 2 : 1
        border.color: root.outline
    }
    header: Item {}
    contentItem: ScrollView {
        id: offerScroll
        objectName: "licenseOfferScroll"
        contentWidth: availableWidth
        clip: true
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        LicenseOfferContent {
            settings: root.settings
            width: offerScroll.availableWidth
            ink: root.ink
            muted: root.muted
            accent: root.accent
        }
    }

    footer: Item {
        implicitHeight: actions.implicitHeight + 24 + (root.fullScreen ? root.parent.SafeArea.margins.bottom : 0)
        GridLayout {
            id: actions
            anchors { left: parent.left; right: parent.right; top: parent.top; margins: 12 }
            anchors.leftMargin: 12 + (root.fullScreen ? root.parent.SafeArea.margins.left : 0)
            anchors.rightMargin: 12 + (root.fullScreen ? root.parent.SafeArea.margins.right : 0)
            columns: root.width < 480 ? 1 : 2
            columnSpacing: 12
            rowSpacing: 8
            AppButton {
                objectName: "licenseOfferBuyButton"
                Layout.fillWidth: true
                text: qsTr("Get license ↗")
                Accessible.description: qsTr("Open pornfetch.to in your browser.")
                implicitHeight: Math.max(48, contentItem.implicitHeight + topPadding + bottomPadding)
                contentItem: Label {
                    text: parent.text
                    color: "#25141e"
                    font.pixelSize: 15 * root.textScale
                    font.weight: Font.DemiBold
                    wrapMode: Text.Wrap
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    radius: 10
                    color: root.highContrast ? Theme.accent : parent.down ? "#d16b96" : parent.hovered ? "#ffa3ca" : root.accent
                    border.width: parent.activeFocus ? 2 : 0
                    border.color: root.ink
                }
                onClicked: Qt.openUrlExternally("https://pornfetch.to")
            }
            AppButton {
                objectName: "licenseOfferContinueButton"
                Layout.fillWidth: true
                text: qsTr("Continue with free version")
                contentItem: Label {
                    text: parent.text
                    color: root.ink
                    font.pixelSize: 14 * root.textScale
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.Wrap
                }
                background: Rectangle {
                    implicitHeight: 48
                    radius: 10
                    color: parent.down || parent.hovered ? "#2b222a" : "transparent"
                    border.width: parent.activeFocus ? 2 : 1
                    border.color: root.muted
                }
                implicitHeight: Math.max(48, contentItem.implicitHeight + topPadding + bottomPadding)
                onClicked: root.close()
            }
        }
    }
}
