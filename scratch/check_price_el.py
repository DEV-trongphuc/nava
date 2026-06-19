import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ram_live.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
# Tìm các đoạn HTML chứa giá trị 3.990.000 hoặc 3.990.000₫
matches = list(re.finditer(r'3\.990\.000', html))
print(f"Found {len(matches)} matches of '3.990.000' in live HTML.")

for idx, m in enumerate(matches):
    start = max(0, m.start() - 150)
    end = min(len(html), m.end() + 150)
    print(f"\n--- MATCH {idx+1} ---")
    print(html[start:end].strip())
