import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for the swatch section
swatch_pattern = re.compile(r'<div[^>]*class=["\'][^"\']*swatch[^"\']*["\'][^>]*>([\s\S]*?)</div>\s*</div>', re.IGNORECASE)
matches = list(swatch_pattern.finditer(html))
print(f"Found {len(matches)} swatch elements:")
for idx, m in enumerate(matches):
    print(f"Swatch {idx + 1}:")
    content = m.group(0)
    # Print the first 500 characters of the swatch content
    print(content[:600])
    print("..." if len(content) > 600 else "")
    print("=" * 60)
