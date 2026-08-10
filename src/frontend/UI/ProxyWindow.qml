import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

Window {
    id: root

    width: 580
    height: 700
    minimumWidth: 480
    minimumHeight: 620
    modality: Qt.ApplicationModal
    flags: Qt.Dialog
    title: qsTr("Proxy connection")

    signal proxyTestRequested(string proxyUrl, bool verifySsl)
    signal proxyAccepted(string proxyUrl, bool verifySsl)
    signal proxyDisabled()

    property string testState: "idle"
    property string statusMessage: qsTr("Enter the proxy details below.")
    property string lastRequestedProxy: ""
    property bool lastTestVerifiedSsl: true
    property var stats: ({})
    property bool loadingFields: false

    readonly property string proxyUrl: buildProxyUrl()
    readonly property bool inputValid: validationMessage() === ""

    function buildProxyUrl() {
        var host = hostField.text.trim()
        if (host.indexOf(":") !== -1 && host.charAt(0) !== "[")
            host = "[" + host + "]"

        var authentication = ""
        if (authenticationCheck.checked) {
            authentication = encodeURIComponent(usernameField.text)
            if (passwordField.text.length > 0)
                authentication += ":" + encodeURIComponent(passwordField.text)
            authentication += "@"
        }

        return schemeBox.currentText + "://" + authentication + host + ":" + portField.text
    }

    function validationMessage() {
        var host = hostField.text.trim()
        var port = Number(portField.text)

        if (host.length === 0)
            return qsTr("Enter a proxy host.")
        if (/\s/.test(host))
            return qsTr("The host cannot contain whitespace.")
        if (portField.text.length === 0 || !Number.isInteger(port) || port < 1 || port > 65535)
            return qsTr("Enter a port between 1 and 65535.")
        if (authenticationCheck.checked && usernameField.text.length === 0)
            return qsTr("Enter the authentication username.")
        return ""
    }

    function fieldsChanged() {
        if (loadingFields)
            return

        stats = ({})
        if (inputValid) {
            testState = "ready"
            statusMessage = qsTr("Format looks valid. Waiting to test…")
            automaticTest.restart()
        } else {
            automaticTest.stop()
            testState = "invalid"
            statusMessage = validationMessage()
        }
    }

    function startTest(verifySsl) {
        automaticTest.stop()
        if (!inputValid) {
            testState = "invalid"
            statusMessage = validationMessage()
            return
        }

        lastRequestedProxy = proxyUrl
        lastTestVerifiedSsl = verifySsl === undefined ? true : verifySsl
        testState = "testing"
        statusMessage = lastTestVerifiedSsl
                ? qsTr("Connecting through the proxy…")
                : qsTr("Connecting without SSL certificate verification…")
        stats = ({})
        proxyTestRequested(lastRequestedProxy, lastTestVerifiedSsl)
    }

    function showTestSuccess(testedProxy, result) {
        if (testedProxy !== lastRequestedProxy || testedProxy !== proxyUrl)
            return
        stats = result
        testState = "success"
        statusMessage = result.sslVerificationEnabled
                ? qsTr("Proxy connection successful")
                : qsTr("Proxy connection successful, but SSL verification is disabled")
    }

    function showTestFailure(testedProxy, message) {
        if (testedProxy !== lastRequestedProxy || testedProxy !== proxyUrl)
            return
        stats = ({})
        testState = "error"
        statusMessage = message
    }

    function showSslWarning(testedProxy, message) {
        if (testedProxy !== lastRequestedProxy || testedProxy !== proxyUrl)
            return
        stats = ({})
        testState = "sslWarning"
        statusMessage = message
    }

    function openWithProxy(value) {
        loadingFields = true
        loadProxyUrl(value || "")
        lastRequestedProxy = ""
        stats = ({})
        testState = inputValid ? "ready" : "idle"
        statusMessage = inputValid
                ? qsTr("Format looks valid. The proxy will be tested automatically.")
                : qsTr("Enter the proxy details below.")
        loadingFields = false
        show()
        raise()
        requestActivate()
        if (inputValid)
            automaticTest.restart()
    }

    function loadProxyUrl(value) {
        schemeBox.currentIndex = 0
        hostField.text = ""
        portField.text = ""
        authenticationCheck.checked = false
        usernameField.text = ""
        passwordField.text = ""

        if (!value)
            return

        var schemeEnd = value.indexOf("://")
        if (schemeEnd < 1)
            return

        var scheme = value.substring(0, schemeEnd).toLowerCase()
        var schemeIndex = schemeBox.find(scheme)
        if (schemeIndex >= 0)
            schemeBox.currentIndex = schemeIndex

        var authority = value.substring(schemeEnd + 3).replace(/\/$/, "")
        var atIndex = authority.lastIndexOf("@")
        if (atIndex >= 0) {
            var credentials = authority.substring(0, atIndex)
            authority = authority.substring(atIndex + 1)
            var credentialSeparator = credentials.indexOf(":")
            authenticationCheck.checked = true
            try {
                usernameField.text = decodeURIComponent(
                            credentialSeparator >= 0
                            ? credentials.substring(0, credentialSeparator)
                            : credentials)
                passwordField.text = credentialSeparator >= 0
                        ? decodeURIComponent(credentials.substring(credentialSeparator + 1))
                        : ""
            } catch (error) {
                usernameField.text = credentials
                passwordField.text = ""
            }
        }

        if (authority.charAt(0) === "[") {
            var bracketEnd = authority.indexOf("]")
            hostField.text = bracketEnd >= 0
                    ? authority.substring(1, bracketEnd)
                    : authority
            portField.text = bracketEnd >= 0 && authority.charAt(bracketEnd + 1) === ":"
                    ? authority.substring(bracketEnd + 2)
                    : ""
        } else {
            var portSeparator = authority.lastIndexOf(":")
            hostField.text = portSeparator >= 0
                    ? authority.substring(0, portSeparator)
                    : authority
            portField.text = portSeparator >= 0
                    ? authority.substring(portSeparator + 1)
                    : ""
        }
    }

    Timer {
        id: automaticTest
        interval: 900
        repeat: false
        onTriggered: root.startTest()
    }

    Pane {
        anchors.fill: parent
        padding: 22

        ColumnLayout {
            anchors.fill: parent
            spacing: 14

            Label {
                Layout.fillWidth: true
                text: qsTr("Configure proxy")
                font.pixelSize: 22
                font.bold: true
            }

            Label {
                Layout.fillWidth: true
                text: qsTr("Connection details are checked as you type. The network test runs after a short pause and uses curl-cffi.")
                wrapMode: Text.WordWrap
                opacity: 0.75
            }

            GridLayout {
                Layout.fillWidth: true
                columns: 2
                columnSpacing: 12
                rowSpacing: 10

                Label { text: qsTr("Protocol") }
                ComboBox {
                    id: schemeBox
                    Layout.fillWidth: true
                    model: ["http", "https", "socks4", "socks4a", "socks5", "socks5h"]
                    onActivated: root.fieldsChanged()
                }

                Label { text: qsTr("Host") }
                TextField {
                    id: hostField
                    Layout.fillWidth: true
                    placeholderText: qsTr("proxy.example.com or 127.0.0.1")
                    onTextEdited: root.fieldsChanged()
                }

                Label { text: qsTr("Port") }
                TextField {
                    id: portField
                    Layout.fillWidth: true
                    placeholderText: qsTr("8080")
                    inputMethodHints: Qt.ImhDigitsOnly
                    validator: IntValidator { bottom: 1; top: 65535 }
                    onTextEdited: root.fieldsChanged()
                }
            }

            CheckBox {
                id: authenticationCheck
                text: qsTr("Proxy requires authentication")
                onToggled: root.fieldsChanged()
            }

            GridLayout {
                Layout.fillWidth: true
                columns: 2
                columnSpacing: 12
                rowSpacing: 10
                visible: authenticationCheck.checked

                Label { text: qsTr("Username") }
                TextField {
                    id: usernameField
                    Layout.fillWidth: true
                    onTextEdited: root.fieldsChanged()
                }

                Label { text: qsTr("Password") }
                TextField {
                    id: passwordField
                    Layout.fillWidth: true
                    echoMode: showPasswordCheck.checked ? TextInput.Normal : TextInput.Password
                    onTextEdited: root.fieldsChanged()
                }

                Item { Layout.preferredWidth: 1; Layout.preferredHeight: 1 }
                CheckBox {
                    id: showPasswordCheck
                    text: qsTr("Show password")
                }
            }

            Frame {
                Layout.fillWidth: true
                padding: 14

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 10

                    RowLayout {
                        Layout.fillWidth: true

                        BusyIndicator {
                            visible: root.testState === "testing"
                            running: visible
                            Layout.preferredWidth: 28
                            Layout.preferredHeight: 28
                        }

                        Label {
                            Layout.fillWidth: true
                            text: root.statusMessage
                            wrapMode: Text.WordWrap
                            font.bold: root.testState === "success"
                            color: root.testState === "success"
                                   ? (root.stats.sslVerificationEnabled ? "#22c55e" : "#f59e0b")
                                 : root.testState === "sslWarning" ? "#f59e0b"
                                 : root.testState === "error" || root.testState === "invalid" ? "#ef4444"
                                 : palette.text
                        }
                    }

                    GridLayout {
                        Layout.fillWidth: true
                        columns: 2
                        columnSpacing: 24
                        rowSpacing: 7
                        visible: root.testState === "success"

                        Label { text: qsTr("Response time") }
                        Label { text: (root.stats.responseTimeMs || 0) + " ms"; font.bold: true }
                        Label { text: qsTr("Connection time") }
                        Label { text: (root.stats.connectionTimeMs || 0) + " ms"; font.bold: true }
                        Label { text: qsTr("Transfer speed") }
                        Label { text: Number(root.stats.connectionSpeedMbps || 0).toFixed(2) + " Mbps"; font.bold: true }
                        Label { text: qsTr("SSL status") }
                        Label { text: root.stats.sslStatus || qsTr("Unknown"); font.bold: true }
                        Label { text: qsTr("HTTP status") }
                        Label { text: root.stats.statusCode || "—"; font.bold: true }
                        Label { text: qsTr("Remote IP") }
                        Label { text: root.stats.remoteIp || "—"; font.bold: true }
                    }
                }
            }

            Item { Layout.fillHeight: true }

            RowLayout {
                Layout.fillWidth: true

                Button {
                    text: qsTr("Disable proxy")
                    onClicked: {
                        root.proxyDisabled()
                        root.close()
                    }
                }

                Item { Layout.fillWidth: true }

                Button {
                    visible: root.testState === "sslWarning"
                    text: qsTr("Ignore SSL and retry")
                    onClicked: root.startTest(false)
                }

                Button {
                    text: qsTr("Test again")
                    enabled: root.inputValid && root.testState !== "testing"
                    onClicked: root.startTest(true)
                }

                Button {
                    text: qsTr("Use proxy")
                    enabled: root.testState === "success"
                    highlighted: true
                    onClicked: {
                        root.proxyAccepted(root.proxyUrl, root.lastTestVerifiedSsl)
                        root.close()
                    }
                }
            }
        }
    }
}
