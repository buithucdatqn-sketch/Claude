# AH Decode — reels nội thất hằng ngày
- `TASK_INSTRUCTION.md`: instruction của scheduled task (đọc file này đầu tiên).
- `engine/`: dựng khung hình và video (Python, OpenCV, ffmpeg). `reel1_source_example.png` là ảnh mẫu của Reel #1. `engine/multi_patch.py` vá engine để một reel dùng nhiều ảnh (từ tập 6).
- `inbox/series.json`: nhật ký các tập đã làm. `inbox/override/`: ảnh do người dùng chọn. `inbox/audio/`: giọng ElevenLabs. `inbox/out/`: kết quả mỗi ngày.
