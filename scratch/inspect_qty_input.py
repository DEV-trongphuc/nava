import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Search for any input with name="quantity" or class containing "qty"
print("Searching for quantity inputs:")
for m in re.finditer(r'<input[^>]*quantity[^>]*>', html, re.IGNORECASE):
    print(m.group(0))
    print("-" * 50)

for m in re.finditer(r'<input[^>]*qty[^>]*>', html, re.IGNORECASE):
    print(m.group(0))
    print("-" * 50)
