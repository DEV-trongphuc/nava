import re

with open("product_page_original.html", "r", encoding="utf-8") as f:
    content = f.read()

selects = re.findall(r'<select.*?>.*?</select>', content, re.DOTALL | re.IGNORECASE)
print(f"Found {len(selects)} select elements:")
for s in selects:
    print(s[:200])
    print("-" * 20)

print("Searching for product forms or buttons in product_page_original.html:")
# find name="variantId"
var_ids = [m.start() for m in re.finditer(r'variantId', content, re.IGNORECASE)]
print(f"Found variantId at: {var_ids}")
for idx in var_ids:
    print(content[idx-100:idx+200])
    print("=" * 40)
