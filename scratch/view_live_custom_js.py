import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find where window.currentProductData starts and end
idx = html.find('window.currentProductData = {')
if idx != -1:
    print("Found custom script block in live HTML. Printing 120 lines from start:")
    # Print 120 lines from the start
    snippet = html[idx:idx + 4000]
    print(snippet)
else:
    print("window.currentProductData not found!")
