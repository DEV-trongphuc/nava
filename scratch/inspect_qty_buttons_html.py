import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for inputs with class prd_quantity or id qtym and print the surrounding HTML block
idx = html.find('id="qtym"')
if idx != -1:
    print("Found id=\"qtym\". HTML around it:")
    start = max(0, idx - 400)
    end = min(len(html), idx + 500)
    print(html[start:end])
else:
    print("id=\"qtym\" not found!")
