import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Dialog {
    id: root
    objectName: "licenseOfferDialog"
    required property var settings
    readonly property bool highContrast: settings.high_contrast
    readonly property real textScale: Math.max(1, settings.font_size / 12)
    readonly property color surface: highContrast ? "#000000" : "#101012"
    readonly property color ink: "#f5f2f4"
    readonly property color muted: highContrast ? ink : "#b7b1ba"
    readonly property color accent: highContrast ? "#ffff00" : "#ef88b2"
    readonly property color outline: highContrast ? "#ffffff" : "#3b343e"
    Material.theme: Material.Dark
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
    width: Math.min(parent.width - 24, 680)
    height: Math.min(parent.height - 24, offerScroll.contentHeight + topPadding + bottomPadding + footer.implicitHeight)
    padding: width < 480 ? 20 : 32
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
        radius: 18
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
                color: root.highContrast ? "#000000" : "#20171d"
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
        implicitHeight: actions.implicitHeight + 24
        GridLayout {
            id: actions
            anchors { left: parent.left; right: parent.right; top: parent.top; margins: 12 }
            columns: root.width < 480 ? 1 : 2
            columnSpacing: 12
            rowSpacing: 8
            Button {
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
                    color: root.highContrast ? "#ffff00" : parent.down ? "#d16b96" : parent.hovered ? "#ffa3ca" : root.accent
                    border.width: parent.activeFocus ? 2 : 0
                    border.color: root.ink
                }
                onClicked: Qt.openUrlExternally("https://pornfetch.to")
            }
            Button {
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
