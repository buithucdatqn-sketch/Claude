"""Tập 2 (làm lại): Tầm nhìn và nơi trú ẩn (prospect-refuge).
Sinh engine_ep02.py + engine_video_ep02.py từ hai engine gốc, và script/elevenlabs từ cùng dữ liệu cảnh."""
import json
import re
import sys

E = "/home/claude/claude/engine/"
OUT = "/home/claude/claude/inbox/out/2026-10-06_tam-nhin-noi-tru/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7

# camera: (focus trên ảnh xem 2000px, zoom, anchor)
WIDE = "WIDE"
SC = [
    dict(part="A", head="Bạn sẽ ngồi đâu?", cam=WIDE, dark=False,
         vo="Vào phòng này, bạn sẽ ngồi đâu?"),
    dict(part="B", head="Tầm nhìn và nơi trú ẩn", cam=WIDE, dark=True,
         vo="Thập niên bảy mươi, Jay Appleton đặt tên cho hai điều: tầm nhìn, và nơi trú ẩn."),
    dict(part="C", head="Vì sao thấy yên tâm?", cam=WIDE, dark=True,
         vo="Giả thuyết: chỗ vừa được che vừa nhìn xa giúp tổ tiên sống sót, nên ta thấy yên tâm."),
    dict(part="D", head="Nơi trú: lưng tựa vách", cam=((975, 640), 1.9, (540, 900)), dark=True,
         vo="Sofa tựa vách gỗ đặc, trần thấp dần: nơi trú."),
    dict(part="D", head="Tầm nhìn: ra tận biển", cam=((560, 640), 1.8, (540, 900)), dark=True,
         vo="Bên trái, vách kính nhìn ra biển: tầm nhìn."),
    dict(part="B", head="Công cụ của Wright", cam=WIDE, dark=True,
         vo="Nghiên cứu nhà Frank Lloyd Wright ghi nhận ông hay dùng độ cao trần và khoảng cách tới tường đặc."),
    dict(part="C", head="Nhưng bằng chứng nói gì?", cam=WIDE, dark=True,
         vo="Nhưng tổng hợp ba mươi tư nghiên cứu: trong nhà, tầm nhìn có bằng chứng mạnh hơn hẳn nơi trú."),
    dict(part="E", head="Đừng quây kín", cam=((560, 640), 1.8, (540, 900)), dark=True,
         vo="Nên tránh quây góc ngồi bằng vách cao hay tủ đứng."),
    dict(part="F", head="Áp dụng", cam=WIDE, dark=True,
         vo="Thử đặt ghế chính tựa tường đặc, mặt hướng ra cửa sổ."),
    dict(part="G", head="Chọn đồ: cao sát tường, thấp ở giữa", cam=((820, 930), 1.9, (540, 860)), dark=True,
         vo="Đồ cao nên sát tường, đồ giữa phòng nên thấp hơn tầm mắt khi ngồi."),
    dict(part="H", head="Công thức", cam=WIDE, dark=False,
         vo="Lưng có chỗ dựa, mắt có đường xa."),
    dict(part="I", head="end", cam="END", dark=False, vo="",
         tts="AH Decode, series về nguyên tắc thiết kế và chọn đồ decor. Theo dõi Giả Thuyết Kiến Trúc, bài viết cho thành viên ở link bình luận."),
]

DOODLE = r'''
def doodle(i, wb, text, cam):
    def lab(p, s_, size=60):
        x, y = cam.pt(D([p])[0])
        text.put((x, y), s_, size)

    def P(p):
        return D([p])[0]

    def note(xy, s_, target, size=56, bow=-30):
        """nhãn trên nền trắng phía trên ảnh + mũi tên mực chỉ vào điểm trên ảnh"""
        text.put(xy, s_, size)
        w_ = text.d.textlength(s_, font=F(size))
        tx, ty = cam.pt(P(target))
        wb.ink_arrow((xy[0] + w_ / 2, xy[1] + size + 14), (tx, ty - 10), bow=bow)

    sofa = OBJ["sofa"]
    if i == 1:  # nguồn gốc: hai cụm khái niệm
        wb.contour(OBJ["window"], offset=14, eps=3, w=7)
        wb.contour(sofa, offset=14, eps=3, w=7)
        note((60, 420), "tầm nhìn", (250, 330), 58, bow=20)
        note((520, 420), "nơi trú", (980, 775), 58, bow=-20)
    elif i == 2:  # cơ chế: nhìn ra xa từ chỗ được che
        wb.contour(sofa, offset=14, eps=3, w=7)
        wb.arrow(P((900, 860)), P((300, 640)), 7, bow=-30)
    elif i == 3:  # nơi trú
        wb.contour(sofa, offset=16, eps=3, w=8)
        wb.line(P((660, 205)), P((1270, 362)), 8)
        wb.dashed(P((645, 230)), P((645, 860)), 7)
        wb.dashed(P((1288, 410)), P((1288, 860)), 7)
        lab((690, 312), "trần dốc xuống", 54)
        lab((760, 560), "vách gỗ đặc", 54)
    elif i == 4:  # tầm nhìn
        wb.contour(OBJ["window"], offset=14, eps=3, w=8)
        wb.arrow(P((900, 870)), P((330, 660)), 8, bow=-36)
        lab((120, 420), "ra biển", 58)
    elif i == 5:  # Wright: trần + tường
        wb.line(P((660, 205)), P((1270, 362)), 7)
        wb.line(P((60, 250)), P((600, 170)), 7)
        wb.dashed(P((645, 230)), P((645, 860)), 6)
        lab((1000, 150), "độ cao trần", 50)
        lab((680, 720), "tường đặc", 50)
    elif i == 6:  # bằng chứng
        wb.contour(OBJ["window"], offset=14, eps=3, w=7)
        wb.contour(sofa, offset=14, eps=3, w=7)
        note((40, 400), "tầm nhìn: mạnh", (250, 330), 56, bow=20)
        note((560, 400), "nơi trú: yếu hơn", (980, 775), 56, bow=-20)
    elif i == 7:  # lỗi: tủ cao chắn
        wb.contour(OBJ["ghost"], offset=4, eps=2, w=8)
        wb.line(P((470, 390)), P((610, 900)), 6)
        wb.line(P((610, 390)), P((470, 900)), 6)
        wb.arrow(P((900, 870)), P((660, 760)), 7, bow=-16)
        lab((410, 250), "tủ cao ở đây?", 54)
    elif i == 8:  # áp dụng
        wb.contour(sofa, offset=14, eps=3, w=7)
        wb.contour(OBJ["sofa_r"], offset=14, eps=3, w=7)
        wb.arrow(P((960, 860)), P((330, 660)), 7, bow=-30)
        wb.arrow(P((1500, 900)), P((420, 600)), 7, bow=-50)
    elif i == 9:  # chọn đồ
        wb.contour(OBJ["ottomans"], offset=12, eps=3, w=8)
        wb.contour(OBJ["tables"], offset=12, eps=3, w=8)
        wb.dashed(P((300, 650)), P((1340, 650)), 6)
        lab((330, 540), "tầm mắt lúc ngồi", 50)
        lab((420, 1215), "thấp", 54)
    elif i == 10:  # công thức
        wb.contour(sofa, offset=14, eps=3, w=7)
        wb.arrow(P((900, 860)), P((300, 640)), 7, bow=-30)
'''

OBJ = r'''
OBJ = dict(
    window=D([(108, 340), (300, 322), (395, 318), (412, 880), (300, 900), (108, 905)]),
    sofa=D([(632, 785), (1325, 785), (1332, 900), (1325, 985), (632, 990), (628, 900)]),
    sofa_r=D([(1372, 905), (1505, 825), (1840, 980), (1836, 1150), (1700, 1232), (1380, 1060)]),
    ottomans=D([(305, 1000), (460, 930), (690, 925), (688, 1060), (600, 1195), (335, 1190)]),
    tables=D([(792, 935), (1030, 930), (1230, 950), (1310, 1080), (1310, 1195), (820, 1180)]),
    ghost=D([(450, 360), (630, 360), (630, 950), (450, 950)]),
)
'''


def words(s):
    return len(s.split())


def build_data():
    t = 0.0
    scenes = []
    for k, s in enumerate(SC):
        spoken = s.get("tts", s["vo"])
        dur = max(3.5, TRANS + words(spoken) / WPS)
        if s["head"] == "end":
            dur = max(dur, 6.0)
        a, b = round(t, 1), round(t + dur, 1)
        t = b
        s["t"] = f"{a:g}–{b:g}s"
        s["dur"] = b - a
        if s["cam"] == WIDE:
            cam = "WIDE"
        elif s["cam"] == "END":
            cam = "(CENTER, 1.0, (540, 640))"
        else:
            (fx, fy), z, anc = s["cam"]
            cam = f"((({fx} * 1.2), ({fy} * 1.2)), {z}, {anc})"
        scenes.append(f'    dict(t="{s["t"]}", head={json.dumps(s["head"], ensure_ascii=False)}, '
                      f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={cam}, dark={s["dark"]}),')
    data = ('# ---------------- scenes ----------------\nCENTER = (SW / 2, SH / 2)\n\n\n'
            'def D(pts):\n    """toạ độ đo trên ảnh xem 2000px -> ảnh làm việc 2400px"""\n'
            '    return [(x * 1.2, y * 1.2) for x, y in pts]\n\n' + OBJ +
            '\nWIDE = (CENTER, 1.0, (540, 905))\nSCENES = [\n' + "\n".join(scenes) + '\n]\n'
            'END = len(SCENES) - 1\nBOARDS = {}\n' + DOODLE + '\n\n')
    return data, t


def build(src, dst, video, data):
    s = open(E + src).read()
    s = s.replace('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"',
                  'CREDIT = "Ảnh dự án: Anderson Residence · Aaron G. Green · ảnh Sterling Reed · Dwell"')
    s = s.replace('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · TẦM NHÌN & NƠI TRÚ ẨN"')
    a = s.index("# ---------------- scenes")
    b = s.index('def render_scene') if not video else s.index('BOARDS["plain"] = make_board(1.0)')
    s = s[:a] + data + s[b:]
    if video:
        s = s.replace('"reel1_silent.mp4"', '"reel_tam-nhin-noi-tru_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', '"frames"').replace('"storyboard_reel1_v7.png"', '"storyboard.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Tầm nhìn & nơi trú ẩn")
        s = s.replace('font=F(60), fill=(255, 255, 255))', 'font=F(50), fill=(255, 255, 255))')
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Ảnh dán bằng băng giấy · nền trắng · chữ nâu trên nền, trắng trên ảnh")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét vẽ chạy dần theo lời đọc")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ; cảnh mở, công thức và cảnh cuối giữ ảnh nguyên bản.")
    open(E + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v7.py", "engine_ep02.py", False, data)
build("engine_video.py", "engine_video_ep02.py", True, data)

# ---- script.md + elevenlabs.txt ----
NAMES = dict(A="Mở", B="Nguồn gốc", C="Cơ chế / bằng chứng", D="Đọc trên ảnh", E="Lỗi hay gặp", F="Áp dụng",
             G="Chọn đồ", H="Công thức", I="Cảnh cuối")
spoken_all = [s.get("tts", s["vo"]) for s in SC]
nw = sum(words(x) for x in spoken_all)
rows = []
for k, s in enumerate(SC):
    head = "(khung cuối cố định)" if s["head"] == "end" else s["head"]
    rows.append(f'| {k + 1} | {s["t"]} | {s["part"]} · {NAMES[s["part"]]} | {head} | {s.get("tts", s["vo"])} |')
md = (f"# AH Decode · Tầm nhìn & nơi trú ẩn (prospect–refuge) — BẢN NHÁP chờ duyệt\n\n"
      f"Ảnh: Anderson Residence (1959) · Aaron G. Green · ảnh Sterling Reed · Dwell\n"
      f"Thời lượng dự kiến: {total:.1f} giây + 1 giây giữ khung cuối · {nw} từ lời đọc (tính theo cách đọc) · {len(SC)} cảnh.\n\n"
      "| # | Thời lượng | Phần | Tiêu đề trên khung | Lời đọc |\n|---|---|---|---|---|\n" + "\n".join(rows) +
      "\n\n## Lời đọc liền mạch\n\n" + " ".join(spoken_all) + "\n")
open(OUT + "script.md", "w").write(md)


def lines(txt):
    parts = re.split(r'(?<=[.?!])\s+', txt.strip())
    return "\n".join(p for p in parts if p)


el = "\n\n".join(lines(x) for x in spoken_all)
el += ("\n\n--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese. "
       "Chỉ dán phần phía trên dòng này. Tên riêng: Jay Appleton (đọc gần như 'Giây Áp-pồn-tần'), Frank Lloyd Wright (đọc 'Frăng Loi Rai'); "
       "nếu ElevenLabs đọc sai tên AH Decode, thay bằng cách viết theo âm bạn muốn ---\n")
open(OUT + "elevenlabs.txt", "w").write(el)
print("total", round(total, 1), "words", nw)
for s in SC:
    print(s["t"], words(s.get("tts", s["vo"])), s["head"])
