# -*- coding: utf-8 -*-
"""Phòng trống cho cảnh "màu rực nằm ở đồ rời" (Curva Apartment, ảnh ArchDaily _12, góc ăn):
xoá bộ bàn và bốn ghế đỏ cam, ba bức tranh xanh; tường trắng cong và sàn xám nhạt lan bằng inpaint Navier-Stokes,
tường và sàn lan riêng (che phần kia) để màu không chảy qua chân tường; thêm hạt sàn.
Chạy: python3 -I empty_curva12.py <_12.jpg> <ra_source.png> <ra_empty.png>
"""
import sys
import numpy as np, cv2


def poly(sh, pts):
    m = np.zeros(sh[:2], np.uint8); cv2.fillPoly(m, [np.int32(pts)], 255); return m


def main(src, out_src, out_empty):
    img = cv2.imread(src); cv2.imwrite(out_src, img); sh = img.shape
    h, w = sh[:2]
    m = np.zeros((h, w), np.uint8)
    for x0, y0, x1, y1 in ((50, 770, 245, 1040), (245, 785, 410, 1030), (415, 800, 562, 1028)):
        m[y0:y1, x0:x1] = 255                                                  # ba bức tranh
    m |= poly(sh, [(200, 1110), (1220, 1110), (1225, 1870), (195, 1870)])     # bàn + bốn ghế
    m = cv2.dilate(m, np.ones((15, 15), np.uint8))
    # chân tường đo trên các cột sạch: (0,1593) (180,1547) (1240,1478) (1365,1430)
    xs_ = np.arange(w)
    fyx = np.interp(xs_, [0, 180, 1240, 1365], [1593, 1547, 1478, 1430])
    yy = np.arange(h)[:, None].repeat(w, 1); fy = fyx[None, :].repeat(h, 0)
    wall = yy < fy; floor = ~wall
    out = img.copy()
    # tường trắng: lan Navier-Stokes ở nửa cỡ, che sàn khi lan
    mm = ((m > 0) & wall).astype(np.uint8) * 255
    block = (floor | (m > 0)).astype(np.uint8) * 255
    small = cv2.resize(out, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    ms = cv2.dilate(cv2.resize(block, (w // 2, h // 2), interpolation=cv2.INTER_NEAREST), np.ones((3, 3), np.uint8))
    ms[(cv2.resize((~wall).astype(np.uint8), (w // 2, h // 2), interpolation=cv2.INTER_NEAREST) > 0)] = 255
    base = cv2.resize(cv2.inpaint(small, ms, 12, cv2.INPAINT_NS), (w, h), interpolation=cv2.INTER_CUBIC)
    wallfill = cv2.GaussianBlur(base.astype(np.float32), (0, 0), 7)   # tường trơn: làm mượt, bớt vệt loang
    # sàn: độ sáng theo hàng (trung vị phần sàn sạch hai bên), cộng hạt sàn
    clean = floor & (m == 0)
    prof = np.zeros((h, 3), np.float32); ok = np.zeros(h, bool)
    for y in range(h):
        xs = np.nonzero(clean[y])[0]
        if len(xs) > 30:
            prof[y] = np.median(img[y, xs].astype(np.float32), axis=0); ok[y] = True
    idx = np.arange(h)
    for c in range(3):
        prof[:, c] = np.interp(idx, idx[ok], prof[ok, c])
    prof = cv2.GaussianBlur(prof.reshape(h, 1, 3), (1, 0), sigmaX=0.1, sigmaY=12).reshape(h, 3)
    g = img.astype(np.float32); hf = g - cv2.GaussianBlur(g, (0, 0), 3)
    rng = np.random.default_rng(4); noise = np.zeros_like(g)
    fm = (m > 0) & floor
    for by in range(1400, h, 32):
        for bx in range(0, w, 32):
            if not fm[by:by + 32, bx:bx + 32].any():
                continue
            sx = rng.integers(20, 170); sy = rng.integers(1700, h - 34)
            blk = hf[sy:sy + 32, sx:sx + 32]; hh, ww = noise[by:by + 32, bx:bx + 32].shape[:2]
            noise[by:by + hh, bx:bx + ww] = blk[:hh, :ww]
    # mỗi hàng: nội suy ngang giữa mép sàn sạch bên trái và bên phải vùng xoá
    lin = np.repeat(prof[:, None, :], w, axis=1)
    lo = cv2.GaussianBlur(g, (0, 0), 3)
    for y in range(1400, h):
        xs = np.nonzero(fm[y])[0]
        if not len(xs):
            continue
        x0, x1 = xs.min(), xs.max()
        cl = np.nonzero(clean[y, :x0])[0]          # mẫu sàn sạch thật sự bên trái, bên phải (ngoài vùng xoá)
        cr = np.nonzero(clean[y, x1 + 1:])[0]
        L = lo[y, max(cl.max() - 20, 0)] if len(cl) else prof[y]
        Rr = lo[y, min(x1 + 1 + cr.min() + 20, w - 1)] if len(cr) else prof[y]
        t = (np.arange(x0, x1 + 1) - x0) / max(x1 - x0, 1)
        lin[y, x0:x1 + 1] = L[None, :] * (1 - t[:, None]) + Rr[None, :] * t[:, None]
    lin = cv2.GaussianBlur(lin, (0, 0), sigmaX=2, sigmaY=10)
    floorfill = lin + noise * 1.0
    fill = np.where(wall[..., None], wallfill, floorfill)
    a = cv2.GaussianBlur((m > 0).astype(np.float32), (0, 0), 2.5)[..., None]
    out = np.clip(img.astype(np.float32) * (1 - a) + fill * a, 0, 255).astype(np.uint8)
    cv2.imwrite(out_empty, out)


if __name__ == '__main__':
    main(*sys.argv[1:4])
