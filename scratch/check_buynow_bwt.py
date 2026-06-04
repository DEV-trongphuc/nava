with open("sapo_BWT_using_no_change_it/Templates/product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'MUA NGAY', content, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences of 'MUA NGAY':")
for m in matches:
    print(content[max(0, m-200):m+300])
    print("="*40)
