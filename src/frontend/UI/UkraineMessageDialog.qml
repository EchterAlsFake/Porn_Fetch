import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root
    ContrastPopupBackground { popup: root }
    objectName: "ukraineMessageDialog"

    required property var settings
    property bool fullScreen: false
    readonly property bool highContrast: settings.high_contrast
    readonly property bool dark: settings.dark_mode
    readonly property color paper: highContrast ? Theme.background : dark ? "#172235" : "#fffdf6"
    readonly property color ink: highContrast ? Theme.ink : dark ? "#eef3fc" : "#24344c"
    readonly property color mutedInk: highContrast ? Theme.ink : dark ? "#bccbe0" : "#53627a"
    readonly property real textScale: Math.max(1, settings.font_size / 12)

    signal dismissed()

    // Return whether startup should wait for this message to close.
    function presentOnce() {
        if (visible)
            return true
        if (settings.ukraine_message_seen)
            return false
        open()
        return true
    }

    parent: Overlay.overlay
    anchors.centerIn: parent
    width: fullScreen ? parent.width : Math.min(parent.width - 24, 720)
    height: fullScreen ? parent.height : Math.min(parent.height - 24, header.implicitHeight + topPadding
                     + letterScroll.contentHeight + bottomPadding + footer.implicitHeight)
    margins: 0
    topInset: 0
    bottomInset: 0
    leftInset: 0
    rightInset: 0
    modal: true
    focus: true
    z: 1000
    padding: width < 480 ? 20 : 32
    leftPadding: padding + (fullScreen ? parent.SafeArea.margins.left : 0)
    rightPadding: padding + (fullScreen ? parent.SafeArea.margins.right : 0)
    topPadding: 20
    bottomPadding: 12
    closePolicy: Popup.CloseOnEscape
    title: qsTr("I stand with Ukraine. 🇺🇦")
    onOpened: {
        settings.mark_ukraine_message_seen()
        letterScroll.forceActiveFocus()
    }
    onClosed: dismissed()

    background: Rectangle {
        color: root.paper
        radius: root.fullScreen ? 0 : 18
        border.width: root.highContrast ? 2 : 1
        border.color: root.highContrast ? Theme.ink : root.dark ? "#354963" : "#ddd9cd"
    }

    header: Item {
        implicitHeight: heading.implicitHeight + 66 + (root.fullScreen ? root.parent.SafeArea.margins.top : 0)

        Rectangle {
            anchors.fill: parent
            radius: root.fullScreen ? 0 : 18
            gradient: Gradient {
                GradientStop { position: 0; color: root.highContrast ? Theme.background : "#123e78" }
                GradientStop { position: 1; color: root.highContrast ? Theme.background : "#235ca0" }
            }
        }
        Rectangle {
            anchors { left: parent.left; right: parent.right; bottom: parent.bottom }
            height: 18
            color: root.highContrast ? Theme.background : "#235ca0"
        }
        Rectangle {
            anchors { left: parent.left; right: parent.right; bottom: parent.bottom }
            height: 4
            color: "#f3cf63"
        }
        ColumnLayout {
            id: heading
            anchors { left: parent.left; right: discoveryButton.left; top: parent.top; margins: root.padding }
            anchors.topMargin: root.padding + (root.fullScreen ? root.parent.SafeArea.margins.top : 0)
            anchors.leftMargin: root.leftPadding
            spacing: 12
            Label {
                Layout.fillWidth: true
                text: qsTr("A PERSONAL MESSAGE")
                color: root.highContrast ? Theme.accent : "#f3cf63"
                font.pixelSize: 11 * root.textScale
                font.letterSpacing: 2
                wrapMode: Text.Wrap
            }
            Label {
                objectName: "ukraineMessageHeading"
                Layout.fillWidth: true
                // Draw the flag from our own SVG: some systems lack flag emoji fonts.
                text: qsTr("I stand with Ukraine.") + ' <img src="qrc:/images/graphics/ukraine_flag.svg" width="'
                      + Math.round((root.width < 480 ? 30 : 42) * root.textScale) + '" height="'
                      + Math.round((root.width < 480 ? 20 : 28) * root.textScale) + '">'
                textFormat: Text.RichText
                color: root.highContrast ? Theme.ink : "#ffffff"
                font.pixelSize: (root.width < 480 ? 27 : 36) * root.textScale
                font.weight: Font.DemiBold
                wrapMode: Text.Wrap
                Accessible.role: Accessible.Heading
                Accessible.name: root.title
            }
        }
        ToolButton {
            id: discoveryButton
            objectName: "ukraineDiscoveryButton"
            anchors { top: parent.top; right: parent.right; margins: 10 }
            anchors.topMargin: 10 + (root.fullScreen ? root.parent.SafeArea.margins.top : 0)
            anchors.rightMargin: 10 + (root.fullScreen ? root.parent.SafeArea.margins.right : 0)
            width: 60
            height: 44
            hoverEnabled: true
            text: "↗"
            Accessible.name: qsTr("A small discovery")
            Accessible.description: qsTr("Open a video on YouTube in your browser.")
            ToolTip.visible: hovered || activeFocus
            ToolTip.text: qsTr("Curious? Open a video on YouTube")
            HoverHandler { cursorShape: Qt.PointingHandCursor }
            contentItem: Label {
                text: discoveryButton.text
                color: root.highContrast ? Theme.accent : discoveryButton.hovered || discoveryButton.activeFocus ? "#ffe797" : "#a9bdd7"
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                Accessible.ignored: true
            }
            background: Rectangle {
                radius: 12
                color: root.highContrast ? Theme.background : discoveryButton.down ? "#12345d" : discoveryButton.hovered ? "#3a608f" : "#294f7e"
                border.width: discoveryButton.activeFocus || root.highContrast ? 2 : 1
                border.color: root.highContrast ? Theme.outline : discoveryButton.hovered || discoveryButton.activeFocus ? "#f3cf63" : "#7894b8"
            }
            onClicked: Qt.openUrlExternally("https://www.youtube.com/watch?v=lV9q901vS6o")
        }
    }

    contentItem: ScrollView {
        id: letterScroll
        objectName: "ukraineMessageScroll"
        clip: true
        contentWidth: availableWidth
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        UkraineMessageContent {
            settings: root.settings
            width: letterScroll.availableWidth
        }
    }

    footer: DialogButtonBox {
        padding: 12
        bottomPadding: 12 + (root.fullScreen ? root.parent.SafeArea.margins.bottom : 0)
        leftPadding: root.leftPadding
        rightPadding: root.rightPadding
        background: Item {}
        AppButton {
            objectName: "ukraineMessageContinueButton"
            text: qsTr("Continue")
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            contentItem: Label {
                text: parent.text
                color: "#102c50"
                font.pixelSize: 15 * root.textScale
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            background: Rectangle {
                implicitWidth: 128
                implicitHeight: 46
                radius: 10
                color: parent.down ? "#dfbb50" : parent.hovered ? "#ffe28a" : "#f3cf63"
                border.width: parent.activeFocus ? 2 : 0
                border.color: root.ink
            }
        }
        onAccepted: root.close()
    }
}
