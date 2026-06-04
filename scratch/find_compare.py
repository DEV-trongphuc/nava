with open("f:\\BAO_SAPO\\sapo_new\\demo_product.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer("so sánh", content, re.IGNORECASE)]

with open("scratch/find_compare_output.txt", "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} matches for so sánh\n\n")
    for idx, m in enumerate(matches):
        start = max(0, m - 200)
        end = min(len(content), m + 800)
        out.write(f"Match {idx+1}:\n{content[start:end]}\n" + "="*50 + "\n\n")

print("Done! Output written to scratch/find_compare_output.txt")
