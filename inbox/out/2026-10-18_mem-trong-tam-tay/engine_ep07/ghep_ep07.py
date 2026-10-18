"""Ghép video tập 7: cắt đúng đoạn của từng run (runs.json: cut_from, cut_len) từ vid/<tag>/video/<tag>_silent.mp4,
nối theo thứ tự (cắt theo số khung, 30 fps), rồi ghép giọng đã xử lý audio/bai-007_xu-ly.wav (AAC 48 kHz)."""
import json, os, subprocess, sys
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "./") + "/"
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
RUNS = json.load(open(os.path.join(HERE, "runs.json")))
ins, parts, total = [], [], 0
for i, r in enumerate(RUNS):
    f0 = round(r["cut_from"] * FPS)
    n = round(r["cut_len"] * FPS)
    total += n
    ins += ["-i", OUT + f"vid/{r['tag']}/video/{r['tag']}_silent.mp4"]
    parts.append(f"[{i}:v]trim=start_frame={f0}:end_frame={f0 + n},setpts=PTS-STARTPTS,fps={FPS}[v{i}]")
fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(RUNS))) + f"concat=n={len(RUNS)}:v=1:a=0[v]"
dur = total / FPS
ins += ["-i", OUT + "audio/bai-007_xu-ly.wav"]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", fc + f";[{len(RUNS)}:a]apad[a]",
                "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                OUT + "reel_mem-trong-tam-tay_final.mp4"], check=True)
print("xong", round(dur, 2), "giây")
