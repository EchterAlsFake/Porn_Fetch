import QtQuick
import "CreatorFocus.js" as CreatorFocus
import QtQuick.Controls

AppButton {
    id: root
    readonly property real fontScale: typeof appSettings !== "undefined" && appSettings ? Math.max(1, appSettings.font_size / 12) : 1
    readonly property bool motionEnabled: !Theme.highContrast && !(typeof appSettings !== "undefined" && appSettings && appSettings.reduced_motion)
    readonly property color primaryFill: Theme.highContrast ? Theme.accent : Qt.tint(Theme.accent, Theme.dark ? Qt.rgba(1, 1, 1, 0.36) : Qt.rgba(0, 0, 0, 0.28))
    function readableInk(color) {
        function linear(c) { return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4) }
        var luminance = 0.2126 * linear(color.r) + 0.7152 * linear(color.g) + 0.0722 * linear(color.b)
        return (luminance + 0.05) / 0.05 >= 1.05 / (luminance + 0.05) ? "#000000" : "#ffffff"
    }
    implicitHeight: Math.max(48, caption.implicitHeight + 28)
    implicitWidth: caption.implicitWidth + 36
    padding: 14
    hoverEnabled: true
    property real animatedScale: !root.enabled ? 1 : root.down ? 0.98 : root.hovered ? 1.025 : 1
    scale: root.motionEnabled ? animatedScale : 1
    Behavior on animatedScale { enabled: root.motionEnabled; NumberAnimation { duration: 120; easing.type: Easing.OutCubic } }
    Keys.onDownPressed: CreatorFocus.move(root, true)
    Keys.onUpPressed: CreatorFocus.move(root, false)
    Keys.onRightPressed: CreatorFocus.move(root, true)
    Keys.onLeftPressed: CreatorFocus.move(root, false)
    Keys.onReturnPressed: clicked()
    Keys.onEnterPressed: clicked()
    background: Rectangle {
        id: buttonSurface
        objectName: "creatorButtonBackground"
        radius: 7
        color: root.highlighted && root.enabled
            ? Qt.tint(root.primaryFill, root.down ? Qt.rgba(0, 0, 0, 0.16) : root.hovered ? (Theme.dark ? Qt.rgba(1, 1, 1, 0.18) : Qt.rgba(0, 0, 0, 0.12)) : "transparent")
            : root.enabled && (root.down || root.hovered)
                ? Qt.tint(Theme.surface, Qt.rgba(Theme.accent.r, Theme.accent.g, Theme.accent.b, root.down ? 0.30 : 0.18))
                : root.flat ? Qt.tint(Theme.surface, Qt.rgba(Theme.accent.r, Theme.accent.g, Theme.accent.b, 0.06)) : Theme.surface
        border.width: root.visualFocus ? 3 : 1
        border.color: root.visualFocus || (root.enabled && root.hovered) ? Theme.accent : Theme.highContrast ? Theme.ink : Qt.rgba(Theme.outline.r, Theme.outline.g, Theme.outline.b, 0.8)
        opacity: root.enabled ? 1 : 0.6
        Behavior on color { enabled: root.motionEnabled; ColorAnimation { duration: 140; easing.type: Easing.OutCubic } }
        Behavior on border.color { enabled: root.motionEnabled; ColorAnimation { duration: 140 } }
    }
    contentItem: Label {
        id: caption
        text: root.text
        textFormat: Text.PlainText
        color: !root.enabled ? Theme.disabledInk : root.highlighted ? (Theme.highContrast ? Theme.selectionInk : root.readableInk(buttonSurface.color)) : Theme.ink
        font.pixelSize: 14 * root.fontScale
        font.weight: Font.DemiBold
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
