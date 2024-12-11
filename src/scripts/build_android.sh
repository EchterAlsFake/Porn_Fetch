# This is a script for building Porn Fetch for different Android architectures
if command -v python3.11 &>/dev/null; then
    version=$(python3.11 --version 2>&1)
    echo "Python 3.11 is installed: $version"
else
    echo "Python 3.11 is not installed."
    echo "Exiting, please install Python3.11 !"

fi

git clone https://github.com/EchterAlsFake/Porn_Fetch
cd Porn_Fetch
echo "Installing requirements..."
sudo pacman -S base-devel android-tools android-udev clang jdk17-openjdk llvm openssl wget git
echo "Downloading Qt's PySide6-setup to download the Android NDK/SDK"
git clone https://code.qt.io/pyside/pyside-setup
cd pyside-setup
echo "Creating temporary virtual environment"
python3.11 -m venv venv
source venv/bin/activate
source venv/bin/activate
pip install -r tools/cross_compile_android/requirements.txt
pip install -r requirements.txt
python3 tools/cross_compile_android/main.py --download-only --auto-accept-license
echo "Installed Android NDK / SDK in ~/pyside6_android_deploy/"

ANDROID_SDK="$HOME/.pyside6_android_deploy/android-sdk"
ANDROID_NDK="$HOME/.pyside6_android_deploy/android-ndk/android-ndk-r26b/"


cd ../
echo "Cleaning pyside-setup directory"
rm -rf pyside-setup
echo "Creating a new virtual environment for the android build"

echo "Please choose the architecture you want to build for"

options=("aarch64" "armv7a" "x86_64" "i686" "quit")
select choice in "${options[@]}"; do
  case $choice in
        "aarch64")

            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/PySide6-6.8.0a1-6.8.1-cp311-cp311-android_aarch64.whl"
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/shiboken6-6.8.0a1-6.8.1-cp311-cp311-android_aarch64.whl"
            echo "Starting to build the Android application for aarch64 architecture"
            pyside6-android-deploy -c src/build/pysidedeploy_android_aarch64.spec --ndk-path "$HOME"/.pyside6_android_deploy/android-ndk/android-ndk-r26b/ --sdk-path "$HOME"/.pyside6_android_deploy/android-sdk/

            ;;
        "armv7a")
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/PySide6-6.8.0a1-6.8.1-cp311-cp311-android_armv7a.whl"
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/shiboken6-6.8.0a1-6.8.1-cp311-cp311-android_armv7a.whl"
            echo "Starting to build the Android application for armv7a architecture"
            pyside6-android-deploy -c src/build/pysidedeploy_android_armv7a.spec --ndk-path "$HOME"/.pyside6_android_deploy/android-ndk/android-ndk-r26b/ --sdk-path "$HOME"/.pyside6_android_deploy/android-sdk/

            ;;
        "i686")
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/PySide6-6.8.0a1-6.8.1-cp311-cp311-android_i686.whl"
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/shiboken6-6.8.0a1-6.8.1-cp311-cp311-android_i686.whl"
            echo "Starting to build the Android application for i686 architecture"
            pyside6-android-deploy -c src/build/pysidedeploy_android_i686.spec --ndk-path "$HOME"/.pyside6_android_deploy/android-ndk/android-ndk-r26b/ --sdk-path "$HOME"/.pyside6_android_deploy/android-sdk/

            ;;
        "x86_64")
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/PySide6-6.8.0a1-6.8.1-cp311-cp311-android_x86_64.whl"
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/shiboken6-6.8.0a1-6.8.1-cp311-cp311-android_x86_64.whl"
            echo "Starting to build the Android application for x86_64 architecture"
            pyside6-android-deploy -c src/build/pysidedeploy_android_x86_64.spec --ndk-path "$HOME"/.pyside6_android_deploy/android-ndk/android-ndk-r26b/ --sdk-path "$HOME"/.pyside6_android_deploy/android-sdk/

            ;;
        "quit")
            exit

            ;;
        *)
            echo "Invalid option, please try again."
            ;;
    esac
done