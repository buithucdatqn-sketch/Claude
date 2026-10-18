"""Bảng phân cảnh tập 7: thay khung cảnh phòng ngủ bằng khung của engine phụ (ảnh 09) rồi dựng lại storyboard.png (cùng bố cục engine v7)."""
import json, os, shutil, sys
from PIL import Image, ImageDraw, ImageFont
OUT = sys.argv[1] if len(sys.argv) > 1 else "./"
HERE = os.path.dirname(os.path.abspath(__file__))
F = lambda s: ImageFont.truetype(os.path.join(HERE, "PatrickHand-Regular.ttf"), s)
sp = json.load(open(os.path.join(HERE, "splice.json")))
k0, k1 = sp["scenes"]
for j, k in enumerate(range(k0, k1 + 1)):
    shutil.copy(os.path.join(OUT, "frames_ngu", f"scene_{j + 2}.png"), os.path.join(OUT, "frames", f"scene_{k + 1}.png"))
SC = json.load(open(os.path.join(HERE, "scenes.json")))
PW, PH, GAP, MX, TOP, cols = 360, 640, 34, 50, 200, 4
rows = (len(SC) + cols - 1) // cols
sheet = Image.new("RGB", (MX * 2 + cols * PW + (cols - 1) * GAP, TOP + rows * (PH + 86) + 250), (30, 27, 24))
d = ImageDraw.Draw(sheet)
d.text((MX, 38), "AH Decode · Cứng ở xa, mềm trong tầm tay", font=F(60), fill=(255, 255, 255))
d.text((MX, 118), "Ảnh dán bằng băng giấy · nền trắng · chữ nâu trên nền, trắng trên ảnh", font=F(34), fill=(200, 194, 186))
d.text((MX, 158), "Camera zoom vào chi tiết · nét doodle gốc của bài lộ dần theo lời đọc", font=F(34), fill=(200, 194, 186))
for i, sc in enumerate(SC):
    r, c = divmod(i, cols)
    x, y = MX + c * (PW + GAP), TOP + r * (PH + 86)
    sheet.paste(Image.open(os.path.join(OUT, "frames", f"scene_{i + 1}.png")).resize((PW, PH), Image.LANCZOS), (x, y))
    d.text((x, y + PH + 10), f"Cảnh {i + 1}", font=F(40), fill=(255, 255, 255))
    d.text((x + 150, y + PH + 16), sc["t"], font=F(32), fill=(200, 194, 186))
fy = TOP + rows * (PH + 86) + 10
d.text((MX, fy), "Ảnh 08 (phòng khách) cho mọi cảnh, trừ cảnh %d dùng ảnh 09 (phòng ngủ, engine phụ ghép vào)." % (k0 + 1), font=F(32), fill=(255, 255, 255))
d.text((MX, fy + 44), "Nét trắng và nhãn chữ là doodle gốc của bài, tách lớp rồi lộ dần (cảnh 5, 6, 7).", font=F(32), fill=(225, 220, 212))
d.text((MX, fy + 88), "Cảnh zoom kín ảnh: chữ trắng viết lên ảnh, phủ tối nhẹ đúng dải chữ.", font=F(32), fill=(225, 220, 212))
sheet.save(os.path.join(OUT, "storyboard.png"))
print("storyboard", sheet.size)
