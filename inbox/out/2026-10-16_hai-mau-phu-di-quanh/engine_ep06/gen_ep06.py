"""Tập 6 (nhiều ảnh): Một màu chủ đạo, hai màu phụ đi vòng quanh (bài 01 kho AH-Decode-Decor).
Dùng ba ảnh doodle của bài: 13 (bếp xanh, ghế hồng), 10 (lò sưởi: đồng vàng, đá hồng, thảm), 11 (bếp: một màu xanh, ba chất liệu).
Sinh engine_ep06.py + engine_video_ep06.py từ hai engine gốc qua engine/multi_patch.py, và script.md, elevenlabs.txt từ cùng dữ liệu cảnh.
Chạy: python3 -I gen_ep06.py (cần source_<id>.png, doodle_<id>.npz do prep_ep06.py tạo)."""
import json
import os
import re
import sys

REPO = "/home/user/Claude/"
E = REPO + "engine/"
OUT = REPO + "inbox/out/2026-10-16_hai-mau-phu-di-quanh/"
sys.path.insert(0, E)
from multi_patch import patch  # noqa: E402

WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7
IDS = ["13", "09", "08", "03", "11", "10"]
DIM = {"13": (1800, 2400), "10": (1800, 2400), "11": (2400, 1800), "03": (2400, 1451), "09": (1652, 1167), "08": (2160, 2020)}
CR_PLAN = "Mặt bằng: The Green Box, Berlin · Ester Bruzkus Architekten (qua ArchDaily)"
CR_AXO = "Trục đo: The Green Box, Berlin · Ester Bruzkus Architekten (qua ArchDaily)"
CR_DIA = "Sơ đồ theo Kilmer & Kilmer (2014), tr. 166–167; Beadle (2023)"
KITCHEN = ("ellipse", 1134, 752, 330, 140)       # mặt bằng 03: tủ bếp chạy liền + đảo bếp
LIVING = ("ellipse", 1951, 698, 255, 275)        # mặt bằng 03: phòng khách quanh thảm tròn
SOFA = ("ellipse", 991, 455, 82, 88)             # trục đo 09: sofa vàng
FIRE = ("ellipse", 1134, 291, 48, 78)            # trục đo 09: mảng ốp đồng quanh lò sưởi


def wide(i, z=1.0):
    w, h = DIM[i]
    return ((w // 2, h // 2), z, (540, 940))


def cover(i, fx, fy, z, anc, m=40):
    """ảnh phủ kín khung khi zoom: dời điểm neo (thẻ dọc rộng 1440, thẻ ngang rộng 1920 trên canvas 2x)"""
    w, h = DIM[i]
    card = 1440 if h > w else 1920
    sc = z * card / w / 2
    assert sc * h >= 1920 + 2 * m and sc * w >= 1080 + 2 * m, (i, z)
    ax = min(max(anc[0], 1080 + m - sc * (w - fx)), sc * fx - m)
    ay = min(max(anc[1], 1920 + m - sc * (h - fy)), sc * fy - m)
    return (round(ax), round(ay))


SC = [
    dict(part="A", img="13", head="Thêm màu có rối không?", cam=wide("13"), dark=False, dd=[],
         vo="Thêm màu thứ hai, thứ ba vào nhà, có bị rối mắt không?"),
    dict(part="E", img="09", head="Căn hộ có khối xanh ở giữa", cam=((780, 470), 2.0, (540, 960)), free=True, dark=False, ink=True, credit=CR_AXO, dd=[],
         vo="Mọi người nhìn căn hộ The Green Box ở Berlin nè. Giữa nhà là một khối xanh, quanh khối xanh có màu vàng và hồng tím.",
         tts="Mọi người nhìn căn hộ Đờ Grin Bóc ở Béc-lin nè. Giữa nhà là một khối xanh, quanh khối xanh có màu vàng và hồng tím."),
    dict(part="B", img="08", head="Một màu chủ đạo, hai màu phụ", cam=((1080, 1010), 1.0, (540, 880)), free=True, dark=False, ink=True, credit="", dd=[],
         vo="Sách Designing Interiors của Kilmer nói, phòng dễ chịu có một màu chủ đạo và hai màu phụ. Ở đây, xanh là chủ đạo, vàng và hồng tím là hai màu phụ.",
         tts="Sách Đi-dai-ninh In-tia-ri-ơ của Kin-mơ nói, phòng dễ chịu có một màu chủ đạo và hai màu phụ. Ở đây, xanh là chủ đạo, vàng và hồng tím là hai màu phụ."),
    dict(part="C", img="13", head="Sách không gắn với con số nào", cam=((1300, 1300), 2.2, (540, 900)), dark=False, dd=[],
         vo="Mọi người hay nghe công thức sáu mươi, ba mươi, mười. Sách không gắn với con số nào."),
    dict(part="E", img="03", head="Mặt bằng: bếp nằm trong khối xanh", cam=((1050, 740), 1.6, (540, 940)), free=True, dark=False, ink=True, credit=CR_PLAN, dd=[KITCHEN],
         vo="Trên mặt bằng, khối xanh chạy dọc giữa nhà, tủ bếp chạy liền với nó. Mình đứng ở bếp trước."),
    dict(part="E", img="13", head="Ở bếp: xanh phủ, ghế hồng", cam=((1300, 1750), 1.6, (760, 880)), free=True, dark=True, dd=["arr", "lab"],
         vo="Ở bếp, xanh phủ cả tủ lẫn tường. Còn ghế quầy bếp là hồng tím, màu phụ quay lại."),
    dict(part="C", img="11", head="Màu chủ đạo cũng tự lặp lại", cam=((1510, 900), 1.4, (540, 940)), free=True, dark=True,
         dd=["arr_stone", "arr_cab", "lab_stone", "lab_cab", "lab_wall", "lab_same"],
         vo="Màu chủ đạo cũng tự lặp lại, ở tường sơn, mặt đá và tủ."),
    dict(part="E", img="03", head="Sang phòng khách", cam=((1750, 700), 1.6, (540, 940)), free=True, dark=False, ink=True, credit=CR_PLAN, dd=[LIVING],
         vo="Giờ sang phòng khách, quanh tấm thảm tròn."),
    dict(part="E", img="10", head="Màu phụ thứ nhất: vàng", cam=((430, 700), 2.0, (420, 880)), free=True, dark=True, dd=["arr1", "lab1"],
         vo="Màu phụ thứ nhất là vàng, ở mảng ốp đồng quanh lò sưởi."),
    dict(part="E", img="10", head="Màu phụ thứ hai: hồng tím", cam=((330, 1560), 1.6, (440, 880)), free=True, dark=True, dd=["arr2a", "arr2b", "lab2"],
         vo="Màu phụ thứ hai là hồng tím, ở phiến đá và tấm thảm lông."),
    dict(part="C", img="10", head="Hai màu đối nhau thì làm dịu", cam=((420, 1750), 2.2, (330, 1388)), dark=False, dd=[],
         vo="Hồng tím gần như đối diện xanh lá trên bánh xe màu. Hai màu đối nhau mà cùng rực, đặt sát nhau là chói mắt, nên phải làm dịu."),
    dict(part="F", img="09", head="Mỗi màu phụ có mặt hai chỗ", cam=((950, 400), 1.5, (540, 690)), free=True, dark=False, ink=True, credit=CR_AXO, dd=[SOFA, FIRE],
         vo="Ở nhà mình, mỗi màu phụ nên có mặt ít nhất hai chỗ, trên hai chất liệu khác nhau, như vàng ở sofa và mảng ốp đồng. Dịu, nhỏ, quay lại thì không rối."),
    dict(part="I", img="13", head="end", cam="END", dark=False, vo="", dd=[],
         tts="Ây-ết Đi-cốt, series về nguyên tắc thiết kế và chọn đồ đê-co. Theo dõi Giả Thuyết Kiến Trúc. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận.",
         say="AH Decode, series về nguyên tắc thiết kế và chọn đồ decor. Theo dõi Giả Thuyết Kiến Trúc. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận."),
]

DOODLE = r'''
LAYERS = {_i: {k: v for k, v in np.load(os.path.join(HERE, "doodle_%s.npz" % _i)).items()} for _i in IMG_IDS}
# toạ độ nét/nhãn trên ảnh làm việc (cạnh dài 2400) của từng ảnh; mỗi cảnh chỉ hiện cụm nét của ảnh mình (trường img)
RAD = 1.0  # bán kính nét gốc (px ảnh làm việc)


def _stamp(wb, pts, r_src):
    """lộ lại nét doodle gốc theo đúng thứ tự vẽ (mỗi điểm là một chấm bút)"""
    rr = max(1, int(round(r_src * wb.v.s * SS)))
    for p in pts:
        x, y = wb.v.pt((float(p[0]), float(p[1])))
        if hasattr(wb, "circ"):
            wb.circ.append((int(x * SS), int(y * SS), rr))
        else:
            cv2.circle(wb.m, (int(x * SS), int(y * SS)), rr, 255, -1, cv2.LINE_AA)


def _label(text, cam, pts):
    """nhãn chữ viết tay gốc của bài, đưa vào lớp nhãn (hiện khi nét đạt 55-75%)"""
    r = max(0.55, 0.62 * cam.s)
    for p in pts:
        x, y = cam.pt((float(p[0]), float(p[1])))
        text.d.ellipse((x - r, y - r, x + r, y + r), fill=255)


def doodle(i, wb, text, cam):
    layer = LAYERS[SCENES[i]["img"]]
    for k in SCENES[i].get("dd", []):
        if isinstance(k, tuple):   # nét mới vẽ tay (cảnh mực trên mặt bằng/trục đo): ("ellipse", cx, cy, rx, ry) hoặc ("arrow", a, b)
            getattr(wb, k[0])(*k[1:])
        elif k.startswith("lab"):
            _label(text, cam, layer[k])
        else:
            _stamp(wb, layer[k], RAD)
'''


def words(s):
    return len(s.split())


# Giai đoạn 2: mốc bắt đầu từng cảnh đo từ giọng đọc (inbox/audio/hai-mau-phu-di-quanh.mp3, 70,11 giây; silencedetect -35dB d=0,25)
# mỗi cảnh bắt đầu 0,4 giây trước câu đầu của nó; cảnh cuối kéo hết giọng đọc
AUDIO_START = [0.0, 3.44, 10.03, 19.68, 23.62, 31.44, 36.18, 39.77, 42.02, 45.07, 48.33, 55.21, 61.8]
AUDIO_END = 70.11


def build_data():
    t = 0.0
    scenes = []
    for k, s in enumerate(SC):
        spoken = s.get("tts", s["vo"])
        dur = max(3.5, TRANS + words(spoken) / WPS)
        if s["head"] == "end":
            dur = max(dur, 7.0)
        a = AUDIO_START[k]
        b = AUDIO_START[k + 1] if k + 1 < len(SC) else AUDIO_END
        t = b
        s["t"] = f"{a:g}–{b:g}s"
        s["dur"] = b - a
        if s["cam"] == "END":
            w, h = DIM[s["img"]]
            cam = f"(({w // 2}, {h // 2}), 0.8, (540, 600))"
        else:
            (fx, fy), z, anc = s["cam"]
            if not s.get("free") and z > 1.0:
                anc = cover(s["img"], fx, fy, z, anc)
            cam = f"(({fx}, {fy}), {z}, {anc})"
        scenes.append(f'    dict(t="{s["t"]}", img="{s["img"]}", head={json.dumps(s["head"], ensure_ascii=False)}, '
                      f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={cam}, dark={s["dark"]}, dd={s["dd"]}'
                      + (', ink=True' if s.get("ink") else '') + (f', credit={json.dumps(s["credit"], ensure_ascii=False)}' if "credit" in s else '') + '),')
    data = ('# ---------------- scenes ----------------\nOBJ = {}\n\nSCENES = [\n' + "\n".join(scenes) + '\n]\n'
            'END = len(SCENES) - 1\nBOARDS = {}\n' + DOODLE + '\n\n')
    return data, t


def build(src, dst, video, data):
    s = open(E + src).read()
    for a_, b_ in [('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"',
                    'CREDIT = "Ảnh dự án: The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger"'),
                   ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · MỘT MÀU CHỦ ĐẠO, HAI MÀU PHỤ"'),
                   ("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))")]:
        assert a_ in s, a_
        s = s.replace(a_, b_)
    s = patch(s, video, IDS, data)
    if video:
        s = s.replace('"reel1_silent.mp4"', '"reel_hai-mau-phu-di-quanh_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', '"frames"').replace('"storyboard_reel1_v7.png"', '"storyboard.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Một màu chủ đạo, hai màu phụ")
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Ảnh dán bằng băng giấy · nền trắng · chữ nâu trên nền, trắng trên ảnh · mỗi cảnh một ảnh phù hợp nhất")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét doodle gốc của bài lộ dần theo lời đọc")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ; các cảnh khác giữ ảnh nguyên bản.")
    open(OUT + "engine_ep06/" + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v7.py", "engine_ep06.py", False, data)
build("engine_video.py", "engine_video_ep06.py", True, data)

# ---- script.md + elevenlabs.txt ----
NAMES = dict(A="Câu móc", B="Lý thuyết", C="Vấn đề / cơ chế", D="Đọc trên ảnh", E="Ví dụ công trình", F="Áp dụng / kết", I="Mời vào gói thành viên")
shown = [s.get("say", s["vo"]) for s in SC]
spoken_all = [s.get("tts", s["vo"]) for s in SC]
nw = sum(words(x) for x in shown)
rows = []
for k, s in enumerate(SC):
    head = "(khung cuối cố định)" if s["head"] == "end" else s["head"]
    if s["cam"] == "END":
        cam = "khung cuối"
    elif s["cam"][1] == 1.0:
        cam = "cảnh rộng"
    else:
        cam = f"zoom {s['cam'][1]}× vào {s['cam'][0]}"
    dd = ", ".join(k if isinstance(k, str) else "khoanh vùng bằng nét mực" for k in s["dd"]) or "không nét"
    rows.append(f'| {k + 1} | {s["t"]} | {s["part"]} · {NAMES[s["part"]]} | ảnh {s["img"]} | {head} | {shown[k]} | {cam}; {dd} |')
md = (f"# AH Decode · Một màu chủ đạo, hai màu phụ · BẢN DỰNG THEO GIỌNG ĐỌC\n\n"
      f"Bài trong kho: `AH-Decode-Decor/bai-01-3-bai-hoc-phoi-mau-noi-that-can-ho/bai-01.md` (commit 65b5427), ý chính: mục \"Một màu chủ đạo, hai màu phụ đi vòng quanh\".\n"
      f"Ảnh (sáu ảnh, đều trong `anh/` của bài): ảnh chụp có doodle gốc `13-doodle-anh-tong.jpg`, `10-doodle-hai-mau-am.jpg`, `11-doodle-dap-mau-bep.jpg`; ảnh định vị `03-mat-bang-the-green-box.png` (mặt bằng), `09-truc-do-the-green-box.jpg` (trục đo màu), `08-diagram-xanh-o-giua-am-di-quanh.png` (sơ đồ chủ đạo/phụ) · The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger\n"
      f"Thời lượng: {total:.1f} giây giọng đọc (đo từ file ghi âm) + 1 giây giữ khung cuối · {nw} từ lời đọc (chữ viết) · {len(SC)} cảnh.\n"
      f"Nét: ảnh chụp dùng doodle gốc của bài (mũi tên, nhãn chữ), lộ dần. Mặt bằng và trục đo không có doodle nên khoanh vùng bằng nét mực đứt vẽ tay (cảnh mực). Chuyển giữa hai ảnh là chuyển mờ 0,7 giây.\n\n"
      "| # | Thời lượng | Phần | Ảnh | Tiêu đề trên khung | Lời đọc | Hình |\n|---|---|---|---|---|---|---|\n" + "\n".join(rows) +
      "\n\n## Lời đọc liền mạch\n\n" + " ".join(shown) + "\n\n"
      "## Phiên âm cho ElevenLabs\n\n| Chính tả gốc | Phiên âm |\n|---|---|\n"
      "| Kilmer | Kin-mơ |\n| Designing Interiors | Đi-dai-ninh In-tia-ri-ơ |\n| The Green Box | Đờ Grin Bóc |\n| Berlin | Béc-lin |\n"
      "| Ester Bruzkus Architekten | Ét-xtơ Bờ-rút-cút Ác-ki-téc-ten |\n| AH Decode | Ây-ết Đi-cốt |\n| decor | đê-co |\n")
open(OUT + "script.md", "w").write(md)


def lines(txt):
    parts = re.split(r'(?<=[.?!])\s+', txt.strip())
    return "\n".join(p for p in parts if p)


el = "\n<break time=\"1.2s\" />\n".join(lines(x) for x in spoken_all)
el += "\n\n---\n--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese ---\n"
open(OUT + "elevenlabs.txt", "w").write(el)
print("total", round(total, 1), "words", nw)
for s in SC:
    print(s["t"], words(s.get("say", s["vo"])), s["img"], s["head"])
