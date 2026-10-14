# Defaults: module groups, shortcuts, presets

Nothing here has been compiled or run (no GTK/darktable build deps on the authoring PC). All of it is UNVERIFIED until CI builds and someone launches the app.

## 1. Module groups (src/libs/modulegroups.c)
- New shipped preset `workflow: basic, tone curve, color, detail, optics, effects` (write-protected, added in `init_presets`). It is also `FALLBACK_PRESET_NAME`, so it applies whenever the stored `plugins/darkroom/modulegroups_preset` is empty or names a missing preset (the schema default is empty, so fresh installs get it).
- Existing users keep whatever preset they already selected (their stored preset name is not overwritten). They can pick the new one from the module-group presets menu. No preset version bump needed: the module version stays 1 and the preset is a new name.
- Groups (icon in brackets): Basic [basic]: exposure, temperature, colorbalancergb, highlights, shadhi, crop, flip, ashift. Tone Curve [tone]: rgbcurve, tonecurve, toneequal, filmicrgb/sigmoid/agx (per workflow setting), basecurve, rgblevels. Color [color]: colorbalancergb, colorzones, colorequal, colorcorrection, velvia, channelmixerrgb, colorize, splittoning, monochrome. Detail [correct]: sharpen, diffuse, denoiseprofile, nlmeans, bilat, atrous, blurs. Optics [technical]: lens, ashift, cacorrect, cacorrectrgb, hazeremoval, liquify, retouch, hotpixels. Effects [effect]: vignette, grain, borders, enlargecanvas, watermark, bloom, soften, lowpass, graduatednd, overlay, censorize.
- Checked: every op name exists as a file in src/iop. A module may appear in two groups (colorbalancergb, ashift) which darktable allows.
- Review fix: the preset name originally contained "/" (risky in preset menus); renamed to the form above.
- Not verified: C compile (macros reuse the existing SQA/SMG/AM pattern); icon rendering; that deprecated/other modules not listed are still reachable via search and the "active modules" tab.

## 2. Keyboard shortcuts
darktable registers defaults in C (`dt_action_register` / `dt_shortcut_register`); `data/shortcutsrc` is only an optional import file. So defaults were changed in the registering source. Fresh configs get them; an existing user's `~/.config/darktable/shortcutsrc` overrides, so they may need Preferences > shortcuts > restore defaults.

| Lightroom concept | Key | darktable action | Status |
|---|---|---|---|
| Develop module | D | switch views > darkroom | already default |
| Library grid | G | lighttable "toggle filemanager layout" (src/libs/tools/lighttable.c) | changed (was unbound) |
| Library | L | switch views > lighttable | already default |
| Loupe | E | lighttable "preview" (hold/toggle; Shift+E ignores restriction) | changed (was F) |
| Compare/Survey | C | lighttable "toggle culling mode" (Shift+C unrestricted) | changed (was X) |
| Star ratings 1-5, 0 clear | 1-5, 0 | rating | already default |
| Reject | X | rating "reject" (src/libs/tools/ratings.c) | changed (was R) |
| Color labels red/yellow/green/blue | 6/7/8/9 | color label 1-4 (purple stays F5) | changed (were F1-F4) |
| Crop | R | crop module focus (src/iop/crop.c) | changed (was C) |
| Before/After | \ | snapshots "toggle last snapshot" (src/libs/snapshots.c) | changed (was unbound); needs a snapshot taken first |
| Zoom 100% | Z | darkroom "zoom close-up" (src/views/darkroom.c) | changed (was Alt+1) |
| Undo / Redo | Ctrl+Z / Ctrl+Y | undo / redo | already default (Ctrl+Shift+Z not added) |
| Export | Ctrl+Shift+E | export "start export" (src/libs/export.c) | changed (was Ctrl+E) |
| Fullscreen | F | global "fullscreen" (src/gui/gtk.c) | changed (was F11) |
| Hide side panels | Tab | panels "all" | already default |
| Copy / paste settings | Ctrl+Shift+C / Ctrl+Shift+V | copy/paste history (selective) | already default |
| Toolbar/filmstrip toggles | Ctrl+F / Ctrl+H | panels | darktable-native, kept |

Could not map (no equivalent action or conflict): Pick flag (P; darktable has no flag, P is the print view), Unflag (U), Select all Ctrl+A / Deselect Ctrl+D (darktable: Ctrl+A / Ctrl+Shift+A; Ctrl+D is duplicate), Shift+Tab hide all panels, Ctrl+[ ] rotate (darktable rotate has no default key), Shift+Z redo, N (survey), Y (before/after side by side; set snapshot side-by-side by button), T toolbar toggle, J clipping overlay (darktable: O / Shift+O), Ctrl+Shift+Z. Possible conflicts to test: F now fullscreen everywhere (the optional shortcutsrc import binds F+scroll to filmic, unaffected by a plain press), C/E/G are lighttable-only.

## 3. Presets
No editing presets (develop/styles) were added: darktable stores presets in the user database and generating valid binary module params by hand is unsafe. Shipping route if wanted later: export styles from a running build (Styles module > export) as .dtstyle files into `data/styles/` (installed to the share dir; already present in the tree) and import at first run. Module-group layout is the only preset shipped now.
