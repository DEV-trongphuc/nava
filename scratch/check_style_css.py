with open("assets/style.css", "r", encoding="utf-8") as f:
    content = f.read()

import re
with open("scratch/style_css_search.txt", "w", encoding="utf-8") as out:
    for term in ["variant", "select", "qty-selector", "custom-select"]:
        matches = [m.start() for m in re.finditer(re.escape(term), content, re.IGNORECASE)]
        out.write(f"Term '{term}': found {len(matches)} matches\n")
        for m in matches[:3]:
            out.write(content[max(0, m-100):m+250])
            out.write("\n" + "=" * 40 + "\n")
print("Done!")
