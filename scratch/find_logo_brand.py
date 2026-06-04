with open("f:\\BAO_SAPO\sapo_new\\demo_collection.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer("logo_brand", content, re.IGNORECASE)]
print(f"Found {len(matches)} matches for logo_brand")
for idx, m in enumerate(matches[:5]):
    start = max(0, m - 100)
    end = min(len(content), m + 300)
    print(f"Match {idx+1}:\n{content[start:end]}\n" + "="*50)
