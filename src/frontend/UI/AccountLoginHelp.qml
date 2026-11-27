import QtQuick
import QtQuick.Controls

HelpButton {
    property string provider: ""
    property bool usesSessionTokens: false
    property bool usesAccountCredentials: false
    property bool browserUsernameRequired: false
    property bool browserImportAvailable: false

    text: qsTr("How to login")

    readonly property string manualHelp: usesSessionTokens
        ? qsTr("%1: sign in on the website in a browser. In Developer Tools, open Application or Storage, then Cookies. Copy session_token and session_token_auth into the matching fields and select Login with Session Tokens. On Android, you can obtain both tokens from your desktop browser.").arg(provider)
        : usesAccountCredentials
          ? qsTr("%1: enter your account email address and password, then select Login.").arg(provider)
          : ""
    readonly property string browserHelp: browserImportAvailable
        ? qsTr("To import cookies, first sign in to %1 in Chrome, Firefox, Edge, Brave, Opera, Vivaldi, Safari or LibreWolf. Then select Login with Browser Cookies. Your operating system may ask for keychain access. If import fails, try closing the browser. If the session expires, sign in on the website again.").arg(provider)
          + (browserUsernameRequired ? " " + qsTr("Enter your profile username in the browser login section.") : "")
        : qsTr("Automatic browser-cookie import is available on desktop only.")
    helpText: [manualHelp, browserHelp,
               qsTr("Login cookies identify your signed-in session. Treat them like a password and keep them private.")]
              .filter(paragraph => paragraph.length > 0).join("\n\n")
}
