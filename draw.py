"""Draw the entry image for make.fun news-image-20261118.

A newspaper front page, "The Day in One Picture", for Wednesday
18 November 2026. Drawn with Pillow so every word and number is exact.
Output: entry.png (1024x1024) beside this script.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

FD = "/usr/share/fonts/truetype/liberation"
SANS = FD + "/LiberationSans-Regular.ttf"
SANSB = FD + "/LiberationSans-Bold.ttf"
SERIFB = FD + "/LiberationSerif-Bold.ttf"

W = H = 1024
BG = (246, 240, 224)        # newsprint cream
CARD = (255, 253, 245)
INK = (22, 19, 14)
MUTED = (96, 88, 70)
RED = (176, 40, 30)
BLUE = (29, 78, 137)
GOLD_D = (138, 109, 31)
GOLD_F = (227, 185, 60)
GREEN = (66, 110, 24)
WHITE = (255, 255, 255)


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, f):
    return d.textlength(s, font=f)


def fit_font(d, s, path, start, max_w, min_size=16):
    size = start
    while size > min_size:
        f = F(path, size)
        if tw(d, s, f) <= max_w:
            return f
        size -= 2
    return F(path, min_size)


def wrap(d, s, f, max_w):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if tw(d, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked(d, cx, y, s, f, tracking, fill):
    widths = [tw(d, ch, f) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, wch in zip(s, widths):
        d.text((x, y), ch, font=f, fill=fill)
        x += wch + tracking
    return total


def card(d, box, strip):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=CARD, outline=INK, width=2)
    d.rectangle([x0, y0, x1, y0 + 10], fill=strip)


def text_block(d, x, y, tag, tag_fill, headline_lines, sub, max_w,
               tag_size=22, head_size=36, sub_size=23, head_lh=42,
               sub_lh=28, head_fill=INK, sub_fill=(46, 41, 32)):
    f_tag = F(SANSB, tag_size)
    d.text((x, y), tag, font=f_tag, fill=tag_fill)
    y += tag_size + 10
    hs = head_size
    f_head = F(SANSB, hs)
    while hs > 24 and any(tw(d, ln, f_head) > max_w for ln in headline_lines):
        hs -= 2
        f_head = F(SANSB, hs)
    for line in headline_lines:
        d.text((x, y), line, font=f_head, fill=head_fill)
        y += head_lh
    y += 4
    f_sub = F(SANS, sub_size)
    for line in wrap(d, sub, f_sub, max_w):
        d.text((x, y), line, font=f_sub, fill=sub_fill)
        y += sub_lh
    return y


def icon_bars(d, box, color):
    x0, y0, x1, y1 = box
    base = y1 - 6
    bw = 13
    for i, h in enumerate((20, 36, 54)):
        bx = x0 + 4 + i * (bw + 7)
        d.rectangle([bx, base - h, bx + bw, base], fill=color)
    d.line([x0 + 2, base - 16, x1 - 12, y0 + 8], fill=color, width=5)
    ax, ay = x1 - 12, y0 + 8
    d.polygon([(ax, ay), (ax - 15, ay + 3), (ax - 4, ay + 14)], fill=color)
    d.line([x0, base + 2, x1 - 4, base + 2], fill=color, width=3)


def icon_gold(d, box):
    x0, y0, x1, y1 = box
    d.polygon([(x0 + 6, y0 + 52), (x0 + 54, y0 + 52), (x0 + 45, y0 + 36),
               (x0 + 15, y0 + 36)], fill=GOLD_F, outline=GOLD_D)
    d.polygon([(x0 + 15, y0 + 32), (x0 + 45, y0 + 32), (x0 + 38, y0 + 18),
               (x0 + 22, y0 + 18)], fill=GOLD_F, outline=GOLD_D)
    ax = x1 - 10
    d.line([ax, y0 + 6, ax, y0 + 44], fill=RED, width=6)
    d.polygon([(ax, y0 + 58), (ax - 9, y0 + 42), (ax + 9, y0 + 42)], fill=RED)


def icon_chip(d, box, color):
    x0, y0 = box[0], box[1]
    d.rectangle([x0 + 14, y0 + 14, x0 + 58, y0 + 58], outline=color, width=5)
    d.rectangle([x0 + 28, y0 + 28, x0 + 44, y0 + 44], fill=color)
    for i in range(3):
        p = x0 + 22 + i * 14
        d.line([p, y0 + 14, p, y0 + 3], fill=color, width=4)
        d.line([p, y0 + 58, p, y0 + 69], fill=color, width=4)
        q = y0 + 22 + i * 14
        d.line([x0 + 14, q, x0 + 3, q], fill=color, width=4)
        d.line([x0 + 58, q, x0 + 69, q], fill=color, width=4)


def hero_chart(d, box):
    x0, y0, x1, y1 = box
    for gy in (y0 + 34, y0 + 78, y0 + 122):
        x = x0 + 16
        while x < x1 - 6:
            d.line([x, gy, min(x + 8, x1 - 6), gy], fill=(196, 188, 168), width=2)
            x += 16
    d.line([x0 + 14, y0 + 8, x0 + 14, y1 - 18], fill=MUTED, width=3)
    d.line([x0 + 14, y1 - 18, x1 - 6, y1 - 18], fill=MUTED, width=3)
    pts = [(x0 + 26, y1 - 44), (x0 + 74, y1 - 62), (x0 + 122, y1 - 56),
           (x0 + 170, y1 - 106), (x0 + 214, y0 + 16)]
    d.line(pts, fill=RED, width=7, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 19, ey + 4), (ex - 6, ey + 19)], fill=RED)
    f = F(SANSB, 25)
    d.text((x0 + 24, y0 + 2), "%", font=f, fill=RED)


def gta_cell(img, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    top = (38, 18, 74)
    mid = (116, 44, 128)
    bot = (255, 118, 66)
    grad = Image.new("RGB", (1, h))
    for i in range(h):
        t = i / max(h - 1, 1)
        if t < 0.55:
            u = t / 0.55
            c = tuple(int(top[k] + (mid[k] - top[k]) * u) for k in range(3))
        else:
            u = (t - 0.55) / 0.45
            c = tuple(int(mid[k] + (bot[k] - mid[k]) * u) for k in range(3))
        grad.putpixel((0, i), c)
    img.paste(grad.resize((w, h)), (x0, y0))
    d = ImageDraw.Draw(img, "RGBA")
    # sun low over the skyline, right side
    sx, sy, r = x1 - 84, y1 - 50, 24
    d.ellipse([sx - r - 10, sy - r - 10, sx + r + 10, sy + r + 10],
              fill=(255, 190, 80, 90))
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 208, 64, 255))
    # skyline silhouette, kept to the bottom strip
    sil = (18, 9, 36)
    heights = [24, 36, 20, 42, 28, 50, 32, 22, 38, 26, 46, 30, 19, 34, 25]
    bx = x0
    for bh in heights:
        bw = w // len(heights) + 2
        d.rectangle([bx, y1 - bh, bx + bw, y1], fill=sil)
        bx += bw
    d.rectangle([x0, y1 - 14, x1, y1], fill=sil)
    # legibility panel behind the text
    d.rectangle([x0 + 12, y0 + 10, x1 - 12, y0 + 218], fill=(10, 5, 24, 128))
    d.rectangle(box, outline=INK, width=2)
    text_block(d, x0 + 24, y0 + 18, "GAMES · LAUNCH EVE", (255, 208, 64),
               ["GTA VI ARRIVES", "TOMORROW"],
               "Rockstar's most anticipated game ever launches Nov. 19, "
               "with Twitch braced for a record launch day.",
               w - 48, head_fill=WHITE, sub_fill=(240, 234, 255),
               head_lh=40, sub_size=22, sub_lh=26)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    tracked(d, W // 2, 30, "WORLD NEWS SUMMARY", F(SANSB, 25), 6, MUTED)
    f_date = fit_font(d, "WEDNESDAY, NOVEMBER 18, 2026", SERIFB, 68, W - 60)
    s = "WEDNESDAY, NOVEMBER 18, 2026"
    d.text(((W - tw(d, s, f_date)) / 2, 62), s, font=f_date, fill=INK)
    f_head = fit_font(d, "THE DAY IN ONE PICTURE", SERIFB, 54, W - 120)
    s2 = "THE DAY IN ONE PICTURE"
    d.text(((W - tw(d, s2, f_head)) / 2, 142), s2, font=f_head, fill=INK)
    d.line([36, 204, W - 36, 204], fill=INK, width=4)
    d.line([36, 211, W - 36, 211], fill=INK, width=1)

    # ---- hero: the Fed ----
    card(d, [36, 226, 988, 462], RED)
    hero_chart(d, [58, 268, 292, 446])
    text_block(d, 322, 248, "MONEY · WASHINGTON", RED,
               ["FED SIGNALS MORE RATE HIKES"],
               "Minutes of the Oct. 27-28 meeting: 'almost all' officials "
               "backed further hikes to fight 3.6% inflation. Markets price "
               "in a Dec. 9 hike - and stocks fell.",
               640, head_size=43, sub_size=27, head_lh=50, sub_lh=34)

    # ---- grid row 1 ----
    card(d, [36, 476, 506, 711], BLUE)
    icon_bars(d, [404, 512, 480, 588], BLUE)
    text_block(d, 54, 500, "TECHNOLOGY · IPO", BLUE,
               ["ANTHROPIC IPO:", "$83 A SHARE"],
               "Claude's maker priced above its $70-78 range, raising "
               "about $81B. Trades Nov. 19 on Nasdaq: ANT.",
               434)

    card(d, [518, 476, 988, 711], GOLD_D)
    icon_gold(d, [886, 512, 962, 588])
    text_block(d, 536, 500, "MARKETS · GOLD", GOLD_D,
               ["GOLD BREAKS", "BELOW $3,800"],
               "Down about 2.5% to near $3,742 - 33% below February's "
               "$5,595 peak as the dollar hit a 19-month high.",
               434)

    # ---- grid row 2 ----
    card(d, [36, 721, 506, 956], GREEN)
    icon_chip(d, [404, 757, 480, 833], GREEN)
    text_block(d, 54, 745, "CHIPS · EARNINGS", GREEN,
               ["NVIDIA BEATS,", "SHARES SLIP 2.9%"],
               "Sales of $115.8B beat forecasts in the first report under "
               "interim CEO Kress - yet shares slipped.",
               434)

    gta_cell(img, [518, 721, 988, 956])
    d = ImageDraw.Draw(img)

    # ---- footer ----
    f_foot = F(SANS, 22)
    s3 = "Five stories · One day · Wednesday, November 18, 2026"
    d.text(((W - tw(d, s3, f_foot)) / 2, 972), s3, font=f_foot, fill=MUTED)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
