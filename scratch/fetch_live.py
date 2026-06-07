import urllib.request
import ssl

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
        print("Fetched HTML length:", len(html))
        # Search for key strings
        print("Has specs-content-scrollable:", "specs-content-scrollable" in html)
        print("Has specs-scroll-wrapper:", "specs-scroll-wrapper" in html)
        print("Has specs-fade-overlay:", "specs-fade-overlay" in html)
        print("Has specs-scroll-arrow:", "specs-scroll-arrow" in html)
        print("Has SpecsDebug:", "SpecsDebug" in html)
        
        # Print lines around the scrollable div
        idx = html.find("specs-content-scrollable")
        if idx != -1:
            print("FOUND CONTENT:")
            print(html[idx-200:idx+500])
        else:
            print("Not found specs-content-scrollable in HTML!")
except Exception as e:
    print("Error:", e)
