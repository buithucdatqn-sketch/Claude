# -*- coding: utf-8 -*-
"""Demo phong cách "animation sketch graphic" từ ảnh gốc công trình.

Ảnh chụp -> nét ký họa (tự vẽ dần, nét rung kiểu vẽ tay) -> lớp đổ nét chì
(hatching) quét vào -> ảnh thật hiện dần dưới lớp nét -> camera zoom vào chi tiết,
nhãn viết tay, mũi tên đường đi ánh sáng chạy theo nét màu nhấn.

Chạy: python3 -I sketch_demo.py <ảnh_gốc> <thư_mục_ra>
"""
import os, sys, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '..', 'PatrickHand-Regular.ttf')
W, H, FPS = 1080, 1920, 30
VW, VH, VY = 1080, 900, 446          # khung ảnh: phủ kín bề ngang
INK = np.array([38, 34, 30], np.float32)       # mực nâu đen (RGB)
ACC = (224, 86, 43)                            # cam nhấn (RGB)
PAPER = np.array([255, 255, 255], np.float32)
DUR = 20.0
rng = np.random.default_rng(7)

# ---------------- dữ liệu cảnh (toạ độ ảnh làm việc 1600x2400) ----------------
HEAD = 'AH DECODE · ÁNH SÁNG TỪ TRÊN CAO'
CREDIT = 'Ảnh dự án: Union Street House · Prior Barraclough · ảnh Ben Hosking'
SUBS = [  # (bắt đầu, kết thúc, chữ)  — lời mẫu cho demo
    (0.3, 10.6, 'Nhà hai bên chung tường, lấy ánh sáng ở đâu bây giờ?'),
    (11.0, 14.4, 'Ở Union Street House, ánh sáng vào từ ô kính cao sát mái.'),
    (14.8, 20.0, 'Nó chạm vách lam gỗ và trần trước, rồi mới xuống bàn ăn.'),
]
CAMS = [  # (thời điểm, tâm x, tâm y, chiều cao vùng nhìn trên ảnh)
    (0.0, 800, 1180, 1960), (10.6, 800, 1180, 1760),
    (11.4, 600, 620, 1050), (14.4, 640, 640, 1000),
    (15.2, 820, 1010, 1900), (20.0, 820, 1010, 1860),
]
T_LINE = (0.6, 6.4)     # nét viền vẽ dần
T_HATCH = (5.6, 8.6)    # lớp đổ nét chì quét vào
T_PHOTO = (8.4, 10.6)   # ảnh thật hiện dần
# nhãn cảnh 2 (khoanh + chữ), vẽ dần trong khoảng thời gian
LABELS2 = [
    dict(t=(11.6, 12.8), kind='loop', box=(195, 220, 712, 940), text='vách lam gỗ',
         tpos=(250, 1010)),
    dict(t=(12.6, 13.8), kind='arrow', pts=[(1080, 300), (980, 360), (900, 470)],
         text='ô kính cao sát mái', tpos=(890, 200)),
]
# đường đi ánh sáng cảnh 3 (nét cam)
RAYS = [
    dict(t=(15.3, 17.0), pts=[(860, 380), (1060, 210), (1300, 170), (1330, 700), (1250, 1640)]),
    dict(t=(15.6, 17.4), pts=[(450, 560), (560, 900), (720, 1300), (880, 1660)]),
    dict(t=(15.9, 17.8), pts=[(820, 520), (930, 1000), (1030, 1400), (1080, 1660)]),
]
LABELS3 = [
    dict(t=(17.2, 18.2), text='chạm lam, trần trước', pos=(1000, 330), col=(38, 34, 30, 255)),
    dict(t=(17.8, 18.8), text='mặt bàn: không vệt nắng', pos=(470, 1780)),
]


def font(sz):
    return ImageFont.truetype(FONT, sz)


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def prog(t, a, b):
    return min(max((t - a) / (b - a), 0.0), 1.0)


# ---------------- tiền xử lý ảnh ----------------
def prepare(src):
    im = Image.open(src).convert('RGB')
    s = 2400 / max(im.size)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    photo = np.asarray(im).astype(np.float32)
    h, w = photo.shape[:2]
    gray = cv2.cvtColor(photo.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    sm = cv2.bilateralFilter(gray, 9, 40, 9)
    # nét chính (cấu trúc lớn) + nét phụ (chi tiết), ưu tiên nét dài vẽ trước
    e1 = cv2.Canny(cv2.GaussianBlur(sm, (0, 0), 3.0), 18, 45)
    e2 = cv2.Canny(cv2.GaussianBlur(sm, (0, 0), 1.4), 30, 80)
    edges = cv2.bitwise_or(e1, e2)
    cs, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cs = [c[:, 0, :] for c in cs if len(c) >= 18]
    cs.sort(key=lambda c: -len(c))
    total = float(sum(len(c) for c in cs))
    tm = np.full((h, w), 9.0, np.float32)
    lines = np.zeros((h, w), np.float32)
    acc = 0.0
    starts = []
    for c in cs:
        starts.append(acc / total)
        acc += len(c)
    for c, st in zip(reversed(cs), reversed(starts)):
        n = len(c)
        tt = st + np.arange(n, dtype=np.float32) / total
        tm[c[:, 1], c[:, 0]] = tt
        lines[c[:, 1], c[:, 0]] = 1.0
    k = np.ones((3, 3), np.uint8)
    tm = cv2.erode(tm, k)              # phủ bề dày nét
    lines = cv2.dilate(lines, k)
    lines = cv2.GaussianBlur(lines, (0, 0), 0.9)
    lines = np.clip(lines * 1.25, 0, 1) * 0.92

    # đổ nét chì theo độ tối
    tone = cv2.GaussianBlur(gray, (0, 0), 6).astype(np.float32) / 255.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wob = cv2.resize(rng.normal(0, 1, (h // 60 + 2, w // 60 + 2)).astype(np.float32), (w, h)) * 3
    def hatch(angle, spacing, thr):
        a = math.radians(angle)
        d = (xx * math.cos(a) + yy * math.sin(a) + wob) % spacing
        ln = np.clip(1.6 - np.abs(d - spacing / 2), 0, 1)
        return ln * np.clip((thr - tone) / 0.08, 0, 1)
    hat = np.maximum.reduce([hatch(55, 22, 0.52), hatch(-35, 20, 0.34), hatch(10, 17, 0.2)])
    hat = cv2.GaussianBlur(hat, (0, 0), 0.7) * 0.45
    noise = cv2.resize(rng.random((h // 80 + 2, w // 80 + 2)).astype(np.float32), (w, h))
    htm = ((xx + yy) / (w + h)) * 0.8 + noise * 0.2

    # biến thể rung nét (line boil) — cùng một trường dịch chuyển cho nét và thời gian
    variants = []
    for i in range(3):
        dx = cv2.resize(rng.normal(0, 1, (h // 90 + 2, w // 90 + 2)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 1.8
        dy = cv2.resize(rng.normal(0, 1, (h // 90 + 2, w // 90 + 2)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 1.8
        mx, my = xx + dx, yy + dy
        variants.append((cv2.remap(lines, mx, my, cv2.INTER_LINEAR),
                         cv2.remap(tm, mx, my, cv2.INTER_NEAREST, borderValue=9.0),
                         cv2.remap(hat, mx, my, cv2.INTER_LINEAR)))
    return photo, variants, htm, (w, h)


# ---------------- camera ----------------
def cam_at(t):
    for i in range(len(CAMS) - 1):
        t0, *a = CAMS[i]
        t1, *b = CAMS[i + 1]
        if t <= t1:
            p = (t - t0) / (t1 - t0)
            # đoạn chuyển nhanh (<1s) dùng ease, đoạn dài trôi đều
            p = ease(p) if t1 - t0 < 1.2 else p
            return [a[j] + (b[j] - a[j]) * p for j in range(3)]
    return CAMS[-1][1:]


def crop(arr, cx, cy, ch, fill, interp=cv2.INTER_LINEAR):
    cw = ch * VW / VH
    sx = VW / cw
    M = np.float32([[sx, 0, VW / 2 - cx * sx], [0, sx, VH / 2 - cy * sx]])
    return cv2.warpAffine(arr, M, (VW, VH), flags=interp, borderMode=cv2.BORDER_CONSTANT, borderValue=fill)


def to_view(pts, cx, cy, ch):
    s = VW / (ch * VW / VH)
    return [((x - cx) * s + VW / 2, (y - cy) * s + VH / 2) for x, y in pts]


# ---------------- nét vẽ tay ----------------
def jitter_path(pts, seed, amp=2.2, step=10):
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
    ns = cv2.GaussianBlur(ns.reshape(-1, 1, 2), (1, 7), 0).reshape(-1, 2)
    return out + ns


def partial(path, p):
    if p <= 0:
        return path[:1]
    seg = np.hypot(*np.diff(path, axis=0).T)
    L = np.concatenate([[0], np.cumsum(seg)])
    tgt = L[-1] * p
    i = int(np.searchsorted(L, tgt))
    pts = path[:max(i, 1)].tolist()
    if 0 < i < len(path):
        u = (tgt - L[i - 1]) / max(seg[i - 1], 1e-6)
        pts.append((path[i - 1] + (path[i] - path[i - 1]) * u).tolist())
    return np.array(pts, np.float32)


def loop_path(box):
    x0, y0, x1, y1 = box
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 * 1.08, (y1 - y0) / 2 * 1.06
    a = np.linspace(-2.2, -2.2 + 2 * math.pi * 1.08, 60)
    return [(cx + rx * math.cos(t) * (1 + 0.03 * math.sin(3 * t)), cy + ry * math.sin(t)) for t in a]


def draw_poly(dr, pts, col, w):
    pts = [tuple(map(float, p)) for p in pts]
    if len(pts) >= 2:
        dr.line(pts, fill=col, width=w, joint='curve')


def arrow_head(dr, path, col, w, size=22):
    if len(path) < 3:
        return
    x1, y1 = path[-1]
    x0, y0 = path[max(0, len(path) - 4)]
    a = math.atan2(y1 - y0, x1 - x0)
    for s in (2.55, -2.55):
        dr.line([(x1, y1), (x1 + size * math.cos(a + s), y1 + size * math.sin(a + s))], fill=col, width=w)


# ---------------- khung cố định: băng keo, đầu trang ----------------
def tape_img():
    tw, th = 170, 64
    t = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    r = np.random.default_rng(3)
    poly = [(4, 6)] + [(x, 2 + r.random() * 6) for x in range(20, tw, 22)] + [(tw - 3, 5), (tw - 6, th - 5)] + \
           [(x, th - 3 - r.random() * 6) for x in range(tw - 24, 0, -22)] + [(2, th - 6)]
    d.polygon(poly, fill=(222, 210, 180, 215))
    return t.rotate(-2, expand=True, resample=Image.BICUBIC)


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


def render(src, out):
    os.makedirs(out, exist_ok=True)
    photo, variants, htm, (iw, ih) = prepare(src)
    tape = tape_img()
    f_head, f_cred, f_sub, f_lab = font(34), font(26), font(50), font(46)
    tmp = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    probe_t = {1.5, 4.0, 7.2, 9.6, 12.4, 13.9, 16.6, 18.8}
    vid = os.path.join(out, 'demo_sketch_silent.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                           '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
                           '-c:a', 'aac', '-shortest', '-movflags', '+faststart', vid], stdin=subprocess.PIPE)
    nfr = int(DUR * FPS)
    for fi in range(nfr):
        t = fi / FPS
        cx, cy, ch = cam_at(t)
        vi = (fi // 4) % 3                       # nét rung 7,5 lần/giây
        lines, tm, hat = variants[vi]
        pl = prog(t, *T_LINE)
        ph = prog(t, *T_HATCH)
        pp = ease(prog(t, *T_PHOTO))
        L = crop(lines, cx, cy, ch, 0.0)
        TM = crop(tm, cx, cy, ch, 9.0, cv2.INTER_NEAREST)
        HA = crop(hat, cx, cy, ch, 0.0)
        HT = crop(htm, cx, cy, ch, 9.0, cv2.INTER_NEAREST)
        P = crop(photo, cx, cy, ch, (255, 255, 255))
        # nét đang vẽ: đầu nét đậm hơn một chút (tip)
        a_line = L * (TM <= pl).astype(np.float32)
        a_hat = HA * np.clip((ph * 1.15 - HT) / 0.08, 0, 1) * (1 - pp)
        base = PAPER * (1 - pp) + P * pp
        a = np.clip(a_line * (1 - 0.5 * pp) + a_hat, 0, 1)[..., None]
        view = base * (1 - a) + INK * a
        frame = np.full((H, W, 3), 255, np.uint8)
        frame[VY:VY + VH] = np.clip(view, 0, 255).astype(np.uint8)
        im = Image.fromarray(frame)
        dr = ImageDraw.Draw(im)
        # lớp nhãn trên ảnh (toạ độ ảnh -> khung)
        ov = Image.new('RGBA', (VW, VH), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        inkc = (255, 255, 255, 255) if pp > 0.5 else (38, 34, 30, 255)
        fade2 = 1 - prog(t, 14.4, 14.65)
        for k, lb in enumerate(LABELS2):
            p = prog(t, *lb['t'])
            if p <= 0 or fade2 <= 0:
                continue
            raw = loop_path(lb['box']) if lb['kind'] == 'loop' else lb['pts']
            path = jitter_path(to_view(raw, cx, cy, ch), 100 + k * 10 + vi, amp=1.6)
            pp_ = partial(path, ease(min(p / 0.62, 1)))
            col = (255, 255, 255, int(255 * fade2))
            draw_poly(od, pp_, col, 5)
            if lb['kind'] == 'arrow' and p >= 0.62:
                arrow_head(od, path, col, 5)
            if p > 0.6:
                tx, ty = to_view([lb['tpos']], cx, cy, ch)[0]
                txt = lb['text'][:max(1, int(len(lb['text']) * prog(p, 0.6, 0.85)))]
                od.text((tx, ty), txt, font=f_lab, fill=col)
        for k, ry in enumerate(RAYS):
            p = prog(t, *ry['t'])
            if p <= 0:
                continue
            path = jitter_path(to_view(ry['pts'], cx, cy, ch), 300 + k * 10 + vi, amp=1.8)
            pp_ = partial(path, ease(p))
            draw_poly(od, pp_, ACC + (255,), 5)
            if p >= 1:
                arrow_head(od, path, ACC + (255,), 5)
            # chấm sáng chạy dọc đường (hạt ánh sáng)
            if p >= 1:
                for j in range(3):
                    u = ((t * 0.45 + j / 3 + k * 0.17) % 1.0)
                    q = partial(path, u)[-1]
                    od.ellipse([q[0] - 7, q[1] - 7, q[0] + 7, q[1] + 7], outline=ACC + (255,), width=4)
        for lb in LABELS3:
            p = prog(t, *lb['t'])
            if p <= 0:
                continue
            tx, ty = to_view([lb['pos']], cx, cy, ch)[0]
            txt = lb['text'][:max(1, int(len(lb['text']) * p))]
            od.text((tx, ty), txt, font=f_lab, fill=lb.get('col', (255, 255, 255, 255)))
        im.paste(ov, (0, VY), ov)
        im.paste(tape, ((W - tape.width) // 2, VY - 26), tape)
        # đầu trang + credit
        dr.text((60, 336), HEAD, font=f_head, fill=(60, 56, 52))
        dr.text((60, 384), CREDIT, font=f_cred, fill=(110, 105, 100))
        # phụ đề
        for a0, a1, txt in SUBS:
            if a0 <= t < a1:
                al = min(prog(t, a0, a0 + 0.3), 1 - prog(t, a1 - 0.25, a1))
                c = tuple(int(255 - (255 - v) * al) for v in (38, 34, 30))
                for j, ln in enumerate(wrap(txt, f_sub, 960, tmp)):
                    dr.text((60, 1350 + j * 62), ln, font=f_sub, fill=c)
        if any(abs(t - pt) < 0.5 / FPS for pt in probe_t):
            im.save(os.path.join(out, f'probe_{t:05.2f}.png'))
        ff.stdin.write(im.tobytes())
        if fi % 60 == 0:
            print(f'{t:5.1f}s', flush=True)
    ff.stdin.close(); ff.wait()
    print('xong', vid)


if __name__ == '__main__':
    render(sys.argv[1], sys.argv[2])
