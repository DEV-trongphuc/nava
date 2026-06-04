with open("product_page_original.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for RAM DDR5 or SSD NVMe or other headers
import re
with open("scratch/ram_check.txt", "w", encoding="utf-8") as out:
    for term in ["RAM", "SSD", "ExpertCenter", "Wifi 6E"]:
        matches = [m.start() for m in re.finditer(re.escape(term), content, re.IGNORECASE)]
        out.write(f"Term '{term}': found {len(matches)} matches\n")
        for m in matches[:5]:
            out.write(content[max(0, m-100):m+250])
            out.write("\n" + "=" * 40 + "\n")
print("Done!")
