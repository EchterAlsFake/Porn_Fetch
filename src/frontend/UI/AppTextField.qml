import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls

Controls.TextField {
    id: inputControl
    Layout.minimumHeight: Theme.carMode ? 64 : 0
    ContrastOutline { control: inputControl }
    Binding {
        target: inputControl
        property: "placeholderTextColor"
        when: Theme.highContrast
        value: Theme.disabledInk
        restoreMode: Binding.RestoreBindingOrValue
    }
}
