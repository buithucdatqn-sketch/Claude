# -*- coding: utf-8 -*-
"""Ảnh bìa tập 19: ảnh chạng vạng phủ kín khung, hộp chữ trắng thẳng (mục 00b)."""
import os, sys
import cv2, numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
REPO = HERE
while not os.path.exists(os.path.join(REPO, 'engine', 'sketch_anim', 'sketch_reel.py')):
    REPO = os.path.dirname(REPO)
sys.path.insert(0, os.path.join(REPO, 'engine', 'sketch_anim'))
from sketch_reel import cam_matrix, font, wrap, W, H  # noqa: E402
img = cv2.imread(os.path.join(OUT, 'source_h21.png'))
M, s = cam_matrix(820, 1000, 1350, *img.shape[:2])
f = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
im = Image.fromarray(f[..., ::-1]); d = ImageDraw.Draw(im)
x, y, w = 60, 336, 960
lines = wrap('Ban ngày hợp, tối bật đèn lại lệch tông?', font(80), w - 70, d)
hh = 30 + 40 + 92 * len(lines) + 70
d.rectangle([x, y, x + w, y + hh], fill=(255, 255, 255))
d.text((x + 34, y + 24), 'AH DECODE · ĐÈN LÀM LỆCH MÀU GỖ', font=font(32), fill=(95, 90, 85))
for j, ln in enumerate(lines):
    d.text((x + 34, y + 70 + j * 92), ln, font=font(80), fill=(38, 34, 30))
d.text((x + 34, y + 70 + 92 * len(lines) + 12), 'Chỉ số Ra, R9 trên nhãn đèn nói gì về màu gỗ', font=font(36), fill=(110, 105, 100))
im.save(os.path.join(OUT, 'anh_bia_den-lech-mau-go.png'))
print('xong bìa')
