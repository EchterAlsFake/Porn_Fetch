#!/bin/bash

# Automatic compile script
# Detect distribution
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
    "arch"|"archlinux")
        # Arch Linux commands
        echo "Detected Arch Linux"
        sudo pacman -S python-virtualenv git
        ;;
    "ubuntu")
        # Ubuntu commands
        echo "Detected Ubuntu"
        sudo apt-get update
        sudo apt-get install build-essential cmake python3-dev libssl-dev qtbase5-dev qtdeclarative5-dev qttools5-dev libqt5svg5-dev qt5-default git wget python3-venv -y
        ;;
    "termux")
        # Termux commands
        echo "Detected Termux"
        apt-get update
        apt-get full-upgrade -y
        apt-get install python3 python-pip git wget ldd binutils
        ;;
    "fedora")
        # Fedora commands
        echo "Detected Fedora"
        sudo dnf install -y git python3-virtualenv qt5-devel
        ;;
    "opensuse"|"suse")
        # OpenSUSE commands
        echo "Detected OpenSUSE"
        sudo zypper install -y git python3-virtualenv libqt5-qtbase-devel
        ;;
    "alpine")
        # iSH (Alpine Linux) commands
        echo "Detected Alpine Linux (iSH)"
        apk add git python3 py3-pip py3-virtualenv
        ;;
    "darwin")
        # macOS commands
        echo "Detected macOS"
        # Ensure Homebrew is installed
        which -s brew
        if [[ $? != 0 ]] ; then
            echo "Homebrew is not installed. Installing now..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python3 git
        ;;
    *)
        echo "Unsupported distribution: $OS"
        exit 1
        ;;
esac

# Common commands
git clone https://github.com/EchterAlsFake/Porn_Fetch
cd Porn_Fetch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller -F Porn_Fetch.py
cd dist
mv widget Porn_Fetch
chmod +x Porn_Fetch
echo "Porn Fetch is now installed to $(pwd)/"
