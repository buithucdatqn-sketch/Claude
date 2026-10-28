"""Tập 14 (từ bộ khuôn draw_doodle.py): vẽ nét doodle mới (bản gốc: tập 10, inbox/out/2026-10-22_van-tho-xa-van-min-gan/engine_ep10/draw_ep15.py).
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


# ---- nét của từng ảnh (toạ độ ảnh làm việc = ảnh gốc trích từ PDF chương 2, không thu nhỏ), tập 15 ----
DASH = lambda w: (5.5 * w, 3.5 * w)
L = {}

# bep: bếp và bàn ăn nhà Rietveld Schröder (1182x788). Cảnh 2: cả sàn là một mảng màu; cảnh 3: khu vực chỉ nhận ra nhờ đồ đạc
w = 7
L["bep"] = dict(
    san=poly([(40, 548), (580, 530), (700, 700), (520, 775), (30, 775)], w, DASH(w), 1.5, 41),
    lab_san=label("cùng một/mặt sàn", (90, 590), 62),
    ghe=loop((433, 475), 62, 108, w, DASH(w), 1.2, 42, tilt=-4),
    lab_ghe=label("ghế", (365, 598), 56),
    quay=poly([(528, 428), (985, 428), (985, 505), (528, 578)], w, DASH(w), 1.2, 43),
    lab_quay=label("bếp", (545, 478), 56),
    ban=poly([(588, 498), (1170, 498), (1170, 665), (588, 665)], w, DASH(w), 1.5, 44),
    lab_ban=label("bàn ăn", (800, 560), 64))
# tang: tầng trên khi vách trượt mở (1182x788)
w = 7
L["tang"] = dict(
    chung=poly([(230, 505), (470, 432), (760, 440), (872, 562), (862, 705), (520, 772), (240, 548)], w, DASH(w), 1.5, 51),
    lab_chung=label("ban ngày:/một không gian chung", (470, 640), 56),
    do=poly([(618, 490), (735, 452), (866, 508), (866, 572)], w, DASH(w), 1.0, 52),
    lab_do=label("đỏ", (738, 505), 52),
    den=poly([(300, 600), (470, 560), (860, 700), (1010, 775), (300, 775)], w, DASH(w), 1.5, 53),
    lab_den=label("đen", (420, 650), 52),
    a_trang=arrow([(690, 700), (705, 660), (715, 615)], w, DASH(w), 1.0, 54, head=42),
    lab_trang=label("trắng", (640, 700), 52),
    t_do=stroke([(225, 52), (385, 87), (545, 124)], w, DASH(w), 1.2, 55)[0],
    t_den=stroke([(690, 150), (815, 117), (940, 87)], w, DASH(w), 1.2, 56)[0],
    t_vang=stroke([(618, 172), (690, 182), (752, 195)], w, DASH(w), 1.2, 57)[0],
    lab_tran=label("thanh màu/trên trần", (60, 215), 56))
# phong: phòng sàn đỏ, vách trượt bên phải (1182x788)
w = 7
L["phong"] = dict(
    mang=poly([(195, 640), (735, 640), (823, 786), (195, 786)], w, DASH(w), 1.2, 61),
    lab_ranh=label("ranh giới/nằm lại/trên sàn", (212, 642), 42),
    tran_l=stroke([(335, 208), (520, 206), (690, 205)], w, DASH(w), 1.2, 62)[0],
    a_tran=arrow([(520, 280), (520, 240), (520, 212)], w, DASH(w), 1.0, 63, head=38),
    lab_xs=label("màu đặt/xuống sàn", (212, 662), 46),
    lab_lt=label("hoặc lên trần", (360, 292), 50))

os.makedirs(OUT + "doodle_preview", exist_ok=True)
for img, layers in L.items():
    np.savez(os.path.join(HERE, f"doodle_ep15_{img}.npz"), **{k: np.array(v, np.float32) for k, v in layers.items()})
    if not os.path.isfile(OUT + f"source_{img}.png"):     # ảnh của bản cũ (Pawson House) không còn dùng ở bản 7
        continue
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
