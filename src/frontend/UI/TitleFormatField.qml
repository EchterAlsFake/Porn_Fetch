import QtQuick
import QtQuick.Controls

TextArea {
    id: control
    implicitWidth: 240
    implicitHeight: Math.max(48, contentHeight + topPadding + bottomPadding)
    padding: 12
    textFormat: TextEdit.PlainText
    wrapMode: TextEdit.Wrap
    selectByMouse: true
    color: Theme.ink
    selectionColor: Theme.accent
    selectedTextColor: Theme.selectionInk
    placeholderTextColor: Theme.disabledInk
    placeholderText: "$title"
    Accessible.name: qsTr("Custom title formatting")
    Accessible.description: qsTr("Valid placeholders are highlighted. Unknown placeholders and incomplete dollar expressions have a wavy underline. Use $$ for a dollar sign.")

    function updateHighlighting() {
        backend.highlight_title_format(textDocument, Theme.dark, Theme.highContrast);
    }
    Component.onCompleted: updateHighlighting()
    Connections {
        target: Theme
        function onDarkChanged() { control.updateHighlighting(); }
        function onHighContrastChanged() { control.updateHighlighting(); }
    }
    Keys.onReturnPressed: function(event) { event.accepted = true; }
    Keys.onEnterPressed: function(event) { event.accepted = true; }

    background: Rectangle {
        color: Theme.surface
        border.color: control.activeFocus ? Theme.accent : Theme.outline
        border.width: control.activeFocus || Theme.highContrast ? 2 : 1
        radius: 6
    }
}
