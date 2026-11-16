import QtQuick

// Session-only UI fixture. Replace this adapter when the dashboard backend is ready.
QtObject {
    id: root
    signal aboutToChange()
    readonly property bool isPreview: true
    readonly property bool available: true
    readonly property string availability: "ready"
    readonly property string availabilityError: ""
    readonly property string availabilityHelp: ""
    readonly property bool canManageComponents: false
    readonly property bool saving: false
    property bool premium: true
    readonly property bool mobileStorage: false
    readonly property var scanHistory: [
        {started: "2026-11-15T09:42:00Z", finished: "2026-11-15T09:42:18Z", status: "complete", trigger: "manual", discovered: 138, pages: 7, premium: true, error: ""},
        {started: "2026-11-14T18:20:00Z", finished: "2026-11-14T18:20:04Z", status: "incomplete", trigger: "startup", discovered: 60, pages: 3, premium: true, error: qsTr("A page could not be reached. Scan again to retry.")}
    ]
    readonly property string defaultQuality: "best"
    readonly property string defaultFolder: "Downloads/Porn Fetch"
    property var sources: []
    property bool active: true
    property int nextId: 10
    property string message: ""
    property var titles: [qsTr("An afternoon together"), qsTr("Behind the scenes"), qsTr("The weekend collection"),
        qsTr("A new chapter"), qsTr("From the studio"), qsTr("After hours"), qsTr("A little escape"),
        qsTr("The summer edit"), qsTr("Something special"), qsTr("One more take"), qsTr("A quiet evening"), qsTr("The latest session")]
    function makeVideos(count, offset) {
        var rows = []
        for (var i = 0; i < count; ++i) {
            var state = i < 3 ? "new" : i < 6 ? "pending" : i === 6 ? "paused" : i === 7 ? "failed" : "completed"
            rows.push({id: "v" + i, title: titles[(i + offset) % titles.length] + (i >= 12 ? " · " + (i + 1) : ""),
                status: state, progress: state === "completed" ? 100 : state === "paused" ? 46 : 0,
                duration: (12 + i % 31) + ":" + (i % 2 ? "24" : "08"), quality: i % 3 ? "1080p" : "2160p",
                published: i < 3 ? qsTr("Today") : qsTr("Earlier this month")})
        }
        return rows
    }
    function seed() {
        sources = [
            {id: "s1", name: "Luna Studio", initials: "LS", provider: "PornHub", kind: qsTr("Channel"), url: "https://www.pornhub.com/channels/luna-studio", scan: "complete", lastScan: qsTr("Today, 09:42"), startup: true, automatic: true, quality: "1080p", folder: "Downloads/Porn Fetch/Luna Studio", videos: makeVideos(138, 0)},
            {id: "s2", name: "Avery Rose", initials: "AR", provider: "Bellesa", kind: qsTr("Performer"), url: "https://www.bellesa.co/performers/avery-rose", scan: "scanning", lastScan: qsTr("Yesterday, 18:20"), startup: true, automatic: false, quality: qsTr("Best available"), folder: "Downloads/Porn Fetch/Avery Rose", videos: makeVideos(30, 2)},
            {id: "s3", name: "Weekend favourites", initials: "WF", provider: "RedGIFs", kind: qsTr("Collection"), url: "https://www.redgifs.com/users/demo/collections/weekend", scan: "complete", lastScan: qsTr("Today, 09:38"), startup: true, automatic: false, quality: "1080p", folder: "Downloads/Porn Fetch/Weekend", videos: makeVideos(24, 4)},
            {id: "s4", name: "Northlight", initials: "N", provider: "Tube8", kind: qsTr("Channel"), url: "https://www.tube8.com/channel/northlight/", scan: "incomplete", lastScan: qsTr("Today, 09:35"), startup: false, automatic: false, quality: "720p", folder: "Downloads/Porn Fetch/Northlight", videos: makeVideos(46, 6)}
        ]
    }
    Component.onCompleted: seed()
    function source(id) { return sources.find(function(s) { return s.id === id }) || null }
    function counts(source) {
        var result = {total: 0, newCount: 0, pending: 0, downloading: 0, paused: 0, failed: 0, completed: 0, ignored: 0}
        if (!source) return result
        source.videos.forEach(function(v) { result.total++; if (v.status === "new") result.newCount++; else result[v.status]++ })
        return result
    }
    function total(field) { return sources.reduce(function(n, s) { return n + root.counts(s)[field] }, 0) }
    function update(id, callback) {
        var copy = sources.slice()
        var index = copy.findIndex(function(s) { return s.id === id })
        if (index < 0) return
        var item = JSON.parse(JSON.stringify(copy[index]))
        callback(item)
        copy[index] = item
        aboutToChange()
        sources = copy
    }
    function scan(id) {
        update(id, function(s) {
            if (s.scan === "scanning") { s.scan = "stopped"; return }
            s.scan = "scanning"
        })
        message = qsTr("Preview scan updated. No website was contacted.")
    }
    function finishScan(id) {
        update(id, function(s) {
            s.scan = "complete"; s.lastScan = qsTr("Just now")
            var n = s.videos.length
            s.videos.unshift({id: "v" + n, title: qsTr("A new release") + " · " + (n + 1), status: s.automatic ? "pending" : "new", progress: 0, duration: "21:08", quality: s.quality, published: qsTr("Just now")})
        })
        message = qsTr("Preview scan finished. One sample video was added.")
    }
    function bulk(id, action) {
        update(id, function(s) {
            s.videos.forEach(function(v) {
                if (action === "download" && ["new", "pending", "paused"].indexOf(v.status) >= 0) v.status = "pending"
                if (action === "pause" && ["pending", "downloading"].indexOf(v.status) >= 0) v.status = "paused"
                if (action === "retry" && v.status === "failed") v.status = "pending"
            })
            if (action === "pause") s.downloadActive = false
            if (action === "download" || action === "retry") {
                s.downloadActive = true
                var first = s.videos.find(function(v) { return v.status === "pending" })
                if (first) { first.status = "downloading"; first.progress = Math.max(first.progress, 12) }
            }
        })
        message = action === "pause" ? qsTr("Sample downloads paused. Resume whenever you are ready.") : qsTr("Sample queue updated. No files are downloaded in this preview.")
    }
    function videoAction(id, videoId, action) {
        update(id, function(s) {
            var video = s.videos.find(function(v) { return v.id === videoId })
            if (!video) return
            video.status = action
            if (action === "downloading") s.downloadActive = true
            if (action === "downloading") video.progress = Math.max(video.progress, 12)
        })
        message = qsTr("Sample video updated.")
    }
    property Timer simulation: Timer {
        interval: 800
        repeat: true
        running: root.active && root.sources.some(function(s) { return s.downloadActive === true })
        onTriggered: {
            root.aboutToChange()
            root.sources = root.sources.map(function(source) {
                if (!source.downloadActive) return source
                var s = JSON.parse(JSON.stringify(source))
                var current = s.videos.find(function(v) { return v.status === "downloading" })
                if (current) {
                    current.progress = Math.min(100, current.progress + 8)
                    if (current.progress === 100) current.status = "completed"
                } else {
                    var next = s.videos.find(function(v) { return v.status === "pending" })
                    if (next) next.status = "downloading"
                    else s.downloadActive = false
                }
                return s
            })
        }
    }
    function save(id, values) {
        if (id) update(id, function(s) { Object.keys(values).forEach(function(k) { s[k] = values[k] }) })
        else {
            var item = Object.assign({id: "s" + nextId++, scan: "scanning", lastScan: qsTr("Not scanned yet"), videos: []}, values)
            item.initials = item.name.split(/\s+/).map(function(p) { return p[0] }).slice(0, 2).join("").toUpperCase()
            sources = sources.concat([item])
        }
        message = qsTr("Saved for this preview session.")
    }
    function remove(id) { sources = sources.filter(function(s) { return s.id !== id }); message = qsTr("Subscription removed from the preview.") }
}
