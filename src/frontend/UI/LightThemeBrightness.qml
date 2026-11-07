import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    visible: !appSettings.dark_mode
    spacing: 4
    Label {
        Layout.fillWidth: true
        text: qsTr("Light theme brightness: %1%").arg(appSettings.light_theme_brightness)
        wrapMode: Text.WordWrap
    }
    Slider {
        objectName: "lightThemeBrightnessSlider"
        Layout.fillWidth: true
        from: 75
        to: 100
        stepSize: 1
        value: appSettings.light_theme_brightness
        enabled: !appSettings.high_contrast
        Accessible.name: qsTr("Light theme brightness")
        onMoved: appSettings.light_theme_brightness = Math.round(value)
    }
    Label {
        Layout.fillWidth: true
        text: appSettings.high_contrast
              ? qsTr("Turn off high contrast to adjust brightness.")
              : qsTr("Lower the brightness for softer light backgrounds.")
        color: Theme.muted
        wrapMode: Text.WordWrap
    }
}
