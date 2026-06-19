import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for buttons inside forms or around product details
print("Buttons found in HTML:")
for m in re.finditer(r'<button[^>]*>', html, re.IGNORECASE):
    tag = m.group(0)
    if any(k in tag.lower() for k in ['buy', 'cart', 'installment', 'submit', 'btn', 'add']):
        print(tag)
        print("-" * 50)
        
print("\nDivs with classes containing btn-group or similar:")
for m in re.finditer(r'<div[^>]*class=["\'][^"\']*btn[^"\']*["\'][^>]*>', html, re.IGNORECASE):
    print(m.group(0))
    print("-" * 50)
