import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

srcs = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html, re.IGNORECASE)
print("External scripts in live HTML:")
for src in srcs:
    print(src)
