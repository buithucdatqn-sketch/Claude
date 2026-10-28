"""Tập 14: khung cuối toàn màn hình từ ảnh sổ tay AH+ chủ Trang gửi (ảnh tĩnh hoặc GIF động).
Ảnh 800x1000 phóng x1,55 phủ kín khung 1080x1920; phần thiếu ở mép (trên, dưới, phải) lấp bằng vải nền phản chiếu.
iPad (ảnh gốc x 155–780, y 275–768) nằm ở khung x 55–1024, y 498–1262: trọn trong khung 4:5 của bảng tin (y 285–1635).
Chữ ngắn đặt ngoài vùng iPad: credit nhỏ ở trên, ba dòng mời ở dải vải tối phía dưới (y 1280–1480).
Chạy: python3 -I end_ep14.py <ảnh hoặc gif> <OUT> [giây]  ->  OUT/frames/scene_14.png (khung đầu),
và nếu có [giây]: OUT/end_ep14.mp4 (30 fps, GIF lặp theo thời lượng từng khung) để ghép thay đoạn khung cuối ở giai đoạn B."""
import os, subprocess, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageSequence

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "PatrickHand-Regular.ttf")
W, H = 1080, 1920
S, OX, OY = 1.55, 185, -72          # X = S*x - OX, Y = S*y - OY
IPAD = [(155, 405), (480, 275), (780, 580), (430, 768)]   # bốn góc iPad trên ảnh gốc
LINES = [(1280, "Sổ tay Công thức chọn màu nội thất", 54, 255),
         (1340, "bảng tra nhanh 17 tình huống chọn màu", 46, 240),
         (1400, "xem ở phần bình luận", 62, 255)]
CREDIT = (352, "Ảnh: sổ tay AH+ Công thức chọn màu nội thất · Giả Thuyết Kiến Trúc", 28, 225)


def place(frame):
    """phóng ảnh và lấp mép bằng phản chiếu để phủ kín khung"""
    a = np.array(frame.convert("RGB"))
    a = cv2.resize(a, (round(a.shape[1] * S), round(a.shape[0] * S)), interpolation=cv2.INTER_LANCZOS4)
    top, left = max(0, -OY), max(0, -OX)
    bottom = max(0, H - (a.shape[0] - OY))
    right = max(0, W - (a.shape[1] - OX))
    a = cv2.copyMakeBorder(a, top, bottom, left, right, cv2.BORDER_REFLECT)
    y0, x0 = OY + top, OX + left
    return Image.fromarray(a[y0:y0 + H, x0:x0 + W])


def text_layer():
    """chữ trắng có bóng mờ, căn giữa; trả về (lớp chữ, lớp bóng)"""
    t = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(t)
    for y, s, sz, f in LINES + [CREDIT]:
        font = ImageFont.truetype(FONT, sz)
        d.text((W / 2, y), s, font=font, fill=f, anchor="ma")
    sh = t.filter(ImageFilter.GaussianBlur(6))
    return t, sh


def check(t):
    """chữ không được chạm vùng iPad, và phải nằm trong vùng an toàn Reels / bảng tin (y 340–1490, x 60–1020)"""
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(S * x - OX, S * y - OY) for x, y in IPAD], fill=255)
    m = m.filter(ImageFilter.MaxFilter(21))
    a, b = np.array(t) > 40, np.array(m) > 0
    ys, xs = np.nonzero(a)
    err = []
    if (a & b).any():
        err.append("LỖI: chữ đè lên iPad")
    if ys.min() < 340 or ys.max() > 1490 or xs.min() < 60 or xs.max() > 1020:
        err.append(f"LỖI: chữ ra ngoài vùng an toàn (y {ys.min()}–{ys.max()}, x {xs.min()}–{xs.max()})")
    box = [(S * x - OX, S * y - OY) for x, y in IPAD]
    bx, by = [p[0] for p in box], [p[1] for p in box]
    if min(bx) < 0 or max(bx) > W or min(by) < 285 or max(by) > 1635:
        err.append("LỖI: iPad ra ngoài khung 4:5 của bảng tin")
    print("iPad trên khung: x %d–%d, y %d–%d" % (min(bx), max(bx), min(by), max(by)), *err, sep="\n")


def render(frame, t, sh):
    base = place(frame).convert("RGB")
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    base = Image.composite(dark, base, sh.point(lambda v: int(v * 0.55)))
    return Image.composite(Image.new("RGB", (W, H), (255, 255, 255)), base, t)


def main():
    src, out = sys.argv[1], os.path.abspath(sys.argv[2]) + "/"
    dur = float(sys.argv[3]) if len(sys.argv) > 3 else 0
    im = Image.open(src)
    t, sh = text_layer()
    check(t)
    frames = [(f.copy(), f.info.get("duration", 100) or 100) for f in ImageSequence.Iterator(im)]
    print("số khung của ảnh nguồn:", len(frames))
    os.makedirs(out + "frames", exist_ok=True)
    render(frames[0][0], t, sh).save(out + "frames/scene_14.png")
    if dur:
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", out + "end_ep14.mp4"],
                             stdin=subprocess.PIPE)
        cache, n, k, acc = {}, int(round(dur * 30)), 0, 0.0
        for i in range(n):
            while acc + frames[k][1] / 1000 <= i / 30:      # GIF lặp theo thời lượng từng khung
                acc += frames[k][1] / 1000
                k = (k + 1) % len(frames)
            if k not in cache:
                cache[k] = np.array(render(frames[k][0], t, sh)).tobytes()
            p.stdin.write(cache[k])
        p.stdin.close()
        p.wait()
        print("end_ep14.mp4", n, "khung")


main()
