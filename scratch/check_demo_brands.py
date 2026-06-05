with open("demo_collection.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'brand-list|brand-item', content, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences:")
for m in matches:
    print(content[max(0, m-200):m+400])
    print("="*40)
