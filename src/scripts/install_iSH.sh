apk add git python3 py3-pip py3-virtualenv
git clone https://github.com/EchterAlsFake/Porn_Fetch
cd Porn_Fetch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_cli.txt
pip install pyinstaller
pyinstaller -F Porn_Fetch_CLI.py
cd dist
chmod +x Porn_Fetch_CLI
echo "Porn Fetch is now installed in $(pwd)"
