import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

ApplicationWindow {
    width: 1200
    height: 900
    visible: true
    title: qsTr("Porn Fetch · Creator library preview")
    color: Theme.background
    palette.window: Theme.background
    palette.windowText: Theme.ink
    palette.text: Theme.ink
    palette.base: Theme.surface
    palette.buttonText: Theme.ink
    palette.highlight: Theme.accent
    palette.highlightedText: Theme.selectionInk
    Material.theme: Theme.dark ? Material.Dark : Material.Light
    Material.accent: Theme.accent
    CreatorsPage { anchors.fill: parent }
}
