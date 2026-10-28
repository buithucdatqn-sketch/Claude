"""Tập 12 (từ bộ khuôn draw_doodle.py): vẽ nét doodle mới (bản gốc: tập 10, inbox/out/2026-10-22_van-tho-xa-van-min-gan/engine_ep10/draw_ep15.py).
Chép vào OUT/engine_epNN/draw_epNN.py, sửa khối "nét của từng ảnh" và tên file npz (doodle_epNN_<ảnh>.npz).
Vẽ nét doodle mới (nét trắng, nét đứt, nét tay) lên ảnh sạch, lưu thành lớp npz cùng dạng với lớp tách từ doodle gốc
(make_layers): mỗi khoá là mảng điểm (x, y) theo ĐÚNG thứ tự vẽ, để engine lộ dần nét từ đuôi tới đầu mũi tên.
Khoá bắt đầu bằng "lab" là nhãn chữ viết tay (hiện khi nét đạt 55-75%), còn lại là nét.
Toạ độ theo ảnh làm việc (source_<ảnh>.png). Chạy: python3 -I draw_ep15.py <OUT> ; ảnh xem thử ghi ra <OUT>/doodle_preview/."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "./") + "/"
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = next(f for f in (os.path.join(HERE, "PatrickHand-Regular.ttf"), os.path.join(HERE, "..", "PatrickHand-Regular.ttf"),
                        os.path.join(HERE, "..", "..", "..", "..", "engine", "PatrickHand-Regular.ttf")) if os.path.isfile(f))


def _resample(pts, step=1.0):
    pts = np.asarray(pts, float)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    t = np.arange(0, seg[-1], step)
    return np.c_[np.interp(t, seg, pts[:, 0]), np.interp(t, seg, pts[:, 1])], t


def _smooth(pts, n=6):
    """đường cong qua các điểm điều khiển (Catmull-Rom), để nét không thẳng như đồ hoạ vector"""
    P = np.asarray(pts, float)
    P = np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for s in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * s ** 3))
    out.append(P[-2])
    return np.array(out)


def stroke(pts, w, dash=None, wobble=0.0, seed=0, smooth=True):
    """nét tay: rung nhẹ vuông góc với đường, nét đứt (dash = (dài, hở)), điểm sắp theo thứ tự vẽ"""
    rng = np.random.default_rng(seed)
    P = _smooth(pts) if smooth and len(pts) > 2 else np.asarray(pts, float)
    S, t = _resample(P)
    if wobble:
        d = np.gradient(S, axis=0)
        nrm = np.c_[-d[:, 1], d[:, 0]] / (np.hypot(d[:, 0], d[:, 1])[:, None] + 1e-9)
        ph = rng.uniform(0, 6.3, 2)
        off = wobble * (np.sin(t / 97 + ph[0]) * 0.7 + np.sin(t / 31 + ph[1]) * 0.3)
        S = S + nrm * off[:, None]
    r = w / 2.0
    R = int(math.ceil(r))
    disk = [(dx, dy) for dx in range(-R, R + 1) for dy in range(-R, R + 1) if dx * dx + dy * dy <= r * r]
    seen, order = set(), []
    on = True
    for (x, y), tt in zip(S, t):
        if dash:
            on = (tt % (dash[0] + dash[1])) < dash[0]
        if not on:
            continue
        for dx, dy in disk:
            p = (int(round(x)) + dx, int(round(y)) + dy)
            if p not in seen:
                seen.add(p)
                order.append(p)
    return order, S


def arrow(pts, w, dash, wobble=0.0, seed=0, head=None):
    """mũi tên: thân nét đứt, đầu là hai nét liền vẽ sau cùng"""
    body, S = stroke(pts, w, dash, wobble, seed)
    head = head or 9 * w
    tip = S[-1]
    back = S[max(0, len(S) - int(head))]
    ang = math.atan2(tip[1] - back[1], tip[0] - back[0])
    out = list(body)
    for a in (ang + math.radians(150), ang - math.radians(150)):
        end = (tip[0] + head * math.cos(a), tip[1] + head * math.sin(a))
        h, _ = stroke([tuple(tip), end], w, None, 0, seed, smooth=False)
        out += h
    return out


def loop(center, rx, ry, w, dash, wobble=0.0, seed=0, overshoot=0.12, tilt=-6):
    """vòng bao tay: hình bầu dục hơi méo, vẽ quá điểm đầu một đoạn (nét vượt)"""
    cx, cy = center
    a = np.linspace(-0.4, 2 * math.pi * (1 + overshoot) - 0.4, 90)
    k = 1 + 0.06 * np.sin(3 * a + seed)
    tr = math.radians(tilt)
    x, y = rx * k * np.cos(a), ry * k * np.sin(a)
    pts = np.c_[cx + x * math.cos(tr) - y * math.sin(tr), cy + x * math.sin(tr) + y * math.cos(tr)]
    return stroke(pts, w, dash, wobble, seed, smooth=False)[0]


def poly(pts, w, dash, wobble=0.0, seed=0):
    """đường bao gấp khúc, mỗi góc vẽ lố ra một chút như nét tay"""
    P = [np.array(p, float) for p in pts] + [np.array(pts[0], float)]
    out, seen = [], set()
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        v = (b - a) / (np.linalg.norm(b - a) + 1e-9)
        o, _ = stroke([tuple(a - v * 3 * w), tuple(b + v * 3 * w)], w, dash, wobble, seed + i, smooth=False)
        for p in o:
            if p not in seen:
                seen.add(p)
                out.append(p)
    return out


def label(text, xy, size, line=1.12):
    """nhãn chữ viết tay (Patrick Hand), nhiều dòng tách bằng '/'"""
    f = ImageFont.truetype(FONT, size)
    lines = text.split("/")
    W = max(int(f.getlength(s)) for s in lines) + 20
    H = int(size * line * len(lines)) + 20
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    for i, s in enumerate(lines):
        d.text((5, 5 + i * size * line), s.strip(), font=f, fill=255)
    ys, xs = np.nonzero(np.array(im) > 128)
    return [(int(x + xy[0]), int(y + xy[1])) for x, y in zip(xs, ys)]


# ---- nét của từng ảnh (toạ độ ảnh làm việc source_<ảnh>.png), tập 15 ----
# Doodle gốc của bài 04 vẽ mực đen (mục 0.2b): vẽ nét trắng mới trên ảnh anh/goc/, giữ đúng chỗ chỉ và lời nhãn của bài (ảnh 08, 09).
DASH = lambda w: (5.5 * w, 3.5 * w)
L = {}

# ngub: ảnh 04 gốc, dải y 670-2020 của bản 2400 px. Cảnh 5: đứng ở chân giường, đúng trên trục, thấy hai đèn thả
w = 11
L["ngub"] = dict(
    truc=stroke([(1200, 120), (1203, 700), (1200, 1320)], w, DASH(w), 1.5, 1)[0],
    den_t=loop((422, 690), 120, 135, w, DASH(w), 1.5, 2, tilt=0),
    den_p=loop((1963, 690), 120, 135, w, DASH(w), 1.5, 3, tilt=0),
    lab_hai=label("từ chân giường,/thấy đủ hai đèn", (1290, 250), 104))
# ngu: ảnh 04 gốc đủ khung 2400x2400. Cảnh 10: tấm ảnh chỉ chụp từ một chỗ đứng
w = 16
L["ngu"] = dict(
    khung=poly([(150, 150), (2250, 150), (2250, 2250), (150, 2250)], w, DASH(w), 2.5, 4),
    lab_mot=label("chỉ cân từ/một chỗ đứng", (760, 380), 150))
# lech: ảnh 08 gốc, dải y 1150-2300. Cảnh 6: còn một đèn; cảnh 7: khung tranh lệch phải, đầu giường bị cắt (nhãn theo doodle của bài)
w = 9
L["lech"] = dict(
    a_den=arrow([(560, 330), (690, 400), (800, 440)], w, DASH(w), 1.0, 5, head=60),
    lab_den=label("chỉ còn thấy/một đèn thả", (90, 160), 92),
    tranh=poly([(1170, 232), (1532, 232), (1532, 560), (1170, 560)], w, DASH(w), 1.2, 6),
    a_tranh=arrow([(860, 640), (1010, 590), (1150, 520)], w, DASH(w), 1.0, 7, head=55),
    lab_tranh=label("khung tranh giờ/nằm lệch sang phải", (190, 600), 80),
    dau=stroke([(760, 690), (1270, 682), (1786, 676)], w, DASH(w), 1.2, 8)[0],
    lab_dau=label("tấm đầu giường/chỉ còn thấy một đoạn", (820, 722), 68))
# loso: ảnh 09 gốc, dải y 900-2200. Cảnh 8: chụp lò sưởi thành món to nhất; cảnh 9: sofa và tranh sẫm ở ngoài khung
w = 9
L["loso"] = dict(
    chup=poly([(860, 990), (1180, 640), (1460, 505), (1786, 545), (1786, 1000)], w, DASH(w), 1.5, 9),
    a_chup=arrow([(1380, 270), (1420, 400), (1440, 540)], w, DASH(w), 1.0, 10, head=55),
    lab_chup=label("chụp lò sưởi giờ là/vật lớn nhất trong khung", (1010, 70), 78),
    a_ngoai=arrow([(800, 740), (420, 760), (40, 770)], w, DASH(w), 1.0, 11, head=60),
    lab_ngoai=label("sofa và tranh sẫm/đã ra ngoài khung", (60, 810), 78))
# tong: ảnh 10 gốc, dải y 840-2300 của bản 2400 px. Cảnh 11: chụp từ cửa, từ sofa, từ bàn ăn; cảnh 12: lật ảnh như soi gương
w = 11
L["tong"] = dict(
    sofa=loop((330, 1160), 300, 190, w, DASH(w), 1.5, 12, tilt=-8),
    lab_sofa=label("từ sofa", (90, 900), 100),
    an=loop((1190, 880), 200, 110, w, DASH(w), 1.5, 13, tilt=0),
    lab_an=label("từ bàn ăn", (1000, 640), 96),
    cua=poly([(1790, 30), (1965, 30), (1965, 760), (1790, 760)], w, DASH(w), 1.2, 14),
    lab_cua=label("từ cửa", (1520, 820), 100),
    lat1=arrow([(1200, 300), (900, 220), (560, 330)], w, DASH(w), 1.0, 15, head=60),
    lat2=arrow([(1200, 300), (1500, 220), (1840, 330)], w, DASH(w), 1.0, 16, head=60),
    lab_lat=label("lật như soi gương", (870, 360), 104))

os.makedirs(OUT + "doodle_preview", exist_ok=True)
for img, layers in L.items():
    np.savez(os.path.join(HERE, f"doodle_ep15_{img}.npz"), **{k: np.array(v, np.float32) for k, v in layers.items()})
    im = Image.open(OUT + f"source_{img}.png").convert("RGB")
    a = np.array(im)
    for k, v in layers.items():
        v = np.array(v)
        ok = (v[:, 0] >= 0) & (v[:, 0] < a.shape[1]) & (v[:, 1] >= 0) & (v[:, 1] < a.shape[0])
        a[v[ok, 1], v[ok, 0]] = 255
    p = Image.fromarray(a)
    p.thumbnail((900, 900))
    p.save(OUT + f"doodle_preview/{img}.jpg", quality=85)
    print(img, {k: len(v) for k, v in layers.items()})
