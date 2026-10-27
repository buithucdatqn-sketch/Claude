"""Tập 12 (từ bộ khuôn draw_doodle.py): vẽ nét doodle mới (bản gốc: tập 10, inbox/out/2026-10-22_van-tho-xa-van-min-gan/engine_ep10/draw_ep13.py).
Chép vào OUT/engine_epNN/draw_epNN.py, sửa khối "nét của từng ảnh" và tên file npz (doodle_epNN_<ảnh>.npz).
Vẽ nét doodle mới (nét trắng, nét đứt, nét tay) lên ảnh sạch, lưu thành lớp npz cùng dạng với lớp tách từ doodle gốc
(make_layers): mỗi khoá là mảng điểm (x, y) theo ĐÚNG thứ tự vẽ, để engine lộ dần nét từ đuôi tới đầu mũi tên.
Khoá bắt đầu bằng "lab" là nhãn chữ viết tay (hiện khi nét đạt 55-75%), còn lại là nét.
Toạ độ theo ảnh làm việc (source_<ảnh>.png). Chạy: python3 -I draw_ep13.py <OUT> ; ảnh xem thử ghi ra <OUT>/doodle_preview/."""
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


# ---- nét của từng ảnh (toạ độ ảnh làm việc), tập 13 ----
DASH = lambda w: (5.5 * w, 3.5 * w)
K = 2400 / 1932                     # đổi toạ độ đo trên ảnh xem thu nhỏ (1932 px) sang ảnh làm việc 2400 px (ảnh 06, 10 của kho)


def KP(pts, y0=0):
    """toạ độ đo trên ảnh xem thu nhỏ -> ảnh làm việc; y0 = vị trí trên cùng của dải cắt trong ảnh làm việc"""
    return [(round(x * K), round(y * K) - y0) for x, y in pts]


L = {}
# rong: ảnh ArchDaily 21 (2000x1334), cảnh 12, 13: nối lò sưởi to nhạt với tranh nhỏ sẫm ở phía bên kia phòng
w = 6
L["rong"] = dict(
    ls=poly([(40, 975), (255, 620), (520, 905), (480, 1000), (300, 1045), (290, 1170), (150, 1212), (45, 1215)], w, DASH(w), 2.5, 1),
    tr=poly([(1458, 412), (1695, 258), (1698, 688), (1460, 708)], w, DASH(w), 2.5, 2),
    a_ls=arrow([(760, 400), (560, 520), (345, 635)], w, DASH(w), 2.0, 3),
    a_tr=arrow([(1370, 265), (1420, 330), (1448, 392)], w, DASH(w), 2.0, 4),
    lab_dt=label("to mà nhạt cân với/nhỏ mà sẫm", (700, 175), 88),
    ax_r=stroke([(1170, 395), (1172, 800), (1170, 1190)], w, DASH(w), 1.5, 16)[0],
    lab_axr=label("ô cửa làm trục", (1110, 215), 84),
    sofa=loop((1458, 1000), 330, 185, w, DASH(w), 2.5, 17, tilt=-3),
    lab_sofa=label("món to nhất", (1300, 735), 84),
    lab_tr12=label("tranh màu đậm", (1040, 190), 84))
# khachb: dải ảnh 06 (y xem 560-1760, y0 = 696), cảnh 6, 7
w = 9
Y0 = 696
L["khachb"] = dict(
    ls=poly(KP([(30, 1430), (205, 1040), (530, 1365), (500, 1470), (335, 1520), (305, 1630), (160, 1700), (38, 1690)], Y0), w, DASH(w), 3.0, 5),
    lab_ls=label("to nhưng cùng/màu với tường", KP([(55, 730)], Y0)[0], 104),
    tr=poly(KP([(1486, 848), (1742, 684), (1744, 1120), (1488, 1152)], Y0), w, DASH(w), 3.0, 6),
    ax=stroke(KP([(1002, 580), (1004, 1150), (1002, 1700)], Y0), w, DASH(w), 1.5, 7)[0],
    lab_tr=label("nhỏ mà đậm nhất,/treo cao, xa trục", KP([(1020, 572)], Y0)[0], 96),
    lab_ax=label("chính giữa/phòng", KP([(580, 850)], Y0)[0], 104))


def KC(pts, x0, y0):
    """toạ độ đo trên ảnh xem thu nhỏ -> ảnh làm việc 2400 px -> dải cắt có góc trên trái (x0, y0) trong ảnh làm việc"""
    return [(round(x * K) - x0, round(y * K) - y0) for x, y in pts]


# nhomb: dải ảnh 06 (góc trên trái 1193, 1180): phần dưới bức tranh, sofa, ghế gỗ đen, bình hoa khô. Cảnh 9
w = 9
NX, NY = 1193, round(850 * K)
L["nhomb"] = dict(
    tr_n=poly(KC([(1488, 856), (1743, 856), (1744, 1120), (1488, 1152)], NX, NY), w, DASH(w), 3.0, 8),
    grp=loop((770, 960), 410, 235, w, DASH(w), 3.0, 9))
# tub: dải ảnh 06 (góc trên trái 559, 1093): tủ cổ gỗ đậm gần trục giữa. Cảnh 9
w = 9
TX, TY = 559, 1093
L["tub"] = dict(
    tu=poly(KC([(683, 1072), (915, 1072), (925, 1412), (688, 1415)], TX, TY), w, DASH(w), 3.0, 10),
    ax=stroke(KC([(1002, 905), (1004, 1200), (1002, 1480)], TX, TY), w, DASH(w), 1.5, 11)[0],
    lab_tu=label("tủ gỗ đậm/gần trục", KC([(640, 925)], TX, TY)[0], 70),
    lab_ax=label("trục giữa", KC([(1030, 1100)], TX, TY)[0], 76))
# trucb: dải ảnh 10 (y xem 300-1560, y0 = 373), cảnh 10, 11
w = 9
Y0 = round(160 * K)
L["trucb"] = dict(
    ax=stroke(KP([(952, 335), (954, 900), (952, 1480)], Y0), w, DASH(w), 1.5, 12)[0],
    ax2=stroke(KP([(952, 335), (954, 900), (952, 1480)], Y0), w, DASH(w), 1.5, 13)[0],
    lab_ls10=label("lò sưởi", KP([(1520, 1425)], Y0)[0], 90),
    lab_tr10=label("tranh", KP([(150, 540)], Y0)[0], 90),
    lab_ax=label("trục", KP([(975, 560)], Y0)[0], 100),
    hk_l=poly(KP([(478, 985), (778, 985), (778, 1455), (478, 1455)], Y0), w, DASH(w), 3.0, 14),
    hk_r=poly(KP([(1128, 985), (1428, 985), (1428, 1455), (1128, 1455)], Y0), w, DASH(w), 3.0, 15),
    ht=loop(KP([(952, 335)], Y0)[0], 300, 130, w, DASH(w), 2.5, 18, tilt=0),
    lab_ht=label("hoa trần", KP([(1110, 300)], Y0)[0], 100),
    lab_hk=label("hai hốc kệ/giống nhau", KP([(1150, 735)], Y0)[0], 92))

os.makedirs(OUT + "doodle_preview", exist_ok=True)
for img, layers in L.items():
    np.savez(os.path.join(HERE, f"doodle_ep13_{img}.npz"), **{k: np.array(v, np.float32) for k, v in layers.items()})
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
