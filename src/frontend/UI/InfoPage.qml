import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Pane {
    id: root
    padding: 0
    readonly property bool dark: appSettings.dark_mode || appSettings.high_contrast
    readonly property color pageColor: appSettings.high_contrast ? "#000000" : dark ? "#17191f" : "#f5f6f8"
    readonly property color cardColor: appSettings.high_contrast ? "#000000" : dark ? "#22252d" : "#ffffff"
    readonly property color ink: dark ? "#f1f3f8" : "#202431"
    readonly property color muted: appSettings.high_contrast ? ink : dark ? "#b9c0cf" : "#566176"
    readonly property color outline: appSettings.high_contrast ? "#ffffff" : dark ? "#3a404d" : "#dce0e8"
    readonly property real textScale: Math.max(1, appSettings.font_size / 12)
    Material.theme: root.dark ? Material.Dark : Material.Light
    Material.foreground: root.ink
    palette.buttonText: root.ink
    palette.text: root.ink
    palette.button: root.cardColor
    background: Rectangle { color: root.pageColor }

    ScrollView {
        id: scroll
        anchors.fill: parent
        contentWidth: availableWidth
        clip: true
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            width: scroll.availableWidth
            spacing: 16
            Item { implicitHeight: 8 }
            ColumnLayout {
                Layout.fillWidth: true
                Layout.leftMargin: 24
                Layout.rightMargin: 24
                spacing: 8
                Label {
                    text: qsTr("ABOUT THE PROJECT")
                    color: root.muted
                    font.pixelSize: 11 * root.textScale
                    font.letterSpacing: 1.5
                }
                Label {
                    Layout.fillWidth: true
                    text: "Porn Fetch"
                    color: root.ink
                    font.pixelSize: 32 * root.textScale
                    font.weight: Font.DemiBold
                    wrapMode: Text.Wrap
                }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Version %1 · By Johannes Habel (EchterAlsFake)").arg(Qt.application.version)
                    color: root.muted
                    wrapMode: Text.Wrap
                }
                Flow {
                    Layout.fillWidth: true
                    spacing: 8
                    Button { text: qsTr("Website"); onClicked: Qt.openUrlExternally("https://pornfetch.to/") }
                    Button { text: qsTr("Source code"); onClicked: Qt.openUrlExternally("https://github.com/EchterAlsFake/Porn_Fetch") }
                    Button { text: qsTr("Report a problem"); onClicked: Qt.openUrlExternally("https://github.com/EchterAlsFake/Porn_Fetch/issues") }
                }
            }

            CreditCard {
                title: qsTr("People behind Porn Fetch")
                content: qsTr("Created and maintained by **Johannes Habel (EchterAlsFake)**.\n\nSpecial thanks to [Egsagon](https://github.com/Egsagon), whose original PHUB API helped make the early versions possible.")
            }
            CreditCard {
                title: qsTr("Contributors")
                content: qsTr("Thank you for the code, bug reports, ideas and translations contributed to earlier versions. The current interface is English-only.\n\n[Egsagon](https://github.com/Egsagon) · [RSDCFGVHBJNKML](https://github.com/RSDCFGVHBJNKML) · [Joshua-auhsoj](https://github.com/Joshua-auhsoj) · [RonLar1132](https://github.com/RonLar1132) · [xxIndirect](https://github.com/xxIndirect) · [efraxs](https://github.com/efraxs) · [omar-st](https://github.com/omar-st) · [SShattered](https://github.com/SShattered) · [journeym](https://github.com/journeym) · [Joly0](https://github.com/Joly0) · [FatalPuppet](https://github.com/FatalPuppet) · [HeathenSkwerl](https://github.com/HeathenSkwerl)")
            }
            CreditCard {
                title: qsTr("Built with")
                content: qsTr("**Interface** — Python, PySide6 and Qt Quick; Rich and Questionary for the CLI.\n\n**Downloads** — eaf_base_api, curl-cffi and the provider API libraries.\n\n**Media and storage** — a separate FFmpeg program for media processing; PocketBase for optional desktop history and statistics.\n\n**Builds** — Nuitka, PyInstaller, Qt Installer Framework, and the Android and iOS toolchains.\n\nEach component keeps its own license. The third-party notices contain the license information.")
            }
            CreditCard {
                title: qsTr("Licenses and attribution")
                content: qsTr("Application-owned material uses the **Porn Fetch Source-Available License 1.0**. Earlier GPL copies retain their original rights.\n\nThanks to the authors of the libraries, icons and other assets used by Porn Fetch. Full contributor and asset credits are kept in the repository.")
            }
            Flow {
                Layout.fillWidth: true
                Layout.leftMargin: 24
                Layout.rightMargin: 24
                spacing: 8
                Button {
                    text: qsTr("Application license")
                    onClicked: { legalDialog.showNotices = false; legalDialog.open() }
                }
                Button {
                    text: qsTr("Third-party notices")
                    onClicked: { legalDialog.showNotices = true; legalDialog.open() }
                }
                Button {
                    text: qsTr("Full credits")
                    onClicked: Qt.openUrlExternally("https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/CREDITS.md")
                }
            }
            Label {
                Layout.fillWidth: true
                Layout.margins: 24
                text: qsTr("Copyright © 2023–2026 Johannes Habel")
                color: root.muted
                wrapMode: Text.Wrap
            }
        }
    }

    Dialog {
        id: legalDialog
        property bool showNotices: false
        title: showNotices ? qsTr("Third-party notices") : qsTr("Porn Fetch application license")
        modal: true
        anchors.centerIn: parent
        width: Math.min(root.width - 32, 720)
        height: Math.min(root.height - 32, 520)
        standardButtons: Dialog.Close
        contentItem: ScrollView {
            TextArea {
                readOnly: true
                selectByMouse: true
                wrapMode: TextArea.Wrap
                text: legalDialog.showNotices ? thirdPartyNoticesText : applicationLicenseText
            }
        }
    }

    component CreditCard: Rectangle {
        id: card
        objectName: "creditCard"
        property string title
        property string content
        Layout.fillWidth: true
        Layout.leftMargin: 24
        Layout.rightMargin: 24
        Layout.minimumWidth: 0
        implicitHeight: body.implicitHeight + 40
        color: root.cardColor
        border.color: root.outline
        radius: 12
        ColumnLayout {
            id: body
            anchors { left: parent.left; right: parent.right; top: parent.top; margins: 20 }
            spacing: 12
            Label {
                Layout.fillWidth: true
                text: card.title
                color: root.ink
                font.pixelSize: 19 * root.textScale
                font.weight: Font.DemiBold
                wrapMode: Text.Wrap
            }
            Label {
                Layout.fillWidth: true
                text: card.content
                color: root.muted
                textFormat: Text.MarkdownText
                wrapMode: Text.Wrap
                font.pixelSize: 14 * root.textScale
                lineHeight: 1.3
                onLinkActivated: function(link) { Qt.openUrlExternally(link) }
                HoverHandler { cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor }
            }
        }
    }
}
