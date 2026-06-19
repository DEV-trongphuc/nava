import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ram_live.html", "r", encoding="utf-8") as f:
    html = f.read()

print("1. Checking swatch elements:")
swatch_matches = list(re.finditer(r'class="[^"]*swatch[^"]*"', html))
print(f"Found {len(swatch_matches)} swatch-related classes.")
if swatch_matches:
    for m in swatch_matches[:5]:
        start = max(0, m.start() - 100)
        end = min(len(html), m.end() + 200)
        print(f"--- MATCH --- \n{html[start:end].strip()}")

print("\n2. Checking product selectors:")
selectors_idx = html.find('id="product-selectors"')
if selectors_idx != -1:
    print(f"Found product-selectors:")
    print(html[selectors_idx-100:selectors_idx+300])
else:
    print("Not found id='product-selectors'")

print("\n3. Checking variant hidden input:")
hidden_idx = html.find('name="variantId"')
if hidden_idx != -1:
    print(f"Found name='variantId' input:")
    print(html[hidden_idx-100:hidden_idx+300])
else:
    print("Not found name='variantId'")
