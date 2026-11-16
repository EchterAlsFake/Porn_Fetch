import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls

Controls.SpinBox {
    id: inputControl
    Layout.minimumHeight: Theme.carMode ? 64 : 0
    Layout.minimumWidth: Theme.carMode ? 64 : 0
    focusPolicy: Qt.StrongFocus
    ContrastOutline { control: inputControl }
}
