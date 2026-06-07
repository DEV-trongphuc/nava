with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Let's search for '<select'
matches = [m.start() for m in re.finditer("<select", content, re.IGNORECASE)]
for idx in matches:
    print("\nMATCH:")
    print(content[idx:idx+800])
