# Project Plan: darktable Fork (name TBD)

A free, open-source photo editor forked from darktable, re-skinned to feel cleaner and closer to Lightroom. It keeps darktable's editing engine and changes the look, defaults and branding. A GitHub Pages site detects the visitor's OS and hands them the right installer.

## Decisions so far
- Approach: Full fork of darktable (not just a theme pack)
- Mac signing: Unsigned for now; must stay easy to install
- Install methods: Terminal one-liner on all 3 OSes (Linux: only way)
- Distribution: GitHub Releases + GitHub Pages download site
- Build system: GitHub Actions, adapted from darktable's own CI

## Open questions
- Name. Can't use 'darktable', or anything close to 'Lightroom' (Adobe trademark).
- GitHub account. willcoding11? Will forks darktable-org/darktable on github.com, renames it and sends the link. Claude can't create the fork, only push to it.

## What can be changed
| Layer | Examples | Needs rebuild |
| Theme (CSS) | Colors, fonts, spacing, sliders, buttons | No |
| Config | Module set and order, presets, defaults | No |
| Shortcuts | Lightroom-style key bindings | No |
| Lua scripts | Extra buttons, small custom tools | No |
| C source | Panel layout, icons (drawn in code), widgets | Yes |
| Branding | Name, app icon, splash, About screen | Yes |
Since this is a fork, all of these ship baked into the installer. No separate theme install.

## v1 scope
- Lightroom-style theme: colors, typography, spacing, slider styling
- Default module set grouped like Lightroom: Basic, Tone Curve, Color, Detail, Optics, Effects
- Lightroom-like presets and keyboard shortcuts out of the box
- Rebrand: name, app icon, splash screen, About screen
- CI builds: Windows .exe installer; macOS .dmg for Apple Silicon and Intel; Linux AppImage
- Builds attached to GitHub Releases on each tagged version
- GitHub Pages site with OS detection and download buttons

## v2 (after builds are stable)
- Layout changes: panel positions, Lightroom-style filmstrip and toolbar
- New icon set (requires C changes, since icons are drawn in code)
- Optional: paid Apple signing and notarization ($99/yr)

## How distribution works
1. Push a version tag (e.g. v0.1.0).
2. GitHub Actions builds all platforms and uploads to a Release.
3. The Pages site links to stable URLs of the form github.com/<user>/<repo>/releases/latest/download/<file>, so the site never needs editing per release.
4. JavaScript on the page reads the OS and highlights the right button. All other platforms stay listed below it.
Mac caveat: a browser can't reliably tell Apple Silicon from Intel, so the site shows both Mac downloads (Apple Silicon first).

## Installing (unsigned)
Every platform gets a copy-paste terminal command on the Pages site, with a copy button. Mac and Windows also keep a normal download button.
| macOS | curl -fsSL <site>/install.sh | bash | .dmg (Settings trip, below) |
| Windows | irm <site>/install.ps1 | iex | .exe (SmartScreen prompt) |
| Linux | curl -fsSL <site>/install.sh | bash | None; terminal only |
Why the terminal route skips the warnings:
- macOS: files fetched by curl aren't quarantined, so Gatekeeper never checks them. No 'Open Anyway' trip.
- Windows: files fetched by PowerShell don't get the 'downloaded from the internet' mark, so SmartScreen doesn't prompt.
What each script does:
- macOS: detects Apple Silicon vs Intel itself (solving the browser problem above), downloads the right build, copies the app to /Applications.
- Windows: downloads the installer and runs it silently, or unpacks a portable build to the user's AppData. No admin needed for the latter.
- Linux: downloads the AppImage to ~/.local/bin, makes it executable, adds a desktop entry and icon so it shows in the app menu.
All scripts share one uninstall path and pull from releases/latest, so they never need editing per release.
Download-button caveat on macOS: since macOS 15 (Sequoia), the old right-click -> Open bypass no longer works for unsigned apps. Users who pick the .dmg must go to System Settings -> Privacy & Security -> Open Anyway. The site says this next to the button and recommends the terminal command.
Apple Silicon builds must be ad-hoc signed (codesign -s -) or they won't launch at all. This is free and CI handles it.

## Licensing
- darktable is GPL-3.0, so the fork must stay open source under GPL-3.0.
- Keep the original copyright notices; credit darktable in README and About.
- Use a distinct name and icon so it isn't confused with darktable.

## Work plan (parallel agents)
| Theme | Lightroom-style CSS theme, set as default |
| Defaults | Module groups, presets, shortcuts |
| Rebrand | Name, icon, splash, About, app identifiers |
| CI | Adapt darktable workflows for 3 platforms + Releases |
| Pages site | Download page with OS detection and copy-able commands |
| Installers | install.sh (macOS + Linux) and install.ps1 (Windows) |
Screenshots at each milestone: theme first look, first green build per platform, Pages site live.

## Risks
- CI is the slow part. darktable has many dependencies and multi-OS builds take a while to get green.
- Upstream drift. Pulling in new darktable releases means merging their changes into ours. Keeping our edits mostly in theme and config files keeps merges cheap.
- macOS install friction for users who skip the terminal command.
- Script trust. Piping a script into a shell runs whatever the server sends. Serve scripts only from the repo's own Pages site and keep them short and readable so users can check them first.
