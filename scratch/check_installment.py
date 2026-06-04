with open("product_page_original.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'g\u00f3p', content, re.IGNORECASE)] # 'góp'
with open("scratch/check_installment_out.txt", "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} occurrences of 'góp':\n")
    for m in matches:
        out.write(content[max(0, m-250):m+350])
        out.write("\n" + "="*40 + "\n")
print("Done!")
