with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

import re
# Find all script blocks in product.bwt
scripts = [m.start() for m in re.finditer("<script>", content, re.IGNORECASE)]
print(f"Found {len(scripts)} script tags in product.bwt.")

# Let's inspect scripts near the end or search for variant change events
# We can search for event listeners on .swatch, select, input, option, change, etc.
keywords = ["swatch", "change", "price", "update", "variant"]
for kw in ["swatch", "variant", "price"]:
    matches = [m.start() for m in re.finditer(kw, content, re.IGNORECASE)]
    print(f"Keyword '{kw}' found {len(matches)} times.")

# Let's print out lines of javascript at the end of the file or search for variant selection handling
# Let's look for "change" inside script tags
script_matches = []
for start_idx in scripts:
    end_idx = content.find("</script>", start_idx)
    script_text = content[start_idx:end_idx]
    if any(kw in script_text for kw in ["change", "variant", "price", "select"]):
        script_matches.append((start_idx, len(script_text)))

print(f"Found {len(script_matches)} script tags containing relevant keywords.")
for start, length in script_matches[-3:]:
    print(f"\n--- Script starting at index {start} (length {length}) ---")
    print(content[start:start+1200])
