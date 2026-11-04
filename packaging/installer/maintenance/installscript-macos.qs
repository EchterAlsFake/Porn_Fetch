function Component()
{
    installer.installationStarted.connect(this, Component.prototype.onInstallationStarted);
}

Component.prototype.onInstallationStarted = function()
{
    if (component.installationRequested() || component.updateRequested()) {
        installer.setInstallerBaseBinary("@TargetDir@/tmpMaintenanceToolApp/maintenancetool.app");
    }
};

// IFW 4.11 moves this signed bundle and its updater helper to the target directory
// at the end of installation. Extracting separately also permits self-updates.
Component.prototype.createOperationsForArchive = function(archive)
{
    component.addOperation("Extract", archive, "@TargetDir@/tmpMaintenanceToolApp");
};
