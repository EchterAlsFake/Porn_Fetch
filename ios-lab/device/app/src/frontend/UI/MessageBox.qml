import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

Window {
    id: dialogWindow
    title: dialogTitle
    width: 480
    height: Math.max(220, contentColumn.implicitHeight + 40)
    minimumWidth: 320
    minimumHeight: 160
    flags: Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
    color: "#1e1e24"
    visible: true
    visibility: Window.Windowed

    signal closed()
    signal accepted()

    property string dialogTitle: "Notice"
    property string messageText: ""
    property string customIcon: "" // optional override

    // Infer icon type based on customIcon or dialogTitle
    readonly property string effectiveType: {
        if (customIcon !== "") return customIcon
        var t = dialogTitle.toLowerCase()
        if (t.indexOf("error") !== -1 || t.indexOf("failed") !== -1 || t.indexOf("exception") !== -1 || t.indexOf("fuck") !== -1)
            return "error"
        if (t.indexOf("warning") !== -1 || t.indexOf("caution") !== -1)
            return "warning"
        if (t.indexOf("success") !== -1 || t.indexOf("done") !== -1)
            return "success"
        return "info"
    }

    // Color tokens matching Porn Fetch dark theme palette
    readonly property color bgCard:      "#1e1e24"
    readonly property color borderColor: "#383b48"
    readonly property color textPrimary: "#f1f5f9"
    readonly property color textSubtle:  "#94a3b8"
    
    readonly property color accentColor:  effectiveType === "error"   ? "#ef4444" :
                                          effectiveType === "warning" ? "#f59e0b" :
                                          effectiveType === "success" ? "#10b981" : "#3b82f6"

    readonly property string iconSymbol: effectiveType === "error"   ? "✕" :
                                         effectiveType === "warning" ? "!" :
                                         effectiveType === "success" ? "✓" : "i"

    function acceptDialog() {
        accepted()
        closeDialog()
    }

    function closeDialog() {
        exitAnim.start()
    }

    function finalizeClose() {
        closed()
        dialogWindow.close()
    }

    // Animations
    ParallelAnimation {
        id: enterAnim
        running: true
        NumberAnimation { target: mainCard; property: "scale"; from: 0.96; to: 1.0; duration: 160; easing.type: Easing.OutCubic }
        NumberAnimation { target: mainCard; property: "opacity"; from: 0.0; to: 1.0; duration: 160; easing.type: Easing.OutCubic }
    }

    ParallelAnimation {
        id: exitAnim
        running: false
        NumberAnimation { target: mainCard; property: "scale"; from: 1.0; to: 0.96; duration: 120; easing.type: Easing.InCubic }
        NumberAnimation { target: mainCard; property: "opacity"; from: 1.0; to: 0.0; duration: 120; easing.type: Easing.InCubic }
        onFinished: finalizeClose()
    }

    // Keyboard Shortcuts
    Shortcut { sequence: "Escape"; onActivated: closeDialog() }
    Shortcut { sequence: "Return"; onActivated: acceptDialog() }
    Shortcut { sequence: "Enter"; onActivated: acceptDialog() }

    // Main Card Surface
    Rectangle {
        id: mainCard
        anchors.fill: parent
        radius: 12
        color: bgCard
        border.color: borderColor
        border.width: 1

        // Floating Toast feedback overlay (does not alter layout structure)
        Rectangle {
            id: copyToast
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 52
            z: 20
            opacity: 0.0
            visible: opacity > 0
            height: 24
            radius: 12
            color: "#10b981"
            implicitWidth: toastText.implicitWidth + 22

            Text {
                id: toastText
                anchors.centerIn: parent
                text: "Copied to Clipboard!"
                color: "#ffffff"
                font.pixelSize: 11
                font.bold: true
            }

            SequentialAnimation {
                id: toastAnim
                NumberAnimation { target: copyToast; property: "opacity"; from: 0.0; to: 1.0; duration: 140; easing.type: Easing.OutCubic }
                PauseAnimation { duration: 1200 }
                NumberAnimation { target: copyToast; property: "opacity"; from: 1.0; to: 0.0; duration: 180; easing.type: Easing.InCubic }
            }
        }

        ColumnLayout {
            id: contentColumn
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12

            // Header Row: Icon + Title (Draggable) + Close Button
            RowLayout {
                id: headerRow
                Layout.fillWidth: true
                spacing: 12

                // Icon Badge
                Rectangle {
                    width: 34
                    height: 34
                    radius: 17
                    color: Qt.hsla(accentColor.hslHue, accentColor.hslSaturation, accentColor.hslLightness, 0.15)
                    border.color: Qt.hsla(accentColor.hslHue, accentColor.hslSaturation, accentColor.hslLightness, 0.4)
                    border.width: 1

                    Text {
                        anchors.centerIn: parent
                        text: iconSymbol
                        color: accentColor
                        font.pixelSize: 16
                        font.bold: true
                    }

                    // Native System Move on Icon drag
                    MouseArea {
                        anchors.fill: parent
                        onPressed: function(mouse) {
                            if (mouse.button === Qt.LeftButton) {
                                dialogWindow.startSystemMove()
                            }
                        }
                    }
                }

                // Title Text (Draggable Header Area)
                Item {
                    Layout.fillWidth: true
                    implicitHeight: titleText.implicitHeight

                    Text {
                        id: titleText
                        anchors.fill: parent
                        text: dialogTitle
                        color: textPrimary
                        font.pixelSize: 15
                        font.weight: Font.DemiBold
                        elide: Text.ElideRight
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Native System Move on Title drag
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.ArrowCursor
                        onPressed: function(mouse) {
                            if (mouse.button === Qt.LeftButton) {
                                dialogWindow.startSystemMove()
                            }
                        }
                    }
                }

                // Close (X) Button
                Rectangle {
                    width: 26
                    height: 26
                    radius: 13
                    color: closeBtnArea.containsMouse ? "#333b4d" : "transparent"

                    Text {
                        anchors.centerIn: parent
                        text: "✕"
                        color: closeBtnArea.containsMouse ? "#ffffff" : textSubtle
                        font.pixelSize: 12
                    }

                    MouseArea {
                        id: closeBtnArea
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: closeDialog()
                    }
                }
            }

            // Separator Line
            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: "#2a2d3a"
            }

            // Body Message Container (Freely scalable)
            SmoothScrollView {
                id: bodyScrollView
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                TextEdit {
                    id: bodyTextEdit
                    width: bodyScrollView.width - 12
                    text: messageText
                    color: textPrimary
                    font.pixelSize: 13
                    font.family: "Segoe UI, -apple-system, BlinkMacSystemFont, Roboto, sans-serif"
                    wrapMode: Text.Wrap
                    readOnly: true
                    selectByMouse: true
                    selectionColor: accentColor
                    selectedTextColor: "#ffffff"
                }
            }

            // Action Buttons Footer
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                // Copy Button (Secondary)
                Button {
                    id: copyBtn
                    text: "Copy Text"
                    flat: true
                    onClicked: {
                        bodyTextEdit.selectAll()
                        bodyTextEdit.copy()
                        bodyTextEdit.deselect()
                        toastAnim.restart()
                    }

                    contentItem: Text {
                        text: copyBtn.text
                        color: copyBtn.hovered ? textPrimary : textSubtle
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        implicitWidth: 86
                        implicitHeight: 32
                        radius: 8
                        color: copyBtn.down ? "#2d3342" : (copyBtn.hovered ? "#252b38" : "transparent")
                        border.color: copyBtn.hovered ? borderColor : "transparent"
                        border.width: 1
                    }
                }

                Item { Layout.fillWidth: true } // Spacer

                // OK Button (Primary)
                Button {
                    id: okBtn
                    text: "OK"
                    onClicked: acceptDialog()

                    contentItem: Text {
                        text: okBtn.text
                        color: "#ffffff"
                        font.pixelSize: 12
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        implicitWidth: 90
                        implicitHeight: 32
                        radius: 8
                        color: okBtn.down ? Qt.darker(accentColor, 1.2) :
                               okBtn.hovered ? Qt.lighter(accentColor, 1.1) : accentColor
                    }
                }
            }
        }
    }

    // ─── RESIZE HANDLES (Native System Compositor Resizing) ───────────
    readonly property int handleSize: 8

    // Top Edge
    MouseArea {
        anchors { top: parent.top; left: parent.left; right: parent.right; leftMargin: handleSize; rightMargin: handleSize }
        height: handleSize
        cursorShape: Qt.SizeVerCursor
        onPressed: dialogWindow.startSystemResize(Qt.TopEdge)
    }

    // Bottom Edge
    MouseArea {
        anchors { bottom: parent.bottom; left: parent.left; right: parent.right; leftMargin: handleSize; rightMargin: handleSize }
        height: handleSize
        cursorShape: Qt.SizeVerCursor
        onPressed: dialogWindow.startSystemResize(Qt.BottomEdge)
    }

    // Left Edge
    MouseArea {
        anchors { top: parent.top; bottom: parent.bottom; left: parent.left; topMargin: handleSize; bottomMargin: handleSize }
        width: handleSize
        cursorShape: Qt.SizeHorCursor
        onPressed: dialogWindow.startSystemResize(Qt.LeftEdge)
    }

    // Right Edge
    MouseArea {
        anchors { top: parent.top; bottom: parent.bottom; right: parent.right; topMargin: handleSize; bottomMargin: handleSize }
        width: handleSize
        cursorShape: Qt.SizeHorCursor
        onPressed: dialogWindow.startSystemResize(Qt.RightEdge)
    }

    // Top-Left Corner
    MouseArea {
        anchors { top: parent.top; left: parent.left }
        width: handleSize; height: handleSize
        cursorShape: Qt.SizeFDiagCursor
        onPressed: dialogWindow.startSystemResize(Qt.TopEdge | Qt.LeftEdge)
    }

    // Top-Right Corner
    MouseArea {
        anchors { top: parent.top; right: parent.right }
        width: handleSize; height: handleSize
        cursorShape: Qt.SizeBDiagCursor
        onPressed: dialogWindow.startSystemResize(Qt.TopEdge | Qt.RightEdge)
    }

    // Bottom-Left Corner
    MouseArea {
        anchors { bottom: parent.bottom; left: parent.left }
        width: handleSize; height: handleSize
        cursorShape: Qt.SizeBDiagCursor
        onPressed: dialogWindow.startSystemResize(Qt.BottomEdge | Qt.LeftEdge)
    }

    // Bottom-Right Corner
    MouseArea {
        anchors { bottom: parent.bottom; right: parent.right }
        width: handleSize; height: handleSize
        cursorShape: Qt.SizeFDiagCursor
        onPressed: dialogWindow.startSystemResize(Qt.BottomEdge | Qt.RightEdge)
    }
}
