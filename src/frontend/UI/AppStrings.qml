import QtQuick
pragma Singleton

// Shared, plain-language explanations for settings.
QtObject {
    readonly property string libraryExportHelp:
        qsTr("Jellyfin is a media server that organizes videos and lets you watch them through its apps or a browser. Porn Fetch can save a description file (.nfo), a portable metadata record (.json) and an available cover image beside each completed video. Metadata means details such as title, performers, tags and dates.\n\nChoose Export for Jellyfin to do this for new downloads. You can use these files without connecting Porn Fetch to a server: add their folder to a Jellyfin Movies library and scan it. An API key is only needed for automatic notifications. Export requires Premium; unknown details stay empty.")

    readonly property string libraryLayoutHelp:
        qsTr("Sidecars are companion files stored beside a video. Sidecars beside each video keeps your normal download layout and gives each video its own named metadata files.\n\nOne folder per new video groups the video, metadata and cover together, using a source ID to distinguish videos with the same title. This is a convenient starting choice for Jellyfin. Existing videos are not moved or renamed. Keep companion files with the video when copying it to another computer.")

    readonly property string libraryGenresHelp:
        qsTr("Copy the website's video categories into Jellyfin's Genres field so you can browse or filter by them. Source tags are exported separately.\n\nCategories differ between websites. This does not invent categories when the source supplies none.")

    readonly property string libraryStudiosHelp:
        qsTr("Normally, the Studio field only uses an explicit producer credit. A website uploader or channel is not automatically the studio that made the video.\n\nEnable this if you want credited content providers, publishers and channels to appear as studios too. These credits may describe who published the video rather than who produced it. Leave this off if you want to keep that distinction. Review the Exported studio value in the metadata preview.")

    readonly property string jellyfinServerHelp:
        qsTr("The address where Porn Fetch can contact your Jellyfin server. If both programs run on this computer, this is often http://localhost:8096. For a different computer, use its reachable server address.\n\nLeave this blank to export metadata without sending notifications. A notification tells Jellyfin that a completed file is ready to scan; it does not upload or copy the video, poster or metadata files. Jellyfin must already be able to read their folder. For a remote server, arrange shared storage or copy the complete video folder yourself. All app traffic Tor mode also applies to these requests.")

    readonly property string jellyfinLocalRootHelp:
        qsTr("The media folder as Porn Fetch sees it. Choose the shared parent folder containing the videos you want Jellyfin to scan, not an individual video.\n\nFor example, Porn Fetch may save videos under /home/user/Videos while Jellyfin in Docker sees the same files under /media. Enter /home/user/Videos here. This setting translates paths for notifications; it does not share a folder or transfer files.")

    readonly property string jellyfinServerRootHelp:
        qsTr("The same media folder as Jellyfin sees it. This may differ from the path on the computer running Porn Fetch.\n\nFor example, if Docker mounts your /home/user/Videos folder at /media, enter /media here and use /media when adding the Jellyfin library. A video at /home/user/Videos/example/video.mp4 is then announced as /media/example/video.mp4. Both paths must refer to the same files. For native installations on the same computer, the two roots may be identical.")

    readonly property string jellyfinApiKeyHelp:
        qsTr("An API key is a secret credential that lets Porn Fetch send requests to your Jellyfin server without asking you to log in for every notification. Porn Fetch uses it to tell Jellyfin about completed files so the server can scan them.\n\nCreate a key in Jellyfin's administrator Dashboard under Advanced → API Keys; menu names can vary by version. Give it a recognizable name such as Porn Fetch, copy it here and choose Save API key. This is a Jellyfin key, not your Porn Fetch Premium key or your Jellyfin account password.\n\nKeep it private: it can grant broad access to your server. You can revoke it in Jellyfin. You do not need a key for exporting files or scanning the library manually.")

    readonly property string jellyfinSaveKeyHelp:
        qsTr("Save the entered Jellyfin API key on this computer for future notifications. It is stored separately from settings and is not included in exported metadata. The input is cleared after saving; that does not remove the saved key.\n\nTo remove the stored key, leave the input blank and press Save API key. Removing this local copy does not revoke the key in Jellyfin; revoke it through Jellyfin's dashboard if needed.")

    readonly property string libraryExistingFileHelp:
        qsTr("Choose a completed video that is already on your computer. This feature adds or rebuilds the companion metadata and artwork files used to describe it in Jellyfin.\n\nIt can help when an older download has no metadata or a generated companion file is missing. It does not repair a broken video, recover missing video segments, improve quality or download the video again. Use the original source URL if no saved Porn Fetch JSON record is available.")

    readonly property string libraryChooseFileHelp:
        qsTr("Open the file picker and select the existing video you want to describe. Choose the video file itself, not its .nfo, .json or poster file. The video stays in its current location.")

    readonly property string librarySourceUrlHelp:
        qsTr("The original video page on the source website, for example the same URL you used to download it. This is not a Jellyfin address or a temporary streaming link.\n\nWith a URL, Porn Fetch requests the video's currently available metadata from that website. Leave this blank when a matching Porn Fetch JSON record is saved beside the video; that record can rebuild metadata without contacting the source website. Deleted source pages can only be recovered from information you already saved. Missing source fields are not guessed.")

    readonly property string libraryPreviewHelp:
        qsTr("Read the available information and show it for review before writing companion files. With a source URL, this can contact the original website; with saved Porn Fetch JSON, it can work offline.\n\nCheck the title, performers and the distinction between uploader, channel, publisher and producer. Not supplied means the information is unavailable. Preview does not write export files or transfer the video. Turn off Anonymous Mode to view this information.")

    readonly property string libraryWriteHelp:
        qsTr("Write the metadata you previewed beside the existing video, together with available artwork. The video itself is not changed or downloaded again. Existing or manually edited metadata and artwork are preserved by default.\n\nIf the optional Jellyfin connection is configured, Porn Fetch also sends a scan notification after saving. That notification does not transfer any files. Without a connection, scan the library manually. A successful export cannot add details the website or saved JSON did not supply.")

    readonly property string libraryRetryHelp:
        qsTr("Try failed exports or Jellyfin notifications again for completed downloads remembered during this app session. The video is not downloaded again.\n\nIf Jellyfin was offline, start it and retry. If a folder, API key or path mapping was wrong, correct it first. A notification failure does not undo the saved video or metadata.\n\nAfter restarting Porn Fetch, use Export or repair an existing video to rebuild metadata from saved JSON or the original source URL. This button does not search your library for broken videos.")

    readonly property string cleanupOnStopHelp:
        qsTr("When you stop a download, delete its unfinished video parts and temporary files. This frees storage space.\n\nIf you start that video again, it must download from the beginning. Leave this off if you want to keep progress for resuming.")

    readonly property string videoQualityHelp:
        qsTr("Choose the video quality to try first. Higher quality usually needs more storage space and takes longer to download.\n\nIf the website does not offer that quality, Porn Fetch chooses an available quality. Free use supports qualities up to 720p. An active premium license unlocks higher qualities. The quality cannot be higher than the source video.")

    readonly property string modelVideosHelp:
        qsTr("This setting applies to PornHub model pages.\n\nUploaded: videos posted by the model's own account.\nFeatured: videos from other accounts that include the model.\nBoth: include both groups.")

    readonly property string contentLanguageHelp:
        qsTr("Choose the language to request from supported websites, including translated video titles when available.\n\nNot every website provides translated titles. This does not change the language of Porn Fetch's interface.")

    readonly property string resultLimitHelp:
        qsTr("Set the maximum number of videos to load from a profile, channel or playlist.\n\nFor example, a limit of 50 loads up to 50 videos, even if the page has more. A smaller limit makes large lists quicker to load. Without an active premium license, public model, channel and playlist URLs show only their first 5 videos. Account collections are exempt from that preview limit.")

    readonly property string strictEnforcementHelp:
        qsTr("Prefer the website's page text when loading information in your selected content language. This avoids API responses that may return titles in a different language.\n\nLoading can be slower. Websites without support for this may still return English titles. This setting does not control video quality.")

    readonly property string writeMetadataHelp:
        qsTr("Save details such as the title, author, publication date and cover image inside the downloaded MP4 file, when available. Some media players can show these details.\n\nThis needs FFmpeg and MP4 conversion. It does not change the video quality.")

    readonly property string skipExistingFilesHelp:
        qsTr("Skip a download if a file already exists at its final output path. This helps avoid downloading the same file again.\n\nPorn Fetch checks the filename, not the video's contents. When this setting is off, an existing file may be replaced.")

    readonly property string trackVideosHelp:
        qsTr("Keep a local record of downloads for the desktop History and Statistics pages. Porn Fetch uses PocketBase, a small local database service, while the app is running.\n\nTurn this off if you do not want download history. It does not delete existing history or downloaded files. History and statistics are unavailable on Android and iOS.")

    readonly property string parallelDownloadsHelp:
        qsTr("Set how many videos can download at the same time. Extra videos wait in the queue.\n\nStart with a small number. More downloads share your connection and may cause timeouts or website limits. Parallel downloads require a premium license.")

    readonly property string networkDelayHelp:
        qsTr("Wait this many seconds before each website request.\n\nA longer wait makes loading slower but reduces how often Porn Fetch contacts a website. It can help when a website limits frequent requests.")

    readonly property string videosConcurrencyHelp:
        qsTr("Set how many videos Porn Fetch can load information for at once, such as titles, available qualities and video links.\n\nThis affects preparing the list, not how many videos download at once. Lower it if loading causes timeouts or website errors.")

    readonly property string pagesConcurrencyHelp:
        qsTr("Set how many pages of a profile, channel or playlist can be read at once.\n\nHigher values can load large lists faster, but send more requests to the website. Lower this if you see timeouts or request-limit errors.")

    readonly property string downloadWorkersHelp:
        qsTr("Set how many parts of one video can be fetched at once. Many streaming videos are split into small pieces; some direct downloads also support parallel parts.\n\nMore workers may help on a fast connection, but too many can cause errors. This is separate from the number of videos downloading at once.")

    readonly property string timeoutHelp:
        qsTr("Set how many seconds a network request can wait before it is treated as a timeout.\n\nIncrease this if your connection or the website is slow. Failed requests may be tried again, depending on the retry settings. A longer timeout also means waiting longer before an error appears.")

    readonly property string retriesHelp:
        qsTr("Control how many attempts Porn Fetch allows for failed requests and download transfers. Temporary failures, such as timeouts, can be tried again.\n\nMore attempts may help with an unstable connection, but make repeated failures take longer. They will not fix an invalid link or a website that denies access.")

    readonly property string speedLimitHelp:
        qsTr("Limit download speed in megabytes per second (MB/s). Set 0 for no limit.\n\nFor example, 2 means about 2 megabytes per second. This can leave bandwidth for other apps. The limit may vary with the download method and simultaneous transfers; it is not a strict cap for every request.")

    readonly property string processingDelay:
        qsTr("Wait this many seconds before adding each prepared video to the list and before starting a download. Set 0 for no extra wait.\n\nUse a small delay if you want Porn Fetch to process videos more slowly.")

    readonly property string updateChecks:
        qsTr("Check for new versions automatically when Porn Fetch starts. Leave this on to hear about fixes and improvements. You can also check manually.\n\nInstalled desktop copies use Qt Maintenance Tool to install updates. Portable desktop and source copies need to be updated manually. Android uses its own update installer.\n\nChecks contact the Porn Fetch update service. Your selected Tor routing also applies to these requests.")

    readonly property string supressErrors:
        qsTr("Reduce repeated error announcements. Errors still appear in download status and Recent activity, where you can read the details.\n\nThis does not stop downloads from reporting failures, and it does not change whether error reports are sent.")

    readonly property string systemNotificationsHelp:
        qsTr("Show a system notification when a download finishes or fails while Porn Fetch is inactive. Notifications use generic text rather than video titles.\n\nThis is off by default. Your device must allow notifications. It does not keep downloads running after the operating system stops the app. Messages also remain in Recent activity.")

    readonly property string trustEnvironmentHelp:
        qsTr("Allow networking settings from environment variables to affect Porn Fetch, for example a proxy configured outside the app. Environment variables are settings passed to an app when it starts.\n\nLeave this off unless you use such a setup. Those settings may change how requests are routed.")

    readonly property string debugModeHelp:
        qsTr("Write detailed diagnostic logs to help investigate a problem. These can include website requests and the steps Porn Fetch takes while loading or downloading.\n\nLeave this off for normal use. It can slow the app and create large log files. Logs may contain sensitive URLs or other information; review them before sharing.")

    readonly property string logLevel:
        qsTr("Choose how much detail normal logs contain.\n\nDEBUG: the most detail, useful for troubleshooting.\nINFO: general activity and important events.\nWARNING: possible problems.\nERROR: failed operations.\nCRITICAL: the most serious errors only.\n\nChoosing a quieter level hides log messages; it does not fix or prevent errors.")

    readonly property string interfaceHelp:
        qsTr("Choose the network connection used for website requests. Leave this empty to let your operating system choose.\n\nOn Linux, enter an interface name such as wlan0 or eth0. On Windows, enter the local IP address of the adapter, not its name. macOS support has not been verified.\n\nThis is an advanced setting. An incorrect value can stop connections. Proxies can change how it is applied, and All app traffic through Tor overrides it.")

    readonly property string httpVersionHelp:
        qsTr("Choose the HTTP version used to communicate with websites. HTTP is the protocol for sending web requests.\n\nv1: HTTP/1.1.\nv2: HTTP/2, the default.\nv3: HTTP/3, which needs support from the website and network.\n\nKeep v2 unless you are troubleshooting. SNI obfuscation and All app traffic through Tor use HTTP/2 over TCP, even if you select v3.")

    readonly property string impersonationHelp:
        qsTr("Choose the browser connection profile Porn Fetch uses for website requests, for example chrome. This makes the connection resemble one from that browser. It does not open or install a browser.\n\nKeep the default unless you are troubleshooting a website connection. Changing the profile does not guarantee access to a blocked site.")

    readonly property string customJA3Help:
        qsTr("Override the TLS connection fingerprint with a custom JA3 value. A fingerprint describes some of the options sent when starting an encrypted connection. Websites may use it to recognize client software.\n\nLeave this empty to use the browser profile above. Use a custom value only if you understand JA3 and are troubleshooting; an incorrect value can break connections.")

    readonly property string anonymousModeHelp:
        qsTr("Hide sensitive titles, author names and other private details in the interface. Some pages are also hidden.\n\nThis helps when someone can see your screen. It does not make your network connection anonymous or hide saved files from other people using your device.")

    readonly property string encryptedCHHelp:
        qsTr("Try to encrypt the website name sent at the start of an HTTPS connection. This feature is called Encrypted Client Hello (ECH).\n\nIt needs support from the website and the network setup. Leave it off if enabling it causes connection errors. It does not hide the destination IP address or make your traffic anonymous.")

    readonly property string dnsOverHTTPSHelp:
        qsTr("DNS looks up a website's IP address from its name. DNS over HTTPS encrypts those lookup requests between Porn Fetch and the DNS service you choose.\n\nThe DNS service can still see the names you look up. Other parts of the connection can also reveal the website, so this alone does not make browsing anonymous.\n\nUse a DNS-over-HTTPS service you trust. All app traffic through Tor uses Tor's name lookup instead.")

    readonly property string dnsPrimaryHelp:
        qsTr("Enter the HTTPS address of the DNS service to use, for example https://dns.mullvad.net/dns-query.\n\nUse the provider's DNS-over-HTTPS address, not its homepage or a plain IP address. This setting is used when DNS over HTTPS is enabled.")

    readonly property string fallbackDNSHelp:
        qsTr("Enter a second DNS-over-HTTPS service to try if the first service fails. Use its full HTTPS lookup address.\n\nChoose a service you trust, because it can receive your website-name lookups too.")

    readonly property string sniObfuscationHelp:
        qsTr("Restart Porn Fetch after changing SNI obfuscation, its mode or its profile.\n\nSNI is the website name normally sent at the start of an HTTPS connection. Porn Fetch can split this part of the connection into smaller pieces, which may help on some restricted networks.\n\nLite mode\nSplits the data into separate writes. It needs no administrator rights. Your operating system or network may combine those pieces again.\n\nStrict mode\nSplits actual outgoing TCP packets. It needs root on Linux or Run as Administrator on Windows. Strict mode supports Windows x64 and Linux x64/ARM64; Linux also needs a compatible kernel and libbpf. It is unavailable on macOS and Windows ARM64.\n\nStrict profiles\nFragmentation: send the pieces in order.\nReverse: send the later piece first; the server puts them back in order.\nDesync: first send a fake greeting intended to confuse some inspection systems, then send the real pieces in reverse order.\n\nImportant limits\nThis changes only Porn Fetch's connections. It uses HTTP/2 over TCP, not HTTP/3. If you have another proxy configured, the local SNI proxy connects through it.\n\nSplitting is not encryption. An observer can put the pieces back together and read the website name. DNS lookups and destination IP addresses may also reveal it. This is not a VPN and does not guarantee anonymity or access.\n\nFor Linux source runs that need Strict mode, use sudo -E .venv/bin/python main.py to retain your environment. Depending on your sudo setup, a plain sudo launch may use root's separate settings.")

    readonly property string torIntegrationHelp:
        qsTr("Tor sends requests through several relays before they reach the destination. Porn Fetch starts its bundled Tor client when needed.\n\nOff: use your normal connection.\nUpdates + licensing: send only update and license requests through the Porn Fetch onion service. Website requests and video downloads keep their normal route.\nAll app traffic: also send website requests and video downloads through Tor.\n\nIf Tor cannot connect, requests assigned to Tor fail rather than switching to a direct connection. All app traffic overrides the custom proxy, network interface, DNS-over-HTTPS and HTTP/3 settings for Internet requests. Local app services stay on your device.\n\nLinks opened in your browser use that browser's connection settings. Tor does not guarantee anonymity or safety.")

    readonly property string torAllTrafficNotice:
        qsTr("Only use Tor for video downloads when you need it to reach websites on a restricted network. Large downloads use substantial bandwidth and slow the Tor network for other people.\n\nThis setting routes Porn Fetch's Internet requests through Tor. It does not route other apps or links opened in your browser, and it does not guarantee anonymity or safety.")

    readonly property string proxySetupHelp:
        qsTr("A proxy forwards requests to websites for you. It affects Porn Fetch, not every app on your device.\n\nEnter the address and port from your proxy provider. Add a username and password only if the provider requires them, then test the connection.\n\nUse a provider you trust. A proxy can see connection information and does not automatically make you anonymous. All app traffic through Tor overrides this setting.")

    readonly property string guiLanguageHelp:
        qsTr("Porn Fetch is currently English-only. The translation files and translation service are unfinished, so this control is disabled.\n\nThe content-language setting is separate: it requests translated titles from supported websites.")

    readonly property string fontSizeHelp:
        qsTr("Choose the text size used in the interface. A larger value makes text easier to read but leaves less room for controls.\n\nLong help messages and settings pages can be scrolled.")

    readonly property string appStyleHelp:
        qsTr("Choose the appearance of buttons, menus and other controls.\n\nMaterial: an Android-style appearance.\nFusion: a traditional desktop appearance.\nUniversal: a Windows-style appearance.\nWindows: platform-specific Windows controls, where supported.\n\nRestart Porn Fetch after changing the style. It does not change how downloads work.")

    readonly property string darkModeHelp:
        qsTr("Use a dark background and light text. Turn this off for a light background and dark text.\n\nHigh contrast can override these colours when enabled.")

    readonly property string accentColorHelp:
        qsTr("Choose the colour used for selected controls, highlights and other interface details.\n\nThis changes the appearance only. High contrast can override the accent colour.")

    readonly property string responseCacheSizeHelp:
        qsTr("Set how much memory can hold recently received website information, in megabytes (MB). Reusing it can reduce repeated requests.\n\nThis is storage capacity, not download speed. Larger caches use more memory; they do not increase video quality.")

    readonly property string responseCacheTTLHelp:
        qsTr("Set how many seconds cached website information stays valid. TTL means time to live.\n\nA longer time can reduce repeated requests, but information may stay out of date for longer. This is separate from download history.")

    readonly property string segmentCacheSizeHelp:
        qsTr("Set how much memory can hold recently prepared lists of video segments, in megabytes (MB). These lists tell Porn Fetch where to find the small pieces of a streaming video.\n\nThis is separate from partial-download files saved on disk. Increasing it uses more memory.")

    readonly property string segmentCacheTTLHelp:
        qsTr("Set how many seconds a cached list of video segments stays valid. TTL means time to live.\n\nThis does not set how long a paused download can be resumed. Partial-download files on disk are handled separately.")

    readonly property string retryInitialDelayHelp:
        qsTr("Set the starting wait, in seconds, before trying a failed website request again.\n\nFor example, 1 starts with a wait of about one second. The multiplier and random extra delay can increase later waits.")

    readonly property string retryMaxDelayHelp:
        qsTr("Set the maximum wait used by the automatic retry backoff, in seconds. Backoff means waiting longer after repeated failures.\n\nThis limits the wait between attempts, not how long a request itself can run; use Timeout for that.")

    readonly property string retryMultiplierHelp:
        qsTr("Control how quickly retry waits grow after repeated failures.\n\nA larger multiplier increases the waits faster, giving the website more time before another attempt. Keep the default unless you need to tune retry behaviour.")

    readonly property string retryJitterHelp:
        qsTr("Add a random extra wait before retrying, measured in seconds. This helps avoid sending many retries at exactly the same time.\n\nFor example, 0.5 allows up to half a second of extra delay. Set 0 for no random extra wait.")

    readonly property string titleFormattingHelp:
        qsTr("Name your downloaded files using these placeholders:\n\n$title: video title\n$video_id: video ID\n$author: author or channel\n$index: position in the fetched list, such as 01 or 02\n$publish_date: publication date, if available\n$length: duration in minutes, if available\n$output_path: your output folder\n\nExamples\n$author/$index - $title\n${title}_$video_id\n\nLeave the field empty for the default filename. Relative paths are saved inside your output folder. A / in the template can create subfolders. Use $$ to include a dollar sign.\n\nDates use YYYY-MM-DD. Missing dates or durations become unknown. Other placeholders and custom date formats are not supported.\n\nCharacters that cannot be used safely in a filename are replaced. The original title stays visible in the app and is still used for filtering. Add $index or $video_id to help keep filenames unique.")

    readonly property string onionRoutingHelp: torIntegrationHelp
}
