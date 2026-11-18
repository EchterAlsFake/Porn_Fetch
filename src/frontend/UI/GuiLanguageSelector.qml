import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: root
    readonly property var translation: typeof uiTranslation === "undefined" ? null : uiTranslation
    readonly property var options: root.translation ? root.translation.languages : [{index: 1, label: "English"}]

    Label {
        Layout.fillWidth: true
        wrapMode: Text.WordWrap
        text: qsTr("Interface language")
    }
    AppComboBox {
        id: languageChoice
        objectName: "guiLanguageComboBox"
        Layout.fillWidth: true
        Accessible.name: qsTr("Interface language")
        Accessible.description: AppStrings.guiLanguageHelp
        model: root.options
        enabled: count > 2
        textRole: "label"
        valueRole: "index"
        currentIndex: {
            const selected = root.options.findIndex(option => option.index === appSettings.language)
            return selected >= 0 ? selected : root.options.findIndex(option => option.index === 1)
        }
        onActivated: appSettings.language = currentValue
    }
    Label {
        Layout.fillWidth: true
        visible: root.translation !== null && languageChoice.currentValue !== root.translation.startupPreference
        wrapMode: Text.WordWrap
        text: qsTr("Restart Porn Fetch to apply the interface language.")
    }
}
