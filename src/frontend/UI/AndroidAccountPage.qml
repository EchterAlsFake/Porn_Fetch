import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Pane {
    id: root
    padding: 0
    readonly property color pageColor: appSettings.dark_mode ? "#101319" : "#f7f8fc"
    readonly property color cardColor: appSettings.dark_mode ? "#1b202a" : "#ffffff"
    readonly property color textColor: appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    readonly property color accentColor: appSettings.accent_color
    readonly property var providers: ["PornHub", "XHamster", "XVideos"]
    property int providerIndex: 0
    readonly property string provider: providers[providerIndex]
    readonly property bool loggedIn: Boolean(backend.accountLoginStatus[provider])
    readonly property bool busy: backend.loginInProgress || backend.accountFetchInProgress
    readonly property bool tokenLogin: provider === "XVideos"
    background: Rectangle { color: root.pageColor }

    ScrollView {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        contentWidth: availableWidth
        clip: true

        ColumnLayout {
            width: parent.width
            spacing: 14
            Item { Layout.preferredHeight: 4 }
            Label {
                Layout.fillWidth: true
                text: qsTr("Choose a website")
                color: root.textColor
                font.pixelSize: 20
                font.bold: true
            }
            Label {
                Layout.fillWidth: true
                text: qsTr("Sign in to collect videos from your account.")
                color: root.mutedColor
                wrapMode: Text.Wrap
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                Repeater {
                    model: root.providers
                    delegate: Button {
                        required property int index
                        required property string modelData
                        Layout.fillWidth: true
                        text: modelData
                        flat: root.providerIndex !== index
                        highlighted: root.providerIndex === index
                        onClicked: root.providerIndex = index
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                implicitHeight: loginContent.implicitHeight + 36
                radius: 22
                color: root.cardColor
                ColumnLayout {
                    id: loginContent
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.margins: 18
                    spacing: 12
                    Label {
                        Layout.fillWidth: true
                        text: root.loggedIn ? qsTr("Connected to %1").arg(root.provider)
                                            : qsTr("Connect to %1").arg(root.provider)
                        color: root.textColor
                        font.pixelSize: 19
                        font.bold: true
                        wrapMode: Text.Wrap
                    }
                    Label {
                        Layout.fillWidth: true
                        text: root.tokenLogin
                              ? qsTr("Enter the session tokens from your browser.")
                              : root.provider === "XHamster"
                                ? qsTr("Enter your username and password.")
                                : qsTr("Enter your email address and password.")
                        color: root.mutedColor
                        wrapMode: Text.Wrap
                    }
                    TextField {
                        id: identityField
                        Layout.fillWidth: true
                        visible: !root.tokenLogin
                        placeholderText: root.provider === "XHamster" ? qsTr("Username") : qsTr("Email address")
                        inputMethodHints: root.provider === "PornHub" ? Qt.ImhEmailCharactersOnly : Qt.ImhNoPredictiveText
                    }
                    TextField {
                        id: passwordField
                        Layout.fillWidth: true
                        visible: !root.tokenLogin
                        placeholderText: qsTr("Password")
                        echoMode: TextInput.Password
                    }
                    TextField {
                        id: tokenField
                        Layout.fillWidth: true
                        visible: root.tokenLogin
                        placeholderText: qsTr("session_token")
                        echoMode: TextInput.Password
                    }
                    TextField {
                        id: tokenAuthField
                        Layout.fillWidth: true
                        visible: root.tokenLogin
                        placeholderText: qsTr("session_token_auth")
                        echoMode: TextInput.Password
                    }
                    Button {
                        Layout.fillWidth: true
                        text: root.busy ? qsTr("Connecting…") : qsTr("Sign in")
                        highlighted: true
                        enabled: !root.busy && (root.tokenLogin
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
                implicitHeight: collectionsContent.implicitHeight + 36
                radius: 22
                color: root.cardColor
                ColumnLayout {
                    id: collectionsContent
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.margins: 18
                    spacing: 8
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Your collections")
                        color: root.textColor
                        font.pixelSize: 19
                        font.bold: true
                    }
                    Label {
                        Layout.fillWidth: true
                        text: qsTr("Videos you retrieve appear in Downloads.")
                        color: root.mutedColor
                        wrapMode: Text.Wrap
                    }
                    Button {
                        Layout.fillWidth: true
                        visible: root.provider !== "XHamster"
                        text: root.provider === "PornHub" ? qsTr("Watch history") : qsTr("Watch later")
                        enabled: root.loggedIn && !root.busy
                        onClicked: backend.fetch_account_videos(root.provider,
                                     root.provider === "PornHub" ? "history" : "watch_later", "")
                    }
                    Button {
                        Layout.fillWidth: true
                        visible: root.provider !== "XHamster"
                        text: qsTr("Recommended")
                        enabled: root.loggedIn && !root.busy
                        onClicked: backend.fetch_account_videos(root.provider, "recommended", "")
                    }
                    Button {
                        Layout.fillWidth: true
                        text: root.provider === "PornHub" ? qsTr("Favorites") : qsTr("Liked videos")
                        enabled: root.loggedIn && !root.busy
                        onClicked: backend.fetch_account_videos(root.provider,
                                     root.provider === "PornHub" ? "favorites" : "liked", "")
                    }
                    TextField {
                        id: playlistField
                        Layout.fillWidth: true
                        visible: root.provider === "XHamster"
                        placeholderText: qsTr("Account playlist URL")
                        inputMethodHints: Qt.ImhUrlCharactersOnly
                    }
                    Button {
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
            Item { Layout.preferredHeight: 16 }
        }
    }
}
