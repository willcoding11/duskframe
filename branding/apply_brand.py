#!/usr/bin/env python3
"""Apply branding/brand.env to the source tree (python equivalent of apply-brand.sh).

Usage: python3 branding/apply_brand.py [--dry-run] [--icons]

The build itself (CMake, C code, installer templates, macOS scripts) reads
brand.env directly, so only the few static text files listed in MANAGED need
rewriting. The script replaces the values recorded in branding/.applied.env
(what is currently in the files) with the values from brand.env, then records
the new values. It is idempotent. --icons also regenerates all logo/icon/splash
assets via make_icons.py (needs Pillow).
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KEYS = ["ID", "SITE", "GH_REPO_PATH", "NAME", "SLUG", "GH_USER"]  # longest/most specific first

# files (relative to repo root) whose text contains the brand values
MANAGED = [
    "data/org.darktable.darktable.appdata.xml.in",
    "README.md",
]


def load_env(path):
    vals = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r'\s*BRAND_([A-Z_]+)=("([^"]*)"|\'([^\']*)\'|([^\s#]*))', line)
            if m:
                vals[m.group(1)] = next(g for g in m.group(3, 4, 5) if g is not None)
    if "GH_USER" in vals and "GH_REPO" in vals:
        vals["GH_REPO_PATH"] = vals["GH_USER"] + "/" + vals["GH_REPO"]
    return vals


def main(argv):
    dry = "--dry-run" in argv
    new = load_env(os.path.join(HERE, "brand.env"))
    for k in ("NAME", "SLUG", "ID", "GH_USER", "GH_REPO", "SITE"):
        if not new.get(k):
            sys.exit("brand.env: BRAND_%s missing" % k)
    state = os.path.join(HERE, ".applied.env")
    old = load_env(state) if os.path.exists(state) else {}
    pairs = {}
    for k in KEYS:
        if old.get(k) and new.get(k) and old[k] != new[k]:
            pairs[old[k]] = new[k]
    if not pairs:
        print("brand: files already match brand.env (%s)" % new["NAME"])
    else:
        pat = re.compile("|".join(re.escape(o) for o in sorted(pairs, key=len, reverse=True)))
        for rel in MANAGED:
            p = os.path.join(ROOT, *rel.split("/"))
            with open(p, encoding="utf-8", newline="") as f:
                s = f.read()
            t = pat.sub(lambda m: pairs[m.group(0)], s)
            if t != s:
                print("brand: %s%s" % ("(dry) " if dry else "", rel))
                if not dry:
                    with open(p, "w", encoding="utf-8", newline="") as f:
                        f.write(t)
    if not dry:
        with open(state, "w", encoding="utf-8", newline="\n") as f:
            f.write("# written by apply-brand; values currently present in the managed files\n")
            for k in ("NAME", "SLUG", "ID", "GH_USER", "GH_REPO", "SITE"):
                f.write('BRAND_%s="%s"\n' % (k, new[k]))
    if "--icons" in argv and not dry:
        subprocess.check_call([sys.executable, os.path.join(HERE, "make_icons.py")])
    print("brand: done. Rebuild (re-run cmake) to pick up the new name in the binary.")


if __name__ == "__main__":
    main(sys.argv[1:])
