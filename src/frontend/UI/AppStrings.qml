import QtQuick
pragma Singleton


// Contains basically the texts for the QML app so that they are in a unified place
QtObject {
    readonly property string videoQualityHelp:
        qsTr("The Video quality that you apply here is the preference meaning all videos fetched will try to be downloaded in the specified quality.
        If the quality is not available the next 'best' quality will be picked.
        IMPORTANT: https://eporner.com does not support downloading >720p even for paid users. This is a website restriction!")

    readonly property string modelVideosHelp:
        qsTr("Affects only PornHub! A Pornstar may have his own uploaded videos on his PornHub Account but also be featured in other videos from
        different Channels. With this setting you can control whether model videos will include both, only uploaded or only featured videos.")

    readonly property string contentLanguageHelp:
        qsTr("This setting affects the language of the website itself. E.g., if you set this to french then all video titles will be auto-translated to French by PornHub")

    readonly property string resultLimitHelp:
        qsTr("This setting affects how many videos will be loaded into the list view down below. For example if you want to get the videos
        from a channel and the result limit is 50, then only 50 videos will be fetched, even if the channel has 100 videos.")

    readonly property string strictEnforcementHelp:
        qsTr("This (unfortunately) disables API data fetching and it will be a bit slower. Sites that do not support HTML scraping yet like beeg.com will
        fallback to English titles. ")

    readonly property string writeMetadataHelp:
        qsTr("After downloading the video Porn Fetch will write the title, thumbnail, publish date and author directly into the MP4 container.
        This can help organizing files and is a feature for advanced users. Requires remuxing to be enabled!")

    readonly property string skipExistingFilesHelp:
        qsTr("If enabled Porn Fetch will skip downloading already existing files otherwise the files will be replaced.")

    readonly property string trackVideosHelp:
        qsTr("This feature will track videos in a SQLite Database. This feature is absolutely for advanced users. If you don't know
        what an SQLite database is, then you absolutely don't need to enable this.

        For Advanced Users see: https:// #TODO
        ")

    readonly property string parallelDownloadsHelp:
        qsTr("This setting defines how many videos can be downloaded at the same time. Please do not raise this to a high number (5+).
        This will make downloads unstable and timeout more frequently and the website may block your IP!")

    readonly property string networkDelayHelp:
        qsTr("How many seconds to wait before each network requests.")

    readonly property string videosConcurrencyHelp:
        qsTr("How many videos to scrape at the same time from the webpage and load its HTML / API data and process the page.")

    readonly property string pagesConcurrencyHelp:
        qsTr("How many pages to scrape at the same time")

    readonly property string downloadWorkersHelp:
        qsTr("How many network requests at the same time to fetch an HLS Segment (1 Worker = ~2-5 MB)")

    readonly property string timeoutHelp:
        qsTr("The maximum time to wait for a response from a website. If you have a bad internet connection higher values like
        30 seconds can help a lot. Please note that Porn Fetch will retry a request if it fails due to a timeout!")

    readonly property string retriesHelp:
        qsTr("The limit for retrying a failed network request e.g., a timeout.")

    readonly property string speedLimitHelp:
        qsTr("The Global Speed Limit for Porn Fetch in Megabyte/s. I have tried implementing this in a good way, but there could
        still be edge cases especially when using parallel downloads where the speed limit is NOT applied.")

    readonly property string processingDelay:
        qsTr("In seconds how many seconds to wait before processing each video into the List View AND before starting a new download.
        I don't know why you would want to use this, but here you go.")

    readonly property string updateChecks:
        qsTr("Whether to enable automated update checks. It is HIGHLY recommended to TURN THIS ON. Update checking uses my own server
        which is hosted offshore in Sweden. The entire source code is open-source. Your IP address is NOT logged nor stored.

        Tor: If you enable Tor in Porn Fetch, the .onion domain of my server will be used (also hosted in Sweden).
        See: https://github.com/EchterAlsFake/Server for the full source code.

        For macOS Users the Sparkle Framework will be used for update checking. Sparkle does not support the Tor domain.
        ")

    readonly property string supressErrors:
        qsTr("This will basically skip all errors, you will not be notified about anything and if nothing works you will not know why.
        Why did I make this setting? I absolutely don't remember. I think it was from a GitHub issue where someone requested it lol")

    readonly property string enableLoggingHelp:
        qsTr("
Please read extensively before enabling this!

The integrated logging will log all of your errors to my offshore server in Sweden. I have configured this so that most sensitive
data should be stripped.

If that happens I will instantly delete your data.

For Proof:
The Server is fully Open-Source. See: https://github.com/EchterAlsFake/Server
")

    readonly property string trustEnvironmentHelp:
        qsTr("
If you enable ths, Porn Fetch will trust your local Proxy options and other advanced configuration
that have been applied through environment variables.

This is not recommended to turn on, unless you have a specific reason to.
")

    readonly property string debugModeHelp:
        qsTr("
Please only enable the debug mode if you have opened an issue on GitHub and I told you to enable it!

The debug mode will essentially print out anything that Porn Fetch does. Each individual network request, each
processing step and create log files on your computer for all seperate API modules that Porn Fetch uses aswell as for the
main application.

Those log files can instantly pin-point to me what went wrong, but they create unnecessary bloat on your PC and slow things down.
Please only enable if you are a developer and you have an actual reason to do so.")

    readonly property string logLevel:
        qsTr("This defines the internal logging level of Porn Fetch.")

    readonly property string interfaceHelp:
        qsTr("
Warning: This setting can conflict with the SNI Proxy, an own proxy set and the Tor routing and those edge cases have
not been tested. Please keep that in mind when binding to an interface!

Windows:
Enter the IP address of the network interface you want to bind Porn Fetch's network traffic too. Do not use the name
of your physical adapters. This is not supported.

Linux:
Enter the interface name e.g., 'wlan0' or 'eth0'. Use commands like 'iwconfig' or 'ifconfig' to find it out.

macOS:
I have no idea if this works
")

    readonly property string httpVersionHelp:
        qsTr("
Available options: v3, v2, v1

Ask ChatGPT what this is and if you need to change this or not.

The SNI Fragmentation Proxy is not compatible with HTTP/3!
If you enable HTTP/3, SNI will automatically be disabled!")

    readonly property string impersonationHelp:
        qsTr("This defines the browser profile that Porn Fetch tries to emulate in order to
send regular and correct TLS headers.

See: https://curl-cffi.readthedocs.io/en/v0.6.1/impersonate.html
")

    readonly property string customJA3Help:
        qsTr("This topic is so complex not even I can tell you anything.
So you might just want to read: https://medium.com/cu-cyber/impersonating-ja3-fingerprints-b9f555880e42")

    readonly property string anonymousModeHelp:
        qsTr("
This will basically hide sensitive video titles, author names and sensitive text in general in Porn Fetch.
If someone looks over your shoulder while you use this app they will not be able to see you are using
a Porn Downloader right now.
")

    readonly property string encryptedCHHelp:
        qsTr("
This will enable encrypted Client Hello packets. Basically, when you reach out to a website there's a little packet
called SNI (Server Name Identification). This contains the entire server name you are trying to reach e.g.,
pornhub.com. Your Internet Service Provider or anyone in between your connection can see this.

You probably want to hide it and that is what encrypted Client Hello does. However, basically NO site on the Internet
except sites for cloudflare support this yet. If a site doesn't support it, it breaks the entire connection.
This is for future proofing!

However, my web-server (if you enable update checks / logging) actually DOES support it and will use it.
")

    readonly property string dnsOverHTTPSHelp:
        qsTr("
A (D)omain (N)ame (S)erver is a service that basically translates a URL like https://pornhub.com to its IP address.
Usually a DNS server is not encrypted. So your internet provider can actually see the domains you are visiting.
They can't see the exact video, but they can see pornhub.com. With a DNS over HTTPS this is encrypted and they can't see it.
I highly recommend turning this on.

Porn Fetch by default uses a Mullvad DNS Server. Mullvad has a decade long reputation for zero logging policies and strict anonymity.
However, you can also enter your own DNS.
       ")

    readonly property string dnsPrimaryHelp:
        qsTr("This DNS Server will be the primary one used for connecting.")

    readonly property string fallbackDNSHelp:
        qsTr("
If DNS acts like Deutsche Bahn and the packets don't arrive, this will be used as a fallback.")

    readonly property string sniObfuscationHelp:
        qsTr("
What SNI reveals

Server Name Indication, or SNI, is a field inside the TLS ClientHello. It usually contains the hostname Porn Fetch is
connecting to and is normally visible before the encrypted HTTPS session begins. A network provider or other observer
may therefore learn the hostname even though the later request and response are encrypted.

What this feature does

Porn Fetch sends its own HTTP/2-over-TCP connections through a local loopback proxy. The proxy divides the TLS
ClientHello inside the SNI hostname so the complete name is not present in one TCP payload. If another proxy is
configured, the local SNI proxy connects through it. Unrelated applications are not routed through this proxy.

Lite mode

Lite mode splits the ClientHello into separate socket writes with a short delay. It needs no Administrator or root
rights and uses no packet driver. The operating system or network hardware may combine those writes again, so Lite
mode cannot guarantee separate packets on the wire.

Strict mode

Strict mode intercepts only the exact outbound TCP flows created by the local proxy and emits genuine TCP segments with
correct sequence numbers and checksums. It requires root on Linux or Run as Administrator on Windows.
For a Linux source run, start the app with sudo -E .venv/bin/python3 test.py so it retains your user settings. Plain
sudo normally reads root's separate settings profile and can make your saved mode appear to reset.

Strict Fragmentation sends the genuine segments in their normal order.
Strict Reverse sends the later segment first; the destination TCP stack can reorder and reassemble it.
Strict Desync first sends a harmless fake ClientHello with deliberately invalid sequence and acknowledgement values,
then sends the genuine fragments in reverse order. The destination should discard the fake packet, while some
stateless inspection systems may parse it.

Supported strict platforms:
Windows x86-64 using WinDivert
Linux x86-64 or aarch64 using PyDivert, eBPF and TC; kernel 5.8 or newer and libbpf are required
macOS, Windows ARM64 and other platforms are not currently supported

Important limitations

This is obfuscation, not encryption, a VPN or an anonymity system. A stateful observer can buffer and reassemble the TCP
stream and recover an unencrypted SNI. DNS traffic and the destination IP address can also reveal or suggest the site.
Encrypted ClientHello, when supported by both client and server, protects SNI more directly. Results depend on the
network path and inspection system, and no mode guarantees that a hostname will remain hidden.

Porn Fetch forces HTTP/2 over TCP while this feature is active; it does not modify HTTP/3 or other UDP traffic. Verify
the behavior on your own network and make sure using traffic-obfuscation tools complies with the laws and policies that
apply to you.
")

    readonly property string torIntegrationHelp:
        qsTr("
The Tor Network is a heavily encrypted internet which is run by volunteers all over the world. Porn Fetch supports
a native Tor integration. By enabling this, Porn Fetch will start the Tor service on your PC and route its traffic
through the onion network.

This is NOT illegal and absolutely a good way to protect your privacy. However:
It is ethically a bad idea to route internet traffic like video streaming through the Tor network as it slows down
the entire network for everyone. Please only use this feature if you really have to. (Seriously)
")

    readonly property string onionRoutingHelp:
        qsTr("
The server of Porn Fetch that is used for Update and License checking has a native .onion Tor domain. By enabling this,
Porn Fetch will connect to the Tor domain instead of the clearnet domain.
")

    readonly property string proxySetupHelp:
        qsTr("
A Proxy is basically just a service that routes your internet traffic. It is similar to a VPN. You can find free proxies\non the internet, although I absolutely do not recommend you doing that.\n\nInstead, buy yourself a simple and cheap proxy and use the authentication form below. You can also start the Tor service\non your machine and route through tor.       ")

    readonly property string guiLanguageHelp:
        qsTr("This defines the language of Porn Fetch's user interace")

    readonly property string fontSizeHelp:
        qsTr("This sets the point size of the text in the UI")

    readonly property string appStyleHelp:
        qsTr("Material UI looks like Android, Fusion like the native OS, Universal looks just bad")

    readonly property string darkModeHelp:
        qsTr("You really need an explanation for this xD")

    readonly property string accentColorHelp:
        qsTr("You really need an explanation for this xD")
}
