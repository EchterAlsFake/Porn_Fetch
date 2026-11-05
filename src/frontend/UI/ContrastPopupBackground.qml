import QtQuick

Item {
    id: skin
    required property var popup

    Binding {
        target: skin.popup && skin.popup.background ? skin.popup.background.layer : null
        property: "enabled"
        when: Theme.highContrast && skin.popup && skin.popup.background
        value: false
        restoreMode: Binding.RestoreBindingOrValue
    }
    Rectangle {
        objectName: "contrastPopupSurface"
        parent: skin.popup ? skin.popup.background : null
        anchors.fill: parent
        visible: Theme.highContrast
        color: Theme.surface
        radius: 6
        border.width: 2
        border.color: Theme.outline
    }
}
