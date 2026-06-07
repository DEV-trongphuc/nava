import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://navastore.vn/beelink-me-mini-6-slot-o-cung-ssd-nvme-12gb-lpddr5-64gb-emmc-nas-mini-pc-intel-twin-lake-n200?nocache=1"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read().decode('utf-8')
        
        # Search for initSpecsScrollIndicator
        matches = list(re.finditer(r'function initSpecsScrollIndicator', html))
        if matches:
            for i, match in enumerate(matches):
                idx = match.start()
                print(f"Match {i+1} at index {idx}:")
                print(html[idx:idx+1500])
                print("-" * 50)
        else:
            print("initSpecsScrollIndicator JS function not found in HTML!")
except Exception as e:
    print("Error:", e)
