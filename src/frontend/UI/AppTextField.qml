import QtQuick
import QtQuick.Controls as Controls

Controls.TextField {
    id: inputControl
    ContrastOutline { control: inputControl }
    Binding {
        target: inputControl
        property: "placeholderTextColor"
        when: Theme.highContrast
        value: Theme.disabledInk
        restoreMode: Binding.RestoreBindingOrValue
    }
}
