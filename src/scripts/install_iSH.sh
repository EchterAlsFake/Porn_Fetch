# We need to compile Python 3.11, because iSH uses 3.9 by default which is incompatible with PHUB
"""
apk add --no-cache build-base libffi-dev openssl-dev bzip2-dev zlib-dev readline-dev ncurses-dev gdbm-dev sqlite-dev
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tar.xz
tar -xf Python-3.11.0.tar.xz
cd Python-3.11.0
./configure --enable-shared --enable-optimizations
make
make install

cd ..
rm -rf Python-3.11.0 Python-3.11.0.tar.xz
"""
apk add git
git clone https://github.com/EchterAlsFake/Porn_Fetch
cd Porn_Fetch
python3 -m pip install -r requirements_cli.txt
python3 -m pip install pyinstaller
python3 -m pyinstaller -F Porn_Fetch_CLI.py
cd dist
chmod +x Porn_Fetch_CLI
echo "Porn Fetch is now installed in $(pwd)"
