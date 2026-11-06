import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

AppComboBox {
    id: control
    objectName: "contentLanguageComboBox"
    Accessible.name: qsTr("Content Language")
    Accessible.description: AppStrings.contentLanguageHelp
    textRole: "label"
    valueRole: "locale"
    leftPadding: 12
    rightPadding: 12
    model: ListModel {
        ListElement { label: "Čeština"; locale: "cs-CZ"; flag: "cz" }
        ListElement { label: "Deutsch"; locale: "de-DE"; flag: "de" }
        ListElement { label: "English"; locale: "en-US"; flag: "us" }
        ListElement { label: "Español"; locale: "es-ES"; flag: "es" }
        ListElement { label: "Filipino"; locale: "fil-PH"; flag: "ph" }
        ListElement { label: "Français"; locale: "fr-FR"; flag: "fr" }
        ListElement { label: "Italiano"; locale: "it-IT"; flag: "it" }
        ListElement { label: "Nederlands"; locale: "nl-NL"; flag: "nl" }
        ListElement { label: "日本語"; locale: "ja-JP"; flag: "jp" }
        ListElement { label: "Polski"; locale: "pl-PL"; flag: "pl" }
        ListElement { label: "Português"; locale: "pt-PT"; flag: "pt" }
        ListElement { label: "Русский"; locale: "ru-RU"; flag: "ru" }
        ListElement { label: "Українська"; locale: "uk-UA"; flag: "ua" }
        ListElement { label: "中文"; locale: "zh-CN"; flag: "cn" }
    }
    currentIndex: {
        if (count === 0)
            return -1
        var savedIndex = indexOfValue(appSettings.locale)
        return savedIndex >= 0 ? savedIndex : indexOfValue("en-US")
    }
    onActivated: appSettings.locale = currentValue

    contentItem: RowLayout {
        spacing: 10
        Image {
            objectName: "selectedContentLanguageFlag"
            Layout.preferredWidth: 24
            Layout.preferredHeight: 18
            source: control.currentIndex >= 0
                    ? "qrc:/images/graphics/flags/" + control.model.get(control.currentIndex).flag + ".svg" : ""
            sourceSize.width: 48
            sourceSize.height: 36
            fillMode: Image.PreserveAspectFit
            Accessible.ignored: true
        }
        Text {
            Layout.fillWidth: true
            Layout.rightMargin: control.indicator.width + control.spacing
            text: control.displayText
            font: control.font
            color: control.enabled ? control.palette.text : Theme.disabledInk
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
        }
    }
    delegate: ItemDelegate {
        id: languageDelegate
        required property int index
        required property string label
        required property string flag
        width: control.popup.width
        leftPadding: 12
        rightPadding: 12
        highlighted: control.highlightedIndex === index
        text: label
        Accessible.name: label
        contentItem: RowLayout {
            spacing: 10
            Image {
                Layout.preferredWidth: 24
                Layout.preferredHeight: 18
                source: "qrc:/images/graphics/flags/" + languageDelegate.flag + ".svg"
                sourceSize.width: 48
                sourceSize.height: 36
                fillMode: Image.PreserveAspectFit
                Accessible.ignored: true
            }
            Text {
                Layout.fillWidth: true
                text: languageDelegate.label
                font: control.font
                color: control.palette.text
                elide: Text.ElideRight
            }
        }
    }
}
