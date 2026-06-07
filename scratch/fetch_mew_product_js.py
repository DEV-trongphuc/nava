import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/mew_product.js?1780666710862"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        js = response.read().decode('utf-8')
        print("mew_product.js contents:")
        print(js)
except Exception as e:
    print("Error:", e)
