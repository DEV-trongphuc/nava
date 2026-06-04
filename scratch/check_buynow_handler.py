with open("product_page_original.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'js-buynow', content, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences of 'js-buynow':")
for m in matches:
    print(content[max(0, m-200):m+300])
    print("="*40)
