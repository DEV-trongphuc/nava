with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Let's search for event listeners or functions that call syncSwatches
matches = [m.start() for m in re.finditer("syncSwatches", content)]
for idx in matches:
    print(f"\nMatch at index {idx}:")
    print(content[idx-100:idx+300])
