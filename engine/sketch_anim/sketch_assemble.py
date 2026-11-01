# -*- coding: utf-8 -*-
"""Demo phong cách theo video mẫu chủ Trang gửi (2026-11-01):
ảnh phủ kín khung, bắt đầu từ phòng trống; từng món đồ là nét viền dày màu kem,
vẽ tay đơn giản, bay vào từ mép khung, xoay, nảy rồi đáp đúng chỗ; đủ đồ thì hoà sang ảnh thật.
Sau đó cùng kiểu nét bay vào để chỉ ô kính, rồi nét cam vẽ đường đi ánh sáng.

Chạy: python3 -I sketch_assemble.py <ảnh_thật_1600x2400> <ảnh_phòng_trống> <thư_mục_ra>
"""
import os, sys, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '..', 'PatrickHand-Regular.ttf')
W, H, FPS = 1080, 1920, 30
CREAM = (205, 236, 246)      # BGR của kem (246,236,205)
ORANGE = (43, 86, 224)       # BGR của cam nhấn
DUR = 13.6

HEAD = 'AH DECODE · ÁNH SÁNG TỪ TRÊN CAO'
CREDIT = 'Ảnh dự án: Union Street House · Prior Barraclough · ảnh Ben Hosking'
SUBS = [  # (bắt đầu, kết thúc, chữ, vị trí giấy: 'top' | 'bottom' | 'left', bề rộng)
    (0.2, 6.6, 'Nhà hai bên chung tường, lấy ánh sáng ở đâu bây giờ?', 'top', 960),
    (7.3, 9.7, 'Ở Union Street House, ánh sáng vào từ ô kính cao sát mái.', 'bottom', 960),
    (9.9, DUR, 'Nó chạm vách lam gỗ và trần trước, rồi mới xuống bàn ăn.', 'left', 600)]
CAMS = [(0.0, 800, 1250, 2400), (6.6, 800, 1240, 2250),
        (7.5, 600, 650, 1380), (9.6, 600, 660, 1330),
        (10.4, 800, 1180, 2300), (DUR, 800, 1180, 2240)]
T_REAL = (5.3, 6.1)          # hoà sang ảnh thật
T_FADE1 = (5.7, 6.4)         # nét đồ đạc mờ đi


def R(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def circle(cx, cy, r, n=28):
    return [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n)]


# mỗi món: (tên, thời điểm bay vào, hướng bay vào (dx, dy), góc xoay ban đầu, các nét)
OBJS = [
    ('thảm', 0.5, (900, 500), 18, [[(605, 2165), (1300, 2115), (1640, 2110)], [(605, 2165), (705, 2420)]]),
    ('đảo bếp', 1.0, (-1100, 200), -22, [R(480, 1572, 1200, 1594), [(486, 1594), (486, 1925), (1195, 1925), (1195, 1594)],
                                          [(1035, 1572), (1035, 1470), (1010, 1460), (1003, 1490)]]),
    ('bàn', 1.5, (0, 1400), 25, [[(770, 1648), (1318, 1642), (1395, 1706), (950, 1722), (770, 1648)],
                                 [(952, 1722), (955, 2100)], [(1387, 1710), (1385, 1990)],
                                 [(785, 1652), (786, 1985)], [(1315, 1646), (1316, 1950)]]),
    ('ghế 1', 2.0, (-1000, 900), -30, [[(790, 2080), (790, 1665), (840, 1680), (840, 1840)], R(790, 1840, 1050, 1872),
                                       [(840, 1872), (840, 2085)], [(1000, 1872), (1000, 2040)], [(1045, 1872), (1045, 2045)]]),
    ('ghế 2', 2.4, (-900, -300), 20, [[(725, 2000), (725, 1655), (770, 1660), (770, 1810)], [(725, 1810), (795, 1810)],
                                      [(770, 1810), (770, 1990)]]),
    ('ghế 3', 2.8, (1000, -400), 28, [[(1240, 1785), (1240, 1648), (1318, 1640), (1318, 1990)], R(1070, 1785, 1310, 1810),
                                      [(1080, 1810), (1080, 1990)], [(1130, 1810), (1130, 1930)]]),
    ('ghế 4', 3.2, (1100, 700), -26, [[(1350, 1815), (1350, 1660), (1435, 1655), (1435, 2060)], R(1160, 1815, 1380, 1845),
                                      [(1170, 1845), (1170, 2065)], [(1225, 1845), (1225, 2025)], [(1380, 1845), (1380, 2000)]]),
    ('ghế đôn', 3.6, (900, 1000), 35, [[(1300, 2050), (1330, 2010), (1450, 2000), (1640, 2000)], [(1300, 2050), (1310, 2100), (1640, 2100)],
                                       [(1310, 2100), (1312, 2420)]]),
    ('kệ', 4.0, (900, -900), -24, [[(880, 800), (1145, 795), (1150, 815), (890, 825), (880, 800)],
                                   [(895, 822), (895, 950)], [(1140, 815), (1140, 955)], circle(1055, 750, 38),
                                   R(825, 895, 910, 955)]),
]
WIN = [  # cảnh 2: ô kính và vách lam bay vào
    ('vách lam', 8.0, (-900, -600), -20, [R(200, 215, 705, 940), [(200, 465), (705, 465)], [(200, 690), (705, 690)],
                                          [(535, 215), (535, 940)]]),
    ('ô kính', 8.5, (900, -700), 22, [R(712, 330, 915, 950)]),
]
T_FADE2 = (9.6, 10.2)
RAYS = [  # cảnh 3: đường đi ánh sáng (nét cam)
    (10.6, [(860, 380), (1060, 210), (1300, 170), (1330, 700), (1250, 1640)]),
    (10.9, [(450, 780), (560, 1000), (720, 1300), (880, 1660)]),
    (11.2, [(820, 520), (930, 1000), (1030, 1400), (1080, 1660)]),
]


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def prog(t, a, b):
    return min(max((t - a) / (b - a), 0.0), 1.0)


def spring(u):
    """0 -> 1 có vượt quá rồi nảy về (như video mẫu)."""
    if u <= 0:
        return 0.0
    return 1 - math.exp(-5.5 * u) * math.cos(8.5 * u)


def cam_at(t):
    for i in range(len(CAMS) - 1):
        t0, *a = CAMS[i]
        t1, *b = CAMS[i + 1]
        if t <= t1:
            p = (t - t0) / (t1 - t0)
            p = ease(p) if t1 - t0 < 1.2 else p
            return [a[j] + (b[j] - a[j]) * p for j in range(3)]
    return CAMS[-1][1:]


def cam_matrix(cx, cy, ch, iw, ih):
    cw = ch * W / H
    cx = min(max(cx, cw / 2), iw - cw / 2)
    cy = min(max(cy, ch / 2), ih - ch / 2)
    s = H / ch
    return np.float32([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]]), s


def jitter(pts, seed, amp=2.6, step=14):
    r = np.random.default_rng(seed)
    out = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
        for k in range(n):
            u = k / n
            out.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u))
    out.append(pts[-1])
    out = np.array(out, np.float32)
    ns = r.normal(0, amp, out.shape).astype(np.float32)
    k = np.array([1, 2, 3, 2, 1], np.float32); k /= k.sum()
    for c in range(2):
        ns[:, c] = np.convolve(ns[:, c], k, mode='same')
    return out + ns * 1.6


def partial(path, p):
    seg = np.hypot(*np.diff(path, axis=0).T)
    L = np.concatenate([[0], np.cumsum(seg)])
    tgt = L[-1] * p
    i = int(np.searchsorted(L, tgt))
    pts = path[:max(i, 1)].tolist()
    if 0 < i < len(path):
        u = (tgt - L[i - 1]) / max(seg[i - 1], 1e-6)
        pts.append((path[i - 1] + (path[i] - path[i - 1]) * u).tolist())
    return np.array(pts, np.float32)


def place(strokes, t, t0, d, rot):
    """Biến đổi nét của một món theo thời gian bay vào (dịch, xoay, phóng nhẹ quanh tâm)."""
    u = (t - t0) / 0.75
    f = spring(u)
    allp = np.concatenate([np.array(s, np.float32) for s in strokes])
    c = allp.mean(axis=0)
    a = math.radians(rot * (1 - f))
    sc = 0.85 + 0.15 * f
    off = np.array(d, np.float32) * (1 - f)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for s in strokes:
        p = np.array(s, np.float32) - c
        p = np.stack([p[:, 0] * ca - p[:, 1] * sa, p[:, 0] * sa + p[:, 1] * ca], 1) * sc + c + off
        out.append(p)
    return out


def draw_strokes(img, strokes, M, s, col, th, seed, alpha=1.0):
    layer = img.copy() if alpha < 1 else img
    for k, st in enumerate(strokes):
        p = jitter([tuple(q) for q in st], seed + k)
        p = p @ M[:, :2].T + M[:, 2]
        cv2.polylines(layer, [np.int32(p * 4)], False, col, th, cv2.LINE_AA, shift=2)
    if alpha < 1:
        cv2.addWeighted(layer, alpha, img, 1 - alpha, 0, dst=img)


def arrow(img, path_px, col, th):
    if len(path_px) < 3:
        return
    x1, y1 = path_px[-1]
    x0, y0 = path_px[max(0, len(path_px) - 4)]
    a = math.atan2(y1 - y0, x1 - x0)
    for sgn in (2.55, -2.55):
        q = (x1 + 30 * math.cos(a + sgn), y1 + 30 * math.sin(a + sgn))
        cv2.line(img, (int(x1), int(y1)), (int(q[0]), int(q[1])), col, th, cv2.LINE_AA)


# ---------------- chữ: giấy ghi chú dán băng keo ----------------
def font(sz):
    return ImageFont.truetype(FONT, sz)


def wrap(text, f, maxw, dr):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        tst = (cur + ' ' + wd).strip()
        if dr.textlength(tst, font=f) <= maxw:
            cur = tst
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    return lines


def tape(w=150, h=52, seed=3):
    t = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    r = np.random.default_rng(seed)
    poly = [(3, 5)] + [(x, 2 + r.random() * 5) for x in range(18, w, 20)] + [(w - 3, 4), (w - 5, h - 4)] + \
           [(x, h - 3 - r.random() * 5) for x in range(w - 22, 0, -20)] + [(2, h - 5)]
    d.polygon(poly, fill=(222, 210, 180, 225))
    return t


def note(sub, nw=960):
    fh, fs = font(28), font(46)
    tmp = ImageDraw.Draw(Image.new('RGB', (4, 4)))
    lines = wrap(sub, fs, nw - 70, tmp)
    nh = 96 + 56 * len(lines) + 20
    n = Image.new('RGBA', (nw, nh), (255, 255, 255, 255))
    d = ImageDraw.Draw(n)
    d.text((34, 44), HEAD if nw > 700 else HEAD.replace('AH DECODE · ', ''), font=fh, fill=(95, 90, 85))
    for j, ln in enumerate(lines):
        d.text((34, 88 + j * 56), ln, font=fs, fill=(38, 34, 30))
    n = n.rotate(0.8, expand=True, resample=Image.BICUBIC)
    tp = tape()
    n.paste(tp, ((n.width - tp.width) // 2, 0), tp)  # băng keo ở giữa mép trên
    return n


def credit_tag():
    f = font(24)
    tmp = ImageDraw.Draw(Image.new('RGB', (4, 4)))
    w = int(tmp.textlength(CREDIT, font=f)) + 28
    n = Image.new('RGBA', (w, 40), (255, 255, 255, 255))
    ImageDraw.Draw(n).text((14, 6), CREDIT, font=f, fill=(90, 85, 80))
    return n


def render(real_p, empty_p, out):
    os.makedirs(out, exist_ok=True)
    real = cv2.imread(real_p)
    empty = cv2.imread(empty_p)
    ih, iw = real.shape[:2]
    notes = [note(s[2], s[4]) for s in SUBS]
    ctag = credit_tag()
    vid = os.path.join(out, 'demo_lap_rap_silent.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
                           '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
                           '-c:a', 'aac', '-shortest', '-movflags', '+faststart', vid], stdin=subprocess.PIPE)
    probes = {0.9, 1.9, 2.7, 4.3, 5.0, 5.8, 6.8, 8.3, 9.2, 11.0, 12.6}
    for fi in range(int(DUR * FPS)):
        t = fi / FPS
        boil = (fi // 3) % 4
        cx, cy, ch = cam_at(t)
        M, s = cam_matrix(cx, cy, ch, iw, ih)
        th = max(8, int(round(5.2 * s * 2.4)))   # nét dày như video mẫu
        pr = ease(prog(t, *T_REAL))
        A = cv2.warpAffine(empty, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if pr > 0:
            B = cv2.warpAffine(real, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            frame = cv2.addWeighted(A, 1 - pr, B, pr, 0)
        else:
            frame = A
        a1 = 1 - ease(prog(t, *T_FADE1))
        if a1 > 0:
            for k, (name, t0, d, rot, st) in enumerate(OBJS):
                if t >= t0:
                    draw_strokes(frame, place(st, t, t0, d, rot), M, s, CREAM, th, 1000 * k + boil * 37, a1)
        a2 = 1 - ease(prog(t, *T_FADE2))
        if a2 > 0:
            for k, (name, t0, d, rot, st) in enumerate(WIN):
                if t >= t0:
                    draw_strokes(frame, place(st, t, t0, d, rot), M, s, CREAM, max(8, int(th * 0.7)), 5000 + 100 * k + boil * 37, a2)
        for k, (t0, pts) in enumerate(RAYS):
            p = prog(t, t0, t0 + 1.3)
            if p <= 0:
                continue
            path = jitter(pts, 7000 + 10 * k + boil * 37, amp=2.0)
            path = path @ M[:, :2].T + M[:, 2]
            part = partial(path, ease(p))
            cv2.polylines(frame, [np.int32(part * 4)], False, ORANGE, 9, cv2.LINE_AA, shift=2)
            if p >= 1:
                arrow(frame, path, ORANGE, 9)
                for j in range(3):   # vòng sáng chạy dọc mũi tên
                    u = (t * 0.45 + j / 3 + k * 0.17) % 1.0
                    q = partial(path, u)[-1]
                    cv2.circle(frame, (int(q[0]), int(q[1])), 11, ORANGE, 5, cv2.LINE_AA)
        im = Image.fromarray(frame[..., ::-1])
        for (a0, a1_, _, pos, _w), nt in zip(SUBS, notes):
            if a0 <= t < a1_:
                if pos == 'top':
                    xy = ((W - nt.width) // 2, 336)
                elif pos == 'bottom':
                    xy = ((W - nt.width) // 2, 1440 - nt.height)
                else:
                    xy = (44, 336)
                im.paste(nt, xy, nt)
        im.paste(ctag, (52, 1448), ctag)
        if any(abs(t - pt) < 0.5 / FPS for pt in probes):
            im.save(os.path.join(out, f'probe_{t:05.2f}.png'))
        ff.stdin.write(np.asarray(im)[..., ::-1].tobytes())
        if fi % 60 == 0:
            print(f'{t:5.1f}s', flush=True)
    ff.stdin.close(); ff.wait()
    print('xong', vid)


if __name__ == '__main__':
    render(sys.argv[1], sys.argv[2], sys.argv[3])
