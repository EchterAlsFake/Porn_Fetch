import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Dialogs
import QtCore // Required for StandardPaths

ApplicationWindow {
    id: root
    width: 520
    height: 420
    visible: true
    title: "License Manager"

    // Enable Material Dark Theme natively
    Material.theme: Material.Dark
    Material.accent: Material.Blue
    Material.primary: Material.BlueGrey

    // Deep dark background for the main window
    color: "#121212"

    // Exposed properties (can be bound to PySide6 QObject properties)
    property bool isInstalled: false
    property string licensePath: isInstalled ? "/app/data/licenses/license.lic" : "No license file found"

    // Signal emitted when user selects a file to import
    signal importLicenseRequested(string fileUrl)

    // --- File Dialog ---
    FileDialog {
        id: licenseFileDialog
        title: "Select License File"
        currentFolder: StandardPaths.writableLocation(StandardPaths.HomeLocation)
        nameFilters: ["License Files (*.lic *.key *.json)", "All Files (*)"]

        onAccepted: {
            root.importLicenseRequested(licenseFileDialog.selectedFile)
        }
    }

    // --- Main Layout ---
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 24
        spacing: 24

        // Header
        ColumnLayout {
            spacing: 6
            Text {
                text: "Application License"
                font.pixelSize: 22
                font.bold: true
                color: "#ffffff" // Pure white for primary dark mode text
            }
            Text {
                text: "Manage your software activation and license files."
                font.pixelSize: 13
                color: "#b0b0b0" // Soft gray for secondary text
            }
        }

        // Status Card Container
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: 90
            radius: 8
            color: "#1e1e1e" // Elevated Material surface color
            border.color: "#333333" // Subtle dark border
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16

                // Status Indicator Dot
                Rectangle {
                    implicitWidth: 12
                    implicitHeight: 12
                    radius: 6
                    // Material Design Green and Red
                    color: root.isInstalled ? "#4caf50" : "#f44336"
                }

                // Status Text
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4

                    Text {
                        text: "License Status"
                        font.pixelSize: 12
                        color: "#b0b0b0"
                    }
                    Text {
                        text: root.isInstalled ? "Installed (Valid)" : "Not Installed (Invalid)"
                        font.pixelSize: 16
                        font.bold: true
                        color: root.isInstalled ? "#4caf50" : "#f44336"
                    }
                }
            }
        }

        // License Storage Path Card
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: 90
            radius: 8
            color: "#1e1e1e"
            border.color: "#333333"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 8

                Text {
                    text: "License Storage Path"
                    font.pixelSize: 12
                    color: "#b0b0b0"
                }

                // Relies on Material theme for the text field styling (underline effect)
                TextField {
                    Layout.fillWidth: true
                    text: root.licensePath
                    readOnly: true
                    font.pixelSize: 13
                    selectByMouse: true
                }
            }
        }

        Item { Layout.fillHeight: true } // Spacer pushes buttons to the bottom

        // Action Row - Centered Buttons
        RowLayout {
            Layout.fillWidth: true
            spacing: 16

            Item { Layout.fillWidth: true } // Left expanding spacer

            Button {
                text: "Close"
                flat: true // Material flat button style for secondary actions
                Material.foreground: Material.accent
                onClicked: root.close()
            }

            Button {
                text: "Import License..."
                highlighted: true // Automatically filled with Material.accent color
                onClicked: licenseFileDialog.open()
            }

            Item { Layout.fillWidth: true } // Right expanding spacer
        }
    }
}