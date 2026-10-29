import QtQuick
import QtQuick.Controls

HelpButton {
    property string provider: "PornHub"
    property bool browserImportAvailable: true
    text: qsTr("How to login")
    helpText: (provider === "PornHub"
        ? qsTr("PornHub: enter your account email address and password, then press Login. Once connected, use the collection buttons to retrieve your videos. For browser login, enter your PornHub profile username (not your email) in the separate browser section.")
        : provider === "XHamster"
          ? qsTr("XHamster: enter your username and password, then press Login. You can retrieve liked videos or paste an account playlist URL. Browser login does not require a username here.")
          : qsTr("XVideos: sign in on the website in your browser. Open Developer Tools, then Application / Storage → Cookies → the XVideos domain. Copy the values of session_token and session_token_auth into the matching fields, then press Login with Session Tokens. On a phone, use a browser with developer tools or obtain the tokens from your desktop browser. Both tokens are required."))
        + "\n\n" + qsTr("Cookies are small values stored by a website in your browser. Login cookies identify your signed-in session, so treat them like a password and never share them.")
        + "\n\n" + (browserImportAvailable
          ? qsTr("To import cookies, first sign in to the selected website in a supported desktop browser (Chrome, Firefox, Edge, Brave, Opera, Vivaldi, Safari or LibreWolf), then press Login with Browser Cookies. Porn Fetch uses browser-cookie3 to read that site's cookies from local browser profiles and passes them to the site's client. It does not open a new browser login window. Your operating system may ask for keychain access. If import fails, close the browser to release its cookie database, check your permissions, and try again. Expired sessions require signing in on the website again.")
          : qsTr("Automatic browser-cookie import is available on desktop only. On Android, use account credentials for PornHub or XHamster and paste both session tokens for XVideos."))
}
