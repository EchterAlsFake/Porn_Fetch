# v4.0.2

- Pornhub, XVideos, and xHamster sign-in remains available for account browsing
  and collections. Porn Fetch uses separate guest sessions for downloads,
  including retries and resumed jobs across all supported providers.
- Porn Fetch blocks items it identifies as paid or private. Items with unknown
  access stay visible and can be tried as a guest. If the website refuses
  access, Porn Fetch explains why the download may be unavailable.
- Resumed jobs check guest access again. Older partial downloads may restart
  when their saved download state cannot be verified as coming from a guest session.
- Updated the desktop and mobile Accounts pages and clarified each provider's
  sign-in and collection options.
- Updated the Pornhub SDK to 6.0.3 for safer playback retries and fixed channel
  pagination on supported language sites and sort modes.
- Includes the removal of preset age cookies from Pornhub, RedTube, and Tube8
  introduced in v4.0.1.
