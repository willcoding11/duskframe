# CI / Release pipeline

Files (all in `darktable-fork/.github/workflows/`):
- `release.yml` - tag `v*` (or manual dispatch) builds everything and publishes a GitHub Release.
- `pages.yml` - deploys the `site/` folder to GitHub Pages on pushes to `lr-fork`/`main` touching `site/`.
- Upstream `nightly.yml`, `stale.yml`, `check-po.yml` are guarded with `github.repository == 'darktable-org/darktable'`, so they never run on the fork. `ci.yml` (plain build check) only runs on the fork via manual "Run workflow".

## Assets (stable names, slug read from `branding/brand.env`)
`<slug>-macos-arm64.dmg`, `<slug>-macos-x86_64.dmg`, `<slug>-windows-x64-setup.exe`, `<slug>-windows-x64-portable.zip` (single top-level folder `<slug>/` containing bin/ lib/ share/; run `<slug>/bin/darktable.exe`), `<slug>-linux-x86_64.AppImage`, plus `SHA256SUMS.txt`.
URLs: `https://github.com/<user>/<repo>/releases/latest/download/<file>` (prereleases, i.e. tags containing `-` like `v0.1.0-rc1`, are NOT served by `latest`).

## First run
1. Push the fork to GitHub (branch `lr-fork`, plus tags from upstream if you can: `git push origin --tags`).
2. Repo Settings -> Pages -> Source = **GitHub Actions** (one time). Settings -> Actions -> General: workflow permissions can stay "read"; the release job requests write itself.
3. Test build without releasing: Actions -> Release -> Run workflow (artifacts only, kept 7 days).
4. Release: `git tag v0.1.0 && git push origin v0.1.0`. Re-run for a failed tag: fix, then `git tag -d v0.1.0; git push origin :refs/tags/v0.1.0; git tag v0.1.0; git push origin v0.1.0` (or use "Re-run failed jobs").

## Design notes / decisions
- Windows installer is **Inno Setup** (what upstream actually uses: `darktable.iss.in` + `iscc`), not NSIS; the user sees the same thing, a single setup .exe. Portable zip is the plain install tree zipped before the icon/.iss files are added.
- macOS: runners `macos-15` (arm64) and `macos-15-intel` (x86_64). `macos-13` was retired Dec 2025; Intel runners end with the macos-15 image (~fall 2027), after which Intel builds must be dropped. Bundle is ad-hoc signed twice (upstream script, then `codesign --force --deep -s -`).
- Linux: ubuntu-22.04 (glibc 2.35) via upstream `tools/appimage-build-script.sh`; AppImage update info disabled (`DARKTABLE_APPIMAGE_UPDATE=no`) so it doesn't point at upstream.
- Version: upstream scripts use `git describe --match release-*`; checkout uses full history, and if no `release-*` tag exists a local tag `release-5.6.2` is created so scripts do not break. File names do not contain the version anyway.
- Actions are pinned to major versions; only the `release` job has `contents: write`.

## Expected failure points (first runs will probably need iteration)
- **Rebrand vs. packaging scripts**: macOS scripts hard-code `darktable` (app name `darktable.app`, `org.darktable`), Windows `.iss.in` has `MyAppName`, `darktable.exe`. The workflow uses globs for outputs, so renamed outputs are fine, but if the rebrand renames binaries/paths (e.g. `bin/darktable` -> `bin/<slug>`), update `packaging/macosx/*.sh`, `darktable.iss.in` and `tools/appimage-build-script.sh` (`org.darktable.darktable.desktop` path) accordingly.
- **Build time/limits**: each job may take 45-90 min; timeout is 180 min. macOS Homebrew `brew reinstall --build-from-source graphicsmagick` is slow.
- **Homebrew on Intel runner**: `.ci/Brewfile` is only exercised upstream on arm64; missing/changed formulae (note `brew bundle ... || true` hides failures) show up later as CMake or `cp` errors in the package script.
- **PPAs** (`ppa:savoury1/*`) occasionally break `apt-get update` on the Linux job; retry, or drop the PPA step and fall back to Ubuntu packages.
- **MSYS2 package drift**: a renamed pacman package fails `setup-msys2`; fix the pacboy list (compare with upstream `nightly.yml`). exiv2 0.27.7 is built from source as upstream does.
- **dmg creation** (`hdiutil` / Finder `osascript`) can fail intermittently; re-run the job.
- **Action versions**: majors used (checkout v7, upload/download-artifact v7/v8, softprops/action-gh-release v2, Pages configure v5 / upload v4 / deploy v4) were copied from upstream or are recent; if one does not exist, change the major.
- **Pages**: deploy fails with a 404 until Pages source is set to GitHub Actions; `site/` must exist and contain `index.html`.
- **Release job** fails with "MISSING <file>" if any platform did not produce its asset; nothing is published then.
- Nothing here has been executed (the fork is not on GitHub yet); only YAML-parsed and linted with actionlint (remaining notes are shellcheck style hints).
