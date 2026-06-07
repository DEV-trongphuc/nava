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
        
        # Regex to find specs-scroll-wrapper div and its contents
        pattern = r'<div class="specs-scroll-wrapper".*?</div>\s*</div>\s*</div>'
        matches = list(re.finditer(r'<div class="specs-scroll-wrapper"', html))
        if matches:
            idx = matches[0].start()
            with open("scratch/check_elements_output.html", "w", encoding="utf-8") as f:
                f.write(html[idx:idx+2500])
            print("Saved output to scratch/check_elements_output.html successfully!")
        else:
            print("Not found specs-scroll-wrapper starting tag")
except Exception as e:
    print("Error:", e)
