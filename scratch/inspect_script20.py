import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

script_pattern = re.compile(r'<script[^>]*>([\s\S]*?)</script>', re.IGNORECASE)
scripts = script_pattern.findall(html)

s20 = scripts[20]
lines = s20.split('\n')
print(f"Script 20 total lines: {len(lines)}")

# Look for reorderSwatches definition
for l_idx, line in enumerate(lines):
    if 'reorderSwatches' in line:
        start = max(0, l_idx - 5)
        end = min(len(lines), l_idx + 40)
        print(f"--- reorderSwatches at line {l_idx+1} ---")
        for i in range(start, end):
            print(f"  {i+1}: {lines[i]}")
        break
