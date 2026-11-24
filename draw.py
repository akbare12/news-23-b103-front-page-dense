#!/usr/bin/env python3
"""news-23 b103 front-page-dense: draw THE WORLD TODAY, Monday 23 Nov 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 238)          # cream paper
INK = (20, 20, 20)
BLACK = (12, 12, 12)
RED = (168, 24, 24)
GOLD = (184, 134, 11)
NAVY = (24, 48, 96)
TEAL = (18, 110, 110)
GREEN = (34, 110, 52)
GRAY = (110, 110, 110)
DARKGREEN = (18, 78, 44)
CHIP_BLUE = (30, 80, 160)
CHIP_RED = (178, 34, 34)
MAPGREEN = (198, 228, 178)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FD}/{name}.ttf", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold", s)
SANS = lambda s: font("DejaVuSans", s)
SANS_B = lambda s: font("DejaVuSans-Bold", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def text(x, y, s, f, fill=INK, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def wrap(s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def chip(x, y, label, kind="REPORTED"):
    """Right-aligned chip ending at x; returns its left edge."""
    f = SANS_B(8)
    w_ = d.textlength(label, font=f) + 10
    col = CHIP_BLUE if kind == "REPORTED" else CHIP_RED
    d.rounded_rectangle([x - w_, y, x, y + 13], radius=2, fill=col)
    d.text((x - w_ / 2, y + 1), label, font=f, fill=(255, 255, 255), anchor="ma")
    return x - w_


# ---------------- masthead ----------------
d.rectangle([0, 0, W, 56], fill=BLACK)
text(14, 6, "THE WORLD TODAY", SERIF_B(42), fill=(255, 255, 255))
text(W - 14, 18, "MONDAY 23 NOVEMBER 2026", SANS_B(17), fill=(232, 184, 60), anchor="ra")

# ---------------- kicker ----------------
d.rectangle([0, 56, W, 76], fill=RED)
kicker = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
text(W // 2, 61, kicker, SANS_B(13), fill=(255, 255, 255), anchor="ma")

# ---------------- number strip (2 rows x 5) ----------------
nums = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", INK), ("10T won", "SEOUL STABILISATION FUND", GOLD),
    ("2%", "BILLIONAIRE TAX IN PARIS", GREEN),
    ("$450M", "SKUBAL DEAL", NAVY), ("165", "RUSSIAN MISSILES/WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", INK), ("264 kg", "EXPLOSIVES SEIZED", INK),
    ("$107.3B", "ANTHROPIC IPO", GREEN),
]
cw = W / 5
for i, (val, lab, col) in enumerate(nums):
    cx = (i % 5) * cw
    cy = 78 + (i // 5) * 25
    text(cx + 12, cy, val, SANS_B(16), fill=col)
    text(cx + 12, cy + 15, lab, SANS(7), fill=GRAY)

# ---------------- region bar ----------------
regions = [("ASIA-PACIFIC 7", 7, NAVY), ("AMERICAS 8", 8, RED),
           ("MIDDLE EAST 6", 6, GOLD), ("EUROPE 5", 5, TEAL),
           ("AFRICA 3", 3, GREEN), ("WORLD 2", 2, (90, 90, 90))]
x = 0
for label, n, col in regions:
    w_ = W * n / 31
    d.rectangle([x, 128, x + w_, 146], fill=col)
    text(x + w_ / 2, 131, label, SANS_B(11), fill=(255, 255, 255), anchor="ma")
    x += w_

# ---------------- UTC strip ----------------
text(10, 149, "THE DAY IN UTC", SANS_B(9), fill=INK)
text(108, 149, "~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     SANS(9), fill=(90, 90, 90))
text(W - 10, 149, "~ APPROX", SANS(9), fill=GRAY, anchor="ra")

# ---------------- heroes ----------------
HX = [10, 348, 686]
HW = 328
SCENE_Y, SCENE_H = 162, 138
CAP_Y = 306


def scene_frame(x):
    d.rectangle([x, SCENE_Y, x + HW, SCENE_Y + SCENE_H], outline=(60, 60, 60), width=1)


# --- hero 1: Kospi skyline + chart ---
x = HX[0]
d.rectangle([x, SCENE_Y, x + HW, SCENE_Y + SCENE_H], fill=(16, 28, 64))
scene_frame(x)
import random
random.seed(1031)
for bx in range(x + 8, x + HW - 8, 26):
    bh = random.randint(34, 88)
    by = SCENE_Y + SCENE_H - 22 - bh
    d.rectangle([bx, by, bx + 20, SCENE_Y + SCENE_H - 22], fill=(38, 58, 104))
    for wy in range(by + 6, SCENE_Y + SCENE_H - 26, 12):
        for wx in (bx + 4, bx + 12):
            if random.random() < 0.6:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
pts = [(x + 12, SCENE_Y + 96), (x + 62, SCENE_Y + 78), (x + 112, SCENE_Y + 86),
       (x + 162, SCENE_Y + 58), (x + 212, SCENE_Y + 66), (x + 262, SCENE_Y + 40),
       (x + 312, SCENE_Y + 26)]
d.line(pts, fill=(255, 140, 40), width=3)
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255), outline=(255, 140, 40))
text(x + 12, SCENE_Y + 6, "-3.3%", SANS_B(30), fill=(255, 255, 255))
d.rectangle([x, SCENE_Y + SCENE_H - 20, x + HW, SCENE_Y + SCENE_H], fill=BLACK)
text(x + 10, SCENE_Y + SCENE_H - 17, "KOSPI 4,708.54  \u00b7  -161 PTS", SANS_B(10), fill=(255, 255, 255))

# --- hero 2: Guterres globe ---
x = HX[1]
d.rectangle([x, SCENE_Y, x + HW, SCENE_Y + SCENE_H], fill=DARKGREEN)
scene_frame(x)
text(x + 12, SCENE_Y + 6, "150", SANS_B(36), fill=(232, 184, 60))
text(x + 12, SCENE_Y + 44, "DELEGATES", SANS_B(22), fill=(232, 184, 60))
text(x + 12, SCENE_Y + 68, "BACK A RISK", SANS_B(22), fill=(232, 184, 60))
text(x + 12, SCENE_Y + 92, "FRAMEWORK", SANS_B(22), fill=(232, 184, 60))
gx, gy, gr = x + HW - 62, SCENE_Y + 62, 44
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(190, 225, 190), outline=(255, 255, 255), width=2)
for a in (-28, 0, 28):
    d.arc([gx - gr, gy - gr + a, gx + gr, gy + gr + a], 0, 360, fill=(120, 170, 120))
d.line([gx - gr, gy, gx + gr, gy], fill=(120, 170, 120), width=1)
d.ellipse([gx - 10, gy - gr, gx + 10, gy + gr], outline=(120, 170, 120), width=1)
d.rectangle([x, SCENE_Y + SCENE_H - 20, x + HW, SCENE_Y + SCENE_H], fill=BLACK)
text(x + 10, SCENE_Y + SCENE_H - 17, "UN  \u00b7  BRIDGETOWN", SANS_B(10), fill=(255, 255, 255))

# --- hero 3: Power Index bars ---
x = HX[2]
d.rectangle([x, SCENE_Y, x + HW, SCENE_Y + SCENE_H], fill=(245, 240, 224))
scene_frame(x)
text(x + 12, SCENE_Y + 6, "NARROWEST SINCE 2018", SANS_B(11), fill=INK)
text(x + HW - 12, SCENE_Y + 6, "GAP 5.3", SANS_B(11), fill=RED, anchor="ra")
bars = [("US", 78.9, NAVY, 52), ("CHINA", 73.6, RED, 158), ("INDIA", 40.5, GOLD, 264)]
base = SCENE_Y + SCENE_H - 22
for lab, val, col, bx in bars:
    bh = val  # 1 px per point
    d.rectangle([x + bx, base - bh, x + bx + 52, base], fill=col)
    text(x + bx + 26, base - bh - 16, f"{val}", SANS_B(15), fill=INK, anchor="ma")
    text(x + bx + 26, base - 14, lab, SANS_B(10), fill=(255, 255, 255), anchor="ma")
d.rectangle([x, SCENE_Y + SCENE_H - 20, x + HW, SCENE_Y + SCENE_H], fill=BLACK)
text(x + 10, SCENE_Y + SCENE_H - 17, "ASIA POWER INDEX 2026", SANS_B(10), fill=(255, 255, 255))

# --- hero captions ---
heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS", "REPORTED"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED"),
]
for i, (hl, body, src, kind) in enumerate(heroes):
    x = HX[i]
    lines = wrap(hl, SERIF_B(21), HW)
    y = CAP_Y
    for ln in lines[:2]:
        text(x, y, ln, SERIF_B(21))
        y += 24
    blines = wrap(body, SANS(11), HW)
    for ln in blines[:2]:
        text(x, y, ln, SANS(11), fill=(50, 50, 50))
        y += 14
    # source + chip on their own row, below body
    sy = CAP_Y + 128
    text(x, sy, src, SANS(8), fill=GRAY)
    chip(x + HW, sy - 1, kind, kind)

# ---------------- cards ----------------
d.rectangle([0, 466, W, 484], fill=BLACK)
text(10, 469, "MORE OF THE DAY  \u2014  10 STORIES", SANS_B(13), fill=(255, 255, 255))
cards = [
    ("AMERICAS", NAVY, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", RED, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", GOLD, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", TEAL, "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", (110, 60, 140), "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", TEAL, "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", GOLD, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (110, 60, 140), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CW = W / 5
CH = 68
for i, (cat, col, hl, body, src, kind) in enumerate(cards):
    cx = (i % 5) * CW
    cy = 484 + (i // 5) * CH
    d.rectangle([cx + 2, cy, cx + CW - 2, cy + CH - 2], outline=(200, 200, 200), width=1)
    d.rectangle([cx + 2, cy, cx + CW - 2, cy + 15], fill=col)
    text(cx + 8, cy + 2, cat, SANS_B(9), fill=(255, 255, 255))
    text(cx + CW - 8, cy + 2, str(i + 1), SANS_B(9), fill=(255, 255, 255), anchor="ra")
    hlines = wrap(hl, SANS_B(11), CW - 14)
    y = cy + 18
    for ln in hlines[:2]:
        text(cx + 8, y, ln, SANS_B(11))
        y += 13
    text(cx + 8, y, body, SANS(9), fill=(70, 70, 70))
    by = cy + CH - 15
    text(cx + 8, by, src, SANS(8), fill=GRAY)
    chip(cx + CW - 8, by - 1, kind, kind)

# ---------------- map + ALSO ----------------
MAP_X, MAP_Y, MAP_W, MAP_H = 10, 624, 330, 272
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], outline=(60, 60, 60), width=1)
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + 20], fill=BLACK)
text(MAP_X + 8, MAP_Y + 3, "WHERE IT HAPPENED", SANS_B(12), fill=(255, 255, 255))
# blobs
d.polygon([(26, 668), (140, 654), (152, 756), (96, 836), (30, 806)], fill=MAPGREEN)
d.polygon([(168, 664), (232, 656), (242, 716), (192, 738), (164, 700)], fill=MAPGREEN)
d.polygon([(250, 652), (322, 660), (330, 748), (282, 788), (246, 730)], fill=MAPGREEN)
d.polygon([(120, 812), (196, 806), (200, 856), (128, 862)], fill=MAPGREEN)
pins = {1: (300, 700), 2: (88, 826), 3: (314, 688), 4: (100, 766), 5: (120, 732),
        6: (224, 694), 7: (82, 740), 8: (42, 776), 9: (66, 796), 10: (98, 800),
        11: (214, 672), 12: (184, 660), 13: (242, 666)}
for n, (px, py) in pins.items():
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px, py - 1), str(n), font=SANS_B(9), fill=(255, 255, 255), anchor="mm")
text(MAP_X + 8, MAP_Y + MAP_H - 40, "Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", SANS(8), fill=(60, 60, 60))
text(MAP_X + 8, MAP_Y + MAP_H - 28, "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", SANS(8), fill=(60, 60, 60))
text(MAP_X + 8, MAP_Y + MAP_H - 16, "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", SANS(8), fill=(60, 60, 60))

# ALSO list
ALSO_X = 352
text(ALSO_X, 626, "ALSO ON MONDAY", SANS_B(13))
also = [
    "Paris: 100+ back 2% billionaire tax", "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week", "COP31: the day after Antalya pact rejected",
    "Israel unity talks resume", "Gaza: two killed in Israeli strike",
    "West Bank settler attacks", "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives", "Bahrain: strike hits plant, 2 hurt",
    "Benghazi: UN demands probe [CLAIM]", "Sudan: defences down drones [CLAIM]",
    "DRC: fighting traps Ebola teams", "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits in exam row", "SK Telecom -7.3% as hype cools",
    "China eases margin rules", "Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col = i % 2
    row = i // 2
    ax = ALSO_X + col * 336
    ay = 650 + row * 27
    text(ax, ay, f"{14 + i}.  {item}", SANS(11))

# ---------------- DATE CHECK ----------------
d.rectangle([10, 900, W - 10, 958], outline=RED, width=2)
text(16, 906, "DATE CHECK", SANS_B(13), fill=RED)
text(W - 16, 908, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", SANS_B(8), fill=RED, anchor="ra")
text(16, 924, "LEFT OUT \u2014 NOT 23 NOV:  Dems 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo (22 Nov)  \u00b7  EU\u2013Indonesia (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar (19 Nov)",
     SANS(10))
text(16, 940, "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
     SANS(10))

# ---------------- footer ----------------
text(10, 966, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", SANS(8), fill=GRAY)
text(10, 978, "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.", SANS(8), fill=GRAY)
text(10, 990, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", SANS(8), fill=GRAY)
text(W // 2, 1006, "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions", SANS_B(11), fill=GOLD, anchor="ma")

img.save("entry.png")
print("saved entry.png", img.size)
