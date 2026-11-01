# -*- coding: utf-8 -*-
"""Engine reel nhiều cảnh theo phong cách "animation sketch lắp ráp" (TASK_INSTRUCTION mục 00b).

- Ảnh chụp phủ kín khung 1080x1920; cảnh có `empty` mở bằng ảnh phòng trống, nét viền kem bay vào
  lắp từng món rồi hoà sang ảnh thật.
- `objs`: nét kem (hoặc cam) bay vào, xoay, nảy rồi đáp đúng chỗ, chỉ vào chi tiết lời đang nói.
- `rays`: nét cam vẽ dần (đường đi ánh sáng, mũi tên).
- `img2` + `fade`: hoà sang ảnh thứ hai cùng hình học (ví dụ ban ngày sang chạng vạng) ngay trong cảnh.
- Sơ đồ (IMGS kind='diagram'): nét mực hiện dần theo nhóm và thứ tự vẽ trên nền trắng (mục 0.6j).
- Đổi ảnh: hoà tan 0,45 s; cùng ảnh: camera lia 1,1 s.
- Chữ: header, phụ đề, dòng nguồn chung trong một hộp trắng thẳng, không băng keo (mục 00b.3);
  cảnh sơ đồ viết thẳng lên nền trắng. Mọi chữ trong y 340–1490, nửa dưới x ≤ 960 (mục 6a).

Tập dùng engine bằng cách viết một file dữ liệu (xem inbox/out/2026-11-01_den-lech-mau-go/engine_ep19/reel_ep19.py)
gọi `run(EP)`. Chế độ: `frames` (khung chính + storyboard) hoặc `video` (mp4 không tiếng).
"""
import os, sys, math, json, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sketch_assemble import jitter, partial, place, ease, prog, arrow  # noqa: E402

FONT = os.path.join(HERE, '..', 'PatrickHand-Regular.ttf')
W, H, FPS = 1080, 1920, 30
CREAM = (205, 236, 246)       # BGR
ORANGE = (43, 86, 224)        # BGR
INK_TXT = (38, 34, 30)        # RGB chữ nâu
XFADE, PAN = 0.45, 1.1


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


# ---------------- ảnh và sơ đồ ----------------
class Source:
    def __init__(self, key, spec):
        self.key, self.kind = key, spec.get('kind', 'photo')
        self.credit = spec.get('credit', '')
        if self.kind == 'diagram':
            im = cv2.imread(spec['path'])
            x0, y0, x1, y1 = spec.get('crop', (0, 0, im.shape[1], im.shape[0]))
            self.scale = spec.get('up', 2.5)
            im = im[y0:y1, x0:x1]
            im = cv2.resize(im, None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_CUBIC)
            bl = cv2.GaussianBlur(im, (0, 0), 1.2)
            im = cv2.addWeighted(im, 1.5, bl, -0.5, 0)
            self.off = (x0, y0)
            f = im.astype(np.float32)
            mn = f.min(axis=2)
            self.alpha = np.clip((250 - mn) / 150.0, 0, 1)
            self.alpha[self.alpha < 0.06] = 0
            # màu mực: kéo về màu đậm (giữ màu gốc, không loang nền)
            a3 = np.maximum(self.alpha, 1e-3)[..., None]
            self.ink = np.clip(255 - (255 - f) / a3, 0, 255)
            self.img = None
            self.order = {}
            for g in spec['groups']:
                self.order[g['name']] = self._order_map(g)
            self.shape = im.shape[:2]
        else:
            self.img = cv2.imread(spec['path'])
            self.empty = cv2.imread(spec['empty']) if spec.get('empty') else None
            self.shape = self.img.shape[:2]

    def D(self, pts):
        """toạ độ sơ đồ gốc -> toạ độ ảnh làm việc đã phóng."""
        return [((x - self.off[0]) * self.scale, (y - self.off[1]) * self.scale) for x, y in pts]

    def _order_map(self, g):
        """Bản đồ thứ tự vẽ của một nhóm: 0..1, nét lớn trước, mỗi nét quét theo chiều dài của nó."""
        x0, y0, x1, y1 = [v * self.scale for v in ((g['box'][0] - self.off[0]), (g['box'][1] - self.off[1]),
                                                   (g['box'][2] - self.off[0]), (g['box'][3] - self.off[1]))]
        m = (self.alpha > 0.15).astype(np.uint8)
        n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
        sel = [i for i in range(1, n) if x0 <= cen[i][0] <= x1 and y0 <= cen[i][1] <= y1 and st[i][4] > 4]
        key = g.get('by', 'x')
        sel.sort(key=lambda i: (cen[i][1], cen[i][0]) if key == 'y' else (cen[i][0], cen[i][1]))
        tot = float(sum(st[i][4] for i in sel)) or 1.0
        om = np.full(self.alpha.shape, 9.0, np.float32)
        acc = 0.0
        for i in sel:
            bx, by, bw, bh, area = st[i]
            frac = area / tot
            sub = lab[by:by + bh, bx:bx + bw] == i
            if bw >= bh:
                u = (np.arange(bw, dtype=np.float32) / max(bw - 1, 1))[None, :].repeat(bh, 0)
            else:
                u = (np.arange(bh, dtype=np.float32) / max(bh - 1, 1))[:, None].repeat(bw, 1)
            reg = om[by:by + bh, bx:bx + bw]
            reg[sub] = (acc + u * frac)[sub]
            acc += frac
        om = cv2.dilate(om * -1, np.ones((3, 3), np.uint8)) * -1   # phủ mép nét
        return om


def cam_matrix(cx, cy, ch, ih, iw, fill_frame=True):
    cw = ch * W / H
    if fill_frame:
        cw_ = min(cw, iw); ch_ = cw_ * H / W
        if ch_ > ih:
            ch_ = ih; cw_ = ch_ * W / H
        cw, ch = cw_, ch_
        cx = min(max(cx, cw / 2), iw - cw / 2)
        cy = min(max(cy, ch / 2), ih - ch / 2)
    s = H / ch
    return np.float32([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]]), s


def lerp_cam(a, b, p):
    return [a[i] + (b[i] - a[i]) * p for i in range(3)]


# ---------------- hộp chữ ----------------
def text_layer(sc, ep):
    """RGBA 1080x1920: header + phụ đề + dòng nguồn. Hộp trắng (ảnh chụp) hoặc chữ thẳng (sơ đồ)."""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fh, fs, fc = font(30), font(48), font(24)
    pos = sc.get('box', 'top')
    if sc.get('end'):
        fs = font(46)
    if pos == 'diagram':
        x, w = 60, 900
        y = 344
        d.text((x, y), ep['HEAD'], font=fh, fill=(95, 90, 85))
        lines = wrap(sc['sub'], font(54), w, d)
        for j, ln in enumerate(lines):
            d.text((x, 392 + j * 66), ln, font=font(54), fill=INK_TXT)
        if sc.get('src'):
            for j, ln in enumerate(wrap(sc['src'], fc, w, d)):
                d.text((x, sc.get('src_y', 1452) + j * 30), ln, font=fc, fill=(110, 105, 100))
        return lay
    w = {'top': 960, 'bottom': 900, 'left': 620}[pos]
    lines = wrap(sc['sub'], fs, w - 64, d)
    head = ep['HEAD'] if w > 700 else ep['HEAD'].split('·')[-1].strip()
    src = sc.get('src', '')
    slines = wrap(src, fc, w - 64, d) if src else []
    hh = 22 + 34 + 58 * len(lines) + (10 + 28 * len(slines) if slines else 0) + 20
    if pos == 'top':
        x, y = (W - w) // 2, 336
    elif pos == 'bottom':
        x, y = 60, 1490 - hh
    else:
        x, y = 44, 336
    d.rectangle([x, y, x + w, y + hh], fill=(255, 255, 255, 255))
    d.text((x + 32, y + 18), head, font=fh, fill=(95, 90, 85))
    for j, ln in enumerate(lines):
        d.text((x + 32, y + 56 + j * 58), ln, font=fs, fill=INK_TXT)
    for j, ln in enumerate(slines):
        d.text((x + 32, y + 56 + 58 * len(lines) + 10 + j * 28), ln, font=fc, fill=(120, 114, 108))
    if sc.get('end'):
        for j, ln in enumerate(ep.get('END_LINES', [])):
            pass
    return lay


def qa_text(lay, idx):
    a = np.asarray(lay)[..., 3]
    ys, xs = np.nonzero(a > 0)
    errs = []
    if len(ys):
        if ys.min() < 330 or ys.max() > 1500:
            errs.append(f'LỖI: chữ ra ngoài vùng an toàn Reels/bảng tin (cảnh {idx}: y {ys.min()}–{ys.max()})')
        low = xs[ys > 1000]
        if len(low) and low.max() > 1020:
            errs.append(f'LỖI: chữ ra ngoài vùng an toàn Reels/bảng tin (cảnh {idx}: nửa dưới x tới {low.max()})')
    return errs


# ---------------- dựng một khung của một cảnh ----------------
def render_scene(ep, srcs, i, u, layers):
    S = ep['SCENES']
    sc = S[i]
    src = srcs[sc['img']]
    dur = sc['_dur']
    prev = S[i - 1] if i > 0 else None
    # camera: trôi nhẹ trong cảnh; nếu cùng ảnh với cảnh trước thì lia từ camera cuối cảnh trước
    c0, c1 = sc['cam'], sc.get('cam1', sc['cam'])
    pc = ease(min(u / max(dur, 1e-3), 1.0)) if sc.get('move', 'drift') != 'hold' else 0.0
    cam = lerp_cam(c0, c1, pc)
    if prev is not None and prev['img'] == sc['img'] and u < PAN:
        pcam = prev.get('cam1', prev['cam'])
        cam = lerp_cam(pcam, cam, ease(u / PAN))
    ih, iw = src.shape
    M, s = cam_matrix(*cam, ih, iw, fill_frame=(src.kind == 'photo'))
    if src.kind == 'diagram':
        rev = np.zeros(src.alpha.shape, np.float32)
        for gname in sc.get('keep', []):
            rev = np.maximum(rev, (src.order[gname] < 9).astype(np.float32))
        draws = sc.get('draw', [])
        for gname, a, b in draws:
            p = prog(u, a, b)
            if p > 0:
                rev = np.maximum(rev, (src.order[gname] <= p).astype(np.float32))
        A = cv2.warpAffine(src.alpha * rev, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)[..., None]
        INK = cv2.warpAffine(src.ink, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
        frame = (255 * (1 - A) + INK * A).astype(np.uint8)
    else:
        base = src.img
        if sc.get('empty') and src.empty is not None:
            pr = ease(prog(u, *sc['real']))
            A_ = cv2.warpAffine(src.empty, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            if pr > 0:
                B_ = cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                frame = cv2.addWeighted(A_, 1 - pr, B_, pr, 0)
            else:
                frame = A_
        else:
            frame = cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if sc.get('img2'):
            p2 = ease(prog(u, *sc['fade']))
            if p2 > 0:
                F2 = cv2.warpAffine(srcs[sc['img2']].img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                frame = cv2.addWeighted(frame, 1 - p2, F2, p2, 0)
    boil = int(u * FPS) // 3 % 4
    th = max(7, int(round(min(s, 2.4) * 6.0)))
    fo = sc.get('fade_objs')
    aobj = 1 - ease(prog(u, *fo)) if fo else 1.0
    for k, ob in enumerate(sc.get('objs', [])):
        t0 = ob['t']
        if u < t0 or aobj <= 0:
            continue
        col = ORANGE if ob.get('color') == 'orange' else CREAM
        st = place(ob['strokes'], u, t0, ob.get('d', (0, -900)), ob.get('rot', 15)) if ob.get('fly', True) else \
            [np.array(x, np.float32) for x in ob['strokes']]
        layer = frame.copy() if aobj < 1 else frame
        for j, stroke in enumerate(st):
            p = jitter([tuple(q) for q in stroke], 1000 * k + 37 * boil + j, amp=2.2)
            p = p @ M[:, :2].T + M[:, 2]
            cv2.polylines(layer, [np.int32(p * 4)], False, col, ob.get('th', th), cv2.LINE_AA, shift=2)
        if aobj < 1:
            cv2.addWeighted(layer, aobj, frame, 1 - aobj, 0, dst=frame)
    for k, ry in enumerate(sc.get('rays', [])):
        p = prog(u, ry['t'], ry['t'] + ry.get('dur', 1.2))
        if p <= 0:
            continue
        path = jitter(ry['pts'], 7000 + 10 * k + 37 * boil, amp=1.8)
        path = path @ M[:, :2].T + M[:, 2]
        part = partial(path, ease(p))
        cv2.polylines(frame, [np.int32(part * 4)], False, ORANGE, 8, cv2.LINE_AA, shift=2)
        if p >= 1 and ry.get('head', True):
            arrow(frame, path, ORANGE, 8)
    im = Image.fromarray(frame[..., ::-1])
    lay = layers[i]
    ta = ease(prog(u, 0.0, 0.3))
    if ta < 1:
        a = lay.getchannel('A').point(lambda v: int(v * ta))
        lay = lay.copy(); lay.putalpha(a)
    im.paste(lay, (0, 0), lay)
    return np.asarray(im)[..., ::-1]


def timeline(ep):
    t = 0.0
    for sc in ep['SCENES']:
        sc['_t0'] = t
        sc['_dur'] = sc.get('dur') or max(3.5, 0.7 + len(sc['sub'].split()) / 3.2)
        t += sc['_dur']
    return t


def frame_at(ep, srcs, layers, t):
    S = ep['SCENES']
    i = max(j for j in range(len(S)) if S[j]['_t0'] <= t + 1e-6)
    u = t - S[i]['_t0']
    f = render_scene(ep, srcs, i, u, layers)
    if i > 0 and u < XFADE and S[i - 1]['img'] != S[i]['img']:
        g = render_scene(ep, srcs, i - 1, S[i - 1]['_dur'] + u, layers)
        a = ease(u / XFADE)
        f = cv2.addWeighted(g, 1 - a, f, a, 0)
    return f


def run(ep, mode, out):
    os.makedirs(out, exist_ok=True)
    srcs = {k: Source(k, v) for k, v in ep['IMGS'].items()}
    total = timeline(ep)
    layers = [text_layer(sc, ep) for sc in ep['SCENES']]
    errs = []
    for i, l in enumerate(layers):
        errs += qa_text(l, i + 1)
    for e in errs:
        print(e)
    words = sum(len(sc['sub'].split()) for sc in ep['SCENES'])
    print(f'{len(ep["SCENES"])} trang, {words} từ phụ đề, nháp {total:.1f} s')
    json.dump([{k: v for k, v in sc.items() if k in ('_t0', '_dur', 'img', 'sub')} for sc in ep['SCENES']],
              open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
    if mode == 'frames':
        fdir = os.path.join(out, 'frames'); os.makedirs(fdir, exist_ok=True)
        thumbs = []
        for i, sc in enumerate(ep['SCENES']):
            for tag, frac in (('a', 0.35), ('b', 0.92)):
                t = sc['_t0'] + sc['_dur'] * frac
                f = frame_at(ep, srcs, layers, t)
                p = os.path.join(fdir, f'scene_{i + 1:02d}{tag}.png')
                cv2.imwrite(p, f)
                if tag == 'b':
                    thumbs.append((i + 1, f))
        cols = 6
        rows = (len(thumbs) + cols - 1) // cols
        tw, th_ = 300, 533
        sheet = Image.new('RGB', (cols * (tw + 12) + 12, rows * (th_ + 48) + 12), 'white')
        dr = ImageDraw.Draw(sheet)
        for k, (n, f) in enumerate(thumbs):
            x = 12 + (k % cols) * (tw + 12); y = 12 + (k // cols) * (th_ + 48)
            sheet.paste(Image.fromarray(cv2.resize(f, (tw, th_), interpolation=cv2.INTER_AREA)[..., ::-1]), (x, y + 36))
            dr.text((x, y), f'Cảnh {n}', font=font(30), fill=(40, 40, 40))
        sheet.save(os.path.join(out, 'storyboard.png'))
        print('xong khung', fdir)
    else:
        vid = os.path.join(out, ep.get('VIDEO', 'reel_silent.mp4'))
        tail = ep.get('TAIL', 1.0)
        nfr = int((total + tail) * FPS)
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
                               '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                               '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
                               '-c:a', 'aac', '-shortest', '-movflags', '+faststart', vid], stdin=subprocess.PIPE)
        for fi in range(nfr):
            t = min(fi / FPS, total - 1e-3)
            ff.stdin.write(frame_at(ep, srcs, layers, t).tobytes())
            if fi % 150 == 0:
                print(f'{fi / FPS:5.1f}s', flush=True)
        ff.stdin.close(); ff.wait()
        print('xong', vid)
