import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's search for keywords in main.js
keywords = ['qty', 'plus', 'minus', 'quantity']
lines = js.split('\n')

print("Searching for quantity handler in main.js:")
for l_idx, line in enumerate(lines):
    if any(k in line.lower() for k in keywords) and ('click' in line.lower() or 'change' in line.lower() or 'addEventListener' in line or '$(' in line):
        start = max(0, l_idx - 2)
        end = min(len(lines), l_idx + 4)
        print(f"Line {l_idx+1}:")
        for i in range(start, end):
            print(f"  {i+1}: {lines[i]}")
        print("-" * 50)
