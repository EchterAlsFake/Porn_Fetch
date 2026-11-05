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
    title: qsTr("Porn Fetch Premium")
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
        ColumnLayout {
            width: offerScroll.availableWidth
            spacing: 20
            Label {
                Layout.fillWidth: true
                text: qsTr("PORN FETCH PREMIUM")
                color: root.accent
                font.pixelSize: 12 * root.textScale
                font.letterSpacing: 1.5
                font.weight: Font.DemiBold
                wrapMode: Text.Wrap
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 20
                Label {
                    objectName: "licenseOfferPrice"
                    text: "19.99 €"
                    color: root.ink
                    font.pixelSize: 44 * root.textScale
                    font.weight: Font.Bold
                }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("One-time payment.\nNo subscription.")
                    color: root.muted
                    font.pixelSize: 14 * root.textScale
                    wrapMode: Text.Wrap
                }
            }
            Label {
                Layout.fillWidth: true
                text: qsTr("Keep premium access to the version you first activate and all updates released in the following year — for life.")
                color: root.ink
                font.pixelSize: 16 * root.textScale
                wrapMode: Text.Wrap
                lineHeight: 1.2
            }
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 10
                SectionHeading { text: qsTr("Features") }
                Repeater {
                    model: [
                        qsTr("1080p, 1440p and 4K quality, when available"),
                        qsTr("Parallel downloads"),
                        qsTr("Bulk downloads from profiles, channels, models and pornstars"),
                        qsTr("Full playlists"),
                        qsTr("Support independent development"),
                        qsTr("Help cover code signing certificates and server costs")
                    ]
                    RowLayout {
                        required property string modelData
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                        spacing: 12
                        Image {
                            source: "qrc:/images/graphics/payments/check.svg"
                            Layout.preferredWidth: 20
                            Layout.preferredHeight: 20
                            Layout.alignment: Qt.AlignTop
                            Accessible.ignored: true
                        }
                        Label {
                            Layout.fillWidth: true
                            text: modelData
                            color: root.ink
                            font.pixelSize: 15 * root.textScale
                            wrapMode: Text.Wrap
                        }
                    }
                }
            }
            Rectangle {
                Layout.fillWidth: true
                implicitHeight: payments.implicitHeight + 32
                radius: 12
                color: root.highContrast ? Theme.background : "#20171d"
                border.color: root.highContrast ? root.outline : "#5c3447"
                ColumnLayout {
                    id: payments
                    anchors { left: parent.left; right: parent.right; top: parent.top; margins: 16 }
                    spacing: 12
                    SectionHeading { text: qsTr("Pay with crypto or credit card"); color: root.accent }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("350+ currencies supported")
                        color: root.ink
                        font.pixelSize: 15 * root.textScale
                        font.weight: Font.DemiBold
                        wrapMode: Text.Wrap
                    }
                    Flow {
                        Layout.fillWidth: true
                        spacing: 16
                        Repeater {
                            model: [
                                { name: "Bitcoin", file: "bitcoin" },
                                { name: "Monero", file: "monero" },
                                { name: "Ethereum", file: "ethereum" },
                                { name: "Litecoin", file: "litecoin" }
                            ]
                            Column {
                                required property var modelData
                                width: 56 * root.textScale
                                spacing: 6
                                Image {
                                    objectName: "paymentLogo_" + modelData.file
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    width: 30; height: 30
                                    source: "qrc:/images/graphics/payments/" + modelData.file + ".svg"
                                    fillMode: Image.PreserveAspectFit
                                    Accessible.role: Accessible.Graphic
                                    Accessible.name: modelData.name
                                }
                                Label {
                                    width: parent.width
                                    text: modelData.name
                                    color: root.muted
                                    font.pixelSize: 11 * root.textScale
                                    horizontalAlignment: Text.AlignHCenter
                                }
                            }
                        }
                    }
                }
            }
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 8
                SectionHeading { text: qsTr("Private, and made to share") }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("No account, hardware ID, tracking or device fingerprinting for licensing. Your key is not tied to your IP address.")
                    color: root.muted
                    font.pixelSize: 14 * root.textScale
                    wrapMode: Text.Wrap
                }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Share it with friends and family — up to 10 active installations in total.")
                    color: root.ink
                    font.pixelSize: 14 * root.textScale
                    wrapMode: Text.Wrap
                }
            }
            Label {
                Layout.fillWidth: true
                text: qsTr("After purchase, open Settings → Import License File to activate your key.")
                color: root.accent
                font.pixelSize: 14 * root.textScale
                wrapMode: Text.Wrap
            }
            Label {
                Layout.fillWidth: true
                text: qsTr("Activation uses a random installation ID. Online validation is required, with up to 7 days offline after a successful check.")
                color: root.muted
                font.pixelSize: 12 * root.textScale
                wrapMode: Text.Wrap
            }
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
    component SectionHeading: Label {
        Layout.fillWidth: true
        color: root.ink
        font.pixelSize: 18 * root.textScale
        font.weight: Font.DemiBold
        wrapMode: Text.Wrap
    }
}
