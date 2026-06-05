with open("sapo_BWT_new/Templates/collection.bwt", "r", encoding="utf-8") as f:
    content = f.read()

import re
scripts = re.findall(r'<script.*?>.*?</script>', content, re.DOTALL | re.IGNORECASE)
print(f"Found {len(scripts)} scripts in collection.bwt:")
for s in scripts:
    print(s[:250])
    print("-" * 30)
