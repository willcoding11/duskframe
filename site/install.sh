#!/usr/bin/env bash
# Installer for macOS and Linux.  Usage: curl -fsSL <site>/install.sh | bash
# Flags: --uninstall  --dry-run   Env: BASE_URL (override download location)
set -euo pipefail

# ---- brand config (single place; site/sync-installers.py rewrites these from branding/brand.env) ----
BRAND_NAME="Wrenlight"      # @brand
BRAND_SLUG="wrenlight"      # @brand
GH_USER="willcoding11"      # @brand
GH_REPO="wrenlight"         # @brand
# -----------------------------------------------------------------------------------------------------

BASE_URL="${BASE_URL:-https://github.com/$GH_USER/$GH_REPO/releases/latest/download}"
DRY=0; UNINSTALL=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --uninstall) UNINSTALL=1 ;;
    -h|--help) sed -n '2,3p' "$0"; exit 0 ;;
    *) echo "Unknown option: $a" >&2; exit 2 ;;
  esac
done
# When piped from curl, pass flags with:  curl ... | bash -s -- --uninstall

say() { printf '==> %s\n' "$*"; }
run() { if [ "$DRY" = 1 ]; then printf '[dry-run] %s\n' "$*"; else "$@"; fi; }

os="$(uname -s)"; arch="$(uname -m)"
case "$arch" in arm64|aarch64) arch=arm64 ;; x86_64|amd64) arch=x86_64 ;; esac

TMP="$(mktemp -d)"
MNT=""
cleanup() {
  if [ -n "$MNT" ]; then hdiutil detach -quiet "$MNT" 2>/dev/null || true; fi
  rm -rf "$TMP"
}
trap cleanup EXIT

fetch() { # fetch <file>  -> $TMP/<file>
  say "Downloading $BASE_URL/$1"
  run curl -fSL --progress-bar -o "$TMP/$1" "$BASE_URL/$1"
}

install_macos() {
  local file="$BRAND_SLUG-macos-$arch.dmg" app="/Applications/$BRAND_NAME.app"
  [ "$arch" = arm64 ] || [ "$arch" = x86_64 ] || { echo "Unsupported CPU: $arch" >&2; exit 1; }
  if [ "$UNINSTALL" = 1 ]; then say "Removing $app"; run rm -rf "$app"; return; fi
  fetch "$file"
  if [ "$DRY" = 1 ]; then
    echo "[dry-run] hdiutil attach, copy *.app to /Applications, detach"; return
  fi
  MNT="$TMP/mnt"; mkdir -p "$MNT"
  hdiutil attach -nobrowse -readonly -quiet -mountpoint "$MNT" "$TMP/$file"
  local src; src="$(find "$MNT" -maxdepth 1 -name '*.app' | head -n1)"
  [ -n "$src" ] || { echo "No .app found in $file" >&2; exit 1; }
  say "Installing to $app"
  rm -rf "$app"
  ditto "$src" "$app"          # files fetched by curl carry no quarantine flag
  xattr -dr com.apple.quarantine "$app" 2>/dev/null || true
  say "Done. Open $BRAND_NAME from Launchpad or /Applications."
}

install_linux() {
  [ "$arch" = x86_64 ] || { echo "Only x86_64 Linux builds are published (you have $arch)." >&2; exit 1; }
  local file="$BRAND_SLUG-linux-x86_64.AppImage"
  local bin="$HOME/.local/bin/$BRAND_SLUG"
  local data="${XDG_DATA_HOME:-$HOME/.local/share}"
  local desktop="$data/applications/$BRAND_SLUG.desktop"
  local icon="$data/icons/hicolor/256x256/apps/$BRAND_SLUG.png"
  if [ "$UNINSTALL" = 1 ]; then
    say "Removing $BRAND_NAME"; run rm -f "$bin" "$desktop" "$icon"; return
  fi
  fetch "$file"
  run mkdir -p "$(dirname "$bin")" "$(dirname "$desktop")" "$(dirname "$icon")"
  run install -m 755 "$TMP/$file" "$bin"
  if [ "$DRY" = 1 ]; then echo "[dry-run] write $desktop and icon $icon"; return; fi
  # Best effort: pull the icon out of the AppImage; otherwise use a generic one.
  ( cd "$TMP" && "$bin" --appimage-extract .DirIcon >/dev/null 2>&1 &&
      cp -L squashfs-root/.DirIcon "$icon" ) 2>/dev/null || true
  local icon_val=camera-photo
  [ -f "$icon" ] && icon_val="$icon"
  cat > "$desktop" <<DESK
[Desktop Entry]
Type=Application
Name=$BRAND_NAME
Comment=Photo editor
Exec=$bin %F
Icon=$icon_val
Categories=Graphics;Photography;
MimeType=image/jpeg;image/png;image/tiff;
Terminal=false
DESK
  if command -v update-desktop-database >/dev/null; then
    update-desktop-database "$(dirname "$desktop")" 2>/dev/null || true
  fi
  say "Installed $bin (make sure ~/.local/bin is on your PATH)."
}

case "$os" in
  Darwin) install_macos ;;
  Linux)  install_linux ;;
  *) echo "Unsupported OS: $os. On Windows use install.ps1." >&2; exit 1 ;;
esac
