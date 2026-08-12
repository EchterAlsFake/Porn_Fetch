import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    padding: 0

    property var statistics: ({
        "enabled": false,
        "total": 0,
        "successful": 0,
        "failed": 0,
        "other": 0,
        "successRate": 0,
        "totalSizeMb": 0,
        "lastDownloaded": "",
        "sources": []
    })

    readonly property color accentColor: (typeof appSettings !== "undefined" && appSettings)
                                         ? appSettings.accent_color : "#7c5cff"
    readonly property color successColor: "#35d07f"
    readonly property color failureColor: "#ff627d"
    readonly property color pendingColor: "#f5b942"
    readonly property color cardColor: Qt.lighter(palette.window, 1.18)
    readonly property color subtleTextColor: Qt.rgba(palette.text.r, palette.text.g, palette.text.b, 0.62)
    readonly property bool privacyMode: (typeof appSettings !== "undefined" && appSettings)
                                        ? appSettings.anonymous_mode : false
    readonly property int outcomeTotal: statistics.successful + statistics.failed + statistics.other

    function refresh() {
        statistics = databaseBridge.getDashboardStats()
    }

    function formattedDate(value) {
        if (!value)
            return qsTr("No downloads recorded yet")
        var parsed = new Date(value)
        return isNaN(parsed.getTime()) ? value : parsed.toLocaleString(Qt.locale())
    }

    function largestSourceTotal() {
        var largest = 1
        var sources = statistics.sources || []
        for (var index = 0; index < sources.length; ++index)
            largest = Math.max(largest, sources[index].total)
        return largest
    }

    Component.onCompleted: refresh()

    Connections {
        target: databaseBridge

        function onStatisticsChanged() {
            root.refresh()
        }
    }

    background: Rectangle {
        color: "transparent"
    }

    ScrollView {
        id: dashboardScroll
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            width: dashboardScroll.availableWidth
            spacing: 16

            RowLayout {
                Layout.fillWidth: true
                Layout.leftMargin: 8
                Layout.rightMargin: 8
                spacing: 12

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 3

                    RowLayout {
                        spacing: 10

                        Label {
                            text: qsTr("Download insights")
                            font.pixelSize: 28
                            font.bold: true
                        }

                        Rectangle {
                            implicitWidth: previewLabel.implicitWidth + 16
                            implicitHeight: 25
                            radius: height / 2
                            color: Qt.rgba(root.accentColor.r, root.accentColor.g, root.accentColor.b, 0.18)

                            Label {
                                id: previewLabel
                                anchors.centerIn: parent
                                text: qsTr("PREVIEW")
                                color: root.accentColor
                                font.pixelSize: 11
                                font.bold: true
                            }
                        }
                    }

                    Label {
                        text: qsTr("A quick look at your local download history")
                        color: root.subtleTextColor
                    }
                }

                Button {
                    text: qsTr("Refresh")
                    onClicked: root.refresh()
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.leftMargin: 8
                Layout.rightMargin: 8
                implicitHeight: trackingNotice.implicitHeight + 24
                radius: 10
                visible: !root.statistics.enabled
                color: Qt.rgba(root.pendingColor.r, root.pendingColor.g, root.pendingColor.b, 0.12)
                border.color: Qt.rgba(root.pendingColor.r, root.pendingColor.g, root.pendingColor.b, 0.45)

                Label {
                    id: trackingNotice
                    anchors.fill: parent
                    anchors.margins: 12
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.WordWrap
                    text: qsTr("Download tracking is disabled. Enable it in Settings and restart the app to start building this dashboard.")
                }
            }

            GridLayout {
                Layout.fillWidth: true
                Layout.leftMargin: 8
                Layout.rightMargin: 8
                columns: 4
                columnSpacing: 12
                rowSpacing: 12

                MetricCard {
                    label: qsTr("Tracked videos")
                    value: root.statistics.total
                    detail: qsTr("all database records")
                    highlight: root.accentColor
                }

                MetricCard {
                    label: qsTr("Successful")
                    value: root.statistics.successful
                    detail: qsTr("completed downloads")
                    highlight: root.successColor
                }

                MetricCard {
                    label: qsTr("Failed")
                    value: root.statistics.failed
                    detail: qsTr("downloads to revisit")
                    highlight: root.failureColor
                }

                MetricCard {
                    label: qsTr("Success rate")
                    value: root.statistics.successRate + "%"
                    detail: qsTr("finished attempts")
                    highlight: root.pendingColor
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.leftMargin: 8
                Layout.rightMargin: 8
                spacing: 12

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredWidth: 2
                    Layout.preferredHeight: 285
                    radius: 14
                    color: root.cardColor
                    border.color: Qt.rgba(root.accentColor.r, root.accentColor.g, root.accentColor.b, 0.2)

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 18
                        spacing: 10

                        Label {
                            text: qsTr("Download outcomes")
                            font.pixelSize: 18
                            font.bold: true
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            spacing: 24

                            Item {
                                Layout.preferredWidth: 210
                                Layout.fillHeight: true

                                Canvas {
                                    id: outcomeChart
                                    anchors.centerIn: parent
                                    width: 180
                                    height: 180

                                    onPaint: {
                                        var context = getContext("2d")
                                        context.reset()
                                        var center = width / 2
                                        var radius = 66
                                        var start = -Math.PI / 2
                                        var values = [root.statistics.successful, root.statistics.failed, root.statistics.other]
                                        var colors = [root.successColor, root.failureColor, root.pendingColor]

                                        context.lineWidth = 22
                                        context.lineCap = "round"
                                        if (root.outcomeTotal === 0) {
                                            context.strokeStyle = Qt.rgba(root.palette.text.r, root.palette.text.g, root.palette.text.b, 0.12)
                                            context.beginPath()
                                            context.arc(center, center, radius, 0, Math.PI * 2)
                                            context.stroke()
                                            return
                                        }

                                        context.lineCap = "butt"
                                        for (var index = 0; index < values.length; ++index) {
                                            if (values[index] === 0)
                                                continue
                                            var angle = (values[index] / root.outcomeTotal) * Math.PI * 2
                                            context.strokeStyle = colors[index]
                                            context.beginPath()
                                            context.arc(center, center, radius, start, start + angle)
                                            context.stroke()
                                            start += angle
                                        }
                                    }

                                    Connections {
                                        target: root
                                        function onStatisticsChanged() { outcomeChart.requestPaint() }
                                    }
                                }

                                Column {
                                    anchors.centerIn: parent
                                    spacing: 1

                                    Label {
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        text: root.outcomeTotal
                                        font.pixelSize: 28
                                        font.bold: true
                                    }

                                    Label {
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        text: qsTr("attempts")
                                        color: root.subtleTextColor
                                        font.pixelSize: 12
                                    }
                                }
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 14

                                OutcomeLegend {
                                    label: qsTr("Successful")
                                    value: root.statistics.successful
                                    markerColor: root.successColor
                                }

                                OutcomeLegend {
                                    label: qsTr("Failed")
                                    value: root.statistics.failed
                                    markerColor: root.failureColor
                                }

                                OutcomeLegend {
                                    label: qsTr("Other / pending")
                                    value: root.statistics.other
                                    markerColor: root.pendingColor
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredWidth: 1
                    Layout.preferredHeight: 285
                    radius: 14
                    color: root.cardColor
                    border.color: Qt.rgba(root.accentColor.r, root.accentColor.g, root.accentColor.b, 0.2)

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 20
                        spacing: 18

                        Label {
                            text: qsTr("At a glance")
                            font.pixelSize: 18
                            font.bold: true
                        }

                        ColumnLayout {
                            spacing: 4

                            Label {
                                text: qsTr("Last activity")
                                color: root.subtleTextColor
                            }

                            Label {
                                Layout.fillWidth: true
                                text: root.formattedDate(root.statistics.lastDownloaded)
                                font.pixelSize: 16
                                font.bold: true
                                elide: Text.ElideRight
                            }
                        }

                        ColumnLayout {
                            spacing: 4

                            Label {
                                text: qsTr("Recorded file size")
                                color: root.subtleTextColor
                            }

                            Label {
                                text: root.statistics.totalSizeMb.toLocaleString(Qt.locale(), "f", 1) + " MB"
                                font.pixelSize: 22
                                font.bold: true
                            }
                        }

                        Item { Layout.fillHeight: true }

                        Label {
                            Layout.fillWidth: true
                            text: qsTr("Statistics stay on this device in your configured SQLite database.")
                            color: root.subtleTextColor
                            wrapMode: Text.WordWrap
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.leftMargin: 8
                Layout.rightMargin: 8
                Layout.bottomMargin: 8
                implicitHeight: sourcesColumn.implicitHeight + 36
                radius: 14
                color: root.cardColor
                border.color: Qt.rgba(root.accentColor.r, root.accentColor.g, root.accentColor.b, 0.2)

                ColumnLayout {
                    id: sourcesColumn
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.margins: 18
                    spacing: 14

                    RowLayout {
                        Layout.fillWidth: true

                        Label {
                            Layout.fillWidth: true
                            text: qsTr("Downloads by source")
                            font.pixelSize: 18
                            font.bold: true
                        }

                        Label {
                            text: qsTr("Iterator names · not URLs")
                            color: root.subtleTextColor
                        }
                    }

                    Repeater {
                        model: root.statistics.sources || []

                        delegate: ColumnLayout {
                            required property var modelData
                            Layout.fillWidth: true
                            spacing: 6

                            RowLayout {
                                Layout.fillWidth: true

                                Label {
                                    Layout.fillWidth: true
                                    text: root.privacyMode ? qsTr("Hidden source") : modelData.name
                                    font.bold: true
                                    elide: Text.ElideRight
                                }

                                Label {
                                    text: qsTr("%1 videos").arg(modelData.total)
                                    color: root.subtleTextColor
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                implicitHeight: 10
                                radius: height / 2
                                color: Qt.rgba(root.palette.text.r, root.palette.text.g, root.palette.text.b, 0.08)
                                clip: true

                                Rectangle {
                                    width: parent.width * (modelData.total / root.largestSourceTotal())
                                    height: parent.height
                                    radius: parent.radius
                                    color: "transparent"
                                    clip: true

                                    Row {
                                        anchors.fill: parent

                                        Rectangle {
                                            width: parent.width * (modelData.successful / modelData.total)
                                            height: parent.height
                                            color: root.successColor
                                        }

                                        Rectangle {
                                            width: parent.width * (modelData.failed / modelData.total)
                                            height: parent.height
                                            color: root.failureColor
                                        }

                                        Rectangle {
                                            width: parent.width * (modelData.other / modelData.total)
                                            height: parent.height
                                            color: root.pendingColor
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Label {
                        Layout.fillWidth: true
                        visible: !root.statistics.sources || root.statistics.sources.length === 0
                        text: qsTr("Source activity will appear here after tracked downloads.")
                        color: root.subtleTextColor
                        horizontalAlignment: Text.AlignHCenter
                        padding: 24
                    }
                }
            }
        }
    }

    component MetricCard: Rectangle {
        required property string label
        required property var value
        required property string detail
        required property color highlight

        Layout.fillWidth: true
        Layout.preferredHeight: 112
        radius: 13
        color: root.cardColor
        border.color: Qt.rgba(highlight.r, highlight.g, highlight.b, 0.34)

        Rectangle {
            width: 4
            height: parent.height - 28
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            radius: 2
            color: parent.highlight
        }

        Column {
            anchors.left: parent.left
            anchors.leftMargin: 28
            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter
            spacing: 2

            Label {
                text: parent.parent.label
                color: root.subtleTextColor
            }

            Label {
                text: parent.parent.value
                font.pixelSize: 27
                font.bold: true
            }

            Label {
                text: parent.parent.detail
                color: root.subtleTextColor
                font.pixelSize: 11
            }
        }
    }

    component OutcomeLegend: RowLayout {
        required property string label
        required property int value
        required property color markerColor

        spacing: 10

        Rectangle {
            implicitWidth: 11
            implicitHeight: 11
            radius: width / 2
            color: parent.markerColor
        }

        Label {
            Layout.fillWidth: true
            text: parent.label
            color: root.subtleTextColor
        }

        Label {
            text: parent.value
            font.pixelSize: 17
            font.bold: true
        }
    }
}
