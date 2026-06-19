import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ram4_live.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Find selected-variant-price
price_el = soup.find(id="selected-variant-price")
print("selected-variant-price tag:", price_el)

# Find product-selectors
selectors = soup.find(id="product-selectors")
if selectors:
    print("product-selectors element found!")
    for opt in selectors.find_all("option"):
        print(f"  Option: value={opt.get('value')}, text={opt.text.strip()}, data-price={opt.get('data-price')}, data-available={opt.get('data-available')}")
else:
    print("product-selectors NOT found!")

# Let's see if there are other scripts containing mew_product or selectCallback
print("\n--- Script tags with OptionSelectors or selectCallback or syncSwatches ---")
scripts = soup.find_all("script")
for idx, s in enumerate(scripts):
    code = s.string or s.text or ""
    if not code and s.get("src"):
        src = s.get("src")
        if "mew_product" in src or "selectors" in src:
            print(f"External script: {src}")
        continue
    if "OptionSelectors" in code or "selectCallback" in code or "syncSwatches" in code:
        print(f"Script #{idx} (src={s.get('src')}):")
        lines = code.split("\n")
        print(f"  Total lines: {len(lines)}")
        for i, line in enumerate(lines):
            if "syncSwatches" in line or "selectCallback" in line:
                start_line = max(0, i - 2)
                end_line = min(len(lines), i + 3)
                print(f"    --- Match at line {i} ---")
                for j in range(start_line, end_line):
                    print(f"    {j}: {lines[j]}")
