import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://navastore.vn/ram4"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read().decode('utf-8')
        
        idx = html.lower().find('product-selectors')
        if idx != -1:
            chunk = html[idx-100:idx+2500]
            with open("scratch/ram4_selectors.txt", "w", encoding="utf-8") as f:
                f.write(chunk)
            print("Successfully written to scratch/ram4_selectors.txt")
        else:
            print("product-selectors not found in HTML!")
except Exception as e:
    print("Error:", e)
