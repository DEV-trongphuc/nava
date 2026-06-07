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
        
        # Find all stylesheets
        links = re.findall(r'href="([^"]+\.css(?:\?[^"]*)?)"', html)
        links += re.findall(r"href='([^']+\.css(?:\?[^']*)?)'", html)
        
        print("CSS Links:")
        for link in links:
            print("  ", link)
            
        print("\n--- Inline Style Blocks ---")
        styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
        for i, style in enumerate(styles):
            # Check if mentions spec-tables or special-content
            if "spec" in style or "content" in style or "table" in style or "tr" in style:
                print(f"Inline style block {i+1} (contains spec/content/table/tr):")
                print(style[:800])
                print("..." if len(style) > 800 else "")
                print("-" * 50)
                
except Exception as e:
    print("Error:", e)
