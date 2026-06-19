import urllib.request
import ssl
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://navastore.vn/ssd24?nocache=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as r:
    html = r.read().decode('utf-8')

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} script tags in live page HTML.")

with open('scratch/live_scripts.txt', 'w', encoding='utf-8') as out:
    for i, s in enumerate(scripts):
        out.write(f"\n=========================================\nSCRIPT {i+1}:\n=========================================\n")
        out.write(s)

print("Saved all live scripts to scratch/live_scripts.txt")
