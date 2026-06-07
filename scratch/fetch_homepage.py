import urllib.request
import re

url = "https://navastore.vn/"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        matches = re.findall(r'src="[^"]*main\.js[^"]*"', html)
        print("Found script tags:")
        for m in matches:
            print(m)
except Exception as e:
    print("Error fetching:", e)
