import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/product_style.scss.css?1780666203046"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        css = response.read().decode('utf-8')
        
        # Search for max-height or overflow
        for pattern in [r'[^{;]*max-height[^};]*', r'[^{;]*overflow[^};]*']:
            matches = list(re.finditer(pattern, css))
            print(f"Query: {pattern}")
            for m in matches:
                idx = m.start()
                context = css[max(0, idx-60):min(len(css), idx+100)]
                print(f"  ... {context.strip()} ...")
            print("="*60)
except Exception as e:
    print("Error:", e)
