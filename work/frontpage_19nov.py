#!/usr/bin/env python3
"""news-image-20261119 — front page generator (written fresh in this session).

One 1024x1024 newspaper front page summing up world news of
Thursday 19 November 2026. Flat PIL drawing only, no external images.
All facts are the 19 Nov consensus verified against live roundups
(Pollar / Digesta / Level Headlines, 20 Nov 2026): Shenzhen declaration,
ICJ Myanmar 9-6, COP31 draft, Anthropic $81.3bn IPO, GTA VI launch,
Cyclone Akvan, Kerch bridge, plus 20 verified briefs.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (253, 248, 238)      # paper
INK = (20, 20, 20)
RED = (178, 34, 34)
DARK = (31, 41, 55)
LIME = (163, 230, 53)
TEAL = (34, 139, 139)
GOLD = (184, 134, 11)
GREY = (90, 90, 90)
LINE = (120, 110, 95)
GREEN = (22, 120, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap to pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, font, fill=INK, lh=None):
    lh = lh or int(font.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def tag(draw, x, y, text, fill=GREEN):
    """Small credibility tag, returns width used."""
    font = f(SANS_B, 10)
    w = int(draw.textlength(text, font=font)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    draw.text((x + 5, y + 2), text, font=font, fill=(255, 255, 255))
    return w


def rule(draw, x0, y, x1, wdt=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=wdt)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
MX = 16                      # margin
CW = W - 2 * MX              # 992 content width

# ---------------------------------------------------------------- masthead
d.text((MX, 10), "THE WORLD IN ONE PAGE  •  EST. 2026  •  FREE",
       font=f(SANS_B, 11), fill=GREY)
d.text((W - MX - 190, 10), "No. 323  •  PRICE: FREE", font=f(SANS_B, 11), fill=GREY)
d.text((MX + 118, 26), "THE WORLD TODAY", font=f(SERIF_B, 62), fill=INK)
rule(d, MX, 96, W - MX, 3)
d.text((MX, 102), "THURSDAY 19 NOVEMBER 2026", font=f(SERIF_B, 21), fill=RED)
d.text((MX + 400, 105), "33 STORIES  •  7 REGIONS  •  ONE DAY, THE WHOLE WORLD",
       font=f(SANS_B, 13), fill=INK)
rule(d, MX, 128, W - MX, 1, fill=LINE)

# ---------------------------------------------------------------- region strip
d.rectangle([MX, 134, W - MX, 158], fill=DARK)
regions = [("ASIA", 6), ("EUROPE", 7), ("AMERICAS", 6), ("MIDEAST", 4),
           ("AFRICA", 4), ("OCEANIA", 3), ("GLOBAL", 3)]
rx = MX + 10
for name, n in regions:
    t = f"{name} {n}"
    d.text((rx, 140), t, font=f(SANS_B, 13), fill=(255, 255, 255))
    rx += int(d.textlength(t, font=f(SANS_B, 13))) + 34
d.text((W - MX - 150, 140), "33 STORIES TOTAL", font=f(SANS_B, 13), fill=LIME)

# ---------------------------------------------------------------- lead panels
LEAD_Y, LEAD_H, LEAD_W, GAP = 166, 268, 324, 12
leads = [
    dict(kick="SHENZHEN  •  DIPLOMACY", scene="shenzhen",
         head="THREE POWERS,\nONE DECLARATION",
         body=("Trump, Xi and Putin meet for 70 minutes at Kylin Villa, "
               "Shenzhen — the first trilateral summit of the US, China "
               "and Russia — and sign a Declaration toward Peace. "
               "No deal on Ukraine or Iran."),
         src="Sources: AP, Reuters"),
    dict(kick="THE HAGUE  •  WORLD COURT", scene="court",
         head="COURT: MYANMAR\nCOMMITTED GENOCIDE",
         body=("The ICJ rules 9–6 that Myanmar committed genocide "
               "against the Rohingya in 2017 — the first time the court "
               "has held a state responsible for genocide. "
               "Return and reparations ordered."),
         src="Sources: UN News, BBC"),
    dict(kick="ANTALYA  •  CLIMATE", scene="cop",
         head="COP31 DRAFT DROPS\nFOSSIL PHASE-OUT",
         body=("The second draft text in Antalya removes the call to "
               "phase out fossil fuels, as divisions remain. A $120bn "
               "adaptation-aid target is on the table. "
               "Negotiators await a new draft."),
         src="Sources: Reuters, AP"),
]


def scene_shenzhen(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 245))
    d.ellipse([x + w - 52, y + 8, x + w - 16, y + 44], fill=(240, 180, 60))
    # skyline
    for bx, bw, bh in [(0, 46, 62), (52, 38, 84), (96, 52, 58), (154, 40, 92),
                       (200, 44, 66), (250, 46, 80), (286, 22, 52)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=DARK)
        for wy in range(y + h - bh + 8, y + h - 6, 14):
            for wx in range(x + bx + 6, x + bx + bw - 6, 12):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(250, 220, 120))
    # three flags on poles
    cols = [(178, 34, 34), (200, 30, 30), (30, 60, 160)]
    for i, c in enumerate(cols):
        fx = x + 24 + i * 26
        d.line([(fx, y + 6), (fx, y + 34)], fill=INK, width=2)
        d.rectangle([fx, y + 6, fx + 20, y + 18], fill=c)


def scene_court(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 224, 205))
    # pediment + columns
    d.polygon([(x + 20, y + 52), (x + w // 2, y + 12), (x + w - 20, y + 52)],
              fill=(120, 100, 70))
    d.ellipse([x + w // 2 - 12, y + 22, x + w // 2 + 12, y + 46], fill=GOLD)
    for cx in range(x + 34, x + w - 30, 62):
        d.rectangle([cx, y + 52, cx + 16, y + h - 8], fill=(245, 240, 225),
                    outline=INK, width=1)
    d.rectangle([x + 14, y + h - 10, x + w - 14, y + h], fill=(90, 75, 55))
    # scales of justice, small, bottom right
    sx, sy = x + w - 78, y + h - 52
    d.line([(sx, sy), (sx, sy - 26)], fill=INK, width=2)
    d.line([(sx - 22, sy - 26), (sx + 22, sy - 26)], fill=INK, width=2)
    d.polygon([(sx - 30, sy - 8), (sx - 14, sy - 8), (sx - 22, sy + 2)],
              fill=GOLD, outline=INK)
    d.polygon([(sx + 14, sy - 8), (sx + 30, sy - 8), (sx + 22, sy + 2)],
              fill=GOLD, outline=INK)


def scene_cop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 235, 220))
    cx, cy, r = x + w // 2, y + h // 2 + 6, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 160, 200),
              outline=INK, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=1)
    d.arc([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], 20, 160,
          fill=(255, 255, 255), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=(255, 255, 255), width=2)
    # leaf
    d.ellipse([x + 18, y + 12, x + 62, y + 44], fill=GREEN)
    d.line([(x + 20, y + 42), (x + 60, y + 14)], fill=(255, 255, 255), width=2)
    d.ellipse([x + w - 52, y + 10, x + w - 14, y + 48], fill=(240, 180, 60))
    d.text((x + w - 46, y + 18), "$120", font=f(SANS_B, 12), fill=INK)
    d.text((x + w - 40, y + 33), "bn", font=f(SANS_B, 10), fill=INK)


scenes = {"shenzhen": scene_shenzhen, "court": scene_court, "cop": scene_cop}

for i, L in enumerate(leads):
    x = MX + i * (LEAD_W + GAP)
    d.rectangle([x, LEAD_Y, x + LEAD_W, LEAD_Y + LEAD_H], outline=INK, width=2)
    d.rectangle([x, LEAD_Y, x + LEAD_W, LEAD_Y + 22], fill=RED)
    d.text((x + 8, LEAD_Y + 4), L["kick"], font=f(SANS_B, 11), fill=(255, 255, 255))
    scenes[L["scene"]](x + 6, LEAD_Y + 28, LEAD_W - 12, 92)
    hy = LEAD_Y + 128
    for ln in L["head"].split("\n"):
        d.text((x + 8, hy), ln, font=f(SERIF_B, 21), fill=INK)
        hy += 26
    by = draw_lines(d, wrap(d, L["body"], f(SANS, 12), LEAD_W - 16),
                    x + 8, hy + 4, f(SANS, 12), lh=16)
    d.text((x + 8, LEAD_Y + LEAD_H - 22), L["src"], font=f(SANS, 10), fill=GREY)
    tag(d, x + LEAD_W - 82, LEAD_Y + LEAD_H - 24, "REPORTED")

# ---------------------------------------------------------------- hours strip
HY = 442
d.rectangle([MX, HY, W - MX, HY + 34], fill=(255, 243, 205), outline=INK, width=1)
d.text((MX + 8, HY + 9), "THE DAY BY HOURS", font=f(SANS_B, 12), fill=RED)
hours = [("04:34", "ICJ rules"),
         ("06:16", "Shenzhen declaration"),
         ("19:12", "GTA VI UK launch"),
         ("23:19", "Anthropic +17%")]
hx = MX + 168
for t, what in hours:
    d.text((hx, HY + 9), t, font=f(SANS_B, 11), fill=INK)
    hx += int(d.textlength(t, font=f(SANS_B, 11))) + 6
    d.text((hx, HY + 9), what, font=f(SANS, 11), fill=INK)
    hx += int(d.textlength(what, font=f(SANS, 11))) + 16

# ---------------------------------------------------------------- grid 4-13
GY, GH = 484, 208
d.text((MX, GY), "THE DAY IN TEN", font=f(SERIF_B, 17), fill=INK)
rule(d, MX + 170, GY + 10, W - MX, 1, fill=LINE)
grid = [
    ("4", "ANTHROPIC IPO SMASHES RECORD",
     "Priced at $83, raises $81.3bn — the biggest IPO ever; shares +17%."),
    ("5", "GTA VI IS FINALLY HERE",
     "Launches worldwide after 13 years; 15.9m pre-orders. PS5/Xbox, no PC."),
    ("6", "CYCLONE AKVAN NEARS INDIA",
     "More than 80,000 evacuated in Odisha as the storm nears the coast."),
    ("7", "UKRAINE HITS KERCH BRIDGE AGAIN",
     "Third strike on the Crimea bridge in a week; traffic halted."),
    ("8", "SEOUL COURT FREES EX-PM HAN",
     "South Korea's high court clears former PM Han Duck-soo."),
    ("9", "AUSTRALIA JOBLESS RATE 4.9%",
     "Unemployment climbs to 4.9% as hiring slows."),
    ("10", "COLOMBIA UNIONS STRIKE",
     "National strike brings marches to Bogotá and cities nationwide."),
    ("11", "KENYA MARATHON CHAMP BANNED",
     "Champion runner banned for three years over doping."),
    ("12", "DENMARK BACKS ARCTIC PACT",
     "Parliament backs the Arctic pact with the US, 109–0."),
    ("13", "MISSILE DAMAGES RIYADH TOWER",
     "Suspected Houthi missile strikes the PIF Tower in Riyadh."),
]
row_h = 37
for i, (num, head, body) in enumerate(grid):
    col, row = i % 2, i // 2
    gx = MX + col * (CW // 2 + 8)
    gy = GY + 26 + row * row_h
    d.rectangle([gx, gy, gx + 24, gy + 24], fill=DARK)
    d.text((gx + 7, gy + 4), num, font=f(SANS_B, 13), fill=(255, 255, 255))
    d.text((gx + 30, gy), head, font=f(SANS_B, 12), fill=INK)
    body_font = f(SANS, 11)
    max_bw = CW // 2 - 40
    while d.textlength(body, font=body_font) > max_bw and len(body) > 10:
        body = body[:-2]
    d.text((gx + 30, gy + 16), body, font=body_font, fill=(60, 60, 60))

# ---------------------------------------------------------------- middle row
MY, MH = 700, 96
bw3 = (CW - 24) // 3
# bar chart
bx = MX
d.rectangle([bx, MY, bx + bw3, MY + MH], outline=INK, width=1)
d.text((bx + 8, MY + 6), "THE DAY BY FIELD", font=f(SANS_B, 12), fill=RED)
fields = [("Diplomacy", 9), ("Markets", 6), ("Climate", 5),
          ("Conflict", 5), ("Tech", 4), ("Sport", 4)]
fy = MY + 26
for name, n in fields:
    d.text((bx + 8, fy), name, font=f(SANS, 10), fill=INK)
    d.rectangle([bx + 78, fy + 2, bx + 78 + n * 20, fy + 10], fill=TEAL)
    d.text((bx + 78 + n * 20 + 5, fy), str(n), font=f(SANS_B, 10), fill=INK)
    fy += 11
# verdict
vx = MX + bw3 + 12
d.rectangle([vx, MY, vx + bw3, MY + MH], outline=INK, width=1)
d.text((vx + 8, MY + 6), "THE VERDICT", font=f(SANS_B, 12), fill=RED)
draw_lines(d, wrap(d, "Myanmar must allow the Rohingya to return and pay "
                      "reparations — ICJ, 9–6. Shenzhen: peace declared, "
                      "the wars untouched.", f(SANS, 11), bw3 - 16),
           vx + 8, MY + 26, f(SANS, 11), lh=15)
# markets
kx = MX + 2 * (bw3 + 12)
d.rectangle([kx, MY, kx + bw3, MY + MH], outline=INK, width=1)
d.text((kx + 8, MY + 6), "MARKETS & MONEY", font=f(SANS_B, 12), fill=RED)
for j, ln in enumerate(["ANT $83  •  +17% on debut",
                        "IPO raises $81.3bn — record",
                        "GTA VI $79.99  •  Aus jobless 4.9%"]):
    d.text((kx + 8, MY + 28 + j * 20), ln, font=f(SANS, 12), fill=INK)

# ---------------------------------------------------------------- briefs 14-33
BY = 804
d.text((MX, BY), "ALSO ON…", font=f(SERIF_B, 17), fill=INK)
d.text((MX + 120, BY + 4), "20 more stories from Thursday, in brief",
       font=f(SANS, 11), fill=GREY)
rule(d, MX + 380, BY + 10, W - MX, 1, fill=LINE)
briefs = [
    ("14", "Ethiopia–Eritrea troops mass on the border; war fears grow."),
    ("15", "North Korea expands its Yongbyon uranium plant, IAEA says."),
    ("16", "US signs military cooperation deal with Venezuela in Caracas."),
    ("17", "Magnitude 5.7 quake hits Kumamoto, Japan; two people injured."),
    ("18", "Bangladesh switches on its Russian-built nuclear plant."),
    ("19", "Israel delays the E1 West Bank settlement project."),
    ("20", "Spain: snap election 29 Nov; migrants drove half of growth since 2022."),
    ("21", "Fiji declares a disaster as drought bites."),
    ("22", "Migrant boat capsizes off Senegal; many feared dead."),
    ("23", "France protests: about 15,000 people arrested."),
    ("24", "US measles: eighth death recorded in Pennsylvania."),
    ("25", "Judge lets Trump's $15bn defamation suit against NYT proceed."),
    ("26", "Trump asks Supreme Court to let EPA cancel $16bn climate grants."),
    ("27", "SoftBank's Son: missing Anthropic before its IPO was a 'mistake'."),
    ("28", "GTA VI ties a Metacritic record on launch day."),
    ("29", "Seoul: 551,864 students sit the national college exam."),
    ("30", "Jakarta: asset-seizure bill moves forward in parliament."),
    ("31", "Hormuz: three tankers ablaze after hitting naval mines — CLAIM."),
    ("32", "Gaza: Israeli ground operation continues."),
    ("33", "Riyadh hosts US CENTCOM talks; new Hezbollah finance sanctions."),
]
brow = 12
for i, (num, txt) in enumerate(briefs):
    col, row = i % 2, i // 2
    bx2 = MX + col * (CW // 2 + 8)
    by2 = BY + 24 + row * brow
    d.text((bx2, by2), num + ".", font=f(SANS_B, 10), fill=RED)
    d.text((bx2 + 24, by2), txt, font=f(SANS, 10), fill=INK)

# ---------------------------------------------------------------- footer
FY = 960
rule(d, MX, FY, W - MX, 2)
# date check box
d.rectangle([MX, FY + 8, MX + 470, FY + 58], fill=(255, 243, 205),
            outline=INK, width=1)
d.text((MX + 8, FY + 13), "DATE CHECK", font=f(SANS_B, 11), fill=RED)
draw_lines(d, wrap(d, "Left out on purpose: stories dated before 13 Nov 2026 — "
                      "earlier COP31 drafts, last week's bridge attacks. "
                      "Everything on this page is 19 Nov.",
                   f(SANS, 10), 454), MX + 8, FY + 28, f(SANS, 10), lh=13)
# mini world map
mx0, my0 = MX + 486, FY + 8
d.text((mx0, FY + 10), "WHERE IT HAPPENED", font=f(SANS_B, 10), fill=INK)
# rough continents (dots grid style)
d.rectangle([mx0, FY + 24, mx0 + 210, FY + 56], fill=(225, 238, 245),
            outline=LINE, width=1)
land = [(8, 8, 34, 12), (40, 4, 60, 14), (66, 10, 92, 16), (100, 6, 130, 12),
        (136, 12, 168, 18), (172, 18, 198, 26), (96, 20, 120, 28),
        (150, 26, 168, 30)]
for (x0, y0, x1, y1) in land:
    d.ellipse([mx0 + x0, FY + 24 + y0, mx0 + x1, FY + 24 + y1], fill=(150, 180, 160))
for (dx, dy) in [(52, 10), (120, 12), (160, 14), (96, 22), (180, 22), (30, 14)]:
    d.ellipse([mx0 + dx - 3, FY + 24 + dy - 3, mx0 + dx + 3, FY + 24 + dy + 3],
              fill=RED, outline=(255, 255, 255), width=1)
# sources + legend
sx0 = MX + 712
d.text((sx0, FY + 10), "HOW SURE ARE WE?", font=f(SANS_B, 10), fill=INK)
d.text((sx0, FY + 24), "REPORTED = two or more outlets  •  CLAIM = one side",
       font=f(SANS, 9), fill=GREY)
d.text((sx0, FY + 36), "FORECAST = not yet happened",
       font=f(SANS, 9), fill=GREY)
d.text((sx0, FY + 48), "Sources: AP • Reuters • AFP • BBC • UN News • Nasdaq",
       font=f(SANS, 9), fill=INK)

out = "entry.png"
img.save(out, optimize=True)
print("saved", out, img.size)
