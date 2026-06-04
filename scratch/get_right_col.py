with open("f:\\BAO_SAPO\\sapo_new\\demo_product.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
# Let's search for '<div class="nava-prod-info">' to the end of the form/actions
match = re.search(r'<div class="nava-prod-info">.*?<!-- Left: Gallery -->', content, re.DOTALL)
if not match:
    # Let's search from '<div class="nava-prod-info">' to '<!-- Down: Specs & Content -->'
    match = re.search(r'<div class="nava-prod-info">(.*?)<!-- Down: Specs & Content -->', content, re.DOTALL)

with open("scratch/product_right_column.html", "w", encoding="utf-8") as out:
    if match:
        out.write(match.group(1).strip())
        print("Success! Extracted info section.")
    else:
        # Fallback print some chunks
        out.write(content[content.find('<div class="nava-prod-info">'):content.find('<div class="nava-prod-info">')+8000])
        print("Done fallback extract.")
