# Ensure the script is running with elevated privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "You need to run this script as an Administrator!"
    Start-Process powershell -ArgumentList "-noprofile -executionpolicy bypass -file $($myinvocation.mycommand)" -verb RunAs
    exit
}

$userDir = [Environment]::GetFolderPath('UserProfile')
$desktopDir = [System.IO.Path]::Combine($userDir, "Desktop")

# Define the downloads directory
$downloadsDir = "$env:TEMP"

function Check-PythonInstalled {
    try {
        $pythonVersion = py --version 2>&1
        if ($pythonVersion -match "Python (\d+\.\d+\.\d+)") {
            return $true
        } else {
            return $false
        }
    } catch {
        return $false
    }
}

function Install-Python {
    # Download and install Python
    Write-Output "Downloading Python 3.12.8..."
    $pythonInstallerPath = [System.IO.Path]::Combine($downloadsDir, "python-3.12.8-amd64.exe")
    try {
        Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe" -OutFile $pythonInstallerPath -ErrorAction Stop
    } catch {
        Write-Output "Failed to download Python installer. Please check your internet connection."
        return
    }

    Write-Output "Installing Python 3.12.8 silently..."
    try {
        Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait -ErrorAction Stop
    } catch {
        Write-Output "Python installation failed. Please run the installer manually."
        return
    }

    # Verify installation
    if (Check-PythonInstalled) {
        Write-Output "Python installation succeeded. Version: $(py --version 2>&1)"
    } else {
        Write-Output "Python installation failed. Please install it manually from https://www.python.org/downloads/"
    }
}

if (Check-PythonInstalled) {
    Write-Output "Python is already installed. Version: $(py --version 2>&1)"
} else {
    Write-Output "Python is not installed."
    Install-Python
}

# Download and extract the project ZIP
Write-Output "Downloading project ZIP..."
$projectZipPath = [System.IO.Path]::Combine($downloadsDir, "master.zip")
Invoke-WebRequest -Uri "https://github.com/EchterAlsFake/Porn_Fetch/archive/refs/heads/master.zip" -OutFile $projectZipPath
Write-Output "Extracting project ZIP..."
Expand-Archive -Path $projectZipPath -DestinationPath $downloadsDir -Force

# Use Invoke-Command to run commands within the virtual environment
$projectDir = Join-Path -Path $downloadsDir -ChildPath "Porn_Fetch-master"
Set-Location -Path $projectDir
py -m venv ..\venv\
..\venv\Scripts\activate.ps1
pip install -r requirements.txt
pip install pywin32 av
$env:NUITKA_ASSUME_YES_FOR_DOWNLOADS = "1"
Write-Host "NUITKA_ASSUME_YES_FOR_DOWNLOADS is set to $env:NUITKA_ASSUME_YES_FOR_DOWNLOADS"

# Invoke the UI update script
Write-Output "Running UI update script..."
$uiUpdateScriptPath = Join-Path -Path $projectDir -ChildPath "src/frontend/update.ps1"
if (Test-Path -Path $uiUpdateScriptPath) {
    & $uiUpdateScriptPath
} else {
    Write-Error "UI update script not found at $uiUpdateScriptPath. Please ensure it exists."
    exit 1
}
Set-Location -Path $projectDir
pyside6-deploy -c src/build/pysidedeploy_windows.spec -f -v

# Move the final executable to the user's Desktop
$finalExePath = Join-Path -Path $projectDir -ChildPath "Porn Fetch.exe"
$renamedExe = Join-Path -Path $projectDir -ChildPath "PornFetch_Windows_GUI_x64.exe"
Rename-Item -Path $finalExePath -NewName "PornFetch_Windows_GUI_x64.exe"
Move-Item -Path $renamedExe -Destination (Join-Path $desktopDir "PornFetch_Windows_GUI_x64.exe")

# Clean up
deactivate
Set-Location C:\ # Just leaves the directory, so that I can remove the downloaded archive
Write-Output "Cleaning up..."
Remove-Item -Path $projectZipPath -Force
Remove-Item -Recurse -Force -Path (Join-Path $downloadsDir "Porn_Fetch-master")
Write-Output "Done!"
