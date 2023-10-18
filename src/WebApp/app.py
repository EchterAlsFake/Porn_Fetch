import streamlit as st

# This project is highly experimental!


st.set_page_config(page_title="Porn Fetch", layout="wide")

with open("style.css") as style:
    st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)



with st.container():
    st.markdown("<h1 style='text-align: center; color: purple;'>Porn Fetch - A free & open-source PornHub Downloader</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h2 style='text-align: center; color: purple;'>by EchterAlsFake</h2>",
        unsafe_allow_html=True)

x_right_column, x_left_column = st.columns(2)
with x_right_column:
    st.subheader("Features")
    st.markdown("""
- Downloading directly from PornHub itself
- Downloading with selectable quality
- Fetching metadata from Videos
- Downloading multiple videos at once
- Downloading all videos from a whole Channel / User / Model account
- Search for videos and download them directly in the application
- Native dark mode
- CLI for systems without a graphical user interface
- No ADs & restrictions
- No login / PornHub account needed
- No data tracking
- Open-Source
- Cross-platform
- Actively maintained
""")

with x_left_column:

    with st.container():
        st.write("---")
        st.subheader("[Visit Project](https://github.com/EchterAlsFake/Porn_Fetch)")
        st.header("Downloads:")
        left_column, right_column = st.columns(2)



        with left_column:
            st.subheader("Windows:")


            direct_link_windows_1_8 = "https://drive.google.com/uc?export=download&id=1IxYPtU2lPqHZIFfSVNDoO3Z3FWMp_UoQ"
            torrent_link_windows_1_8 = "https://drive.google.com/uc?export=download&id=1KTBEgqx2p27x2UY8aNzvlhc0FoimDzkg"

            st.markdown(f'<a href="{direct_link_windows_1_8}" target="_blank"><input type="button" class="yeah" value="1.8 (.exe)"></a>',
                        unsafe_allow_html=True)

            st.subheader("Torrents:")
            st.markdown(
                f'<a href="{torrent_link_windows_1_8}" target="_blank"><input type="button" class="yeah" value="1.8 (.torrent)"></a>',
                unsafe_allow_html=True)

        with right_column:
            direct_link_linux_1_8 = "https://drive.google.com/uc?export=download&id=11mo-bKMVnJNgVzi6gEP4bcPP42ziULCs"
            torrent_link_linux_1_8 = "https://drive.google.com/uc?export=download&id=1Csq0EYQKKgfGHpOPvUMTjVyb-de5TZa7"

            st.subheader("Linux:")
            st.markdown(
                f'<a href="{direct_link_linux_1_8}" target="_blank"><input type="button" class="yeah" value="1.8 (AppImage)"></a>',
                unsafe_allow_html=True)


            st.subheader("Torrents:")
            st.markdown(
                f'<a href="{direct_link_linux_1_8}" target="_blank"><input type="button" class="yeah" value="1.8 (.torrent)"></a>',
                unsafe_allow_html=True)

st.header("Legal information")
st.write("""
Porn Fetch isn't permitted by PornHub. 
PornHub prohibits scraping content on their website and downloading videos for non registered users.
Please use a VPN, when using my Application!
""")

st.markdown("<h2 style='text-align: center; color: orange;'>Building from Source</h2>", unsafe_allow_html=True)

build_left, build_right, = st.columns(2)

with build_left:

    st.subheader("Windows")
    st.write("Requirements:")
    st.markdown("""
- Git
- Python 3.11
- Windows 10 / 11""")

    st.markdown("""
```
git clone https://github.com/EchterAlsFake/Porn_Fetch
cd Porn_Fetch
pip install -r requirements.txt
pyinstaller -F Porn_Fetch.py
``` 
""")

with build_right:
    st.subheader("Linux")
    st.write("I've made an automatic build script to make the process easier. Just choose your distribution!")
    st.markdown("""
Currently supported:

- Termux
- Arch Linux
- Ubuntu
""")
    st.markdown("""
```
wget "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/install.sh" && bash install.sh
``` 
""")







