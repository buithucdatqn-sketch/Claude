# -*- coding: utf-8 -*-
"""Phòng trống cho cảnh mở tập 19 (Stage in Hayama, ảnh ArchDaily _10, ban ngày).
Xoá sofa trắng (cả tấm lông), bàn gốc cây và tấm thảm nhỏ; giữ nguyên bàn ăn, ghế, đèn.
Dùng lại hàm của engine/sketch_anim/empty_room.py.
Chạy: python3 -I empty_ep19.py <ảnh_10.jpg> <ra_source_h10.png> <ra_empty_h10.png>
"""
import os, sys
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = HERE
while not os.path.exists(os.path.join(REPO, 'engine', 'sketch_anim', 'empty_room.py')):
    REPO = os.path.dirname(REPO)
sys.path.insert(0, os.path.join(REPO, 'engine', 'sketch_anim'))
from empty_room import poly_mask, col_copy  # noqa: E402


def main(src, out_src, out_empty):
    img = cv2.imread(src)                      # 2000x1600, giữ nguyên cỡ (<2400)
    cv2.imwrite(out_src, img)
    sh = img.shape
    sofa = poly_mask(sh, [[(935, 1140), (1178, 1140), (1182, 1198), (1290, 1222), (1302, 1505), (898, 1505), (900, 1262)]])
    stump = poly_mask(sh, [[(1255, 1282), (1560, 1282), (1612, 1440), (1600, 1540), (1290, 1540)]])
    allm = sofa | stump
    yy, xx = np.mgrid[0:sh[0], 0:sh[1]]
    fy = 1246
    wall_m = ((allm > 0) & (yy < fy)).astype(np.uint8)
    floor_m = ((allm > 0) & (yy >= fy)).astype(np.uint8) * 255
    out = img.copy()
    # vách gỗ và cạnh tủ (x 930–1084): chép theo cột từ đoạn y 920–1000 (không có đèn bàn, không vệt sáng)
    m = wall_m.copy(); m[:, 1085:] = 0
    col_copy(out, m, 900, 1085, 920, 1000)
    # mặt ngăn kéo (x 1085–1300, vân ngang): lặp theo hàng dải sạch x 1176–1196
    m = wall_m.copy(); m[:, :1085] = 0
    ys, xs = np.nonzero(m)
    for y, x in zip(ys, xs):
        out[y, x] = out[y, 1176 + (x - 1085) % 20]
    # sàn bê tông có vệt nắng: lan theo đường đẳng sáng (Navier-Stokes) rồi thêm hạt bê tông
    big = cv2.dilate(floor_m, np.ones((5, 5), np.uint8))
    # chỉ cho sàn lan vào sàn: che luôn phần tường phía trên chân tường khi lan
    lf_mask = big.copy(); lf_mask[:fy + 2, 860:1340] = 255
    small = cv2.resize(out, (sh[1] // 2, sh[0] // 2), interpolation=cv2.INTER_AREA)
    ms = cv2.resize(lf_mask, (sh[1] // 2, sh[0] // 2), interpolation=cv2.INTER_NEAREST)
    base = cv2.inpaint(small, ms, 12, cv2.INPAINT_NS)
    base = cv2.resize(base, (sh[1], sh[0]), interpolation=cv2.INTER_CUBIC)
    base = cv2.GaussianBlur(base, (0, 0), 1.2)
    clean = ((yy >= fy + 10) & (allm == 0)).astype(np.uint8)
    g = out.astype(np.float32)
    hf = g - cv2.GaussianBlur(g, (0, 0), 4)
    ys, xs = np.nonzero(clean[1420:1600, 650:1300]); ys += 1420; xs += 650
    rng = np.random.default_rng(5)
    noise = np.zeros_like(g)
    for by in range(1240, 1560, 32):
        for bx in range(880, 1600, 32):
            i = rng.integers(len(ys)); sy, sx = ys[i], xs[i]
            sy = min(max(sy, 16), sh[0] - 17); sx = min(max(sx, 16), sh[1] - 17)
            noise[by:by + 32, bx:bx + 32] = hf[sy - 16:sy + 16, sx - 16:sx + 16][:min(32, sh[0] - by), :min(32, sh[1] - bx)]
    a_ = cv2.GaussianBlur((big > 0).astype(np.float32), (0, 0), 2.5)[..., None]
    fill = np.clip(base.astype(np.float32) + noise * 0.3, 0, 255)
    out = (out.astype(np.float32) * (1 - a_) + fill * a_).astype(np.uint8)
    cv2.imwrite(out_empty, out)


if __name__ == '__main__':
    main(*sys.argv[1:4])
