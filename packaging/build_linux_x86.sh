#!/usr/bin/env bash
set -euo pipefail

project_dir=$PWD
python_version=3.14.7
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y build-essential ca-certificates curl git libbz2-dev libffi-dev liblzma-dev libncurses-dev libreadline-dev libsqlite3-dev libssl-dev libzstd-dev pkg-config zlib1g-dev

cd /tmp
curl -fsSLo Python.tgz "https://www.python.org/ftp/python/$python_version/Python-$python_version.tgz"
tar -xzf Python.tgz
cd "Python-$python_version"
./configure --prefix=/opt/python-3.14 --enable-shared
make -j2
make altinstall

export LD_LIBRARY_PATH=/opt/python-3.14/lib
export PATH="/opt/python-3.14/bin:/root/.local/bin:/root/.cargo/bin:$PATH"
python3.14 -c 'import struct; assert struct.calcsize("P") == 4'
curl -fsSLo /tmp/rustup-init https://static.rust-lang.org/rustup/dist/i686-unknown-linux-gnu/rustup-init
chmod +x /tmp/rustup-init
/tmp/rustup-init -y --profile minimal --default-host i686-unknown-linux-gnu
rustc -vV | grep -q 'host: i686-unknown-linux-gnu'
curl -fsSLo /tmp/uv.tar.gz https://github.com/astral-sh/uv/releases/latest/download/uv-i686-unknown-linux-gnu.tar.gz
tar -xzf /tmp/uv.tar.gz -C /tmp
install -m 755 /tmp/uv-i686-unknown-linux-gnu/uv /usr/local/bin/uv

cd "$project_dir"
uv sync --locked --no-dev --extra build --python /opt/python-3.14/bin/python3.14
uv run --no-sync python -c 'import struct; assert struct.calcsize("P") == 4'
uv run --no-sync python packaging/write_cli_build_version.py "$BUILD_RUN_NUMBER" linux x32
uv run --no-sync pyinstaller --clean packaging/pyinstaller_cli.spec
readelf -h dist/Porn_Fetch_CLI | grep -q 'Machine:.*Intel 80386'

mv dist/Porn_Fetch_CLI PornFetch_Linux_CLI_x32
uv run --no-sync python scripts/write_checksum.py PornFetch_Linux_CLI_x32
./PornFetch_Linux_CLI_x32 --test-mode --filter offline
uv run --no-sync python packaging/collect_legal.py PornFetch_Linux_CLI_x32_LEGAL
