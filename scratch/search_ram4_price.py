import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ram4_live.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's search for any class containing price
matches = re.finditer(r'class="[^"]*price[^"]*"', html, re.IGNORECASE)
print("Matches for class containing 'price':")
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(html), m.end() + 100)
    print(html[start:end].strip())
    print("-" * 60)

print("\nMatches for id containing 'price':")
matches = re.finditer(r'id="[^"]*price[^"]*"', html, re.IGNORECASE)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(html), m.end() + 100)
    print(html[start:end].strip())
    print("-" * 60)
