sudo apt update
sudo apt-get full-upgrade -y
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev git build-essential libstdc++6
git clone https://github.com/EchterAlsFake/Porn_Fetch -b android
cd Porn_Fetch
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
source Porn_Fetch/venv/bin/activate
pip install -r Porn_Fetch/requirements.txt
pip install buildozer cython==0.29.36
source Porn_Fetch/venv/bin/activate
cd Porn_Fetch
buildozer -v android debug
echo "Porn Fetch apk is in bin directory."