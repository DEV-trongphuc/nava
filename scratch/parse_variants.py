import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for <select id="product-selectors" ...>
select_pattern = re.compile(r'<select[^>]*id=["\']product-selectors["\'][^>]*>([\s\S]*?)</select>', re.IGNORECASE)
m = select_pattern.search(html)
if m:
    print("Found #product-selectors:")
    options_html = m.group(1)
    option_pattern = re.compile(r'<option([^>]*)>([\s\S]*?)</option>', re.IGNORECASE)
    for opt_m in option_pattern.finditer(options_html):
        attrs = opt_m.group(1)
        text = opt_m.group(2).strip()
        print(f"Option text: {text}")
        print(f"Attrs: {attrs.strip()}")
        print("-" * 50)
else:
    print("#product-selectors select element not found!")

# Let's also find the product schema or JSON representation
# e.g., var product = ... or window.product = ...
json_pattern = re.compile(r'var\s+product\s*=\s*(\{[\s\S]*?\});', re.IGNORECASE)
jm = json_pattern.search(html)
if jm:
    print("\nFound product JSON in script tags.")
else:
    print("\nDid not find 'var product ='")
