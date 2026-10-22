"""Tập 10: chạy engine khung hình của từng run (runs.json), gom khung của mỗi cảnh vào frames/, dựng storyboard.png (bố cục engine v7)."""
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
    out = subprocess.run(["/usr/bin/python3", "-I", os.path.join(HERE, f"engine_ep10_{r['tag']}.py"), OUT + r["src"], OUT],
                         capture_output=True, text=True)
    for line in (out.stdout + out.stderr).splitlines():
        if "LỖI" in line or "CẢNH BÁO" in line or "Error" in line:
            print(r["tag"], line)
    for j, k in enumerate(r["scenes"]):
        shutil.copy(OUT + f"frames_{r['tag']}/scene_{r['first_frame'] + j}.png", OUT + f"frames/scene_{k}.png")
    shutil.rmtree(OUT + "frames_" + r["tag"])
    if os.path.exists(OUT + f"storyboard_{r['tag']}.png"):
        os.remove(OUT + f"storyboard_{r['tag']}.png")
NAME = dict(dgt="ảnh 10 diagram (hàng trên)", dgb="ảnh 10 diagram (hàng dưới)", hl="ảnh 11 hành lang", mb="ảnh 03 mặt bằng tầng một", ph="ảnh 12 phòng ngủ")
img_of = {k: r["img"] for r in RUNS for k in r["scenes"]}
PW, PH, GAP, MX, TOP, cols = 360, 640, 34, 50, 200, 4
rows = (len(SC) + cols - 1) // cols
sheet = Image.new("RGB", (MX * 2 + cols * PW + (cols - 1) * GAP, TOP + rows * (PH + 120) + 200), (30, 27, 24))
d = ImageDraw.Draw(sheet)
d.text((MX, 38), "AH Decode · Vân thô ở xa, vân mịn ở gần", font=F(60), fill=(255, 255, 255))
d.text((MX, 118), "Bốn ảnh của bài: diagram 10, mặt bằng tầng một 03, hành lang 11, phòng ngủ 12 (kho chưa có thêm ảnh không gian khác)", font=F(34), fill=(200, 194, 186))
d.text((MX, 158), "Ảnh sạch (nhãn doodle gốc nằm sát mép ảnh, ngoài dải chữ an toàn) · camera trôi nhẹ", font=F(34), fill=(200, 194, 186))
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
