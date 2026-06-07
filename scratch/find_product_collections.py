import os
import re

base_dir = r"f:\BAO_SAPO\sapo_new"

matches = []
for root, dirs, files in os.walk(base_dir):
    for f_name in files:
        if f_name.endswith(".bwt") or f_name.endswith(".html"):
            path = os.path.join(root, f_name)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "product.collections" in content:
                    matches.append((path, content.count("product.collections")))
            except Exception:
                pass

print("Found references:")
for m in matches:
    print(m)
