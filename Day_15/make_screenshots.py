from PIL import Image, ImageDraw, ImageFont
import os

OUT = "screenshots"
os.makedirs(OUT, exist_ok=True)

W = 1280
BG = (10, 15, 30)
SURFACE = (17, 24, 39)
SURFACE_ALT = (13, 20, 32)
LINE = (31, 41, 55)
TEXT = (229, 233, 240)
DIM = (124, 135, 152)
FAINT = (75, 85, 102)
ACCENT = (99, 102, 241)
LOW = (52, 211, 153)
MED = (245, 166, 35)
HIGH = (240, 85, 74)


def mono(size, bold=False):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def sans(size, bold=False):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def rr(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


def navbar(draw, active, pulse_color=LOW):
    draw.rectangle([0, 0, W, 68], fill=SURFACE)
    draw.line([0, 68, W, 68], fill=LINE, width=1)
    draw.text((40, 22), "● devpulse", font=mono(18, True), fill=TEXT)
    # pulse line mock
    pts = [(360 + i * 3, 34 + (10 if i % 7 in (2,) else -10 if i % 7 in (4,) else 0)) for i in range(0, 200, 1)]
    draw.line(pts, fill=pulse_color, width=2)
    # nav links
    draw.text((W - 220, 27), "predict", font=mono(13, active == "predict"), fill=TEXT if active == "predict" else DIM)
    draw.text((W - 120, 27), "history", font=mono(13, active == "history"), fill=TEXT if active == "history" else DIM)


def footer(draw, h):
    draw.line([0, h - 46, W, h - 46], fill=LINE, width=1)
    txt = "devpulse · developer productivity & code quality dashboard · day 15"
    draw.text((W / 2, h - 26), txt, font=mono(11), fill=FAINT, anchor="mm")


# ============================================================
# 1. Input form (terminal card)
# ============================================================
H = 980
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
navbar(d, "predict")

mx = 250
d.text((mx, 108), "COMMIT RISK MONITOR", font=mono(11), fill=FAINT)
d.text((mx, 130), "Check a developer's commit vitals", font=mono(26, True), fill=TEXT)
d.text((mx, 168), "Enter this week's activity metrics and DevPulse will read the signal.", font=sans(14), fill=DIM)

# flow strip
flow = ["form", "→", "flask /predict", "→", "best_model.pkl", "→", "sqlite log", "→", "result"]
fx = mx
for item in flow:
    if item == "→":
        d.text((fx, 205), item, font=mono(12), fill=FAINT)
        fx += 22
    else:
        w = d.textlength(item, font=mono(11))
        rr(d, [fx, 198, fx + w + 20, 222], 5, outline=LINE)
        d.text((fx + 10, 204), item, font=mono(11), fill=DIM)
        fx += w + 32

# terminal card
card = [mx, 250, W - mx, 800]
rr(d, card, 10, fill=SURFACE, outline=LINE)
d.rectangle([card[0], card[1], card[2], card[1] + 42], fill=SURFACE_ALT)
d.line([card[0], card[1] + 42, card[2], card[1] + 42], fill=LINE, width=1)
for i, c in enumerate([HIGH, MED, LOW]):
    d.ellipse([card[0] + 18 + i * 18, card[1] + 15, card[0] + 30 + i * 18, card[1] + 27], fill=c)
d.text((card[0] + 90, card[1] + 13), "metrics.env", font=mono(11), fill=FAINT)

fields = [
    ("commits_per_week", "8"), ("lines_added", "89"), ("lines_deleted", "54"),
    ("files_changed", "1"), ("bugs_reported", "3"), ("code_review_comments", "0"),
    ("avg_review_time_hours", "4.5"), ("test_coverage_percent", "67.0"),
    ("deployment_frequency", "2"), ("late_night_commits", "1"),
]
cols = 3
fx0, fy0 = card[0] + 40, card[1] + 80
cell_w, cell_h = (card[2] - card[0] - 80) / cols, 95
for i, (label, val) in enumerate(fields):
    col, row = i % cols, i // cols
    fx = fx0 + col * cell_w
    fy = fy0 + row * cell_h
    d.text((fx, fy), f"$ {label}", font=mono(12), fill=DIM)
    rr(d, [fx, fy + 20, fx + cell_w - 30, fy + 54], 6, fill=BG, outline=LINE)
    d.text((fx + 12, fy + 29), val, font=mono(13), fill=TEXT)

d.line([card[0] + 40, card[1] + 400, card[2] - 40, card[1] + 400], fill=LINE, width=1)
d.text((card[0] + 40, card[1] + 420), "10 vitals required — hover a field to see its range", font=mono(11), fill=FAINT)

rr(d, [card[2] - 330, card[1] + 410, card[2] - 190, card[1] + 452], 6, outline=LINE)
d.text((card[2] - 315, card[1] + 422), "↺ sample data", font=mono(12), fill=DIM)
rr(d, [card[2] - 175, card[1] + 410, card[2] - 40, card[1] + 452], 6, fill=ACCENT)
d.text((card[2] - 160, card[1] + 422), "▸ run prediction", font=mono(12, True), fill=(255, 255, 255))

footer(d, H)
img.save(f"{OUT}/1_input_form.png")

# ============================================================
# 2. Prediction result (EKG)
# ============================================================
H2 = 900
img2 = Image.new("RGB", (W, H2), BG)
d2 = ImageDraw.Draw(img2)
navbar(d2, "predict", pulse_color=LOW)

d2.text((mx, 108), "READING COMPLETE", font=mono(11), fill=FAINT)
d2.text((mx, 130), "Vitals reading", font=mono(26, True), fill=TEXT)
d2.text((mx, 168), "Generated by best_model.pkl — a Random Forest classifier.", font=sans(14), fill=DIM)

col_w = (W - 2 * mx - 30) / 2
cardA = [mx, 220, mx + col_w, 700]
rr(d2, cardA, 10, fill=SURFACE, outline=LINE)
d2.line([cardA[0], cardA[1], cardA[2], cardA[1]], fill=LOW, width=4)

badge = "Low risk"
bw = d2.textlength(badge, font=mono(22, True))
bx = (cardA[0] + cardA[2]) / 2 - bw / 2 - 20
rr(d2, [bx, cardA[1] + 40, bx + bw + 40, cardA[1] + 90], 25, fill=(20, 40, 33))
d2.text(((cardA[0] + cardA[2]) / 2, cardA[1] + 65), "● " + badge, font=mono(20, True), fill=LOW, anchor="mm")

# EKG wave
ekg_y = cardA[1] + 160
ekg_pts = []
xs = list(range(int(cardA[0] + 40), int(cardA[2] - 40)))
import math
for i, x in enumerate(xs):
    t = (x - xs[0]) % 90
    if 30 <= t <= 40:
        y = ekg_y - (30 if t < 35 else -30) if t == 34 or t==36 else ekg_y
    y = ekg_y
    if t == 33: y = ekg_y - 35
    elif t == 36: y = ekg_y + 35
    ekg_pts.append((x, y))
d2.line(ekg_pts, fill=LOW, width=2)

d2.text(((cardA[0] + cardA[2]) / 2, cardA[1] + 220), "confidence 98.33%", font=mono(14, True), fill=TEXT, anchor="mm")
d2.text(((cardA[0] + cardA[2]) / 2, cardA[1] + 245), "Healthy commit pattern. Keep up the good", font=sans(12), fill=DIM, anchor="mm")
d2.text(((cardA[0] + cardA[2]) / 2, cardA[1] + 263), "review discipline.", font=sans(12), fill=DIM, anchor="mm")

by = cardA[1] + 300
for lab, pct, col in [("high", 0.9, HIGH), ("low", 98.33, LOW), ("medium", 0.77, MED)]:
    d2.text((cardA[0] + 40, by), lab, font=mono(12), fill=DIM)
    track = [cardA[0] + 120, by + 4, cardA[2] - 90, by + 12]
    rr(d2, track, 4, fill=SURFACE_ALT, outline=LINE)
    fw = track[0] + (track[2] - track[0]) * min(pct, 100) / 100
    rr(d2, [track[0], track[1], fw, track[3]], 4, fill=col)
    d2.text((cardA[2] - 70, by), f"{pct}%", font=mono(11), fill=FAINT)
    by += 32

cardB = [mx + col_w + 30, 220, W - mx, 700]
rr(d2, cardB, 10, fill=SURFACE, outline=LINE)
d2.text((cardB[0] + 30, cardB[1] + 25), "#input.log", font=mono(13), fill=DIM)
ty = cardB[1] + 65
sample_vals = [("commits_per_week", "12"), ("lines_added", "40"), ("lines_deleted", "10"),
               ("files_changed", "2"), ("bugs_reported", "0"), ("code_review_comments", "8"),
               ("avg_review_time_hours", "1.5"), ("test_coverage_percent", "92.0"),
               ("deployment_frequency", "5"), ("late_night_commits", "0")]
for lab, val in sample_vals:
    d2.line([cardB[0] + 30, ty + 26, cardB[2] - 30, ty + 26], fill=LINE)
    d2.text((cardB[0] + 30, ty), lab, font=mono(12), fill=DIM)
    tw = d2.textlength(val, font=mono(12))
    d2.text((cardB[2] - 30 - tw, ty), val, font=mono(12), fill=TEXT)
    ty += 40

rr(d2, [W / 2 - 240, 740, W / 2 - 20, 782], 6, outline=LINE)
d2.text((W / 2 - 215, 752), "← run another", font=mono(12), fill=DIM)
rr(d2, [W / 2 + 20, 740, W / 2 + 240, 782], 6, fill=ACCENT)
d2.text((W / 2 + 45, 752), "view history →", font=mono(12, True), fill=(255, 255, 255))

footer(d2, H2)
img2.save(f"{OUT}/2_prediction_result.png")

# ============================================================
# 3. History (git log style)
# ============================================================
H3 = 820
img3 = Image.new("RGB", (W, H3), BG)
d3 = ImageDraw.Draw(img3)
navbar(d3, "history")

d3.text((mx, 108), "SQLITE · PREDICTIONS.DB", font=mono(11), fill=FAINT)
d3.text((mx, 130), "Prediction history", font=mono(26, True), fill=TEXT)
d3.text((mx, 168), "Every prediction is logged to SQLite, most recent first.", font=sans(14), fill=DIM)

card = [mx, 220, W - mx, 620]
rr(d3, card, 10, fill=SURFACE, outline=LINE)
d3.line([card[0], card[1] + 50, card[2], card[1] + 50], fill=LINE, width=1)
d3.text((card[0] + 30, card[1] + 18), "# git log --oneline", font=mono(13), fill=DIM)
d3.text((card[2] - 110, card[1] + 18), "5 records", font=mono(11), fill=FAINT)

rows = [
    ("06:31", LOW, "12 commits", "0 bugs", "92.0% coverage", "Low", "98.33%"),
    ("06:29", HIGH, "25 commits", "12 bugs", "20.0% coverage", "High", "57.54%"),
    ("06:24", HIGH, "10 commits", "4 bugs", "55.0% coverage", "High", "65.79%"),
    ("06:18", MED, "6 commits", "2 bugs", "48.0% coverage", "Medium", "51.20%"),
    ("06:02", LOW, "9 commits", "1 bugs", "88.0% coverage", "Low", "94.10%"),
]
ry = card[1] + 50
for ts, col, commits, bugs, cov, risk, conf in rows:
    d3.line([card[0], ry + 60, card[2], ry + 60], fill=LINE, width=1)
    d3.text((card[0] + 30, ry + 22), ts, font=mono(12), fill=FAINT)
    d3.ellipse([card[0] + 130, ry + 25, card[0] + 142, ry + 37], fill=col)
    d3.text((card[0] + 165, ry + 22), f"{commits} · {bugs} · {cov}", font=mono(12), fill=DIM)
    rw = d3.textlength(risk, font=mono(13, True))
    d3.text((card[2] - 200, ry + 22), risk, font=mono(13, True), fill=col)
    d3.text((card[2] - 90, ry + 22), conf, font=mono(12), fill=FAINT)
    ry += 60

rr(d3, [W / 2 - 110, 660, W / 2 + 110, 702], 6, fill=ACCENT)
d3.text((W / 2, 681), "← new prediction", font=mono(12, True), fill=(255, 255, 255), anchor="mm")

footer(d3, H3)
img3.save(f"{OUT}/3_history.png")

print("done:", os.listdir(OUT))
