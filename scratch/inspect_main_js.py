import re

path = r"f:\BAO_SAPO\sapo_new\assets\main.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

keywords = ["swatch", "variant", "price", "product-selectors", "change"]
for kw in keywords:
    matches = [m.start() for m in re.finditer(kw, content, re.IGNORECASE)]
    print(f"Keyword '{kw}' found {len(matches)} times.")
