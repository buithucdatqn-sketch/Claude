# -*- coding: utf-8 -*-
"""Tạo ảnh "phòng trống" từ ảnh gốc: xoá đồ đạc để nét viền bay vào lắp lại.

Tường ván gỗ dọc: chép theo cột từ phần tường phía trên (giữ đường ván).
Sàn bê tông: ghép mảnh vá lấy từ vùng sàn sạch cùng độ sâu, chỉnh sáng theo nền tần số thấp.
Chạy: python3 -I empty_room.py <ảnh_làm_việc_1600x2400> <ảnh_ra>
"""
import sys
import numpy as np, cv2

rng = np.random.default_rng(11)


def poly_mask(shape, polys):
    m = np.zeros(shape[:2], np.uint8)
    for p in polys:
        cv2.fillPoly(m, [np.int32(p)], 255)
    return m


def col_copy(img, m, x0, x1, src_y0, src_y1):
    """Lấp vùng mặt nạ trong dải cột x0..x1 bằng cách lặp đoạn tường src_y0..src_y1 theo chiều dọc."""
    h = src_y1 - src_y0
    ys, xs = np.nonzero(m[:, x0:x1])
    xs = xs + x0
    for y, x in zip(ys, xs):
        k = (y - src_y1) % (2 * h)
        sy = src_y1 - 1 - k if k < h else src_y0 + (k - h)   # phản chiếu để không lộ đường nối
        img[y, x] = img[sy, x]


def lowfreq_fill(img, m, scale=8):
    small = cv2.resize(img, (img.shape[1] // scale, img.shape[0] // scale), interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, (small.shape[1], small.shape[0]), interpolation=cv2.INTER_NEAREST)
    ms = cv2.dilate(ms, np.ones((3, 3), np.uint8))
    lf = cv2.inpaint(small, ms, 6, cv2.INPAINT_TELEA)
    lf = cv2.resize(lf, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
    return cv2.GaussianBlur(lf, (0, 0), 6)


def row_profile(img, clean, m):
    """Độ sáng nền sàn theo độ sâu: trung vị từng hàng của sàn sạch, làm mượt theo y."""
    h, w = img.shape[:2]
    prof = np.full((h, 3), np.nan, np.float32)
    for y in range(h):
        xs = np.nonzero(clean[y])[0]
        if len(xs) > 20:
            prof[y] = np.median(img[y, xs].astype(np.float32), axis=0)
    ok = ~np.isnan(prof[:, 0])
    idx = np.arange(h)
    for c in range(3):
        prof[:, c] = np.interp(idx, idx[ok], prof[ok, c])
    prof = cv2.GaussianBlur(prof.reshape(h, 1, 3), (1, 0), sigmaX=0.1, sigmaY=25).reshape(h, 3)
    return np.repeat(prof[:, None, :], w, axis=1)


def poly_fit(img, clean, m, deg=3, sc=8):
    """Mặt sáng tối nền sàn: đa thức bậc 3 theo x, y khớp trên sàn sạch (không bị tường tối kéo vào)."""
    h, w = img.shape[:2]
    lf = cv2.GaussianBlur(img.astype(np.float32), (0, 0), 10)
    ys, xs = np.nonzero(clean[::sc, ::sc]); ys, xs = ys * sc, xs * sc
    def feats(x, y):
        x, y = x / w, y / h
        return np.stack([x ** i * y ** j for i in range(deg + 1) for j in range(deg + 1 - i)], -1)
    A = feats(xs.astype(np.float32), ys.astype(np.float32))
    out = np.zeros((h, w, 3), np.float32)
    my, mx = np.nonzero(cv2.dilate(m, np.ones((15, 15), np.uint8)))
    B = feats(mx.astype(np.float32), my.astype(np.float32))
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, lf[ys, xs, c], rcond=None)
        out[my, mx, c] = B @ coef
    return out


def floor_quilt(img, m, clean, ps=72, step=48, ywin=140):
    out = img.astype(np.float32)
    lf_all = cv2.GaussianBlur(img.astype(np.float32), (0, 0), 14)
    target_lf = row_profile(img, clean, m)
    acc = np.zeros(img.shape[:2], np.float32)
    col = np.zeros_like(out)
    ys, xs = np.nonzero(m)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    # vị trí có thể làm nguồn: mảnh vá nằm trọn trong sàn sạch
    ok = cv2.erode(clean, np.ones((ps, ps), np.uint8))
    ok[:ps, :] = 0; ok[-ps:, :] = 0; ok[:, :ps] = 0; ok[:, -ps:] = 0
    cy, cx = np.nonzero(ok)
    win = np.outer(np.hanning(ps + 2)[1:-1], np.hanning(ps + 2)[1:-1]).astype(np.float32) + 1e-3
    for by in range(y0 - ps // 2, y1 + 1, step):
        for bx in range(x0 - ps // 2, x1 + 1, step):
            ty, tx = by, bx
            if ty < 0 or tx < 0 or ty + ps > img.shape[0] or tx + ps > img.shape[1]:
                ty, tx = np.clip(ty, 0, img.shape[0] - ps), np.clip(tx, 0, img.shape[1] - ps)
            if not m[ty:ty + ps, tx:tx + ps].any():
                continue
            sel = np.nonzero(np.abs(cy - (ty + ps // 2)) < ywin)[0]
            if len(sel) == 0:
                sel = np.arange(len(cy))
            i = rng.choice(sel)
            sy, sx = cy[i] - ps // 2, cx[i] - ps // 2
            patch = out[sy:sy + ps, sx:sx + ps] - lf_all[sy:sy + ps, sx:sx + ps]
            col[ty:ty + ps, tx:tx + ps] += patch * win[..., None]
            acc[ty:ty + ps, tx:tx + ps] += win
    hf = col / np.maximum(acc, 1e-3)[..., None]
    fill = target_lf + hf
    a = cv2.GaussianBlur((m > 0).astype(np.float32), (0, 0), 3)[..., None]
    return np.clip(out * (1 - a) + fill * a, 0, 255).astype(np.uint8)


def make(src, dst):
    img = cv2.imread(src)
    sh = img.shape
    # đảo bếp + vòi + đồ trên mặt bếp
    island = poly_mask(sh, [[(482, 1568), (1200, 1568), (1200, 1935), (482, 1935)],
                            [(1000, 1450), (1060, 1450), (1060, 1575), (1000, 1575)],
                            [(600, 1530), (760, 1530), (760, 1575), (600, 1575)]])
    # bàn + bốn ghế
    table = poly_mask(sh, [[(700, 1630), (1600, 1630), (1600, 2180), (700, 2180)], [(300, 1842), (700, 1842), (700, 2180), (300, 2095)]])
    stool = poly_mask(sh, [[(1265, 1990), (1600, 1990), (1600, 2400), (1265, 2400)]])
    rug = poly_mask(sh, [[(598, 2160), (1300, 2112), (1600, 2105), (1600, 2400), (705, 2400)]])
    shelf = poly_mask(sh, [[(870, 700), (1215, 700), (1215, 955), (870, 955)]])
    pot = poly_mask(sh, [[(810, 880), (920, 880), (920, 962), (810, 962)]])
    allm = island | table | stool | rug | shelf | pot

    # đường chân tường: tường sau (x<1200) chạm sàn ở y≈1840; tường phải chéo xuống
    def floor_y(x):
        return 1840 if x < 1200 else 1840 + (x - 1200) * 0.40
    yy, xx = np.mgrid[0:sh[0], 0:sh[1]]
    fy = np.where(xx < 1200, 1840, 1840 + (xx - 1200) * 0.25)
    allm = allm | poly_mask(sh, [[(482, 1440), (1200, 1440), (1200, 1570), (482, 1570)], [(290, 1550), (482, 1550), (482, 1590), (290, 1590)]])
    wall_m = (allm > 0) & (yy < fy) & (yy > 1000)
    floor_m = (allm > 0) & (yy >= fy)
    out = img.copy()
    # tường sau ván gỗ: chép cột từ đoạn y 1300–1560
    wm = wall_m.astype(np.uint8)
    col_copy(out, wm * (xx < 1200), 290, 1200, 1210, 1440)
    col_copy(out, wm * (xx >= 1200), 1200, 1600, 1330, 1620)
    # kệ trên tường gác: chép cột từ y 420–690
    sm = (shelf > 0).astype(np.uint8)
    col_copy(out, sm, 870, 1215, 420, 690)
    # chậu cây nhỏ ở mép gác: inpaint
    out = cv2.inpaint(out, pot, 7, cv2.INPAINT_TELEA)
    # sàn: vùng sạch = sàn bê tông không có đồ, không có thảm, không có tủ trái
    left_wall = poly_mask(sh, [[(0, 1300), (300, 1300), (300, 2090), (110, 2400), (0, 2400)]])
    clean = ((yy >= fy + 15) & (allm == 0) & (left_wall == 0)).astype(np.uint8) * 255
    clean[:, :300] = 0
    clean[:1990, :] = 0          # dải sàn sát đảo bếp còn bóng phản chiếu
    clean[:, 590:] = 0           # mép thảm và chân ghế
    out = floor_quilt(out, floor_m.astype(np.uint8) * 255, clean)
    # mép chân tường: một nét tối mảnh như ảnh thật
    cv2.line(out, (300, 1841), (1200, 1841), (60, 58, 58), 2, cv2.LINE_AA)
    cv2.line(out, (1200, 1841), (1600, 1941), (60, 58, 58), 2, cv2.LINE_AA)
    cv2.imwrite(dst, out)


if __name__ == '__main__':
    make(sys.argv[1], sys.argv[2])
