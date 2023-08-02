#!/bin/bash

# Automatic compile script for Porn Fetch
# Currently supported: Arch Linux, Ubuntu, Termux

echo "Please select your distribution. If your distribution is not in the list, make an Issue about it!"
options="Arch-Linux Ubuntu Termux"
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


  elif [ "Termux" = $option]; then
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
  else
        echo "Error"
  fi

done