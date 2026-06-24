import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import QtQuick.Controls.impl

// ApplicationWindow is the root element for our main window.
// It provides a standard top-level window with background color and basic properties.
ApplicationWindow {
    id: windowHome // 'id' allows us to reference this window from other parts of the code

    // We set a slightly custom background color.
    // Since we enabled Material Dark theme in Python, most things will automatically be dark,
    // but setting a specific background ensures a clean, cohesive look.
    color: "#121212"
    height: 700 // Initial height of the window
    title: "Download" // Window title

    visible: true // Ensure the window is shown when the app starts
    width: 900 // Initial width of the window

    // ColumnLayout arranges its children vertically.
    // This is the main structure: Main Content Area on top, Action Buttons on the bottom.

    Row {
        id: layoutSidebar
        anchors.fill: parent

        Rectangle {
            id: sidebar
            height: parent.height
            color: "black"
            clip: true // Prevents children from bleeding out when collapsing
            state: "expanded"

            states: [
                State {
                    name: "expanded"
                    PropertyChanges { target: sidebar; width: 200 }
                },
                State {
                    name: "collapsed"
                    PropertyChanges { target: sidebar; width: 60 }
                }
            ]

            transitions: [
                Transition {
                    from: "*"
                    to: "*"
                    NumberAnimation {
                        properties: "width"
                        duration: 250
                        easing.type: Easing.InOutQuad
                    }
                }
            ]

            Column {
                width: sidebar.availableWidth
                Layout.fillWidth: true

                CustomButton {
                    text: "Home"
                    Layout.fillWidth: true
                }

                CustomButton {
                    text: "Login"
                    Layout.fillWidth: true
                }

            }

        }


        Frame {
        width: parent.width - sidebar.width
        Layout.fillHeight: true
        Layout.fillWidth: true
        padding: 5


        StackLayout {
            id: stackview_home
            anchors.fill: parent

            GridLayout {
                width: stackview_home.availableWidth
                Layout.fillWidth: true
                columnSpacing: 7
                rowSpacing: 7
                columns: 3

                CustomButton {
                    text: "Get Videos"
                    Layout.fillWidth: false
                    Layout.alignment: Qt.AlignBottom
                }

                CustomTextField {
                    placeholderText: "Enter a Video / Model / Channel / Playlist URL..."
                    Layout.fillWidth: true

                }

                HelpButton {Layout.fillWidth: false
                text: "Supported Websites / URL types"}


            }
        }

    }

    }









}