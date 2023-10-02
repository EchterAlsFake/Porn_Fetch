@echo off
setlocal enabledelayedexpansion

:: Check if Python is already installed
python --version >nul 2>&1
if errorlevel 1 (
    :: Python isn't installed. Download and install it silently.

    echo Downloading Python 3.11.6...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe -OutFile python-3.11.6-amd64.exe"

    echo Installing Python 3.11.6 silently...
    python-3.11.6-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Wait for a moment to ensure the installation completes before moving on
    timeout /t 30
) else (
    echo Python is already installed.
)

:: Step 2: Download and extract the ZIP file
echo Downloading project ZIP...
powershell -Command "Invoke-WebRequest -Uri https://github.com/EchterAlsFake/Porn_Fetch/archive/refs/heads/master.zip -OutFile master.zip"

echo Extracting project ZIP...
powershell -Command "Expand-Archive -Path master.zip -DestinationPath ."

:: Step 3: Install pip requirements
cd Porn_Fetch-master

echo Installing pip requirements...
pip install -r requirements.txt
pip install pyinstaller

:: Step 4: Build the project
echo Building the project...
pyinstaller -F Porn_Fetch.py

echo Done!

endlocal
exit /b 0