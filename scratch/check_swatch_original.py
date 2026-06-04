import re

with open("product_page_original.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for product-selectors or variant selectors
print("Searching product-selectors:")
idx = content.find("product-selectors")
if idx != -1:
    print(content[idx-100:idx+400])

print("Searching swatch:")
swatch_matches = [m.start() for m in re.finditer(r'swatch', content, re.IGNORECASE)]
print(f"Found {len(swatch_matches)} swatch matches")
for m in swatch_matches[:3]:
    print(content[max(0, m-100):m+300])
    print("="*40)
