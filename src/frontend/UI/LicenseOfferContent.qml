import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: root
    required property var settings
    readonly property bool highContrast: settings.high_contrast
    readonly property real textScale: Math.max(1, settings.font_size / 12)
    property color ink: Theme.ink
    property color muted: highContrast ? ink : Theme.muted
    property color accent: Theme.accent
    readonly property color outline: Theme.outline
    spacing: 20
    Label {
        Layout.fillWidth: true
        text: qsTr("LIFETIME PREMIUM")
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
            text: "29.99 €"
            color: root.ink
            font.pixelSize: 44 * root.textScale
            font.weight: Font.Bold
        }
        Label {
            Layout.fillWidth: true
            text: qsTr("Buy once. Use forever.\nNo subscription.")
            color: root.muted
            font.pixelSize: 14 * root.textScale
            wrapMode: Text.Wrap
        }
    }
    Label {
        Layout.fillWidth: true
        text: qsTr("Your Premium license never expires. Every future Porn Fetch update and feature I release is included. Future development has no guaranteed duration.")
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
                qsTr("Every future update and feature included"),
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
        color: Theme.surface
        border.color: root.outline
        ColumnLayout {
            id: payments
            anchors { left: parent.left; right: parent.right; top: parent.top; margins: 16 }
            spacing: 12
            SectionHeading { text: qsTr("Pay with Crypto (NowPayments) or Credit Card / PayPal (Patreon)"); color: root.accent }
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
            text: qsTr("Share your license with family and personal friends you know in real life and have met in person, with up to 10 active installations in total, including your own. Membership in a Discord server or another online community alone does not make someone a friend for private sharing.")
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
        text: qsTr("Activation uses a random installation ID. Periodic online validation is required, with up to 7 days offline after a successful check. If I permanently close the licensing service, I will provide an offline unlock before closure so existing buyers can continue using Premium.")
        color: root.muted
        font.pixelSize: 12 * root.textScale
        wrapMode: Text.Wrap
    }
    component SectionHeading: Label {
        Layout.fillWidth: true
        color: root.ink
        font.pixelSize: 18 * root.textScale
        font.weight: Font.DemiBold
        wrapMode: Text.Wrap
    }
}
