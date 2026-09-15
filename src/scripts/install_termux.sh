#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

pkg update -y
pkg install -y python git binutils libxml2 libxslt

git clone https://github.com/EchterAlsFake/Porn_Fetch
cd Porn_Fetch
python -m venv venv
source venv/bin/activate
python -m pip install '.[cli]'
python -m PyInstaller --clean src/build/pyinstaller_cli.spec
mv dist/Porn_Fetch_CLI Porn_Fetch
chmod +x Porn_Fetch
echo "Porn Fetch is now installed to $(pwd)/Porn_Fetch"
