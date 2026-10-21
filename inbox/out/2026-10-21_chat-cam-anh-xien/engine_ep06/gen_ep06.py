"""Tập 6: Chất cảm cần ánh xiên (bài 02 kho AH-Decode-Decor, ảnh 04 có doodle sẵn).
Sinh engine_ep06.py + engine_video_ep06.py từ hai engine gốc, và script.md/elevenlabs.txt từ cùng dữ liệu cảnh.
Ảnh dọc (1600x2400): thu nhỏ thẻ ảnh (CARD_W2 1320) và hạ tâm thẻ (C2 y 1880) để tiêu đề và lời đọc nằm ngoài ảnh ở cảnh rộng.
Doodle: không vẽ nét mới; lộ dần chính các nét doodle gốc của bài (doodle_ep06.npz: elip, mũi tên, nhãn chữ) theo mục 2c."""
import json
import re

E = "/home/user/Claude/engine/"
OUT = "/home/user/Claude/inbox/out/2026-10-21_chat-cam-anh-xien/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7

WIDE = "WIDE"
SC = [
    dict(part="A", head="Ảnh ấm, ngoài đời lạnh?", cam=WIDE, dark=False, dd=[],
         vo="Cùng một bức tường bê tông, sao trên ảnh thì ấm, ngoài đời lại lạnh?"),
    dict(part="B", head="Kilmer & Kilmer (2014): chất cảm cần ánh xiên", cam=((500, 420), 2.2, (540, 900)), dark=False, dd=[],
         vo="Theo hai tác giả Kilmer, chất cảm là thứ mình cảm nhận bằng mắt lẫn tay. Nhưng nó chỉ hiện ra khi ánh sáng rọi xiên.",
         tts="Theo hai tác giả Kin-mơ, chất cảm là thứ mình cảm nhận bằng mắt lẫn tay. Nhưng nó chỉ hiện ra khi ánh sáng rọi xiên."),
    dict(part="C", head="Đèn sáng đều làm vân chìm mất", cam=((700, 1000), 2.1, (540, 900)), dark=False, dd=[],
         vo="Nhiều nhà giữ bê tông mộc rất công phu. Rồi lắp đèn âm trần sáng đều, vân chìm mất."),
    dict(part="C", head="Nắng sát tường: mỗi gờ một vệt bóng", cam=((1050, 700), 2.1, (540, 900)), dark=True, dd=["ray"],
         vo="Mặt bê tông thô có vô số gờ nhỏ. Nắng chiếu sát tường, mỗi gờ đổ một vệt bóng, mắt nhờ đó thấy vân. Rọi thẳng thì bóng mất."),
    dict(part="E", head="Có nắng: hiện từng vệt ván khuôn", cam=((880, 650), 2.1, (540, 900)), dark=True, dd=["arr1", "lab1"],
         vo="Ban công nhà MS House của Studio Saransh, ở Ahmedabad, Ấn Độ. Nắng chéo xuống tường, chỗ có nắng hiện rõ từng vệt ván khuôn.",
         tts="Ban công nhà Ém-ét Hao-xơ của Xtu-đi-ô Xa-ran, ở A-mê-đa-bát, Ấn Độ. Nắng chéo xuống tường, chỗ có nắng hiện rõ từng vệt ván khuôn."),
    dict(part="E", head="Trong bóng: mảng xám phẳng", cam=((450, 1450), 2.1, (540, 900)), dark=True, dd=["arr2"],
         vo="Chỗ trong bóng chỉ còn mảng xám phẳng."),
    dict(part="H", head="Chốt lại", cam=WIDE, dark=False, dd=[],
         vo="Tường ấm hay lạnh, nhiều khi do ánh sáng. Muốn giữ vân, cho ánh sáng đi sát mặt tường. Bài phân tích đầy đủ cho thành viên ở phần bình luận nha."),
    dict(part="I", head="end", cam="END", dark=False, vo="", dd=[],
         tts="Ây-ết Đi-cốt, series về nguyên tắc thiết kế và chọn đồ đê-co. Theo dõi Giả Thuyết Kiến Trúc. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận.",
         say="AH Decode, series về nguyên tắc thiết kế và chọn đồ decor. Theo dõi Giả Thuyết Kiến Trúc. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận."),
]

DOODLE = r'''
_L = np.load(os.path.join(HERE, "doodle_ep06.npz"))
LAYER = {k: _L[k] for k in _L.files}   # toạ độ trên ảnh làm việc 1600x2400 (source.png)
RAD = dict(ray=0.8, arr1=0.8, arr2=0.8)         # bán kính nét gốc (px ảnh làm việc)


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
    for k in SCENES[i].get("dd", []):
        if k.startswith("lab"):
            _label(text, cam, LAYER[k])
        else:
            _stamp(wb, LAYER[k], RAD[k])
'''


def cover(fx, fy, z, anc, m=40):
    """dời điểm neo để ảnh phủ kín khung 1080x1920 khi zoom (ảnh dọc 1600x2400, 0.4 px khung / px ảnh ở z=1)"""
    sc = z * 0.4125
    assert sc * 2400 >= 1920 + 2 * m, z
    ax = min(max(anc[0], 1080 + m - sc * (1600 - fx)), sc * fx - m)
    ay = min(max(anc[1], 1920 + m - sc * (2400 - fy)), sc * fy - m)
    return (round(ax), round(ay))


def words(s):
    return len(s.split())


def build_data():
    t = 0.0
    scenes = []
    for k, s in enumerate(SC):
        spoken = s.get("tts", s["vo"])
        dur = max(3.5, TRANS + words(spoken) / WPS)
        if s["head"] == "end":
            dur = max(dur, 7.0)
        a, b = round(t, 1), round(t + dur, 1)
        t = b
        s["t"] = f"{a:g}–{b:g}s"
        s["dur"] = b - a
        if s["cam"] == WIDE:
            cam = "WIDE"
        elif s["cam"] == "END":
            cam = "(CENTER, 0.8, (540, 600))"
        else:
            (fx, fy), z, anc = s["cam"]
            if not s.get("free"):
                anc = cover(fx, fy, z, anc)
            cam = f"(({fx}, {fy}), {z}, {anc})"
        scenes.append(f'    dict(t="{s["t"]}", head={json.dumps(s["head"], ensure_ascii=False)}, '
                      f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={cam}, dark={s["dark"]}, dd={s["dd"]}),')
    data = ('# ---------------- scenes ----------------\nCENTER = (SW / 2, SH / 2)\nOBJ = {}\n\n'
            'WIDE = (CENTER, 1.0, (540, 940))\nSCENES = [\n' + "\n".join(scenes) + '\n]\n'
            'END = len(SCENES) - 1\nBOARDS = {}\n' + DOODLE + '\n\n')
    return data, t


def build(src, dst, video, data):
    s = open(E + src).read()
    rep = [('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"',
            'CREDIT = "Ảnh dự án: MS House, Ahmedabad, Ấn Độ · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project"'),
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · CHẤT CẢM CẦN ÁNH XIÊN"'),
           ("CARD_W2, BORDER2 = 1920, 0", "CARD_W2, BORDER2 = 1320, 0  # ảnh dọc 3:4: thẻ hẹp hơn để chữ nằm ngoài ảnh"),
           ("C2 = (B2W / 2, 1810.0)", "C2 = (B2W / 2, 1880.0)")]
    rep.append(("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"))
    for a_, b_ in rep:
        assert a_ in s, a_
        s = s.replace(a_, b_)
    a = s.index("# ---------------- scenes")
    b = s.index('def render_scene') if not video else s.index('BOARDS["plain"] = make_board(1.0)')
    s = s[:a] + data + s[b:]
    if video:
        s = s.replace('"reel1_silent.mp4"', '"reel_chat-cam-anh-xien_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', '"frames"').replace('"storyboard_reel1_v7.png"', '"storyboard.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Chất cảm cần ánh xiên")
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Ảnh dán bằng băng giấy · nền trắng · chữ nâu trên nền, trắng trên ảnh")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét doodle gốc của bài lộ dần theo lời đọc")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ (cảnh 4, 5, 6); các cảnh khác giữ ảnh nguyên bản.")
    open(OUT + "engine_ep06/" + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v7.py", "engine_ep06.py", False, data)
build("engine_video.py", "engine_video_ep06.py", True, data)

# ---- script.md + elevenlabs.txt ----
NAMES = dict(A="Mở", B="Nguồn gốc", C="Cơ chế", D="Đọc trên ảnh", E="Phản ví dụ", F="Áp dụng",
             G="Chọn đồ", H="Chốt", I="Cảnh cuối")
shown = [s.get("say", s["vo"]) for s in SC]
spoken_all = [s.get("tts", s["vo"]) for s in SC]
nw = sum(words(x) for x in shown)
rows = []
for k, s in enumerate(SC):
    head = "(khung cuối cố định)" if s["head"] == "end" else s["head"]
    cam = "rộng" if s["cam"] == WIDE else ("khung cuối" if s["cam"] == "END" else f"zoom {s['cam'][1]}× vào {s['cam'][0]}")
    dd = ", ".join(s["dd"]) or "không nét"
    rows.append(f'| {k + 1} | {s["t"]} | {s["part"]} · {NAMES[s["part"]]} | {head} | {shown[k]} | {cam}; {dd} |')
md = (f"# AH Decode · Chất cảm cần ánh xiên · BẢN NHÁP chờ duyệt\n\n"
      f"Bài trong kho: `AH-Decode-Decor/bai-02-3-bai-hoc-chat-cam-vat-lieu-noi-that/bai-02.md` (commit 4becc17), ý chính: mục \"Chất cảm chỉ hiện rõ khi ánh sáng chiếu xiên qua bề mặt\".\n"
      f"Ảnh: `anh/04-doodle-nang-xien-ban-cong.jpg` · MS House, Ahmedabad, Ấn Độ · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project\n"
      f"Thời lượng dự kiến: {total:.1f} giây + 1 giây giữ khung cuối · {nw} từ lời đọc (chữ viết) · {len(SC)} cảnh.\n"
      f"Nét: chỉ dùng doodle gốc của bài (các tia nắng nét đứt, hai mũi tên và các nhãn gốc \"nắng chéo qua tán cây, vân mới hiện\", \"phần có nắng lộ từng vệt ván khuôn\", \"phần trong bóng chỉ còn mảng xám phẳng\"), lộ dần; không vẽ nét mới.\n\n"
      "| # | Thời lượng | Phần | Tiêu đề trên khung | Lời đọc | Hình |\n|---|---|---|---|---|---|\n" + "\n".join(rows) +
      "\n\n## Lời đọc liền mạch\n\n" + " ".join(shown) + "\n\n"
      "## Phiên âm cho ElevenLabs\n\n| Chính tả gốc | Phiên âm |\n|---|---|\n"
      "| Kilmer | Kin-mơ |\n| MS House | Ém-ét Hao-xơ |\n| Studio Saransh | Xtu-đi-ô Xa-ran |\n| Ahmedabad | A-mê-đa-bát |\n| Designing Interiors | Đi-dai-ninh In-tia-ri-ơ |\n"
      "| AH Decode | Ây-ết Đi-cốt |\n| decor | đê-co |\n")
open(OUT + "script.md", "w").write(md)


def lines(txt):
    parts = re.split(r'(?<=[.?!])\s+', txt.strip())
    return "\n".join(p for p in parts if p)


el = "\n\n".join(lines(x) for x in spoken_all)
el += "\n\n---\n--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese ---\n"
open(OUT + "elevenlabs.txt", "w").write(el)
print("total", round(total, 1), "words", nw)
for s in SC:
    print(s["t"], words(s.get("say", s["vo"])), s["head"])
