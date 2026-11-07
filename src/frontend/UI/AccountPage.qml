// qml/pages/AccountPage.qml

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root

    required property var backendController
    readonly property bool androidLayoutMode: Qt.platform.os === "android"
                                              || (typeof androidLayout !== "undefined" && androidLayout)
    readonly property string selectedProvider: {
        if (providerTabs.currentIndex === 1)
            return "XHamster"
        if (providerTabs.currentIndex === 2)
            return "XVideos"
        return "PornHub"
    }
    readonly property bool usesAccountCredentials: selectedProvider !== "XVideos"
    readonly property bool invalidXhamsterEmail: selectedProvider === "XHamster"
                                               && identityField.text.trim().length > 0
                                               && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(identityField.text.trim())
    readonly property bool providerLoggedIn:
        Boolean(backendController.accountLoginStatus[selectedProvider])
    readonly property bool accountBusy: backendController.loginInProgress
                                        || backendController.accountFetchInProgress

    padding: 8

    background: Rectangle {
        color: "transparent"
        border.width: 2
        border.color: Theme.outline
        radius: 10
    }

    component CollectionButton: AppButton {
        id: actionButton
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.minimumWidth: 0
        Layout.preferredWidth: 1
        implicitHeight: Math.max(48, contentItem.implicitHeight + topPadding + bottomPadding)
        contentItem: Label {
            text: actionButton.text
            font: actionButton.font
            color: actionButton.enabled ? actionButton.palette.buttonText : actionButton.palette.mid
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            wrapMode: Text.WordWrap
        }
    }

    ScrollView {
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth

        ColumnLayout {
            width: parent.width
            spacing: 6

            TabBar {
                id: providerTabs

                Layout.fillWidth: true

                TabButton {
                    text: qsTr("PornHub")
                }

                TabButton {
                    text: qsTr("XHamster")
                }

                TabButton {
                    text: qsTr("XVideos")
                }
            }

            GridLayout {
                Layout.fillWidth: true
                columns: root.width < 700 ? 1 : 2
                visible: root.usesAccountCredentials

                Label {
                    text: qsTr("Email:")
                }

                AppTextField {
                    id: identityField

                    Layout.fillWidth: true
                    Accessible.name: placeholderText
                    placeholderText: qsTr("Enter your email address")
                    inputMethodHints: Qt.ImhEmailCharactersOnly
                    Accessible.description: root.invalidXhamsterEmail ? emailWarning.text : ""
                    selectByMouse: true
                }

                Label {
                    text: qsTr("Password:")
                }

                AppTextField {
                    id: passwordField

                    Layout.fillWidth: true

                    echoMode: TextInput.Password
                    Accessible.name: placeholderText
                    placeholderText: qsTr("Enter your password")
                    selectByMouse: true

                    onAccepted: {
                        if (loginButton.enabled)
                            loginButton.clicked()
                    }
                }
            }

            Label {
                id: emailWarning
                objectName: "xhamsterEmailWarning"
                Layout.fillWidth: true
                visible: root.invalidXhamsterEmail
                text: qsTr("XHamster requires your email address, not your username.")
                color: Theme.highContrast ? Theme.ink : Theme.dark ? "#fca5a5" : "#b91c1c"
                wrapMode: Text.WordWrap
            }

            GridLayout {
                Layout.fillWidth: true
                columns: root.width < 700 ? 1 : 2
                visible: !root.usesAccountCredentials

                Label {
                    text: qsTr("Session token:")
                }

                AppTextField {
                    id: sessionTokenField
                    Layout.fillWidth: true
                    echoMode: TextInput.Password
                    Accessible.name: placeholderText
                    placeholderText: qsTr("Enter session_token")
                    selectByMouse: true
                }

                Label {
                    text: qsTr("Session token auth:")
                }

                AppTextField {
                    id: sessionTokenAuthField
                    Layout.fillWidth: true
                    echoMode: TextInput.Password
                    placeholderText: qsTr("Enter session_token_auth")
                    selectByMouse: true

                    onAccepted: {
                        if (loginButton.enabled)
                            loginButton.clicked()
                    }
                }
            }

            AppButton {
                id: loginButton
                Layout.fillWidth: true

                text: root.selectedProvider === "XVideos"
                      ? qsTr("Login with Session Tokens")
                      : qsTr("Login")

                enabled: !root.accountBusy
                         && !root.invalidXhamsterEmail
                         && (root.usesAccountCredentials
                             ? identityField.text.trim().length > 0
                               && passwordField.text.length > 0
                             : sessionTokenField.text.trim().length > 0
                               && sessionTokenAuthField.text.trim().length > 0)

                onClicked: {
                    root.backendController.login_account(
                        root.selectedProvider,
                        root.usesAccountCredentials
                            ? identityField.text : sessionTokenField.text,
                        root.usesAccountCredentials
                            ? passwordField.text : sessionTokenAuthField.text,
                        false
                    )
                }
            }


            GridLayout {
                Layout.fillWidth: true
                columns: root.androidLayoutMode ? (root.width < 700 ? 1 : 2) : 4
                uniformCellWidths: true
                uniformCellHeights: true
                columnSpacing: 12

                CollectionButton {
                    visible: root.selectedProvider !== "XHamster"
                    text: root.selectedProvider === "PornHub"
                          ? qsTr("Get Watch History")
                          : qsTr("Get Watch Later Videos")
                    enabled: root.providerLoggedIn && !root.accountBusy

                    onClicked: {
                        root.backendController.fetch_account_videos(
                            root.selectedProvider,
                            root.selectedProvider === "PornHub" ? "history" : "watch_later",
                            ""
                        )
                    }
                }

                CollectionButton {
                    visible: root.selectedProvider !== "XHamster"
                    text: root.selectedProvider === "PornHub" ? qsTr("Get Recommended Videos") : qsTr("Get Watch History")
                    enabled: root.providerLoggedIn && !root.accountBusy

                    onClicked: {
                        root.backendController.fetch_account_videos(
                            root.selectedProvider, root.selectedProvider === "PornHub" ? "recommended" : "history", ""
                        )
                    }
                }

                CollectionButton {
                    visible: root.selectedProvider === "PornHub"
                    text: qsTr("Get Subscription Feed")
                    enabled: root.providerLoggedIn && !root.accountBusy
                    onClicked: root.backendController.fetch_account_videos(root.selectedProvider, "feed", "")
                }

                CollectionButton {
                    text: root.selectedProvider === "PornHub"
                          ? qsTr("Get Favorite Videos")
                          : qsTr("Get Liked Videos")
                    enabled: root.providerLoggedIn && !root.accountBusy

                    onClicked: {
                        root.backendController.fetch_account_videos(
                            root.selectedProvider,
                            root.selectedProvider === "PornHub" ? "favorites" : "liked",
                            ""
                        )
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                visible: !root.androidLayoutMode

                AppTextField {
                    id: browserUsernameField
                    Layout.fillWidth: true
                    visible: root.selectedProvider === "PornHub"
                    Accessible.name: placeholderText
                    placeholderText: qsTr("PornHub username for browser cookies (not email)")
                    selectByMouse: true
                }

                AppButton {
                    Layout.fillWidth: root.selectedProvider !== "PornHub"
                    text: qsTr("Login with Browser Cookies")
                    enabled: !root.accountBusy && (root.selectedProvider !== "PornHub"
                                                  || browserUsernameField.text.trim().length > 0)
                    onClicked: root.backendController.login_account(
                        root.selectedProvider, browserUsernameField.text, "", true)
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Label {
                    Layout.fillWidth: true
                    wrapMode: Text.Wrap
                    text: root.providerLoggedIn
                          ? qsTr("Logged in to %1").arg(root.selectedProvider)
                          : qsTr("Not logged in to %1").arg(root.selectedProvider)
                }
                AccountLoginHelp {
                    provider: root.selectedProvider
                    browserImportAvailable: !root.androidLayoutMode
                }
            }

            GridLayout {
                Layout.fillWidth: true
                columns: root.width < 700 ? 1 : 3
                visible: root.selectedProvider === "XHamster"

                Label {
                    text: qsTr("Account playlist URL:")
                }

                AppTextField {
                    id: accountPlaylistField
                    Layout.fillWidth: true
                    Accessible.name: placeholderText
                    placeholderText: qsTr("https://xhamster.com/my/playlists/...")
                    selectByMouse: true

                    onAccepted: {
                        if (accountPlaylistButton.enabled)
                            accountPlaylistButton.clicked()
                    }
                }

                AppButton {
                    id: accountPlaylistButton
                    text: qsTr("Get Playlist Videos")
                    enabled: root.providerLoggedIn
                             && !root.accountBusy
                             && accountPlaylistField.text.trim().length > 0

                    onClicked: {
                        root.backendController.fetch_account_videos(
                            root.selectedProvider,
                            "playlist",
                            accountPlaylistField.text.trim()
                        )
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                implicitHeight: 56
                color: "transparent"

                Label {
                    anchors.centerIn: parent

                    text: root.backendController.accountFetchInProgress
                          ? qsTr("Loading account videos...")
                          : qsTr("Retrieved videos are added to the Downloads page")
                }
            }
        }
    }
}
