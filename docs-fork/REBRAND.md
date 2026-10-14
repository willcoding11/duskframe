# Rebrand notes

Working codename: **Wrenlight** (placeholder). The name lives in one file: `darktable-fork/branding/brand.env`.

## How to rename (one-line change)

1. Edit `darktable-fork/branding/brand.env` (at minimum `BRAND_NAME`, `BRAND_SLUG`, `BRAND_ID`; also `BRAND_GH_USER`, `BRAND_GH_REPO`, `BRAND_SITE` when the repo/site change).
2. Run `sh branding/apply-brand.sh --icons` (POSIX) or `python branding/apply_brand.py --icons` (Windows). `--icons` regenerates the splash, dmg background and other name-bearing images (needs Pillow). `--dry-run` shows what would change.
3. Re-run CMake and rebuild.

Two mechanisms, so most of the tree never needs rewriting:
- **Read live from brand.env at build time** (nothing to apply): `cmake/Branding.cmake` (included from `DefineOptions.cmake`) turns it into `DT_BRAND_NAME/SLUG/ID/GH_USER/GH_REPO/SITE`. These feed `src/config.cmake.h` (`PACKAGE_NAME`, `PACKAGE_SLUG`, `PACKAGE_BRAND_SITE`), the `.desktop` file, the Inno Setup template, CPack/NSIS settings, and (by sourcing brand.env) the macOS bundle and dmg scripts.
- **Static text rewritten by apply-brand** (old values are tracked in `branding/.applied.env`, replaced by the new ones, idempotent, line endings preserved): `data/org.darktable.darktable.appdata.xml.in` and `README.md`.

## Decisions

- **CMake project name and binaries stay `darktable`** (`darktable.exe`, `darktable-cli`, `libdarktable`, icon theme name `darktable`, gettext domain, `org.darktable.darktable.*` source file names). Renaming those touches hundreds of paths and makes upstream merges painful. Only user-visible strings and identifiers change.
- **Config, cache and AI-model dirs are separate from darktable**: `~/.config/<slug>`, `~/.cache/<slug>`, `~/.local/share/<slug>/models` (Windows: `%APPDATA%\<slug>`, etc.), via `PACKAGE_SLUG` in `src/common/file_location.c`, `src/ai/backend_common.c`, `src/common/ai_models.c`. So both apps coexist with separate libraries and settings. Consequence: no automatic import of an existing darktable config (users can copy the folder by hand). Per-user *data* dirs for Lua scripts/styles etc. still follow darktable's own logic under the config dir.
- Installed `.desktop` and appdata files are renamed to `<BRAND_ID>.desktop` / `<BRAND_ID>.appdata.xml` at install time (`data/CMakeLists.txt`, `RENAME`). Source file names unchanged. The Windows installer AppId derives from the name, so it installs next to darktable; Explorer context-menu registry keys are suffixed with the name.
- GPL-3.0 and all upstream copyright headers are untouched. Credit is added in README (top section), About dialog (copyright line, comments text, license type GPL-3.0, "based on" credits section linking darktable), appdata developer line, installer publisher/copyright.
- "Help > darktable Manual" still points at the upstream manual on purpose (it documents the engine).

## Files touched

Source: `src/config.cmake.h`, `src/gui/about.c`, `src/gui/splash.c` (name as text label instead of darktable wordmark SVG), `src/gui/gtk.c` (window/header titles, Help > Homepage -> brand site), `src/gui/preferences.c`, `src/views/darkroom.c`, `src/views/view.c` (window titles), `src/common/file_location.c`, `src/ai/backend_common.c`, `src/common/ai_models.c`.
Build/packaging: `DefineOptions.cmake`, new `cmake/Branding.cmake`, `cmake/darktable-packaging.cmake`, `data/CMakeLists.txt`, `data/org.darktable.darktable.desktop.in`, `data/org.darktable.darktable.appdata.xml.in` (screenshots of darktable and its mailing-list contact removed), `packaging/windows/darktable.iss.in` (also fixes Quick Launch shortcut to use the exe name), `packaging/macosx/Info.plist` (`{BRAND_NAME}`/`{BRAND_ID}` placeholders), `packaging/macosx/3_make_hb_darktable_package.sh`, `4_make_hb_darktable_dmg.sh`, `generate-macos-app-icon.sh`.
New: `branding/apply-brand.sh`, `branding/apply_brand.py`, `branding/make_icons.py`, `branding/.applied.env`, `branding/logo.svg`, `branding/logo-512.png`, `branding/logo-1024.png`, `cmake/Branding.cmake`.
Generated art (all original, drawn from vector primitives in `make_icons.py`): `data/pixmaps/{16,22,24,32,48,64,256}*/darktable.png`, `data/pixmaps/dt_logo_128x128.{png,ico}`, `data/pixmaps/idbutton*.{svg,png}`, `data/pixmaps/darktable.svg` and `dt_text.svg` (text wordmarks), `data/pixmaps/splashscreen.png`, `data/pixmaps/macos_install_background.svg`, `packaging/macosx/Icons.icns`, `packaging/macosx/macos_install_background.png`.

## Logo

A flat wren (cocked tail) in front of a rising sun on a navy rounded square; rays are dropped below 48 px so it stays legible at 16 px. Edit shapes/colours in `branding/make_icons.py`, rerun it.

## Notes for other tracks

- Installer file name is now `<slug>-<version>-<arch>.exe` (was `darktable-...`). CI (`.github/`, owned by another track) must use the new name.
- The macOS app bundle is `<BRAND_NAME>.app`, the dmg `<BRAND_NAME>-<version>-<arch>.dmg`; the executable inside is still `darktable`.
- AppImage and Linux packaging (`packaging/AppImage`, arch, nix, opensuse, Solaris) were not renamed: they reference the unchanged binary. The AppImage file name is chosen by CI.

## Not verified / open

- No full C build was run (dependencies not present on this machine); C edits are small and syntax-reviewed only. CMake parsing of brand.env was tested with `cmake -P`.
- `.icns`/`.ico` written with Pillow; not opened on macOS/Windows shells.
- Translations: edited strings (e.g. About text) fall back to English because their msgids changed.
- The splash/welcome screens still use the existing CSS of the theme track for styling the name label.
