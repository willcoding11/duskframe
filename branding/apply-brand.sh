#!/bin/sh
# Apply branding/brand.env to the source tree. POSIX sh; python equivalent: apply_brand.py
# Usage: sh branding/apply-brand.sh [--dry-run] [--icons]
#
# The build (CMake, C code, installer templates, macOS scripts) reads brand.env
# directly. This script only rewrites the few static text files in MANAGED,
# replacing the values recorded in branding/.applied.env (what the files hold
# now) with the values from brand.env. Idempotent. --icons regenerates logo,
# icon and splash assets through make_icons.py (python3 + Pillow).
set -eu

HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(dirname "$HERE")
MANAGED="data/org.darktable.darktable.appdata.xml.in README.md"
DRY=0; ICONS=0
for a in "$@"; do
  case "$a" in --dry-run) DRY=1 ;; --icons) ICONS=1 ;; *) echo "unknown option $a" >&2; exit 2 ;; esac
done

# new values
. "$HERE/brand.env"
for v in BRAND_NAME BRAND_SLUG BRAND_ID BRAND_GH_USER BRAND_GH_REPO BRAND_SITE; do
  eval "[ -n \"\${$v:-}\" ]" || { echo "brand.env: $v missing" >&2; exit 1; }
done
N_NAME=$BRAND_NAME; N_SLUG=$BRAND_SLUG; N_ID=$BRAND_ID
N_USER=$BRAND_GH_USER; N_REPO=$BRAND_GH_REPO; N_SITE=$BRAND_SITE

# old values (as currently applied); empty if never applied
O_NAME=; O_SLUG=; O_ID=; O_USER=; O_REPO=; O_SITE=
if [ -f "$HERE/.applied.env" ]; then
  . "$HERE/.applied.env"
  O_NAME=$BRAND_NAME; O_SLUG=$BRAND_SLUG; O_ID=$BRAND_ID
  O_USER=$BRAND_GH_USER; O_REPO=$BRAND_GH_REPO; O_SITE=$BRAND_SITE
fi

esc_re()  { printf '%s' "$1" | sed 's/[][\.*^$/]/\&/g'; }
esc_rep() { printf '%s' "$1" | sed 's/[\&/]/\&/g'; }

# build a sed script: old -> placeholder (specific first), placeholder -> new
SCRIPT=$(mktemp)
trap 'rm -f "$SCRIPT"' EXIT
i=0
add() { # old new
  [ -n "$1" ] && [ "$1" != "$2" ] || return 0
  i=$((i+1))
  printf 's/%s/@@BRAND%d@@/g\n' "$(esc_re "$1")" "$i" >> "$SCRIPT"
  printf '%s\n' "$i|$2" >> "$SCRIPT.map"
}
rm -f "$SCRIPT.map"
if [ -f "$HERE/.applied.env" ]; then
add "$O_ID" "$N_ID"
add "$O_SITE" "$N_SITE"
add "$O_USER/$O_REPO" "$N_USER/$N_REPO"
add "$O_NAME" "$N_NAME"
add "$O_SLUG" "$N_SLUG"
add "$O_USER" "$N_USER"
fi
if [ -f "$SCRIPT.map" ]; then
  while IFS='|' read -r idx val; do
    printf 's/@@BRAND%s@@/%s/g\n' "$idx" "$(esc_rep "$val")" >> "$SCRIPT"
  done < "$SCRIPT.map"
  rm -f "$SCRIPT.map"
  for rel in $MANAGED; do
    f="$ROOT/$rel"
    # sed -b/-i differ between GNU and BSD; write to a temp file instead (keeps CRLF)
    sed -f "$SCRIPT" "$f" > "$f.brand.tmp"
    if cmp -s "$f" "$f.brand.tmp"; then rm -f "$f.brand.tmp"
    elif [ "$DRY" = 1 ]; then echo "brand: (dry) $rel"; rm -f "$f.brand.tmp"
    else mv "$f.brand.tmp" "$f"; echo "brand: $rel"; fi
  done
else
  echo "brand: files already match brand.env ($N_NAME)"
fi

if [ "$DRY" = 0 ]; then
  cat > "$HERE/.applied.env" <<EOT
# written by apply-brand; values currently present in the managed files
BRAND_NAME="$N_NAME"
BRAND_SLUG="$N_SLUG"
BRAND_ID="$N_ID"
BRAND_GH_USER="$N_USER"
BRAND_GH_REPO="$N_REPO"
BRAND_SITE="$N_SITE"
EOT
  if [ "$ICONS" = 1 ]; then
    PY=$(command -v python3 || command -v python) || { echo "python3 needed for --icons" >&2; exit 1; }
    "$PY" "$HERE/make_icons.py"
  fi
fi
echo "brand: done. Re-run cmake to pick up the new name in the binary."
