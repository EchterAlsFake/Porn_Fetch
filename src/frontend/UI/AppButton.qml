import QtQuick
import QtQuick.Controls as Controls

Controls.Button {
    id: control

    // Keep the platform style and its sizing. Override only the rendered colors
    // while high contrast is active; disabling it restores the style's bindings.
    Binding {
        target: control.contentItem
        property: "color"
        when: Theme.highContrast && control.contentItem
        value: !control.enabled ? Theme.disabledInk : control.highlighted ? Theme.selectionInk : Theme.ink
        restoreMode: Binding.RestoreBindingOrValue
    }

    Binding {
        target: control.background ? control.background.layer : null
        property: "enabled"
        when: Theme.highContrast && control.background
        value: false
        restoreMode: Binding.RestoreBindingOrValue
    }

    Rectangle {
        objectName: "contrastButtonBackground"
        parent: control.background
        anchors.fill: parent
        visible: Theme.highContrast
        color: control.enabled && control.highlighted ? Theme.accent : Theme.background
        radius: 6
        border.width: control.visualFocus ? 3 : 2
        border.color: !control.enabled ? Theme.disabledInk : control.visualFocus ? Theme.accent : Theme.ink
    }
}
