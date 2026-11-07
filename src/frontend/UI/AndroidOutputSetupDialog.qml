import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Dialogs as Dialogs
import QtQuick.Layouts

Dialog {
    id: root
    ContrastPopupBackground { popup: root }
    objectName: "androidOutputSetupDialog"
    required property var settings
    readonly property color ink: settings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property real textScale: Math.max(1, settings.font_size / 12)
    readonly property color accent: settings.high_contrast ? Theme.accent : settings.accent_color
    Material.theme: settings.dark_mode ? Material.Dark : Material.Light

    parent: Overlay.overlay
    anchors.centerIn: parent
    width: parent.width
    height: parent.height
    margins: 0
    topInset: 0
    bottomInset: 0
    leftInset: 0
    rightInset: 0
    padding: 24
    topPadding: padding + parent.SafeArea.margins.top
    bottomPadding: padding + parent.SafeArea.margins.bottom
    leftPadding: padding + parent.SafeArea.margins.left
    rightPadding: padding + parent.SafeArea.margins.right
    modal: true
    focus: true
    z: 1000
    closePolicy: Popup.NoAutoClose
    title: qsTr("Choose your video folder")
    header: Item {}
    background: Rectangle {
        color: root.settings.high_contrast ? Theme.background : root.settings.dark_mode ? "#101319" : Theme.lightShade("#f7f8fc")
    }

    Dialogs.FolderDialog {
        id: folderPicker
        objectName: "androidSetupFolderPicker"
        title: qsTr("Choose where to save videos")
        onAccepted: {
            backend.set_android_output_folder(selectedFolder.toString())
            if (root.settings.android_output_folder)
                root.close()
        }
    }

    contentItem: ScrollView {
        id: setupScroll
        contentWidth: availableWidth
        clip: true
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            width: setupScroll.availableWidth
            spacing: 20
            Image {
                Layout.preferredWidth: 56
                Layout.preferredHeight: 56
                source: "qrc:/images/graphics/download.png"
                fillMode: Image.PreserveAspectFit
                Accessible.ignored: true
            }
            Label {
                Layout.fillWidth: true
                text: root.title
                color: root.ink
                font.pixelSize: 28 * root.textScale
                font.bold: true
                wrapMode: Text.Wrap
                Accessible.role: Accessible.Heading
            }
            Label {
                Layout.fillWidth: true
                text: qsTr("Choose a folder where Porn Fetch will save your completed videos so you can find them outside the app.")
                color: root.ink
                font.pixelSize: 16 * root.textScale
                wrapMode: Text.Wrap
                lineHeight: 1.2
            }
            Label {
                Layout.fillWidth: true
                text: qsTr("In the system picker, open or create a folder, then allow Porn Fetch to use it. You can change this later in Settings → Video.")
                color: root.ink
                font.pixelSize: 14 * root.textScale
                wrapMode: Text.Wrap
                lineHeight: 1.2
            }
        }
    }

    footer: Item {
        implicitHeight: chooseButton.implicitHeight + 32 + root.parent.SafeArea.margins.bottom
        AppButton {
            id: chooseButton
            objectName: "androidSetupChooseFolderButton"
            anchors {
                left: parent.left; right: parent.right; top: parent.top
                leftMargin: root.leftPadding; rightMargin: root.rightPadding; topMargin: 16
            }
            text: qsTr("Choose folder")
            highlighted: true
            implicitHeight: Math.max(52, contentItem.implicitHeight + topPadding + bottomPadding)
            contentItem: Label {
                text: chooseButton.text
                color: root.settings.high_contrast ? Theme.background : Theme.lightShade("#ffffff")
                font.pixelSize: 16 * root.textScale
                font.weight: Font.DemiBold
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            background: Rectangle {
                radius: 12
                color: chooseButton.down ? Qt.darker(root.accent, 1.15) : root.accent
                border.width: chooseButton.activeFocus ? 2 : 0
                border.color: root.ink
            }
            onClicked: folderPicker.open()
        }
    }
}
