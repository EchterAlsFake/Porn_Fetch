import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls

Controls.ComboBox {
    id: inputControl
    Layout.minimumHeight: Theme.carMode ? 64 : 0
    // On TV, center opens the choices; Up/Down outside the popup move to the
    // neighboring form controls. The popup retains native choice navigation.
    Keys.onPressed: function(event) {
        var window = inputControl.Window.window
        var navigation = window && window.remoteNavigation
        if (navigation && !popup.visible && (event.key === Qt.Key_Up || event.key === Qt.Key_Down))
            event.accepted = navigation.move(event.key)
    }
    ContrastOutline { control: inputControl }
    ContrastPopupBackground { popup: inputControl.popup }
}
