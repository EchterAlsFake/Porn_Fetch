import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import QtQuick.Controls.impl

// ApplicationWindow is the root element for our main window.
// It provides a standard top-level window with background color and basic properties.
ApplicationWindow {
    id: window // 'id' allows us to reference this window from other parts of the code

    // We set a slightly custom background color.
    // Since we enabled Material Dark theme in Python, most things will automatically be dark,
    // but setting a specific background ensures a clean, cohesive look.
    color: "#121212"
    height: 700 // Initial height of the window
    title: "Porn Fetch Settings" // Window title

    visible: true // Ensure the window is shown when the app starts
    width: 900 // Initial width of the window

    // ColumnLayout arranges its children vertically.
    // This is the main structure: Main Content Area on top, Action Buttons on the bottom.
    ColumnLayout {
        anchors.fill: parent // Make the layout fill the entire window
        anchors.margins: 20 // Add some breathing room (padding) around the edges
        spacing: 20 // Space between the top area and the bottom buttons

        // RowLayout arranges its children horizontally.
        // This splits the upper part into Left (Sidebar) and Right (Settings Content)
        RowLayout {
            Layout.fillHeight: true // Take up all available vertical space
            Layout.fillWidth: true // Take up all available horizontal space
            spacing: 20 // Space between sidebar and content

            // ---------------------------------------------------------
            // LEFT SIDEBAR: Navigation Menu
            // ---------------------------------------------------------
            // Frame provides a modern, elevated background panel for the sidebar
            Frame {
                Layout.fillHeight: true
                Layout.preferredWidth: 200 // Fixed width for the sidebar
                padding: 0 // Remove internal padding so items go edge-to-edge

                // ListView displays a scrollable list of items based on a model
                ListView {
                    id: navList

                    anchors.fill: parent // Fill the frame

                    // Keep the selection synced with the content currently displayed
                    currentIndex: stackLayout.currentIndex

                    // The 'model' is the data. Here it's just a simple list of strings.
                    model: ["Video", "Performance", "System", "UI"]

                    // 'delegate' defines how each individual item in the list looks
                    delegate: ItemDelegate {
                        font.pixelSize: 15
                        // Make font bold if this item is currently selected
                        font.weight: ListView.isCurrentItem ? Font.Bold : Font.Normal
                        height: 50
                        highlighted: ListView.isCurrentItem // Visual highlight

                        text: modelData // 'modelData' refers to the string ("Video", etc.)
                        width: parent.width // Span full width of sidebar

                        // When clicked, switch both the list highlight and the content view
                        onClicked: {
                            stackLayout.currentIndex = index;
                            navList.currentIndex = index;
                        }
                    }
                }
            }

            // ---------------------------------------------------------
            // RIGHT CONTENT AREA: The actual settings forms
            // ---------------------------------------------------------
            Frame {
                Layout.fillHeight: true
                Layout.fillWidth: true
                padding: 20

                // StackLayout allows having multiple children, but only ONE is visible at a time.
                // It acts exactly like QStackedWidget from Qt Widgets.
                StackLayout {
                    id: stackLayout

                    anchors.fill: parent
                    currentIndex: 0 // Start by showing the first item (Video)

                    // ==========================================
                    // TAB 1: VIDEO SETTINGS
                    // ==========================================
                    // ScrollView ensures that if the window is too small, the user can scroll.
                    ScrollView {
                        id: "scrollviewVideo"
                        clip: true // Prevents content from drawing outside the scroll view

                        // GridLayout arranges items in a grid.
                        // Here we use 2 columns: Label on the left, Control on the right.

                        ColumnLayout {
                            width: scrollviewVideo.availableWidth
                            Layout.fillWidth: true


                            GridLayout {
                                columnSpacing: 15
                                rowSpacing: 15
                                width: scrollviewVideo.availableWidth
                                Layout.fillWidth: true
                                columns: 3


                                HelpButton {Layout.fillWidth: false}
                                Label {Layout.fillWidth: false; text: "Quality"}
                                ComboBox {
                                    Layout.fillWidth: true
                                    model: ["144p", "240p", "360p", "480p", "720p", "1080p", "Worst", "Middle", "Best Available"]
                                }

                                HelpButton {Layout.fillWidth: false}
                                Label {Layout.fillWidth: false; text: "Model Videos"}
                                ComboBox {
                                    Layout.fillWidth: true
                                    model: ["Both", "Uploaded Videos", "Featured Videos"]
                                }

                                HelpButton {Layout.fillWidth: false}
                                Label {Layout.fillWidth: false; text: "Max Result Limit"}
                                SpinBox {
                                    Layout.fillWidth: true
                                    editable: true
                                    from: 1
                                    to: 5000

                                }
                            }

                            GridLayout {
                                rowSpacing: 15
                                columnSpacing: 15
                                width: scrollviewVideo.availableWidth
                                Layout.fillWidth: true

                                Label {Layout.fillWidth: false; text: "Output Path"}
                                TextField {
                                    id: "outputPathInput"
                                    placeholderText: "Enter the output path for the videos..."
                                    Layout.fillWidth: true
                                    }
                                Button {
                                    Layout.fillWidth: false
                                    text: "Select Path"
                                    }


                                }

                            GridLayout {
                                columnSpacing: 15
                                rowSpacing: 15
                                width: scrollviewVideo.availableWidth
                                Layout.fillWidth: false
                                columns: 2

                                HelpButton {Layout.fillWidth: false}
                                CheckBox {
                                    Layout.fillWidth: true
                                    text: "Write metadata"

                                }

                                HelpButton {Layout.fillWidth: false}
                                CheckBox {
                                    Layout.fillWidth: true
                                    text: "Use directory system"
                                }

                                HelpButton {Layout.fillWidth: false}
                                CheckBox {
                                    Layout.fillWidth: true
                                    text: "Skip existing files"
                                }

                            }

                        }


                    }

                    // ==========================================
                    // TAB 2: LEISTUNG SETTINGS (Performance)
                    // ==========================================
                    ScrollView {
                        id: "scrollviewPerformance"
                        clip: true

                        GridLayout {

                            columnSpacing: 15
                            columns: 3 // We use 6 columns to create two pairs of (Label, Spinbox)
                            width: scrollviewPerformance.availableWidth
                            Layout.fillWidth: true
                            rowSpacing: 15


                            // Left Pair                        // Right Pair
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                Layout.fillWidth: false
                                text: "Download workers:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 10
                                value: 20
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Network delay (requests/sec):"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: 0
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Parallel Downloads:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: 1
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Maximum retries:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: 5
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Maximum timeout:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: 10
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Processing Delay (videos/sec):"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: 1
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Speed Limit (MB/s):"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: 0
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Videos Concurrency:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: 10
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Pages concurrency:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                editable: true
                                to: 100
                                value: 2
                            }

                            // Empty spaces for layout balance where the right side has no items
                            Item {
                                Layout.fillWidth: false
                            }
                            Item {
                                Layout.columnSpan: 3
                                Layout.fillHeight: true
                            }
                        }
                    }

                    // ==========================================
                    // TAB 3: SYSTEM SETTINGS
                    // ==========================================
                    ScrollView {
                        clip: true
                        id: "scrollviewSettings"

                        GridLayout {
                            columnSpacing: 15
                            columns: 2 // We use 6 columns to create two pairs of (Label, Spinbox)
                            width: scrollviewPerformance.availableWidth
                            Layout.fillWidth: true
                            rowSpacing: 15

                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                text: "Search for Updates (On startup)"
                                Layout.fillWidth: true
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                text: "Anonymous mode"
                                Layout.fillWidth: true
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                text: "Ignore Errors"
                                Layout.fillWidth: true
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                // Use \n for multi-line text
                                text: "Allow error reports (100% anonymous)"
                                Layout.fillWidth: true
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                text: "Enable Proxy"
                                Layout.fillWidth: true
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                text: "Enable Debug Mode (Not recommended)"
                                Layout.fillWidth: true
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            CheckBox {
                                checked: true
                                text: "Use Truststore"
                                Layout.fillWidth: true
                            }
                        }
                    }

                    // ==========================================
                    // TAB 4: UI SETTINGS
                    // ==========================================
                    ScrollView {
                        id: "scrollviewUI"
                        clip: true

                        GridLayout {
                            width: scrollviewUI.availableWidth
                            columnSpacing: 15
                            columns: 3
                            rowSpacing: 15
                            Layout.fillWidth: true

                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Graphical User Interface language:"
                            }
                            ComboBox {
                                Layout.fillWidth: true
                                model: ["System", "English", "German", "French", "Italian"]
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Font Size:"
                            }
                            SpinBox {
                                Layout.fillWidth: true
                                from: 8
                                to: 72
                                value: 10
                            }
                            HelpButton {
                                Layout.fillWidth: false
                            }
                            Label {
                                text: "Theme:"
                            }
                            ComboBox {
                                Layout.fillWidth: true
                                model: ["Dark", "Light", "System"]
                            }

                        }
                    }
                }
            }
        }

        // ---------------------------------------------------------
        // HORIZONTAL SEPARATOR LINE
        // ---------------------------------------------------------
        // A simple Rectangle acts as a line to visually separate content from bottom buttons
        Rectangle {
            Layout.fillWidth: true
            color: "#333333" // Dark grey border
            height: 1
        }

        // ---------------------------------------------------------
        // BOTTOM GLOBAL ACTION BUTTONS
        // ---------------------------------------------------------
        // A ColumnLayout containing 3 RowLayouts to perfectly align the buttons in a grid structure
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 10 // Space between rows of buttons

            // Row 1
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Button {
                    Layout.fillWidth: true
                    // Material styling overrides for specific buttons to make them stand out
                    Material.background: "#6366f1" // Premium Indigo color
                    Material.foreground: "white"   // White text
                    font.bold: true // Make text bold
                    text: "Buy License (11.99€)"
                }
                Button {
                    Layout.fillWidth: true
                    text: "Import License File"
                    // No custom colors here, defaults to normal Material dark button
                }
            }

            // Row 2
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Button {
                    Layout.fillWidth: true
                    Material.background: "#3b82f6" // Primary Blue color
                    Material.foreground: "white"
                    text: "Apply (requires restart)"
                }
                Button {
                    Layout.fillWidth: true
                    Material.background: "#ef4444" // Danger Red color
                    Material.foreground: "white"
                    text: "Reset Porn Fetch to default settings"
                }
            }

            // Row 3
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Button {
                    Layout.fillWidth: true
                    Material.background: "#10b981" // Success Green color
                    Material.foreground: "white"
                    text: "Install Porn Fetch"
                }
                Button {
                    Layout.fillWidth: true
                    Material.background: "#ef4444" // Danger Red color
                    Material.foreground: "white"
                    text: "Uninstall Porn Fetch"
                }
                Button {
                    Layout.fillWidth: true
                    text: "Clear Temporary Files"
                }
            }
        }
    }
}
