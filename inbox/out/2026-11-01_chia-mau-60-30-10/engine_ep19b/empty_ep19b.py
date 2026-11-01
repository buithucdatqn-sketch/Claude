# -*- coding: utf-8 -*-
"""Phòng trống cho cảnh "món nhấn 10%" (First House, ảnh ArchDaily _12):
xoá xô vàng, chồng sách, thảm xanh dương cùng ấm trắng và miếng bọt biển; giữ ghế gấp trắng.
Sàn, tường trắng: lan bằng inpaint Navier-Stokes ở nửa cỡ rồi thêm hạt sàn lấy từ vùng sạch.
Chạy: python3 -I empty_ep19b.py <_12.jpg> <ra_source.png> <ra_empty.png>
"""
import sys
import numpy as np, cv2


def poly(sh, pts):
    m = np.zeros(sh[:2], np.uint8); cv2.fillPoly(m, [np.int32(pts)], 255); return m


def main(src, out_src, out_empty):
    img = cv2.imread(src); cv2.imwrite(out_src, img); sh = img.shape
    m = poly(sh, [(50, 1165), (292, 1165), (300, 1475), (48, 1478)])            # xô vàng
    m |= poly(sh, [(318, 1222), (560, 1222), (562, 1395), (318, 1395)])         # chồng sách
    m |= poly(sh, [(1088, 1188), (1632, 1186), (2000, 1480), (2000, 1500), (1100, 1500)])   # thảm + ấm + bọt biển
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    # mặt tường trụ trái (x < 314, trên chân tường y 1398): chép tường trắng phía trên xô xuống
    img = img.copy()
    ref = img[:, 4:40].astype(np.float32).mean(axis=1)          # dải tường sạch sát mép trái làm thước sáng
    for y in range(1150, 1399):
        r = ref[y] / np.maximum(ref[y - 270], 1)
        img[y, 40:314] = np.clip(img[y - 270, 40:314].astype(np.float32) * r, 0, 255).astype(np.uint8)
    m[1150:1399, 40:314] = 0
    small = cv2.resize(img, (sh[1] // 2, sh[0] // 2), interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, (sh[1] // 2, sh[0] // 2), interpolation=cv2.INTER_NEAREST)
    ms = cv2.dilate(ms, np.ones((5, 5), np.uint8))
    base = cv2.inpaint(small, ms, 10, cv2.INPAINT_NS)
    base = cv2.resize(base, (sh[1], sh[0]), interpolation=cv2.INTER_CUBIC)
    g = img.astype(np.float32)
    hf = g - cv2.GaussianBlur(g, (0, 0), 3)
    rng = np.random.default_rng(3)
    noise = np.zeros_like(g)
    src_box = (700, 1120, 1050, 1480)            # sàn sạch giữa phòng
    for by in range(1100, sh[0], 32):
        for bx in range(0, sh[1], 32):
            if not m[by:by + 32, bx:bx + 32].any():
                continue
            sx = rng.integers(src_box[0], src_box[2] - 32); sy = rng.integers(src_box[1], src_box[3] - 32)
            blk = hf[sy:sy + 32, sx:sx + 32]
            hh, ww = noise[by:by + 32, bx:bx + 32].shape[:2]
            noise[by:by + hh, bx:bx + ww] = blk[:hh, :ww]
    a = cv2.GaussianBlur((m > 0).astype(np.float32), (0, 0), 3)[..., None]
    fill = np.clip(base.astype(np.float32) + noise * 0.5, 0, 255)
    cv2.imwrite(out_empty, (g * (1 - a) + fill * a).astype(np.uint8))


if __name__ == '__main__':
    main(*sys.argv[1:4])
