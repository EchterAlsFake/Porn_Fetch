apt-get update
apt-get full-upgrade -y
apt-get install python3 python-pip git wget ldd binutils
git clone https://github.com/EchterAlsFake/Porn_Fetch
cd Porn_Fetch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller -F widget.py
cd dist
mv widget Porn_Fetch
chmod +x Porn_Fetch
echo "Installation is now installed to $(pwd)/"

