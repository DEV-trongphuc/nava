import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find all swatch elements and their inputs
element_pattern = re.compile(r'<div[^>]*data-value=["\']([^"\']*)["\'][^>]*class=["\']([^"\']*)["\'][^>]*>([\s\S]*?)</div>\s*</div>', re.IGNORECASE)

print("Parsed Swatch Elements:")
for m in re.finditer(r'<div\s+data-value="([^"]+)"\s+class="([^"]+)"', html):
    val = m.group(1)
    cls = m.group(2)
    print(f"Value: {val}, Classes: {cls}")
    
    # Check if there is an input inside this element and print its checked status
    # We find the matching end tag or next sibling
    start_pos = m.end()
    end_pos = html.find('</div>', start_pos)
    sub_html = html[start_pos:end_pos]
    input_m = re.search(r'<input[^>]*>', sub_html)
    if input_m:
        print(f"  Input tag: {input_m.group(0).strip()}")
    print("-" * 50)
