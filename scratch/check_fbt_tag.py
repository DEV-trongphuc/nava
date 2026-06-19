import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
# Tìm các thẻ frequently-buy-together trong HTML (không nằm trong thẻ script)
# Một cách đơn giản là strip các script tags đi trước
html_no_scripts = re.sub(r'<script[^>]*>(.*?)</script>', '', html, flags=re.DOTALL)

matches = list(re.finditer(r'<frequently-buy-together', html_no_scripts))
print(f"Found {len(matches)} occurrences of '<frequently-buy-together' tag in HTML (excluding scripts).")
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(html_no_scripts), m.end() + 200)
    print("--- CONTEXT ---")
    print(html_no_scripts[start:end].strip())
