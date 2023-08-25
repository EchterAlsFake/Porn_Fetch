#!/bin/bash

# Automatic compile script for Porn Fetch
# Currently supported: Arch Linux, Ubuntu, Termux

echo "Please select your distribution. If your distribution is not in the list, make an Issue about it!"
options="Arch-Linux Ubuntu Termux Fedora OpenSUSE"
select option in $options; do
  if [ "Arch-Linux" = $option ]; then
        echo "You've chosen arch linux"
        sudo pacman -S python-virtualenv git
        git clone https://github.com/EchterAlsFake/Porn_Fetch
        cd Porn_Fetch
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        pyinstaller -F widget.py
        cd dist
        mv widget Porn_Fetch
        chmod +x Porn_Fetch
        echo "Porn Fetch is now installed to /Porn_Fetch/dist/"
        exit

  elif [ $option = "Ubuntu" ]; then
        echo "You've chosen ubuntu"
        sudo apt-get update
        sudo apt-get install build-essential cmake python3-dev libssl-dev qtbase5-dev qtdeclarative5-dev qttools5-dev libqt5svg5-dev qt5-default git wget python3-venv -y
        wget "https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tar.xz"
        tar -xvf "Python-3.11.4.tar.xz"
        cd Python-3.11.4
        ./configure --enable-optimizations
        make -j 8
        sudo make altinstall
        cd ..
        rm -rf Python-3.11.4
        git clone https://github.com/EchterAlsFake/Porn_Fetch
        cd Porn_Fetch
        python3.11 -m venv venv
        source venv/bin/activate
        pip instal -r requirements.txt
        pyinstaller -F widget.py
        cd dist
        chmod +x widget
        mv widget Porn_Fetch
        echo "You can run Porn Fetch now in the dist directory with ./Porn_Fetch"
        echo "Note, at first startup the graphics resources will be downloaded..."

  elif [ "Termux" = $option ]; then
        echo "You've chosen termux"
        echo "Please make sure, that you've installed Termux from the F-Droid store. The Playstore version is outdated!"
        sleep 2
        apt-get update
        echo "NOTE: If you get asked some questions, just press N and continue"
        apt-get full-upgrade -y
        apt-get install python3 python-pip git wget ldd binutils
        git clone https://github.com/EchterAlsFake/Porn_Fetch
        cd Porn_Fetch
        cd src
        pip install -r requirements_termux.txt
        pyinstaller -F cli.py
        cd dist
        mv cli Porn_Fetch
        chmod +x Porn_Fetch
        echo "Porn Fetch is now in the dist directory (Porn_Fetch/src/dist/) Run it with ./Porn_Fetch"
        exit

  elif [ $option = "Fedora" ]; then
      echo "You've chosen fedora"
      sudo dnf install -y git python3-virtualenv qt5-devel
      git clone https://github.com/EchterAlsFake/Porn_Fetch
        cd Porn_Fetch
        cd src
        pip install -r requirements_termux.txt
        pyinstaller -F cli.py
        cd dist
        mv cli Porn_Fetch
        chmod +x Porn_Fetch
        echo "Porn Fetch is now in the dist directory (Porn_Fetch/src/dist/) Run it with ./Porn_Fetch"
        exit

    elif [ "OpenSUSE" = $option ]; then

      echo "You've chosen OpenSUSE"
      sudo zypper install -y git python3-virtualenv libqt5-qtbase-devel
      git clone https://github.com/EchterAlsFake/Porn_Fetch
        cd Porn_Fetch
        cd src
        pip install -r requirements_termux.txt
        pyinstaller -F cli.py
        cd dist
        mv cli Porn_Fetch
        chmod +x Porn_Fetch
        echo "Porn Fetch is now in the dist directory (Porn_Fetch/src/dist/) Run it with ./Porn_Fetch"
        exit

  else
        echo "Error"
  fi

done