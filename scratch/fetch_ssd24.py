import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://navastore.vn/ssd24?nocache=1"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read().decode('utf-8')
        print("Fetched HTML length:", len(html))
        with open("scratch/ssd24_live.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved HTML to scratch/ssd24_live.html")
except Exception as e:
    print("Error:", e)
