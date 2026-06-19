import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer("formatVietnameseCurrency", html)]
print(f"Found {len(matches)} occurrences of 'formatVietnameseCurrency'.")

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "formatVietnameseCurrency" in line:
        print(f"Line {idx+1}: {line.strip()[:180]}")
