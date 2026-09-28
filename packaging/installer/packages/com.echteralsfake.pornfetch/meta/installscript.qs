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
    var isMac = (systemInfo.kernelType === "darwin");

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
        // Ensure execution permissions on Linux for main app and PocketBase
        component.addOperation("Execute", "chmod", "0755", "@TargetDir@/Porn Fetch");
        component.addOperation("Execute", "chmod", "0755", "@TargetDir@/pocketbase");

        // Desktop shortcut on Linux
        component.addOperation(
            "CreateDesktopEntry",
            "@HomeDir@/.local/share/applications/pornfetch.desktop",
            "Type=Application\nExec=\"@TargetDir@/Porn Fetch\"\nPath=@TargetDir@\nName=Porn Fetch\nIcon=@TargetDir@/logo_transparent.png\nCategories=AudioVideo;Utility;\nTerminal=false"
        );
    } else if (isMac) {
        // Ensure execution permissions on macOS
        component.addOperation("Execute", "chmod", "0755", "@TargetDir@/Porn Fetch.app/Contents/MacOS/Porn Fetch");
        component.addOperation("Execute", "chmod", "0755", "@TargetDir@/Porn Fetch.app/Contents/MacOS/pocketbase");
    }
};
