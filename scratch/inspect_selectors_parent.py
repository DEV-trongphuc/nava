import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's locate id="product-selectors" and search backwards for its parent
idx = html.find('id="product-selectors"')
if idx != -1:
    print("Found id=\"product-selectors\" at index:", idx)
    # Print 500 characters before and after the select element
    start = max(0, idx - 300)
    end = min(len(html), idx + 300)
    print(html[start:end].strip())
else:
    print("id=\"product-selectors\" not found!")
