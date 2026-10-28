"""Tập 14: chạy engine khung hình của từng run (runs.json), gom khung của mỗi cảnh vào frames/, dựng storyboard.png (bố cục engine v7)."""
import json, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "./") + "/"
HERE = os.path.dirname(os.path.abspath(__file__))
F = lambda s: ImageFont.truetype(os.path.join(HERE, "PatrickHand-Regular.ttf"), s)
RUNS = json.load(open(os.path.join(HERE, "runs.json")))
SC = json.load(open(os.path.join(HERE, "scenes.json")))
os.makedirs(OUT + "frames", exist_ok=True)
for r in RUNS:
    os.makedirs(OUT + "frames_" + r["tag"], exist_ok=True)
    out = subprocess.run(["/usr/bin/python3", "-I", os.path.join(HERE, f"engine_ep14_{r['tag']}.py"), OUT + r["src"], OUT],
                         capture_output=True, text=True)
    for line in (out.stdout + out.stderr).splitlines():
        if "LỖI" in line or "CẢNH BÁO" in line or "Error" in line:
            print(r["tag"], line)
    for j, k in enumerate(r["scenes"]):
        shutil.copy(OUT + f"frames_{r['tag']}/scene_{r['first_frame'] + j}.png", OUT + f"frames/scene_{k}.png")
    shutil.rmtree(OUT + "frames_" + r["tag"])
    if os.path.exists(OUT + f"storyboard_{r['tag']}.png"):
        os.remove(OUT + f"storyboard_{r['tag']}.png")
# khung cuối toàn màn hình từ video sổ tay chủ Trang gửi (AH_mockup_tablet.mp4; không có thì GIF, rồi bản WebP tĩnh)
_cands = [OUT + "original/chu-trang/" + f for f in sorted(os.listdir(OUT + "original/chu-trang")) if f.endswith((".mp4", ".gif"))] + [OUT + "original/chu-trang/ebook-so-tay-ah-plus.webp"]
_out = subprocess.run(["/usr/bin/python3", "-I", os.path.join(HERE, "end_ep14.py"), _cands[0], OUT], capture_output=True, text=True)
print(_out.stdout.strip(), _out.stderr.strip())
NAME = dict(hanh="trang tên chương 1, hành lang (Unsplash)", khe="mục 1.3, góc tường trắng (Unsplash)", dg="Hình 1.2 tường sáng nới phòng", banan="Pawson House, bàn ăn", thang="Pawson House, cầu thang", bep="Pawson House, bếp", ebook="sổ tay AH+ toàn màn hình (chủ Trang gửi)")
img_of = {k: r["img"] for r in RUNS for k in r["scenes"]}
PW, PH, GAP, MX, TOP, cols = 360, 640, 34, 50, 200, 4
rows = (len(SC) + cols - 1) // cols
sheet = Image.new("RGB", (MX * 2 + cols * PW + (cols - 1) * GAP, TOP + rows * (PH + 120) + 200), (30, 27, 24))
d = ImageDraw.Draw(sheet)
d.text((MX, 38), "AH Decode · Sơn trắng nới phòng hẹp được bao nhiêu?", font=F(60), fill=(255, 255, 255))
d.text((MX, 118), "Ảnh của sổ tay AH+ Công thức chọn màu nội thất, chương 1: Hình 1.2, hành lang, góc tường trắng, ba ảnh Pawson House", font=F(34), fill=(200, 194, 186))
d.text((MX, 158), "Nét doodle trắng nét đứt vẽ mới trên ảnh, lộ dần theo lời (cảnh 4–9) · camera trôi nhẹ", font=F(34), fill=(200, 194, 186))
for i, sc in enumerate(SC):
    r, c = divmod(i, cols)
    x, y = MX + c * (PW + GAP), TOP + r * (PH + 120)
    sheet.paste(Image.open(OUT + f"frames/scene_{i + 1}.png").resize((PW, PH), Image.LANCZOS), (x, y))
    d.text((x, y + PH + 8), f"Cảnh {i + 1}", font=F(40), fill=(255, 255, 255))
    d.text((x + 150, y + PH + 14), sc["t"], font=F(32), fill=(200, 194, 186))
    d.text((x, y + PH + 58), NAME[img_of[i + 1]], font=F(28), fill=(200, 194, 186))
fy = TOP + rows * (PH + 120) + 10
d.text((MX, fy), "Mỗi đoạn cảnh cùng ảnh dựng bằng một engine riêng (runs.json), video ghép theo mốc thời gian.", font=F(32), fill=(255, 255, 255))
d.text((MX, fy + 44), "Cảnh zoom kín ảnh: chữ trắng viết lên ảnh, phủ tối nhẹ đúng dải chữ; diagram, mặt bằng: chữ nâu trên nền trắng.", font=F(32), fill=(225, 220, 212))
sheet.save(OUT + "storyboard.png")
print("storyboard", sheet.size)
