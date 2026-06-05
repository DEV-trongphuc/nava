import os
import re

results = []
for root, dirs, files in os.walk("sapo_BWT_using_no_change_it"):
    for file in files:
        if file.endswith(('.bwt', '.html')):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Find brand names or filter loops
                if 'vendor' in content.lower() or 'thuong-hieu' in content.lower() or 'brand' in content.lower():
                    results.append(path)
            except:
                pass

print(f"Files referencing vendor/brand in sapo_BWT_using_no_change_it: {results}")
