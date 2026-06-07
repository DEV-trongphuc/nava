with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\layout\theme.bwt", "r", encoding="utf-8") as f:
    content = f.read()

import re
scripts = [m.start() for m in re.finditer("<script", content)]
print(f"Found {len(scripts)} script tags in theme.bwt.")
for idx in scripts:
    print(content[idx:idx+250])
