function Component()
{
    installer.installationStarted.connect(this, Component.prototype.onInstallationStarted);
}

Component.prototype.onInstallationStarted = function()
{
    if (component.installationRequested() || component.updateRequested()) {
        // IFW copies this signed PE unchanged; mutable resources live in .dat files.
        installer.setInstallerBaseBinary("@TargetDir@/installerbase.exe");
    }
};
