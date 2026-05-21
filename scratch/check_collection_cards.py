import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

collection_path = r"f:\BAO_SAPO\sapo_new\demo_collection.html"
if os.path.exists(collection_path):
    with open(collection_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    import re
    matches = re.findall(r'<div class="product-card"[^>]*>', content)
    print(f"Found {len(matches)} product-cards in demo_collection.html")
    for idx, match in enumerate(matches, 1):
        print(f"Card {idx}: {match}")
else:
    print("demo_collection.html does not exist yet")
