with open("demo_product.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'So sánh', content, re.IGNORECASE)]
with open("scratch/check_specs_out.txt", "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} occurrences of 'So sánh':\n")
    for m in matches:
        out.write(content[max(0, m-250):m+350])
        out.write("\n" + "="*40 + "\n")
print("Done!")
