import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for function syncSwatches() {
idx = html.find('function syncSwatches() {')
if idx != -1:
    print("Found function syncSwatches() { in live HTML. Printing 100 lines:")
    # Print 100 lines
    snippet = html[idx:idx + 6000]
    print(snippet)
else:
    print("function syncSwatches() { not found!")
