import QtQuick

// Match the reviewed UI adapter while fetching only the visible video page.
QtObject {
    id: root
    property var bridge
    readonly property bool isPreview: false
    readonly property bool available: bridge && bridge.available
    readonly property string availability: bridge ? bridge.availability : "checking"
    readonly property string availabilityError: bridge ? bridge.availabilityError : ""
    readonly property string availabilityHelp: bridge ? bridge.availabilityHelp : ""
    readonly property bool canManageComponents: bridge && bridge.canManageComponents
    readonly property bool transferBusy: bridge && bridge.transferBusy
    readonly property bool integrityPaused: bridge && bridge.integrityPaused
    readonly property bool integrityBusy: bridge && bridge.integrityBusy
    readonly property string integrityMessage: bridge ? bridge.integrityMessage : ""
    readonly property int integrityDone: bridge ? bridge.integrityDone : 0
    readonly property int integrityTotal: bridge ? bridge.integrityTotal : 0
    readonly property int integrityIssues: bridge ? bridge.integrityIssues : 0
    readonly property bool saving: bridge && bridge.saving
    readonly property bool premium: bridge && bridge.premium
    readonly property var sources: bridge ? bridge.sources : []
    readonly property var videos: bridge ? bridge.videos : []
    readonly property var scanHistory: bridge ? bridge.scanHistory : []
    readonly property bool mobileStorage: bridge && bridge.mobileStorage
    readonly property int videoTotal: bridge ? bridge.videoTotal : 0
    readonly property string message: bridge ? bridge.message : ""
    readonly property string defaultQuality: bridge ? bridge.defaultQuality : "best"
    readonly property string defaultFolder: bridge ? bridge.defaultFolder : ""
    signal aboutToChange()
    signal saveFinished(string id, string error)
    property Connections updates: Connections {
        target: root.bridge
        function onAboutToChange() { root.aboutToChange() }
        function onSaveFinished(id, error) { root.saveFinished(id, error) }
    }
    function source(id) { return sources.find(function(s) { return s.id === id }) || null }
    function counts(source) { return source ? source.counts : {total: 0, newCount: 0, pending: 0, downloading: 0, paused: 0, failed: 0, completed: 0, ignored: 0} }
    function total(field) { return sources.reduce(function(n, s) { return n + (root.counts(s)[field] || 0) }, 0) }
    function select(id, filter, page) { if (bridge) bridge.select(id, filter, page) }
    function providerForUrl(url) { return bridge ? bridge.providerForUrl(url) : "" }
    function scan(id) { bridge.scan(id) }
    function bulk(id, action) { bridge.bulk(id, action) }
    function videoAction(id, member, action) { bridge.videoAction(id, member, action) }
    function save(id, values) { bridge.save(id, values) }
    function remove(id) { bridge.remove(id) }
    function fullVerification() { if (bridge) bridge.fullVerification() }
    function checkIntegrity() { if (bridge) bridge.checkIntegrity() }
    function checkAvailability() { if (bridge) bridge.checkAvailability() }
    function manageComponents() { if (bridge) bridge.manageComponents() }
}
