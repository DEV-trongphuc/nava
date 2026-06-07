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
        
        # Find all js script tags
        js_urls = re.findall(r'src="([^"]+\.js(?:\?[^"]*)?)"', html)
        js_urls += re.findall(r"src='([^']+\.js(?:\?[^']*)?)'", html)
        
        for js_url in js_urls:
            if js_url.startswith("//"):
                js_url = "https:" + js_url
            elif js_url.startswith("/"):
                js_url = "https://navastore.vn" + js_url
            
            print(f"Fetching JS: {js_url}")
            req_js = urllib.request.Request(
                js_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            try:
                with urllib.request.urlopen(req_js, context=ctx) as res_js:
                    js_code = res_js.read().decode('utf-8')
                    if "special-content" in js_code:
                        print(f"  FOUND 'special-content' in {js_url.split('/')[-1]}:")
                        idx = js_code.find("special-content")
                        print(js_code[max(0, idx-100):min(len(js_code), idx+300)])
            except Exception as js_err:
                print(f"  Error fetching JS: {js_err}")
except Exception as e:
    print("Error:", e)
