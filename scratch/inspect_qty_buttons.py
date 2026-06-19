import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for quantity button elements, like class="qty" or similar
# in the script tags of ssd24_live.html
script_pattern = re.compile(r'<script[^>]*>([\s\S]*?)</script>', re.IGNORECASE)
scripts = script_pattern.findall(html)

print("Searching for quantity buttons code:")
for idx, s in enumerate(scripts):
    if 'qtym' in s or 'js-quantity' in s or 'qtyBtn' in s or 'quantity' in s:
        lines = s.split('\n')
        for l_idx, line in enumerate(lines):
            if ('qtym' in line or 'qty' in line) and ('click' in line or 'change' in line or 'val' in line or 'trigger' in line):
                start = max(0, l_idx - 2)
                end = min(len(lines), l_idx + 4)
                print(f"Script {idx} | Line {l_idx+1}:")
                for i in range(start, end):
                    print(f"  {i+1}: {lines[i]}")
                print("-" * 50)
