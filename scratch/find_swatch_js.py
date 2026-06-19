import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Search for swatch click listeners or jQuery event bindings in script tags
script_pattern = re.compile(r'<script[^>]*>([\s\S]*?)</script>', re.IGNORECASE)
scripts = script_pattern.findall(html)

for idx, s in enumerate(scripts):
    if '.swatch' in s or 'swatch-element' in s or 'select-option' in s or 'option-0' in s:
        print(f"--- Script {idx} contains swatch terms ---")
        lines = s.split('\n')
        for l_idx, line in enumerate(lines):
            if any(term in line for term in ['.swatch', 'swatch-element', 'select-option', 'option-0', 'radio']):
                start = max(0, l_idx - 2)
                end = min(len(lines), l_idx + 3)
                print(f"Line {l_idx+1}:")
                for i in range(start, end):
                    print(f"  {i+1}: {lines[i]}")
        print("=" * 60)
