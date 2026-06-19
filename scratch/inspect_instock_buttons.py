import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find class="btn-group-instock"
idx = html.find('class="btn-group-instock"')
if idx != -1:
    print("Found btn-group-instock. Printing 2000 characters:")
    print(html[idx-100:idx+2000])
else:
    print("btn-group-instock not found!")
