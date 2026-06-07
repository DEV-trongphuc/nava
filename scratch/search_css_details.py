import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/mew_style_gb.scss.css?1780666203046"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        css = response.read().decode('utf-8')
        
        # Search for any display:none or display: none
        print("--- DISPLAY NONE OR SIMILAR ---")
        for m in re.finditer(r'[^}]*display\s*:\s*none[^}]*}', css):
            print(m.group(0))
            
        print("\n--- TABLE OR TR STYLES ---")
        for m in re.finditer(r'[^}]*(?:tr|table)[^}]*{[^}]*}', css):
            print(m.group(0))
            
except Exception as e:
    print("Error:", e)
