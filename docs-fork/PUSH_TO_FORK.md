# Fork status (done 2026-10-13)
- Name: Duskframe (brand.env). Fork: https://github.com/willcoding11/duskframe (created with gh, fork-name duskframe).
- Local remote `fork`; branch lr-fork pushed and set as the fork's DEFAULT branch (so workflow_dispatch works). Actions enabled via API.
- Pages workflow is manual-only and Pages is NOT enabled. No tag, no Release.
- Run builds: `gh workflow run release.yml -R willcoding11/duskframe --ref lr-fork` (artifacts only, no Release).
## Needs user OK
1. Enable Pages: repo Settings -> Pages -> Source: GitHub Actions, then run the Pages workflow (or restore its push trigger).
2. First Release: `git tag v0.1.0 && git push fork v0.1.0` (creates a public Release with all 5 assets).
