function Component()
{
    // Default constructor
}

Component.prototype.createOperations = function()
{
    // Call default implementation to copy extracted files
    component.createOperations();

    var isWindows = (systemInfo.kernelType === "winnt");
    var isLinux = (systemInfo.kernelType === "linux");
    var isMacOS = (systemInfo.kernelType === "darwin");

    if (isWindows) {
        // Desktop & Start Menu Shortcuts on Windows
        component.addOperation(
            "CreateShortcut",
            "@TargetDir@/Porn Fetch.exe",
            "@DesktopDir@/Porn Fetch.lnk",
            "workingDirectory=@TargetDir@",
            "iconPath=@TargetDir@/Porn Fetch.exe",
            "description=Launch Porn Fetch"
        );
        component.addOperation(
            "CreateShortcut",
            "@TargetDir@/Porn Fetch.exe",
            "@StartMenuDir@/Porn Fetch.lnk",
            "workingDirectory=@TargetDir@",
            "iconPath=@TargetDir@/Porn Fetch.exe",
            "description=Launch Porn Fetch"
        );
    } else if (isLinux) {
        // Optional tools carry their executable permissions in their own packages.
        component.addOperation("Execute", "chmod", "0755", "@TargetDir@/Porn Fetch");

        // Desktop shortcut on Linux
        component.addOperation("Mkdir", "@HomeDir@/.local/share/applications");
        component.addOperation(
            "CreateDesktopEntry",
            "@HomeDir@/.local/share/applications/pornfetch.desktop",
            "Type=Application\nExec=\"@TargetDir@/Porn Fetch\"\nPath=@TargetDir@\nName=Porn Fetch\nIcon=@TargetDir@/logo_transparent.png\nCategories=AudioVideo;Utility;\nTerminal=false"
        );
    } else if (isMacOS) {
        var app = installer.value("TargetDir") + "/Porn Fetch.app";
        var shortcut = installer.value("ApplicationsDirUser") + "/Porn Fetch.app";
        var existingLink = installer.execute("/usr/bin/readlink", [shortcut]);
        var isLink = existingLink.length === 2 && existingLink[1] === 0;
        // Recreate our own shortcut on updates, preserving other installations.
        if ((isLink && existingLink[0].trim() === app)
                || (!isLink && !installer.fileExists(shortcut))) {
            component.addOperation("CreateLink", shortcut, app);
        }

        // Register the real bundle so macOS can find it by name.
        var launchServices = "/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister";
        if (installer.fileExists(launchServices)) {
            component.addOperation("Execute", launchServices, "-f", app,
                "UNDOEXECUTE", launchServices, "-u", app);
        }
    }
};
