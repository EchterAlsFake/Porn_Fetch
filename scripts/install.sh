#!/usr/bin/env bash
# Build the current source checkout, or clone it when run outside a checkout.
set -Eeuo pipefail
IFS=$'\n\t'

# Keep the old switch accepted; builds always show their full output.
for argument in "$@"; do
  case "$argument" in
    -v|--verbose) export PORN_FETCH_BUILD_VERBOSE=1 ;;
    -h|--help) echo "Usage: bash scripts/install.sh [--verbose]"; exit 0 ;;
    *) echo "Unknown option: $argument" >&2; exit 2 ;;
  esac
done
export PORN_FETCH_BUILD_VERBOSE=1
export PYTHONUNBUFFERED=1

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
if [[ -n "${NO_COLOR+x}" ]] || { [[ ! -t 1 && "${GITHUB_ACTIONS:-}" != true && "${FORCE_COLOR:-0}" == 0 ]]; }; then
  BOLD=""; DIM=""; RED=""; GREEN=""; YELLOW=""; BLUE=""; MAGENTA=""; CYAN=""; RESET=""
fi

info()    { echo -e "${CYAN}${BOLD}[INFO]${RESET} $*"; }
ok()      { echo -e "${GREEN}${BOLD}[ OK ]${RESET} $*"; }
warn()    { echo -e "${YELLOW}${BOLD}[WARN]${RESET} $*"; }
error()   { echo -e "${RED}${BOLD}[ERR ]${RESET} $*" >&2; }
cmd()     { echo -e "${MAGENTA}${BOLD}>>${RESET} ${DIM}$*${RESET}"; }

run() {
  # Authenticate directly so sudo retains its terminal for password prompts.
  if [[ "$1" == sudo ]]; then sudo -v || return $?; fi
  local command_log result
  command_log=$(mktemp "${TMPDIR:-/tmp}/pornfetch-build.XXXXXX")
  cmd "$*"
  info "Full log: $command_log"
  if "$@" 2>&1 | tee "$command_log"; then result=0; else result=$?; fi
  if [[ "$result" != 0 ]]; then
    error "Command failed (exit $result). Full log: $command_log"
    return "$result"
  fi
  return 0
}

# ------------------------------------------------------------
# OS detection
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
ARCH="$(uname -m 2>/dev/null || echo unknown)"

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

  info "uv not found. Installing via official installer..."
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
# Install system dependencies
# ------------------------------------------------------------
install_linux_build_deps() {
  if command -v pacman >/dev/null 2>&1; then
    info "Detected Arch Linux (pacman)"
    run sudo pacman -S --noconfirm --needed \
      base-devel git cmake curl pkgconf openssl libevent zlib mesa libxkbcommon-x11 libxcb
  elif command -v apt-get >/dev/null 2>&1; then
    info "Detected Debian/Ubuntu (apt)"
    run sudo apt-get update
    run sudo apt-get install -y \
      build-essential cmake python3-dev libssl-dev libevent-dev zlib1g-dev pkg-config \
      libegl1 libgles2 libxkbcommon-x11-0 libdbus-1-3 libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xinerama0 libxcb-xkb1 \
      git wget curl
  elif command -v dnf >/dev/null 2>&1; then
    info "Detected Fedora (dnf)"
    run sudo dnf install -y \
      git wget curl cmake gcc gcc-c++ make zlib-devel openssl-devel libevent-devel pkgconf-pkg-config \
      mesa-libEGL libxkbcommon-x11 xcb-util-cursor xcb-util-wm xcb-util-image xcb-util-keysyms xcb-util-renderutil
  elif command -v zypper >/dev/null 2>&1; then
    info "Detected openSUSE (zypper)"
    run sudo zypper refresh
    run sudo zypper install -y \
      git wget curl cmake gcc gcc-c++ make zlib-devel libopenssl-devel libevent-devel pkg-config \
      Mesa-libEGL1 libxkbcommon-x11-0 libxcb-cursor0
  else
    warn "No known Linux package manager detected. Continuing without system deps install."
  fi
}

ensure_macos_clt() {
  # Xcode Command Line Tools are required for compiling many Python deps
  if xcode-select -p >/dev/null 2>&1; then
    ok "Xcode Command Line Tools detected."
    return 0
  fi

  warn "Xcode Command Line Tools not found."
  info "Triggering installation (macOS will show a GUI dialog)..."
  xcode-select --install || true
  error "Please complete the Xcode Command Line Tools installation, then re-run this script."
  exit 1
}

install_macos_build_deps() {
  info "Setting up macOS build dependencies..."

  ensure_macos_clt

  if ! command -v brew >/dev/null 2>&1; then
    error "Homebrew not found."
    error "Install Homebrew first (https://brew.sh), then re-run this script."
    exit 1
  fi

  # Basics used by builds & fetch/update
  run env HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_UPGRADE=1 \
    brew install --verbose git cmake curl pkg-config make lz4

  ok "macOS build deps installed (or already present)."
}

main() {
  case "$OS" in
    darwin) install_macos_build_deps ;;
    *) install_linux_build_deps ;;
  esac
  install_uv_if_missing

  # Keep an existing checkout and its changes. Do not switch tags or pull over it.
  if [[ -f pyproject.toml && -f scripts/build_desktop.py ]]; then
    PROJECT_DIR="$PWD"
  elif [[ -n "${BASH_SOURCE[0]:-}" && -f "$(dirname "${BASH_SOURCE[0]}")/../scripts/build_desktop.py" ]]; then
    PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  else
    if [[ ! -d Porn_Fetch ]]; then
      run git clone https://github.com/EchterAlsFake/Porn_Fetch.git Porn_Fetch
    fi
    PROJECT_DIR="$PWD/Porn_Fetch"
  fi
  cd "$PROJECT_DIR"
  [[ -f scripts/build_desktop.py ]] || { error "This checkout is too old for this builder. Use its own tagged instructions."; return 1; }
  if ! run uv python install 3.15.2; then
    warn "Python 3.15.2 could not be installed. Updating uv's bundled Python catalog and retrying..."
    run uv self update
    run uv python install 3.15.2
  fi
  run uv sync --python 3.15.2 --upgrade --extra gui --extra build --extra desktop-build
  export UV_NO_SYNC=1
  uv run --no-sync python scripts/build_desktop.py
}

# Define the entire script before a child command can consume piped stdin.
main
