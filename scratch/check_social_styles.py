with open("assets/style.css", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'floating|social', content, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences of 'floating' or 'social' in style.css:")
for m in matches[:5]:
    print(content[max(0, m-50):m+150])
    print("="*40)
