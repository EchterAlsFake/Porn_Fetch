import QtQml

QtObject {
    objectName: "websiteSupportData"
    readonly property var headers: [qsTr("Website"), qsTr("Videos"), qsTr("Profiles/channels"),
        qsTr("Playlists/collections"), qsTr("Shorts"), qsTr("Search"), qsTr("Login"), qsTr("Photo albums")]
    // Capability cells match the end-user table in docs/WEBSITES.md.
    readonly property var sites: [
        { provider: "pornhub", name: "PornHub",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("Yes"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("Yes"), qsTr("Yes")] },
        { provider: "eporner", name: "Eporner",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")] },
        { provider: "xnxx", name: "XNXX",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")] },
        { provider: "xvideos", name: "XVideos",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("Yes"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("Yes"), qsTr("—")] },
        { provider: "xhamster", name: "XHamster",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("Account only"), qsTr("Yes"), qsTr("—"), qsTr("Yes"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("Account only"), qsTr("Yes"), qsTr("—"), qsTr("Yes"), qsTr("—")] },
        { provider: "spankbang", name: "SpankBang",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")] },
        { provider: "youporn", name: "YouPorn",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")] },
        { provider: "beeg", name: "Beeg",
          gui: [qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")] },
        { provider: "porntrex", name: "Porntrex",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")] },
        { provider: "xfreehd", name: "XFreeHD",
          gui: [qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("Yes")] },
        { provider: "redtube", name: "RedTube",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")] },
        { provider: "thumbzilla", name: "Thumbzilla",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")] },
        { provider: "tube8", name: "Tube8",
          gui: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")],
          cli: [qsTr("Yes"), qsTr("Yes"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—"), qsTr("—")] }
    ]
    readonly property var notes: [
        qsTr("Supported in Porn Fetch 3.9. Yes = supported; — = unavailable."),
        qsTr("Paste a full video, profile, or playlist URL. Supported profile types vary by website."),
        qsTr("Keyword search is unavailable for legal reasons."),
        qsTr("Photo albums are CLI-only."),
        qsTr("Availability and quality depend on the video, your region, and any required website account. Free downloads are limited to 720p; higher qualities require a Porn Fetch license. Some YouPorn MP4-only videos also require a license because their resolution is unknown."),
        qsTr("HQporner, MissAV, and unlisted websites are not supported.")
    ]

    function rowFor(site, terminal) {
        return [site.name].concat(terminal ? site.cli : site.gui)
    }
}
