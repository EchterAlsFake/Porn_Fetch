#!/bin/bash

# Install Python 3.13.1
echo "Installing Python 3.13.1..."
PYTHON_VERSION="3.13.1"
PYTHON_DMG="python-${PYTHON_VERSION}-macos11.pkg"
PYTHON_URL="https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON_DMG}"

# Download Python installer
curl -o "/tmp/${PYTHON_DMG}" "${PYTHON_URL}" --silent

# Install Python
sudo installer -pkg "/tmp/${PYTHON_DMG}" -target / > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Python 3.13.1 installed successfully."
else
    echo "[ERROR] Python installation failed."
    exit 1
fi

# Clean up
rm "/tmp/${PYTHON_DMG}"

# Verify Python installation
echo "Verifying Python installation..."
python3.13 --version

echo "Python installation script completed successfully."

# Fix SSL Certificate Issue
echo "Fixing SSL certificate issue for Python's requests library..."
/Applications/Python\ 3.13/Install\ Certificates.command > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "SSL certificates updated successfully."
else
    echo "[ERROR] Failed to update SSL certificates."
    exit 1
fi


echo "Building Porn Fetch!"

cd "${HOME}" || { echo "[ERROR] Failed to change directory to ${HOME}"; exit 1; }
git clone https://github.com/EchterAlsFake/Porn_Fetch
cd "Porn_Fetch"

python3.13 -m venv /tmp/.venv # This is needed, because Qt has some issues if the virtual environment is in the same directory, as there the script gets executed in
source /tmp/.venv/bin/activate
pip install -r requirements.txt
pip install nuitka --upgrade
cd src/frontend
bash update.sh
cd ../../
pyside6-deploy -c src/build/pysidedeploy_macOS.spec -f -v
deactivate
echo "Deleting the temporary created virtual environment..."
rm -rf /tmp/.venv
echo "Porn Fetch is now installed in $(pwd)/main.bin"

