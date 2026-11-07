import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: root
    required property var settings
    readonly property bool highContrast: settings.high_contrast
    readonly property bool dark: settings.dark_mode
    readonly property real textScale: Math.max(1, settings.font_size / 12)
    readonly property color ink: Theme.ink
    readonly property color mutedInk: Theme.muted
    spacing: 18

    Repeater {
        model: [
            qsTr("Russia's full-scale invasion has brought immense suffering and loss of life to Ukraine. Civilians continue to be killed and injured."),
            qsTr("[The UN has documented conflict-related sexual violence](%1). The International Criminal Court has [issued arrest warrants over the alleged unlawful deportation and transfer of Ukrainian children](%2).")
                .arg("https://ukraine.ohchr.org/en/UN-Human-Rights-report-details-shocking-pattern-of-sexual-violence-amid-Russia-s-full-scale-armed-attack-on-Ukraine")
                .arg("https://www.icc-cpi.int/news/situation-ukraine-icc-judges-issue-arrest-warrants-against-vladimir-vladimirovich-putin-and"),
            qsTr("Ukraine and its people deserve a peaceful, independent future. I don't want their suffering to be forgotten."),
            qsTr("You don't need thousands of euros to make a difference. Even a small donation to a trusted humanitarian organization, such as [UNHCR](%1) or [UNICEF](%2), can help.")
                .arg("https://www.unhcr.org/emergencies/ukraine-emergency")
                .arg("https://www.unicef.org/emergencies/war-ukraine-pose-immediate-threat-children"),
            qsTr("Sharing reliable information and countering disinformation are other ways to contribute.")
        ]
        Label {
            required property string modelData
            required property int index
            Layout.fillWidth: true
            objectName: "ukraineMessageParagraph" + index
            text: modelData
            textFormat: Text.MarkdownText
            linkColor: root.highContrast ? Theme.accent : root.dark ? "#9dc9ff" : "#155eaa"
            onLinkActivated: function(link) { Qt.openUrlExternally(link) }
            HoverHandler {
                cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
            }
            wrapMode: Text.Wrap
            color: root.ink
            font.pixelSize: 15 * root.textScale
            lineHeight: 1.3
        }
    }
    Rectangle {
        Layout.preferredWidth: 48
        implicitHeight: 2
        color: root.dark ? "#f3cf63" : "#9c7617"
    }
    Label {
        Layout.fillWidth: true
        text: qsTr("Thank you for taking a moment to read this.")
        textFormat: Text.PlainText
        wrapMode: Text.Wrap
        color: root.mutedInk
        font.pixelSize: 15 * root.textScale
        font.italic: true
        lineHeight: 1.3
    }

}
