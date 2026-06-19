import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for specific price selectors
price_patterns = [
    r'id=["\']selected-variant-price["\']',
    r'class=["\']special-price["\']',
    r'class=["\'][^"\']*product-price[^"\']*["\']',
]

print("Searching for elements:")
for p in price_patterns:
    for m in re.finditer(p, html, re.IGNORECASE):
        start = max(0, m.start() - 100)
        end = min(len(html), m.end() + 150)
        print(f"Match for pattern {p}:")
        print(html[start:end].strip())
        print("-" * 60)

