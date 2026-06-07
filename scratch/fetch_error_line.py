import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://navastore.vn/nas-synology-ds223j-2-bay?nocache=1"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read().decode('utf-8')
        lines = html.splitlines()
        print(f"Total lines: {len(lines)}")
        
        start = max(0, 4490 - 50)
        end = min(len(lines), 4490 + 50)
        
        for idx in range(start, end):
            print(f"{idx+1}: {lines[idx]}")
            
except Exception as e:
    print("Error:", e)
