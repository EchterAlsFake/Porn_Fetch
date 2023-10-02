# Ensure the script is running with elevated privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "You need to run this script as an Administrator!"
    Start-Process powershell -ArgumentList "-noprofile -executionpolicy bypass -file $($myinvocation.mycommand)" -verb RunAs
    exit
}

# Check if Python is already installed
$pythonInstalled = $true
try {
    python --version | Out-Null
} catch {
    $pythonInstalled = $false
}

if (-not $pythonInstalled) {
    # Download and install Python
    Write-Output "Downloading Python 3.11.6..."
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe" -OutFile "python-3.11.6-amd64.exe"
    
    Write-Output "Installing Python 3.11.6 silently..."
    Start-Process -Wait "python-3.11.6-amd64.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1"
} else {
    Write-Output "Python is already installed."
}

# Download and extract the project ZIP
Write-Output "Downloading project ZIP..."
Invoke-WebRequest -Uri "https://github.com/EchterAlsFake/Porn_Fetch/archive/refs/heads/master.zip" -OutFile "master.zip"

Write-Output "Extracting project ZIP..."
Expand-Archive -Path "master.zip" -DestinationPath "."

# Install pip requirements
Set-Location -Path ".\Porn_Fetch-master"

Write-Output "Installing pip requirements..."
pip install -r requirements.txt
pip install pyinstaller

# Build the project
Write-Output "Building the project..."
pyinstaller -F Porn_Fetch.py

Write-Output "Done!"
