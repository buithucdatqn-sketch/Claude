"""Sinh engine v8 (nhiều ảnh nguồn, mỗi cảnh một ảnh) từ engine v7 bằng thay thế văn bản có kiểm tra.
Chạy một lần: python3 make_v8.py  → engine_storyboard_v8.py, engine_video_v8.py"""
import re

GEOM_OLD_START = 'src = Image.open(SRC).convert("RGB")'
GEOM_OLD_END = '# ---------------- colour ----------------'
GEOM_NEW = '''# ---------------- board geometry (2x master, 1x = reel canvas) ----------------
B2W, B2H = W * 2, H * 2
CARD_W2, BORDER2 = 1920, 0
C2 = (B2W / 2, 1810.0)
ANGLE = 1.2  # degrees, counter-clockwise (card is hung very slightly crooked)


class Photo:
    """một ảnh nguồn và hình học thẻ ảnh của nó; cảnh chỉ tới ảnh qua SCENES[i]["img"] (mặc định "main")"""

    def __init__(self, path, card_w2=None, c2y=None, border2=None, credit=None, angle=ANGLE):
        self.src = Image.open(path).convert("RGB")
        self.SW, self.SH = self.src.size
        self.CARD_W2 = CARD_W2 if card_w2 is None else card_w2
        self.BORDER2 = BORDER2 if border2 is None else border2
        self.PH_W2 = self.CARD_W2 - 2 * self.BORDER2
        self.PH_H2 = int(round(self.PH_W2 * self.SH / self.SW))
        self.CARD_H2 = self.PH_H2 + 2 * self.BORDER2
        self.C2 = (B2W / 2, C2[1] if c2y is None else c2y)
        self.ANGLE = angle
        self.S2 = self.PH_W2 / self.SW
        self.ROT = cv2.getRotationMatrix2D(self.C2, angle, 1.0)
        self.CARD_TOP1, self.CARD_BOT1 = (self.C2[1] - self.CARD_H2 / 2) / 2, (self.C2[1] + self.CARD_H2 / 2) / 2
        self.CARD_L1, self.CARD_R1 = (self.C2[0] - self.CARD_W2 / 2) / 2, (self.C2[0] + self.CARD_W2 / 2) / 2
        self.center = (self.SW / 2, self.SH / 2)
        self.credit = credit
        self.boards = {}

    def src_to_b2(self, p):
        ux = self.C2[0] + p[0] * self.S2 - self.PH_W2 / 2
        uy = self.C2[1] + p[1] * self.S2 - self.PH_H2 / 2
        R = self.ROT
        return (R[0, 0] * ux + R[0, 1] * uy + R[0, 2], R[1, 0] * ux + R[1, 1] * uy + R[1, 2])

    def board(self, key):
        if key not in self.boards:
            self.boards[key] = make_board(0.86 if key == "dark" else 1.0, self)
        return self.boards[key]


PHOTOS = {"main": Photo(SRC)}
DEFAULT_IMG = "main"
src = PHOTOS["main"].src
SW, SH = src.size
PH_W2, PH_H2, CARD_H2 = PHOTOS["main"].PH_W2, PHOTOS["main"].PH_H2, PHOTOS["main"].CARD_H2
S2, ROT = PHOTOS["main"].S2, PHOTOS["main"].ROT
CARD_TOP1, CARD_BOT1 = PHOTOS["main"].CARD_TOP1, PHOTOS["main"].CARD_BOT1


def src_to_b2(p):
    return PHOTOS[DEFAULT_IMG].src_to_b2(p)


'''

CREDIT_OLD = '''def put_credit(t, xy, size, fill, anchor="la"):
    """credit một dòng; dài quá 960 px thì giảm cỡ chữ (tối thiểu 26)"""
    s = size
    while s > 26 and t.d.textlength(CREDIT, font=F(s)) > 960:
        s -= 1
    t.put(xy, CREDIT, s, fill, anchor)
'''
CREDIT_NEW = '''def put_credit(t, xy, size, fill, anchor="la", credit=None):
    """credit một dòng (riêng cho từng ảnh); dài quá 960 px thì giảm cỡ chữ (tối thiểu 26)"""
    txt = credit or CREDIT
    s = size
    while s > 26 and t.d.textlength(txt, font=F(s)) > 960:
        s -= 1
    t.put(xy, txt, s, fill, anchor)
'''

CAM_OLD = '''class Cam:
    def __init__(self, focus_src, z, anchor):
        self.z, self.A = z, anchor
        fb = src_to_b2(focus_src)
        self.F = (fb[0] / 2, fb[1] / 2)
        self.s = z * S2 / 2  # canvas px per source px

    def pt(self, p):
        bx, by = src_to_b2(p)
        return (self.A[0] + self.z * (bx / 2 - self.F[0]), self.A[1] + self.z * (by / 2 - self.F[1]))

    def board_y(self, y1):
        return self.A[1] + self.z * (y1 - self.F[1])

    @property
    def card_top(self):
        return self.board_y(CARD_TOP1)

    @property
    def card_bottom(self):
        return self.board_y(CARD_BOT1)
'''
CAM_NEW = '''class Cam:
    """focus_src: điểm trên ảnh (hoặc "C" = tâm ảnh); anchor: (x, y) trên khung, ("top", y[, x]) đặt mép trên thẻ ở y,
    ("cover"[, x, y]) dời neo để thẻ phủ kín khung nếu zoom đủ lớn"""

    def __init__(self, focus_src, z, anchor, P=None):
        self.P = P or PHOTOS[DEFAULT_IMG]
        self.focus = self.P.center if focus_src == "C" else tuple(focus_src)
        self.z = z
        fb = self.P.src_to_b2(self.focus)
        self.F = (fb[0] / 2, fb[1] / 2)
        self.s = z * self.P.S2 / 2  # canvas px per source px
        self.A = self._anchor(anchor)

    def _anchor(self, anchor):
        if isinstance(anchor, (tuple, list)) and anchor and isinstance(anchor[0], str):
            kind = anchor[0]
            if kind == "top":
                ax = anchor[2] if len(anchor) > 2 else W / 2
                return (ax, anchor[1] + self.z * (self.F[1] - self.P.CARD_TOP1))
            if kind == "cover":
                ax = anchor[1] if len(anchor) > 1 else W / 2
                ay = anchor[2] if len(anchor) > 2 else 900
                m = 40
                z, F, P = self.z, self.F, self.P
                lo, hi = W + m - z * (P.CARD_R1 - F[0]), -m - z * (P.CARD_L1 - F[0])
                if lo <= hi:
                    ax = min(max(ax, lo), hi)
                lo, hi = H + m - z * (P.CARD_BOT1 - F[1]), -m - z * (P.CARD_TOP1 - F[1])
                if lo <= hi:
                    ay = min(max(ay, lo), hi)
                return (ax, ay)
            raise ValueError(anchor)
        return tuple(anchor)

    def pt(self, p):
        bx, by = self.P.src_to_b2(p)
        return (self.A[0] + self.z * (bx / 2 - self.F[0]), self.A[1] + self.z * (by / 2 - self.F[1]))

    def board_y(self, y1):
        return self.A[1] + self.z * (y1 - self.F[1])

    @property
    def card_top(self):
        return self.board_y(self.P.CARD_TOP1)

    @property
    def card_bottom(self):
        return self.board_y(self.P.CARD_BOT1)
'''

CONTOUR_OLD = '        mask = np.zeros((SH + 2 * pad, SW + 2 * pad), np.uint8)'
CONTOUR_NEW = '        mask = np.zeros((self.v.P.SH + 2 * pad, self.v.P.SW + 2 * pad), np.uint8)'


def patch_make_board(s):
    a = s.index('def make_board(dark, swatches=False):')
    b = s.index('# ---------------- camera ----------------')
    f = s[a:b]
    f = f.replace('def make_board(dark, swatches=False):', 'def make_board(dark, P=None, swatches=False):\n    P = P or PHOTOS[DEFAULT_IMG]')
    for name in ('C2', 'CARD_W2', 'CARD_H2', 'PH_W2', 'PH_H2', 'BORDER2', 'ROT', 'ANGLE', 'src'):
        f = re.sub(r'(?<![\w.])' + name + r'(?!\w)', 'P.' + name, f)
    f = f.replace('P = P.P or', 'P = P or')  # chữa dòng gán vừa thêm nếu bị thay
    f = f.replace('def make_board(dark, P.P=None', 'def make_board(dark, P=None')
    return s[:a] + f + s[b:]


def common(s):
    a = s.index(GEOM_OLD_START); b = s.index(GEOM_OLD_END)
    s = s[:a] + GEOM_NEW + s[b:]
    for o, n in ((CREDIT_OLD, CREDIT_NEW), (CAM_OLD, CAM_NEW), (CONTOUR_OLD, CONTOUR_NEW)):
        assert o in s, o[:40]
        s = s.replace(o, n)
    s = patch_make_board(s)
    s = s.replace('class Brush:\n    def __init__(self, cam):', 'class Brush:\n    def __init__(self, cam):\n        self.P = cam.P')
    return s


# ---- storyboard ----
s = open('engine_storyboard_v7.py').read()
s = common(s)
RS_OLD = '''def render_scene(i):
    sc = SCENES[i]
    cam = Cam(*sc["cam"])
    key = "clean" if i == END else ("dark" if sc["dark"] else "plain")
    rr = cam.render(*BOARDS[key])
'''
RS_NEW = '''# ---------------- render ----------------
def render_scene(i):
    sc = SCENES[i]
    P = PHOTOS[sc.get("img", DEFAULT_IMG)]
    cam = Cam(*sc["cam"], P=P)
    key = "plain" if i == END else ("dark" if sc["dark"] else "plain")
    rr = cam.render(*P.board(key))
'''
assert RS_OLD in s; s = s.replace(RS_OLD, RS_NEW)
s = s.replace('put_credit(text, (W // 2, bot + 30), 34, 225, "ma")', 'put_credit(text, (W // 2, bot + 30), 34, 225, "ma", credit=P.credit)')
s = s.replace('put_credit(text, (60, bot + 26), 34, 230)', 'put_credit(text, (60, bot + 26), 34, 230, credit=P.credit)')
s = s.replace('put_credit(text, (60, 1388), 32, 235)', 'put_credit(text, (60, 1388), 32, 235, credit=P.credit)')
B_OLD = 'BOARDS["plain"] = make_board(1.0)\nBOARDS["dark"] = make_board(0.86)\nBOARDS["clean"] = make_board(1.0)\n'
assert B_OLD in s; s = s.replace(B_OLD, '')
s = s.replace('Reel storyboard generator v5', 'Reel storyboard generator v8 (nhiều ảnh nguồn: PHOTOS, SCENES[i]["img"])', 1)
open('engine_storyboard_v8.py', 'w').write(s)

# ---- video ----
s = open('engine_video.py').read()
s = common(s)
B_OLD = 'BOARDS["plain"] = make_board(1.0)\nBOARDS["dark"] = make_board(0.86)\nBOARDS["clean"] = BOARDS["plain"]\n'
assert B_OLD in s; s = s.replace(B_OLD, '# ---------------- render ----------------\n')
L_OLD = '''def layout(i):
    sc = SCENES[i]
    cam = Cam(*sc["cam"])
    key = "dark" if sc["dark"] else "plain"
    if i == END:
        key = "clean"
'''
L_NEW = '''def layout(i):
    sc = SCENES[i]
    P = PHOTOS[sc.get("img", DEFAULT_IMG)]
    cam = Cam(*sc["cam"], P=P)
    key = "dark" if sc["dark"] else "plain"
'''
assert L_OLD in s; s = s.replace(L_OLD, L_NEW)
s = s.replace('put_credit(tm, (W // 2, bot + 30), 34, 225, "ma")', 'put_credit(tm, (W // 2, bot + 30), 34, 225, "ma", credit=P.credit)')
s = s.replace('put_credit(tm, (60, bot + 26), 34, 230)', 'put_credit(tm, (60, bot + 26), 34, 230, credit=P.credit)')
s = s.replace('put_credit(tm, (60, 1388), 32, 235)', 'put_credit(tm, (60, 1388), 32, 235, credit=P.credit)')
R_OLD = 'return dict(sc=sc, cam=sc["cam"], key=key,'
assert R_OLD in s; s = s.replace(R_OLD, 'return dict(sc=sc, cam=sc["cam"], P=P, key=key,')
RC_OLD = '''def render_cam(key, cam):
    return cam.render(*BOARDS[key])


def lerp_cam(c0, c1, p):
    (f0, z0, a0), (f1, z1, a1) = c0, c1
    z = math.exp(math.log(z0) * (1 - p) + math.log(z1) * p)
    f = (f0[0] + (f1[0] - f0[0]) * p, f0[1] + (f1[1] - f0[1]) * p)
    a = (a0[0] + (a1[0] - a0[0]) * p, a0[1] + (a1[1] - a0[1]) * p)
    return Cam(f, z, a)
'''
RC_NEW = '''def render_cam(key, cam):
    return cam.render(*cam.P.board(key))


def lerp_cam(c0, c1, p, P):
    """nội suy giữa hai camera trên CÙNG một ảnh (focus, zoom theo log, neo)"""
    C0, C1 = Cam(*c0, P=P), Cam(*c1, P=P)
    z = math.exp(math.log(C0.z) * (1 - p) + math.log(C1.z) * p)
    f = (C0.focus[0] + (C1.focus[0] - C0.focus[0]) * p, C0.focus[1] + (C1.focus[1] - C0.focus[1]) * p)
    a = (C0.A[0] + (C1.A[0] - C0.A[0]) * p, C0.A[1] + (C1.A[1] - C0.A[1]) * p)
    return Cam(f, z, a, P=P)
'''
assert RC_OLD in s; s = s.replace(RC_OLD, RC_NEW)
LOOP_OLD = '''        cam = Cam(*ly["cam"])
        rr = render_cam(ly["key"], cam)
        fac = ly["f"]
        a_old = 0.0
        a_main = sm((u - 0.15) / 0.5)
        t_start = 0.0
    else:
        prev = L[i - 1]
        p = sm(u / TRANS)
        cam = lerp_cam(prev["cam"], ly["cam"], p)
        r1 = render_cam(ly["key"], cam)
        if prev["key"] != ly["key"] and p < 1:
            r0 = render_cam(prev["key"], cam)
            rr = r0 * (1 - p) + r1 * p
        else:
            rr = r1
'''
LOOP_NEW = '''        cam = Cam(*ly["cam"], P=ly["P"])
        rr = render_cam(ly["key"], cam)
        fac = ly["f"]
        a_old = 0.0
        a_main = sm((u - 0.15) / 0.5)
        t_start = 0.0
    else:
        prev = L[i - 1]
        p = sm(u / TRANS)
        if prev["P"] is ly["P"]:
            cam = lerp_cam(prev["cam"], ly["cam"], p, ly["P"])
            r1 = render_cam(ly["key"], cam)
            if prev["key"] != ly["key"] and p < 1:
                r0 = render_cam(prev["key"], cam)
                rr = r0 * (1 - p) + r1 * p
            else:
                rr = r1
        else:
            # đổi ảnh nguồn: mờ chéo 0,7 giây giữa hai thẻ ảnh, mỗi thẻ đứng yên ở camera của cảnh mình
            cam = Cam(*ly["cam"], P=ly["P"])
            r1 = render_cam(ly["key"], cam)
            if p < 1:
                r0 = render_cam(prev["key"], Cam(*prev["cam"], P=prev["P"]))
                rr = r0 * (1 - p) + r1 * p
            else:
                rr = r1
'''
assert LOOP_OLD in s; s = s.replace(LOOP_OLD, LOOP_NEW)
s = s.replace('Reel storyboard generator v5', 'Reel video engine v8 (nhiều ảnh nguồn: PHOTOS, SCENES[i]["img"]; đổi ảnh = mờ chéo)', 1)
open('engine_video_v8.py', 'w').write(s)
print('ok')
