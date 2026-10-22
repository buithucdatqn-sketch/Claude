"""Tập 10: sinh script.md (bảng cảnh từ scenes.json + phần viết tay trong NOTES) và sources.md."""
import json, os, sys
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "./") + "/"
HERE = os.path.dirname(os.path.abspath(__file__))
sc = json.load(open(HERE + "/scenes.json")); runs = json.load(open(HERE + "/runs.json"))
img = {k: r["img"] for r in runs for k in r["scenes"]}
NAME = dict(a39="ArchDaily 39 mặt ngoài", a26="ArchDaily 26 mặt ngoài nhìn xa (doodle mới)", a24="ArchDaily 24 tường nhìn sát (doodle mới)", a29="ArchDaily 29 phòng khách (doodle mới)", a6c="ArchDaily 6 phòng ngủ con gái (doodle mới)", a35c="ArchDaily 35 cổng lối vào (doodle mới)", hl="ảnh 11 hành lang lối vào (dùng lại từ tập 7, doodle mới)", dgt="ảnh 10 diagram, hàng trên",
            dgb="ảnh 10 diagram, hàng dưới", dgc="ảnh 10 diagram, dòng kết", mb="ảnh 03 mặt bằng tầng một", ph="ảnh 12 phòng ngủ (doodle mới)")
rows = []
for i, s in enumerate(sc, 1):
    head = s["head"] if s["head"] != "end" else "(khung cuối)"
    rows.append(f"| {i} | {s['blk']} | {s['part']} | {s['t']} | {NAME[img[i]]} | {head} | {s['loi']} | "
                f"{'giữ nguyên' if s['tts'] == s['loi'] else s['tts']} |")
words = sum(len(s["loi"].split()) for s in sc)
el = open(OUT + "elevenlabs.txt").read()
notes = open(HERE + "/script_notes.md").read()
open(OUT + "script.md", "w").write(
    "# AH Decode · Vân thô ở xa, vân mịn ở gần · tập 10, bản 2 (chạy lại theo góp ý chủ Trang) · chờ ghi âm\n\n"
    "Bài: bai-02 (kho AH-Decode-Decor, commit 6d869f9), mục \"Độ thô của bề mặt phải hợp với kích thước phòng và khoảng cách nhìn\".\n\n"
    f"## Bảng cảnh ({len(sc)} cảnh, {words} từ phụ đề; cột thời lượng là bản nháp 3,2 từ/giây, giai đoạn B căn lại theo ghi âm)\n"
    "| # | Khối | Phần | Thời lượng | Ảnh | Tiêu đề trên khung | Phụ đề (loi) | Bản đọc (tts) |\n|---|---|---|---|---|---|---|---|\n"
    + "\n".join(rows) + "\n\n## Lời đọc dán vào ElevenLabs\n```\n" + el + "```\n\n" + notes)
print("script.md", len(sc), "cảnh", words, "từ")
