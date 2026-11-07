pragma Singleton
import QtQuick

QtObject {
    property real globalPointSize: 14
    readonly property bool highContrast: typeof appSettings !== "undefined" && appSettings && appSettings.high_contrast === true
    readonly property bool dark: typeof appSettings === "undefined" || !appSettings || appSettings.dark_mode !== false
    readonly property real lightBrightness: typeof appSettings !== "undefined" && appSettings
                                           && typeof appSettings.light_theme_brightness === "number"
                                           ? appSettings.light_theme_brightness / 100 : 1
    function lightShade(value) {
        const color = Qt.color(value)
        return Qt.rgba(color.r * lightBrightness, color.g * lightBrightness,
                       color.b * lightBrightness, color.a)
    }
    readonly property color background: highContrast ? (dark ? "#000000" : "#ffffff")
                                                    : (dark ? "#121212" : lightShade("#ffffff"))
    readonly property color surface: highContrast ? background : (dark ? "#1e1e24" : lightShade("#ffffff"))
    readonly property color ink: highContrast ? (dark ? "#ffffff" : "#000000")
                                             : (dark ? "#f0f2f8" : "#202431")
    readonly property color muted: highContrast ? ink : (dark ? "#b9c0cf" : "#566176")
    readonly property color disabledInk: dark ? "#b3b3b3" : "#555555"
    readonly property color outline: highContrast ? ink : (dark ? "#686b76" : "#80838c")
    readonly property color accent: highContrast ? (dark ? "#ffff00" : "#000080")
                                                : (typeof appSettings !== "undefined" && appSettings && appSettings.accent_color
                                                   ? appSettings.accent_color : "#6366f1")
    readonly property color selectionInk: highContrast && dark ? "#000000" : "#ffffff"
}
