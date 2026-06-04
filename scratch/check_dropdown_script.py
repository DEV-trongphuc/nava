with open("demo_product.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'selectVariantDropdown', content, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences of selectVariantDropdown:")
for m in matches:
    print(content[m-100:m+300])
    print("="*40)
