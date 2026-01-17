#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

# ------------------------------------------------------------
# Pretty colors (works in most terminals)
# ------------------------------------------------------------
BOLD="\033[1m"
DIM="\033[2m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
RESET="\033[0m"

info()    { echo -e "${CYAN}${BOLD}[INFO]${RESET} $*"; }
ok()      { echo -e "${GREEN}${BOLD}[ OK ]${RESET} $*"; }
warn()    { echo -e "${YELLOW}${BOLD}[WARN]${RESET} $*"; }
error()   { echo -e "${RED}${BOLD}[ERR ]${RESET} $*" >&2; }
cmd()     { echo -e "${MAGENTA}${BOLD}>>${RESET} ${DIM}$*${RESET}"; }

run() {
  cmd "$*"
  "$@"
}

# ------------------------------------------------------------
# OS detection (same idea as your script)
# ------------------------------------------------------------
detect_os() {
  local os="unknown"
  if [ -f /etc/os-release ]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    os="${ID:-unknown}"
  elif type lsb_release >/dev/null 2>&1; then
    os="$(lsb_release -si)"
  else
    os="$(uname -s)"
  fi
  echo "$os" | tr '[:upper:]' '[:lower:]'
}

OS="$(detect_os)"

# ------------------------------------------------------------
# Cleanup trap for temp venv
# ------------------------------------------------------------
VENV_DIR=""
cleanup() {
  if [[ -n "${VENV_DIR}" && -d "${VENV_DIR}" ]]; then
    warn "Cleaning up temporary environment: ${VENV_DIR}"
    rm -rf "${VENV_DIR}" || true
  fi
}
trap cleanup EXIT

# ------------------------------------------------------------
# Ensure basic tools exist
# ------------------------------------------------------------
ensure_downloader_tools() {
  if command -v curl >/dev/null 2>&1; then
    return 0
  fi

  warn "curl not found. Trying to install curl..."
  if command -v apt-get >/dev/null 2>&1; then
    run sudo apt-get update
    run sudo apt-get install -y curl
  elif command -v dnf >/dev/null 2>&1; then
    run sudo dnf install -y curl
  elif command -v zypper >/dev/null 2>&1; then
    run sudo zypper install -y curl
  elif command -v pacman >/dev/null 2>&1; then
    run sudo pacman -S --noconfirm --needed curl
  else
    error "No supported package manager found to install curl."
    exit 1
  fi
}

# ------------------------------------------------------------
# Install uv via the OFFICIAL installer script if missing
# ------------------------------------------------------------
install_uv_if_missing() {
  if command -v uv >/dev/null 2>&1; then
    ok "uv already installed: $(uv --version)"
    return 0
  fi

  info "uv not found. Installing via official inf-staller..."
  ensure_downloader_tools

  # Official installer for Linux/macOS:
  # https://astral.sh/uv/install.sh
  run bash -c "curl -LsSf https://astral.sh/uv/install.sh | sh"

  # The installer usually puts uv into ~/.local/bin
  export PATH="${HOME}/.local/bin:${PATH}"
  hash -r || true

  if ! command -v uv >/dev/null 2>&1; then
    error "uv installation finished but 'uv' is still not on PATH."
    error "Try restarting your shell, or ensure ~/.local/bin is in PATH."
    exit 1
  fi

  ok "uv installed successfully: $(uv --version)"
}

# ------------------------------------------------------------
# Install system dependencies (Linux only)
# ------------------------------------------------------------
install_linux_build_deps() {
  if command -v pacman >/dev/null 2>&1; then
    info "Detected Arch Linux (pacman)"
    run sudo pacman -Syu --noconfirm
    run sudo pacman -S --noconfirm --needed \
      base-devel git cmake wget \
      qt5-base qt5-declarative qt5-tools qt5-svg
  elif command -v apt-get >/dev/null 2>&1; then
    info "Detected Debian/Ubuntu (apt)"
    run sudo apt-get update
    run sudo apt-get install -y \
      build-essential cmake python3-dev libssl-dev \
      qtbase5-dev qtdeclarative5-dev qttools5-dev libqt5svg5-dev \
      git wget curl
  elif command -v dnf >/dev/null 2>&1; then
    info "Detected Fedora (dnf)"
    run sudo dnf install -y \
      git wget curl cmake gcc gcc-c++ make \
      qt5-qtbase-devel qt5-qtdeclarative-devel qt5-qtsvg-devel
  elif command -v zypper >/dev/null 2>&1; then
    info "Detected openSUSE (zypper)"
    run sudo zypper refresh
    run sudo zypper install -y \
      git wget curl cmake gcc gcc-c++ make \
      libqt5-qtbase-devel libqt5-qtdeclarative-devel libqt5-qtsvg-devel
  else
    warn "No known Linux package manager detected. Continuing without system deps install."
  fi
}

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
case "$OS" in
  termux)
    info "Detected Termux"
    warn "Building the GUI with PySide6 on Termux is usually not supported."
    warn "If you want, you can still try, but expect issues."
    ;;
  darwin)
    info "Detected macOS"
    error "macOS is not supported by this script!, use the other one, thanks :)"
    exit 1
    ;;
  *)
    info "Detected OS: ${OS}"
    install_linux_build_deps
    ;;
esac

install_uv_if_missing

# ------------------------------------------------------------
# Project fetch/update
# ------------------------------------------------------------
REPO_URL="https://github.com/EchterAlsFake/Porn_Fetch"
PROJECT_DIR="Porn_Fetch"

if [[ -d "${PROJECT_DIR}/.git" ]]; then
  info "Repository already exists. Updating..."
  run git -C "${PROJECT_DIR}" pull --ff-only
else
  info "Cloning repository..."
  run git clone "${REPO_URL}"
fi

cd "${PROJECT_DIR}"

# ------------------------------------------------------------
# Create a temporary uv environment in /tmp
# (Qt can be unhappy if the venv is inside the project dir)
# ------------------------------------------------------------
VENV_DIR="/tmp/porn_fetch_uv_venv_${USER:-user}_$$"
info "Using temporary uv environment: ${VENV_DIR}"
rm -rf "${VENV_DIR}" || true

# Install Python 3.13 (uv will download it if needed)
run uv --color always python install 3.13

# Create the venv with Python 3.13
run uv --color always venv "${VENV_DIR}" --python 3.13

# Tell uv to use this venv for the project
export UV_PROJECT_ENVIRONMENT="${VENV_DIR}"

# ------------------------------------------------------------
# Sync dependencies (GUI extra) with verbose output
# ------------------------------------------------------------
info "Syncing dependencies using uv (with --extra gui)..."
run uv --color always sync --extra gui

# ------------------------------------------------------------
# Build using pyside6-deploy (verbose)
# ------------------------------------------------------------
info "Building with pyside6-deploy..."
run uv --color always run -- \
  pyside6-deploy -c src/build/pysidedeploy_linux.spec -f -v

# Rename output (same as before)
if [[ -f "Porn Fetch.bin" ]]; then
  run mv "Porn Fetch.bin" "PornFetch_Linux_GUI_x64.bin"
  ok "Build successful: $(pwd)/PornFetch_Linux_GUI_x64.bin"
else
  error "Build finished but output file 'Porn Fetch.bin' was not found!"
  exit 1
fi

ok "Done."

