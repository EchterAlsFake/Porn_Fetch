import QtQuick
import QtQuick.Controls as Controls

Controls.ComboBox {
    id: inputControl
    ContrastOutline { control: inputControl }
    ContrastPopupBackground { popup: inputControl.popup }
}
