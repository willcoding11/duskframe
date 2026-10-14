#!/usr/bin/env python3
"""Generate the original app logo and every derived asset (needs Pillow only).

The logo (a setting sun in viewfinder brackets, flat colours) is defined once
as a list of vector primitives below; the same list is written to SVG and
rasterised with Pillow, so no SVG renderer is required.

Run: python3 branding/make_icons.py     (also run by apply-brand --icons)
Outputs go where the build/packaging expects them (see docs/REBRAND.md).
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from apply_brand import load_env  # noqa: E402

BRAND = load_env(os.path.join(HERE, "brand.env"))
NAME = BRAND["NAME"]

NAVY = "#1B2336"
SUN = "#F7B538"
CREAM = "#FFF4DC"
TAN = "#E3B873"
BRANCH = "#8A6A45"


# ---- the logo, 512x512 canvas -------------------------------------------
# last tuple item = min_px: shape is hidden when rendered smaller than that
def logo_shapes():
    # Duskframe: a setting sun on the horizon inside viewfinder corner brackets
    def box(x1, y1, x2, y2, c, m=0):
        return ("poly", [(x1, y1), (x2, y1), (x2, y2), (x1, y2)], 0, c, m)
    s = [("rrect", 0, 0, 512, 512, 112, "#2A1F4A", 0),
         box(0, 150, 512, 300, "#4B2F6B"), box(0, 300, 512, 340, "#8A3F6E"),
         ("circle", 256, 330, 120, "#FF9A3C", 0),
         box(0, 330, 512, 512, "#1B1530"),
         box(90, 352, 422, 366, "#FF9A3C", 48), box(130, 384, 382, 394, "#C8567A", 48),
         box(170, 410, 342, 418, "#8A3F6E", 48)]
    L, T, B, W = 78, 78, 434, 22   # viewfinder corners
    for (cx, cy, dx, dy) in [(L, T, 1, 1), (B, T, -1, 1), (L, B, 1, -1), (B, B, -1, -1)]:
        s.append(("line", cx, cy, cx + dx * 70, cy, W, "#FFE9C9", 0))
        s.append(("line", cx, cy, cx, cy + dy * 70, W, "#FFE9C9", 0))
    return s


def svg_of(shapes, size=512):
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="%d" height="%d">' % (size, size),
           '<title>%s logo</title>' % NAME]
    for sh in shapes:
        k = sh[0]
        if k == "rrect":
            _, x, y, w, h, r, f, _m = sh
            out.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s"/>' % (x, y, w, h, r, f))
        elif k == "circle":
            _, cx, cy, r, f, _m = sh
            out.append('<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (cx, cy, r, f))
        elif k == "ellipse":
            _, cx, cy, rx, ry, rot, f, _m = sh
            out.append('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" transform="rotate(%g %g %g)" fill="%s"/>'
                       % (cx, cy, rx, ry, rot, cx, cy, f))
        elif k == "poly":
            _, pts, rd, f, _m = sh
            out.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%g" stroke-linejoin="round"/>'
                       % (" ".join("%g,%g" % p for p in pts), f, f, 2 * rd))
        elif k == "line":
            _, x1, y1, x2, y2, w, f, _m = sh
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%g" '
                       'stroke-linecap="round"/>' % (x1, y1, x2, y2, f, w))
    out.append("</svg>")
    return "\n".join(out) + "\n"


def render(shapes, px, ss=4):
    """Rasterise the shapes at px x px using supersampling."""
    S = px * ss
    k = S / 512.0
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for sh in shapes:
        if px < sh[-1]:
            continue
        kind = sh[0]
        if kind == "rrect":
            _, x, y, w, h, r, f, _m = sh
            d.rounded_rectangle([x * k, y * k, (x + w) * k - 1, (y + h) * k - 1], r * k, fill=f)
        elif kind == "circle":
            _, cx, cy, r, f, _m = sh
            d.ellipse([(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k], fill=f)
        elif kind == "ellipse":
            _, cx, cy, rx, ry, rot, f, _m = sh
            th = math.radians(rot)
            pts = []
            for i in range(120):
                t = 2 * math.pi * i / 120
                ex, ey = rx * math.cos(t), ry * math.sin(t)
                pts.append(((cx + ex * math.cos(th) - ey * math.sin(th)) * k,
                            (cy + ex * math.sin(th) + ey * math.cos(th)) * k))
            d.polygon(pts, fill=f)
        elif kind == "poly":
            _, pts, rd, f, _m = sh
            sp = [(x * k, y * k) for x, y in pts]
            d.polygon(sp, fill=f)
            d.line(sp + [sp[0], sp[1]], fill=f, width=int(2 * rd * k), joint="curve")
            for x, y in sp:
                d.ellipse([x - rd * k, y - rd * k, x + rd * k, y + rd * k], fill=f)
        elif kind == "line":
            _, x1, y1, x2, y2, w, f, _m = sh
            d.line([x1 * k, y1 * k, x2 * k, y2 * k], fill=f, width=int(w * k))
            for x, y in ((x1, y1), (x2, y2)):
                d.ellipse([(x - w / 2) * k, (y - w / 2) * k, (x + w / 2) * k, (y + w / 2) * k], fill=f)
    return im.resize((px, px), Image.LANCZOS)


def font(size, bold=False):
    names = (["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"] if bold else
             ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"])
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    return ImageFont.load_default()


def wordmark_svg(w=640, h=128, fill=CREAM):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">\n'
            '<title>%s</title>\n'
            '<text x="0" y="%d" font-family="Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif" '
            'font-size="%d" font-weight="600" letter-spacing="2" fill="%s">%s</text>\n</svg>\n'
            % (w, h, w, h, NAME, int(h * 0.78), int(h * 0.9), fill, NAME))


def write(path, data):
    full = os.path.join(ROOT, *path.split("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(data)


def save(im, path, **kw):
    full = os.path.join(ROOT, *path.split("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    im.save(full, **kw)


def main():
    shapes = logo_shapes()
    svg = svg_of(shapes)
    write("branding/logo.svg", svg)
    for px in (512, 1024):
        save(render(shapes, px), "branding/logo-%d.png" % px)

    # icon theme sizes (icon name stays "darktable" internally, see REBRAND.md)
    for px in (16, 22, 24, 32, 48, 64, 256):
        save(render(shapes, px), "data/pixmaps/%dx%d/darktable.png" % (px, px))

    # Windows .ico (exe resource + installers) and png
    save(render(shapes, 128), "data/pixmaps/dt_logo_128x128.png")
    save(render(shapes, 256), "data/pixmaps/dt_logo_128x128.ico",
         sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (24, 24), (16, 16)])

    # splash / welcome logo button (seasonal variants are all the same logo)
    for name in ("idbutton", "idbutton-1", "idbutton-2", "idbutton-3"):
        # intrinsic size must stay 40x40 like upstream: the GUI draws it at native size
        write("data/pixmaps/%s.svg" % name, svg.replace('width="512" height="512"', 'width="40" height="40"', 1))
        save(render(shapes, 40), "data/pixmaps/%s.png" % name)
    write("data/pixmaps/darktable.svg", wordmark_svg())
    # header wordmark is drawn at native size too (upstream: 103 x 18)
    write("data/pixmaps/dt_text.svg",
          wordmark_svg().replace('width="640" height="128"', 'width="103" height="20.6"', 1))

    # macOS icns
    save(render(shapes, 1024), "packaging/macosx/Icons.icns",
         sizes=[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)])

    # splash image 860x280
    W, H = 860, 280
    sp = Image.new("RGBA", (W, H), NAVY)
    sp.alpha_composite(render(shapes, 200), (48, 40))
    d = ImageDraw.Draw(sp)
    d.text((290, 60), NAME, font=font(92, True), fill=CREAM)
    d.text((294, 168), "Photo editor and raw developer", font=font(28), fill=SUN)
    d.text((294, 212), "Based on darktable  |  GPL-3.0", font=font(20), fill=TAN)
    save(sp.convert("RGB"), "data/pixmaps/splashscreen.png")

    # macOS dmg background 1000x1000 (same layout as the upstream template)
    bg = Image.new("RGBA", (1000, 1000), "#6a6a6a")
    bg.alpha_composite(render(shapes, 64), (34, 24))
    d = ImageDraw.Draw(bg)
    d.text((112, 36), NAME, font=font(40, True), fill="#d9d9d9")
    d.line([(295, 203), (372, 203)], fill="#b0b0b0", width=9)
    d.line([(345, 178), (374, 203), (345, 229)], fill="#b0b0b0", width=9, joint="curve")
    d.text((65, 330), "To install drag the %s icon to the Applications folder" % NAME,
           font=font(23), fill="#f0f0f0")
    save(bg.convert("RGB"), "packaging/macosx/macos_install_background.png")
    write("data/pixmaps/macos_install_background.svg",
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">\n'
          '<rect width="1000" height="1000" fill="#6a6a6a"/>\n'
          '<text x="65" y="350" font-family="Helvetica, Arial, sans-serif" font-size="23" fill="#f0f0f0">'
          'To install drag the %s icon to the Applications folder</text>\n</svg>\n' % NAME)
    print("make_icons: wrote logo, icon sizes, .ico, .icns, splash for %s" % NAME)


if __name__ == "__main__":
    main()
