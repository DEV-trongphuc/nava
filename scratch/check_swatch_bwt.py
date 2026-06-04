with open("sapo_BWT_using_no_change_it/Templates/product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'swatch', content, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences of 'swatch' in sapo_BWT_using_no_change_it/product.bwt:")
for m in matches[:5]:
    print(content[max(0, m-50):m+150])
    print("="*40)
