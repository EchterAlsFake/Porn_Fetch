#!/bin/bash

# Automatic compile script
# If not on a Linux distro, the OS name is used to ensure compatibility

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
elif type lsb_release >/dev/null 2>&1; then
    OS=$(lsb_release -si)
elif [ -f /etc/lsb-release ]; then
    . /etc/lsb-release
    OS=$DISTRIB_ID
elif [ -f /etc/debian_version ]; then
    OS=Debian
elif [ -f /etc/alpine-release ]; then
    OS=Alpine
else
    OS=$(uname -s)
fi

# Convert to lowercase
OS=$(echo $OS | tr '[:upper:]' '[:lower:]')

case $OS in
    "termux")
        # Termux commands
        echo "Detected Termux"
        apt-get update
        apt-get full-upgrade -y
        apt-get install python3 python-pip git wget ldd binutils
        pip install -r requirements_cli.txt
        pip install pyinstaller
        pyinstaller -F main.py
        cd dist
        chmod +x main
        mv main Porn_Fetch
        echo "Porn Fetch is now installed in $(pwd)"
        ;;
    "darwin")
        # macOS commands
        echo "Detected macOS"
        echo "macOS is not supported with this script! Please use the other one. See GitHub Readme!"
        ;;
    esac

# For most Linux Distros
# Detect Package Manager
if command -v pacman ; then
# Arch Linux commands
    echo "Detected Arch Linux"
    sudo pacman -S python-virtualenv git
elif  command -v apt ; then
# Ubuntu commands
    echo "Detected Ubuntu/Debian"
    sudo apt-get update
    sudo apt-get install build-essential cmake python3-dev libssl-dev qtbase5-dev qtdeclarative5-dev qttools5-dev libqt5svg5-dev qt5-default git wget python3-venv -y
elif  command -v dnf ; then
# Fedora commands
    echo "Detected Fedora"
    sudo dnf install -y git python3-virtualenv qt5-devel
elif  command -v zypper ; then
# OpenSUSE commands
    echo "Detected OpenSUSE"
    sudo zypper install -y git python3-virtualenv libqt5-qtbase-devel
fi


# Common commands
git clone https://github.com/EchterAlsFake/Porn_Fetch
cd Porn_Fetch
python3 -m venv /tmp/.venv # This is needed, because Qt has some issues if the virtual environment is in the same directory, as there the script gets executed in
source /tmp/.venv/bin/activate
pip install -r requirements.txt
pyside6-deploy -c src/build/pysidedeploy_linux.spec -f -v
mv "Porn Fetch.bin" "PornFetch_Linux_GUI_x64.bin"
deactivate
echo "Deleting the temporary created virtual environment..."
rm -rf /tmp/.venv
echo "Porn Fetch is now installed in $(pwd)/PornFetch_Linux_GUI_x64.bin"