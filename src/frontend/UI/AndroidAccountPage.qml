import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Pane {
    id: root
    padding: 0
    readonly property color pageColor: appSettings.high_contrast ? Theme.background : appSettings.dark_mode ? "#101319" : Theme.lightShade("#f7f8fc")
    readonly property color cardColor: appSettings.high_contrast ? Theme.background : appSettings.dark_mode ? "#1b202a" : Theme.lightShade("#ffffff")
    readonly property color textColor: appSettings.high_contrast ? Theme.ink : appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.high_contrast ? Theme.ink : appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    readonly property color accentColor: appSettings.high_contrast ? Theme.accent : appSettings.accent_color
    readonly property var providers: ["PornHub", "XHamster", "XVideos"]
    property int providerIndex: 0
    readonly property string provider: providers[providerIndex]
    readonly property bool loggedIn: Boolean(backend.accountLoginStatus[provider])
    readonly property bool busy: backend.loginInProgress || backend.accountFetchInProgress
    readonly property bool tokenLogin: provider === "XVideos"
    readonly property bool invalidXhamsterEmail: provider === "XHamster"
                                               && identityField.text.trim().length > 0
                                               && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(identityField.text.trim())
    background: Rectangle { color: root.pageColor }

    ScrollView {
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 16
        width: Math.min(parent.width - 32, 640)
        id: accountScroll
        contentWidth: availableWidth
        clip: true

        ColumnLayout {
            width: accountScroll.availableWidth
            spacing: 8
            Label {
                Layout.fillWidth: true
                text: qsTr("Choose a website")
                color: root.textColor
                font.pixelSize: 20 * appSettings.font_size / 12
                font.bold: true
                wrapMode: Text.Wrap
            }
            AppComboBox {
                id: providerSelector
                objectName: "mobileAccountProviderSelector"
                Layout.fillWidth: true
                model: root.providers
                currentIndex: root.providerIndex
                Accessible.name: qsTr("Choose a website")
                onActivated: root.providerIndex = currentIndex
            }

            AccountLoginHelp {
                provider: root.provider
                browserImportAvailable: false
            }

            Rectangle {
                Layout.fillWidth: true
                implicitHeight: loginContent.implicitHeight + 24
                radius: 22
                color: root.cardColor
                ColumnLayout {
                    id: loginContent
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.margins: 12
                    spacing: 8
                    Label {
                        Layout.fillWidth: true
                        text: root.loggedIn ? qsTr("Connected to %1").arg(root.provider)
                                            : qsTr("Connect to %1").arg(root.provider)
                        color: root.textColor
                        font.pixelSize: 19 * appSettings.font_size / 12
                        font.bold: true
                        wrapMode: Text.Wrap
                    }
                    AppTextField {
                        id: identityField
                        Layout.fillWidth: true
                        visible: !root.tokenLogin
                        Accessible.name: placeholderText
                        placeholderText: qsTr("Email address")
                        inputMethodHints: Qt.ImhEmailCharactersOnly
                        Accessible.description: root.invalidXhamsterEmail ? emailWarning.text : ""
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
                    AppTextField {
                        id: passwordField
                        Layout.fillWidth: true
                        visible: !root.tokenLogin
                        placeholderText: qsTr("Password")
                        echoMode: TextInput.Password
                    }
                    AppTextField {
                        id: tokenField
                        Layout.fillWidth: true
                        visible: root.tokenLogin
                        Accessible.name: placeholderText
                        placeholderText: qsTr("session_token")
                        echoMode: TextInput.Password
                    }
                    AppTextField {
                        id: tokenAuthField
                        Layout.fillWidth: true
                        visible: root.tokenLogin
                        placeholderText: qsTr("session_token_auth")
                        echoMode: TextInput.Password
                    }
                    AppButton {
                        Layout.fillWidth: true
                        text: root.busy ? qsTr("Connecting…") : qsTr("Sign in")
                        highlighted: true
                        enabled: !root.busy && !root.invalidXhamsterEmail && (root.tokenLogin
                                 ? tokenField.text.trim().length > 0 && tokenAuthField.text.trim().length > 0
                                 : identityField.text.trim().length > 0 && passwordField.text.length > 0)
                        onClicked: backend.login_account(root.provider,
                                                         root.tokenLogin ? tokenField.text : identityField.text,
                                                         root.tokenLogin ? tokenAuthField.text : passwordField.text,
                                                         false)
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                implicitHeight: collectionsContent.implicitHeight + 24
                radius: 22
                color: root.cardColor
                ColumnLayout {
                    id: collectionsContent
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.margins: 12
                    spacing: 8
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Your collections")
                        color: root.textColor
                        font.pixelSize: 19 * appSettings.font_size / 12
                        font.bold: true
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Videos you retrieve appear in Downloads.")
                        color: root.mutedColor
                        wrapMode: Text.Wrap
                    }
                    AppButton {
                        Layout.fillWidth: true
                        visible: root.provider !== "XHamster"
                        text: root.provider === "PornHub" ? qsTr("Watch history") : qsTr("Watch later")
                        enabled: root.loggedIn && !root.busy
                        onClicked: backend.fetch_account_videos(root.provider,
                                     root.provider === "PornHub" ? "history" : "watch_later", "")
                    }
                    AppButton {
                        Layout.fillWidth: true
                        visible: root.provider !== "XHamster"
                        text: root.provider === "PornHub" ? qsTr("Recommended") : qsTr("Watch history")
                        enabled: root.loggedIn && !root.busy
                        onClicked: backend.fetch_account_videos(root.provider, root.provider === "PornHub" ? "recommended" : "history", "")
                    }
                    AppButton {
                        Layout.fillWidth: true
                        visible: root.provider === "PornHub"
                        text: qsTr("Subscription feed")
                        enabled: root.loggedIn && !root.busy
                        onClicked: backend.fetch_account_videos(root.provider, "feed", "")
                    }
                    AppButton {
                        Layout.fillWidth: true
                        text: root.provider === "PornHub" ? qsTr("Favorites") : qsTr("Liked videos")
                        enabled: root.loggedIn && !root.busy
                        onClicked: backend.fetch_account_videos(root.provider,
                                     root.provider === "PornHub" ? "favorites" : "liked", "")
                    }
                    AppTextField {
                        id: playlistField
                        Layout.fillWidth: true
                        visible: root.provider === "XHamster"
                        Accessible.name: placeholderText
                        placeholderText: qsTr("Account playlist URL")
                        inputMethodHints: Qt.ImhUrlCharactersOnly
                    }
                    AppButton {
                        Layout.fillWidth: true
                        visible: root.provider === "XHamster"
                        text: qsTr("Get playlist videos")
                        enabled: root.loggedIn && !root.busy && playlistField.text.trim().length > 0
                        onClicked: backend.fetch_account_videos(root.provider, "playlist", playlistField.text.trim())
                    }
                    Label {
                        Layout.fillWidth: true
                        visible: backend.accountFetchInProgress
                        text: qsTr("Loading account videos…")
                        color: root.mutedColor
                    }
                }
            }
        }
    }
}
