# Push-to-fork checklist
1. User forks https://github.com/darktable-org/darktable on github.com (account willcoding11), renames it (e.g. wrenlight or final name), sends the link.
2. Update `darktable-fork/branding/brand.env` (BRAND_GH_REPO, BRAND_SITE, final BRAND_NAME), run `python branding/apply_brand.py --icons`, `python site/sync-installers.py`.
3. `cd darktable-fork && git remote add fork https://github.com/<user>/<repo>.git && git push fork lr-fork:main` (gh is already authed as willcoding11).
4. Repo Settings -> Pages -> Source: GitHub Actions. Settings -> Actions: allow workflows.
5. `git tag v0.1.0 && git push fork v0.1.0`; watch Actions; iterate on failures (see docs/CI.md).
6. Check release asset names match docs/SITE_AND_INSTALLERS.md; test install one-liners.
