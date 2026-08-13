This just contains files and stuff that I need to check for before every new release,
to ensure quality control of each release, because I only release one version every few months lol.


# Checklist
- [] Updated version in window title
- [] Updated UI with update.sh script
- [] Updated dependencies for Nuitka / Qt
- [] Verified that a clean fresh run of Porn Fetch on an independent system works
- [] Test Installation on macOS, Windows and Linux
- [] Text Proxy and Kill Switch feature for reliability, disconnect connection to see what happens
- [] Test each supported function for each website with default settings (See urls.txt)
- [] Test all widgets of the GUI
- [] Test donation nag
- [] Especially test the update changelog with a fake update (temporary)
- [] Test all build scripts

## Fake update popup

Start the local fake-update server in one terminal:

```bash
python testing/fake_update_server.py
```

Then start the QML application from another terminal with the development
endpoint override:

```bash
PORNFETCH_UPDATE_URL=http://127.0.0.1:8765/update python test.py
```

The server advertises version 4.0 with fake HTML release notes and harmless
download-link test pages. It deliberately does not advertise a platform binary,
so it cannot be used to install or replace the application.
