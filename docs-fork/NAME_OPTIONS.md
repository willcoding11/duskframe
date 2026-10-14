# Name options for the darktable fork

Date: 2026-10-13. **This is not legal advice.** It is a quick, free, desk-level screen using web search (standard mode) plus an unauthenticated GitHub profile check. It did NOT query USPTO/EUIPO/WIPO databases directly, did not check domain registrars reliably, and nothing was registered. Before public launch, run a proper search (USPTO TESS/Trademark Search, EUIPO TMview, WIPO Global Brand Database) or ask a trademark attorney.

Constraints applied: not "darktable"; nothing resembling Lightroom / Adobe / Lumina-/Luminar-style names.

## Table

GitHub column: HTTP status of `github.com/<name>` (404 = no user/org with that handle; 200 = handle already taken by someone, which is not necessarily a photo project). Domains: the DNS check in this environment was inconclusive, so treat all domains as UNCHECKED; verify with a registrar whois.

| # | Name | Why it fits | Conflicts found (search) | Risk | GitHub handle |
|---|------|-------------|--------------------------|------|---------------|
| 0 | **Wrenlight** (current placeholder) | Small bird + light; friendly, calm, easy to say; clearly not Lightroom | No product, repo or app-store hit for "Wrenlight photo editor" in search ([results](https://www.lenovo.com/au/en/knowledgebase/comprehensive-guide-to-computer-photo-editing-software/) were unrelated). Ends in "-light" like many photo tools, but not confusable with Lightroom | **Low** | 404 (free) |
| 1 | **Aperline** | Aperture + line; photographic, short | No product or repo found for "Aperline" in photo/GitHub search. Looks like "Aperture" (Apple's discontinued app) only loosely | Low | 200 (taken, unrelated per search) |
| 2 | **Halation** | Film term for highlight glow; evocative | Name is a generic effect word used by many tools: [VSCO Halation](https://www.vsco.co/features/halation), [Halationify](https://mwm.ai/apps/halationify-analog-photos/6739345616), [FilmConvert Halation](https://www.filmconvert.com/plugin/halation), [Colourtone](https://apps.apple.com/us/app/-/id1383338239). Hard to trademark, hard to search for | **High** | 200 (taken) |
| 3 | **Emulsa** | From "emulsion" (film); short | No exact match, but crowded neighbours: [Emulsion (Mac photo library)](https://www.mactech.com/2015/06/02/emulsion-is-new-photo-library-app-for-mac-os-x/), [Emulsify](https://apps.apple.com/cn/app/id1408272207), Emulsio | Med | 404 (free) |
| 4 | **Duskframe** | Dusk + frame; moody, descriptive | No exact match found; only unrelated "photo frame" apps in results | Low | 200 (taken, unrelated per search) |
| 5 | **Sorrel** | Plant/reddish-brown horse colour; warm, one word | No photo editor found in search (results were RawTherapee, darktable, RapidRAW etc.). Very common English word and surname, so likely used in other software and trademark classes; not verified | Med | 200 (taken) |
| 6 | **Oakgrain** | Wood grain + film grain; sturdy, organic | No product found; film-grain apps exist ([Grain: Photo Editor](https://apps.apple.com/us/app/-/id6741040418), [GrainLab](https://apps.apple.com/app/id6630375395)) but names differ | Low | 404 (free) |
| 7 | **Plover** | Shore bird, pairs with Wren theme | No photo editor found in search, BUT "Plover" is a well-known open-source stenography program (Open Steno Project, from my own knowledge, not confirmed in this search); same OSS/desktop space | Med-High | 200 (taken) |
| 8 | **Kelvara** | Kelvin (colour temperature) + suffix; invented word | No software hit. Nearby marks: [KELVAR (cleaning products, USPTO)](https://www.trademarkelite.com/trademark/trademark-detail/71587413/KELVAR), [KELVA (India, Class 9 software)](https://www.registerkaro.in/trademark-search/kelva-5151441) | Med | 200 (taken) |

## Recommendation (top 3)

1. **Wrenlight** - lowest conflict signal, handle free, already the codename so renaming costs nothing. Keep it unless the team dislikes it.
2. **Oakgrain** - no conflicts found, handle free, distinctive; slightly less "light/photo" feeling.
3. **Duskframe** (runner-up: Aperline) - no conflicts found, descriptive of photography. GitHub handle is taken (use e.g. `duskframe-app` or an org name).

Avoid Halation (generic, many users) and Plover (known OSS project).

Next steps before committing: verify domains (.com/.org/.app) at a registrar, check the chosen name on USPTO and EUIPO TMview in classes 9 and 42, and search GitHub/Flathub/winget/Microsoft Store directly.

## How to rename

The codename lives only in `darktable-fork/branding/brand.env`. Edit the name value(s) there (e.g. the Wrenlight entry) and rebuild/re-apply branding as the project's branding script does. Nothing else should hard-code the name.
