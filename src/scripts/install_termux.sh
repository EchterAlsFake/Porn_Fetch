apt-get update
apt-get full-upgrade -y
apt-get install python3 python-pip git wget ldd binutils libxslt libxml2 -y
git clone https://github.com/EchterAlsFake/Porn_Fetch
cd Porn_Fetch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_cli.txt
pip install pyinstaller
pyinstaller -F Porn_Fetch_CLI.py
cd dist
mv Porn_Fetch_CLI Porn_Fetch
chmod +x Porn_Fetch
echo "Porn Fetch is now installed to $(pwd)/"

