# Site and installers

Code: `darktable-fork/installers/` (install.sh, install.ps1) and `darktable-fork/site/` (index.html, config.js, sync-installers.py).

## Brand values
Single source: `branding/brand.env`. Run `python site/sync-installers.py`; it rewrites the `# @brand` lines at the top of both installers, generates `site/config.js` (read by index.html), and copies the installers into `site/` so Pages serves `<site>/install.sh` and `<site>/install.ps1`. Re-run before every Pages publish.

## Release asset names (CI must use exactly these)
`<slug>-macos-arm64.dmg`, `<slug>-macos-x86_64.dmg`, `<slug>-windows-x64-setup.exe` (NSIS, supports /S and /D=), `<slug>-windows-x64-portable.zip` (contains `<slug>.exe` somewhere inside; NSIS uninstaller `Uninstall.exe` in install dir), `<slug>-linux-x86_64.AppImage`. macOS app bundle must be named `<BRAND_NAME>.app`.

## Usage
- `curl -fsSL <site>/install.sh | bash`; uninstall: `... | bash -s -- --uninstall`; `--dry-run`; env `BASE_URL` overrides download location.
- `irm <site>/install.ps1 | iex`; with switches: `& ([scriptblock]::Create((irm <site>/install.ps1))) -Portable` (also `-Uninstall -DryRun -BaseUrl -InstallDir`). Installs to `%LOCALAPPDATA%\<name>`, no admin.

## Tested
shellcheck clean; install.ps1 parses with no errors (PSScriptAnalyzer not available). Against a local mock release (python http.server): Linux install/uninstall into a temp HOME (uname shimmed, Git Bash) and Windows `-Portable` install/uninstall into a temp dir passed. Not tested: the macOS branch (needs hdiutil) and the NSIS silent path; test them on real builds.

Screenshots: `docs/screenshots/site-desktop.png`, `site-mobile.png`.
