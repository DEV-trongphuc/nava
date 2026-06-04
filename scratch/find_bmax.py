with open("f:\\BAO_SAPO\\sapo_new\\demo_collection.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
match = re.search(r'<div class="brand-list">(.*?)</div>\s*</div>', content, re.DOTALL)
if match:
    print("Found brand list:")
    print(match.group(1).strip())
else:
    # Try finding the brand items directly
    items = re.findall(r'<div class="brand-item".*?><img src="(.*?)".*?>', content)
    print("Found brand items:")
    for item in items:
        print(item)
