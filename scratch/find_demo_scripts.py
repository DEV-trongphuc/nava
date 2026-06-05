with open("demo_collection.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
scripts = re.findall(r'<script.*?>.*?</script>', content, re.DOTALL | re.IGNORECASE)
print(f"Total script elements in demo_collection.html: {len(scripts)}")
with open("scratch/collection_scripts_found.txt", "w", encoding="utf-8") as out:
    for s in scripts:
        if 'src' in s or 'search' in s.lower() or 'filter' in s.lower():
            out.write(s + "\n-------------------\n")
print("Done!")
