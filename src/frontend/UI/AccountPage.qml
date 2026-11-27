import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root

    required property var backendController
    property bool compact: Qt.platform.os === "android"
                           || (typeof androidLayout !== "undefined" && androidLayout)
    readonly property var accountProvider: (backendController.accountProviders || [])[providerSelector.currentIndex]
                                           || ({})
    readonly property string selectedProvider: accountProvider.name || ""
    readonly property bool usesAccountCredentials: accountProvider.login === "password"
    readonly property bool usesSessionTokens: accountProvider.login === "tokens"
    readonly property bool browserImportAvailable: !compact && Boolean(accountProvider.browserImport)
    readonly property bool browserUsernameRequired: accountProvider.browserImport === "username"
    readonly property bool accountAvailable: usesAccountCredentials || usesSessionTokens || browserImportAvailable
    readonly property var accountCollections: accountAvailable ? (accountProvider.collections || []) : []
    readonly property bool invalidAccountEmail: Boolean(accountProvider.emailRequired)
                                                && identityField.text.trim().length > 0
                                                && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(identityField.text.trim())
    readonly property bool providerLoggedIn:
        Boolean(backendController.accountLoginStatus[selectedProvider])
    readonly property bool accountBusy: backendController.loginInProgress
                                        || backendController.accountFetchInProgress

    padding: compact ? 16 : 8

    background: Rectangle {
        color: "transparent"
        border.width: root.compact ? 0 : 2
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
        id: accountScroll
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth

        ColumnLayout {
            width: accountScroll.availableWidth
            spacing: root.compact ? 10 : 6

            Label {
                id: providerLabel
                text: qsTr("Choose a website")
            }

            AppComboBox {
                id: providerSelector
                objectName: "accountProviderSelector"
                Layout.fillWidth: true
                textRole: "name"
                model: root.backendController.accountProviders
                Accessible.name: providerLabel.text
                onActivated: {
                    identityField.clear()
                    passwordField.clear()
                    sessionTokenField.clear()
                    sessionTokenAuthField.clear()
                    browserUsernameField.clear()
                }
            }

            Label {
                Layout.fillWidth: true
                visible: !root.accountAvailable && root.selectedProvider.length > 0
                text: qsTr("Account access for %1 is unavailable in Porn Fetch.").arg(root.selectedProvider)
                wrapMode: Text.Wrap
            }

            GridLayout {
                Layout.fillWidth: true
                columns: root.compact || root.width < 700 ? 1 : 2
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
                    Accessible.description: root.invalidAccountEmail ? emailWarning.text : ""
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
                visible: root.invalidAccountEmail
                text: qsTr("%1 requires your email address, not your username.").arg(root.selectedProvider)
                color: Theme.highContrast ? Theme.ink : Theme.dark ? "#fca5a5" : "#b91c1c"
                wrapMode: Text.WordWrap
            }

            GridLayout {
                Layout.fillWidth: true
                columns: root.compact || root.width < 700 ? 1 : 2
                visible: root.usesSessionTokens

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
                    Accessible.name: placeholderText
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

                visible: root.usesAccountCredentials || root.usesSessionTokens
                text: root.usesSessionTokens
                      ? qsTr("Login with Session Tokens")
                      : qsTr("Login")

                enabled: !root.accountBusy
                         && !root.invalidAccountEmail
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
                visible: root.accountCollections.some(collection => !collection.urlHint)
                columns: root.compact ? 1 : (root.width < 700 ? 2 : 4)
                uniformCellWidths: true
                uniformCellHeights: true
                columnSpacing: 12

                Repeater {
                    model: root.accountCollections.filter(collection => !collection.urlHint)

                    CollectionButton {
                        required property var modelData
                        text: qsTranslate("AccountPage", modelData.label)
                        enabled: root.providerLoggedIn && !root.accountBusy
                        onClicked: root.backendController.fetch_account_videos(root.selectedProvider, modelData.key, "")
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                visible: root.browserImportAvailable

                AppTextField {
                    id: browserUsernameField
                    Layout.fillWidth: true
                    visible: root.browserUsernameRequired
                    Accessible.name: placeholderText
                    placeholderText: qsTr("%1 username for browser cookies (not email)").arg(root.selectedProvider)
                    selectByMouse: true
                }

                AppButton {
                    Layout.fillWidth: !root.browserUsernameRequired
                    text: qsTr("Login with Browser Cookies")
                    enabled: !root.accountBusy
                             && (!root.browserUsernameRequired || browserUsernameField.text.trim().length > 0)
                    onClicked: root.backendController.login_account(
                        root.selectedProvider, root.browserUsernameRequired ? browserUsernameField.text : "", "", true)
                }
            }

            RowLayout {
                Layout.fillWidth: true
                visible: root.accountAvailable
                Label {
                    Layout.fillWidth: true
                    wrapMode: Text.Wrap
                    text: root.providerLoggedIn
                          ? qsTr("Logged in to %1").arg(root.selectedProvider)
                          : qsTr("Not logged in to %1").arg(root.selectedProvider)
                }
                AccountLoginHelp {
                    provider: root.selectedProvider
                    usesSessionTokens: root.usesSessionTokens
                    usesAccountCredentials: root.usesAccountCredentials
                    browserUsernameRequired: root.browserUsernameRequired
                    browserImportAvailable: root.browserImportAvailable
                }
            }

            Repeater {
                model: root.accountCollections.filter(collection => collection.urlHint)

                GridLayout {
                    id: urlCollection
                    required property var modelData
                    Layout.fillWidth: true
                    columns: root.compact || root.width < 700 ? 1 : 3

                    Label {
                        text: qsTr("Account playlist URL:")
                    }

                    AppTextField {
                        id: accountPlaylistField
                        Layout.fillWidth: true
                        Accessible.name: qsTr("Account playlist URL")
                        placeholderText: urlCollection.modelData.urlHint
                        inputMethodHints: Qt.ImhUrlCharactersOnly
                        selectByMouse: true

                        onAccepted: {
                            if (accountPlaylistButton.enabled)
                                accountPlaylistButton.clicked()
                        }
                    }

                    AppButton {
                        id: accountPlaylistButton
                        text: qsTranslate("AccountPage", urlCollection.modelData.label)
                        enabled: root.providerLoggedIn
                                 && !root.accountBusy
                                 && accountPlaylistField.text.trim().length > 0

                        onClicked: root.backendController.fetch_account_videos(
                            root.selectedProvider, urlCollection.modelData.key, accountPlaylistField.text.trim())
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                implicitHeight: accountFeedback.implicitHeight + 20
                visible: root.accountCollections.length > 0
                color: "transparent"

                Label {
                    id: accountFeedback
                    anchors.fill: parent
                    anchors.topMargin: 10
                    anchors.bottomMargin: 10
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.Wrap

                    text: root.backendController.accountFetchInProgress
                          ? qsTr("Loading account videos...")
                          : qsTr("Retrieved videos are added to the Downloads page")
                }
            }
        }
    }
}
