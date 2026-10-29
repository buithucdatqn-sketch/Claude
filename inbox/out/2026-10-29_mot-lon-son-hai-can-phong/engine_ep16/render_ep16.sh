#!/bin/sh
# Dựng video của từng run (runs.json) song song, mỗi run một thư mục ra riêng: vid/<tag>/video/<tag>_silent.mp4
cd "$(dirname "$0")/.."
python3 -c "import json;[print(r['tag'],r['src']) for r in json.load(open('engine_ep16/runs.json'))]" |
  xargs -P 6 -n 2 sh -c 'mkdir -p vid/$0 && /usr/bin/python3 -I engine_ep16/engine_video_ep16_$0.py "$1" vid/$0/ > vid/$0.log 2>&1; echo "xong $0 $?"'
