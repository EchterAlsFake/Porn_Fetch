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
echo "Downloading Qt's PySide6-setup to download the Android NDK/SDK"
git clone https://code.qt.io/pyside/pyside-setup
cd pyside-setup
echo "Creating temporary virtual environment"
python3.11 -m venv venv
source venv/bin/activate
source venv/bin/activate
pip install -r tools/cross_compile_android/requirements.txt
pip install -r requirements.txt
python3 tools/cross_compile_android/main.py --download-only --auto-accept-license --clean-cache all
echo "Installed Android NDK / SDK in ~/pyside6_android_deploy/"

ANDROID_SDK="$HOME/.pyside6_android_deploy/android-sdk"
ANDROID_NDK="$HOME/.pyside6_android_deploy/android-ndk/android-ndk-r26b/"


cd ../
echo "Cleaning pyside-setup directory"
rm -rf pyside-setup
echo "Creating a new virtual environment for the android build"
python3.11 -m venv /tmp/venv
source /tmp/venv/bin/activate
pip install PySide6
echo """
[ACTION]
You need to edit the file in '/tmp/venv/lib/python3.11/site-packages/PySide6/scripts/android_deploy.py'
and write this: 'input(\"edit requirements\")' after line 129.

Here's an example:

        # run buildozer
        logging.info(\"[DEPLOY] Running buildozer deployment\")
        input(\"edit requirements\")
        Buildozer.create_executable(config.mode)

Now save that file. When the build process starts you will at some point see this input statement and then you need
to go into \$HOME/Porn_Fetch/ and edit the file 'buildozer.spec'. In this file you will see a line named 'requirments = python3,shiboken6,PySide6'
After the PySide6 requirement write exactly this:

,charset-normalizer==2.1.1,git+https://github.com/EchterAlsFake/PHUB,idna,urllib3,certifi,hue_shift,markdown,colorama,requests,git+https://github.com/EchterAlsFake/hqporner_api,ffmpeg-progress-yield,tqdm,git+https://github.com/EchterAlsFake/eporner_api,git+https://github.com/EchterAlsFake/xnxx_api,git+https://github.com/EchterAlsFake/xvideos_api,beautifulsoup4,mutagen,git+https://github.com/EchterAlsFake/eaf_base_api,httpx,httpcore,h11,certifi,idna,sniffio,git+https://github.com/EchterAlsFake/spankbang_api

Then save that file and hit ENTER in this window to continue the build process. If you need help, feel free to contact me
on Discord: 'echteralsfake'
"""


read -r fortnite
echo "Please choose the architecture you want to build for"

options=("aarch64" "armv7a" "x86_64" "i686" "quit")
select choice in "${options[@]}"; do
  case $choice in
        "aarch64")

            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/PySide6-6.8.0a1-6.8.1-cp311-cp311-android_aarch64.whl"
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/shiboken6-6.8.0a1-6.8.1-cp311-cp311-android_aarch64.whl"
            echo "Starting to build the Android application for aarch64 architecture"
            pyside6-android-deploy -c src/build/pysidedeploy_android_aarch64.spec

            ;;
        "armv7a")
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/PySide6-6.8.0a1-6.8.1-cp311-cp311-android_armv7a.whl"
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/shiboken6-6.8.0a1-6.8.1-cp311-cp311-android_armv7a.whl"
            echo "Starting to build the Android application for armv7a architecture"
            pyside6-android-deploy -c src/build/pysidedeploy_android_armv7a.spec

            ;;
        "i686")
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/PySide6-6.8.0a1-6.8.1-cp311-cp311-android_i686.whl"
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/shiboken6-6.8.0a1-6.8.1-cp311-cp311-android_i686.whl"
            echo "Starting to build the Android application for i686 architecture"
            pyside6-android-deploy -c src/build/pysidedeploy_android_i686.spec

            ;;
        "x86_64")
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/PySide6-6.8.0a1-6.8.1-cp311-cp311-android_x86_64.whl"
            wget "https://github.com/EchterAlsFake/PySide6-to-Android/releases/download/6.8.1_3.11/shiboken6-6.8.0a1-6.8.1-cp311-cp311-android_x86_64.whl"
            echo "Starting to build the Android application for x86_64 architecture"
            pyside6-android-deploy -c src/build/pysidedeploy_android_x86_64.spec

            ;;
        "quit")
            exit

            ;;
        *)
            echo "Invalid option, please try again."
            ;;
    esac
done

echo "Porn Fetch is now compiled for Android!, you can install the .apk file "