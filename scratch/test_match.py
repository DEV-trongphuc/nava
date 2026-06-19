import urllib.request
import ssl
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://navastore.vn/ssd24?nocache=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as r:
    html = r.read().decode('utf-8')

# Extract option texts from #product-selectors
options = re.findall(r'<option[^>]*>(.*?)</option>', html)
print("Option texts:")
for opt in options:
    print(f"  - {repr(opt)}")

# Simulate selected values
selectedValues = ["512GB"]
print("\nSimulating match for selectedValues:", selectedValues)

for opt in options:
    textParts = opt.split('-')
    # Use titlePart = textParts.slice(0, -1).join('-').trim();
    titlePart = '-'.join(textParts[:-1]).strip()
    # Remove leading numbers
    titlePart = re.sub(r'^\d+\s+', '', titlePart).strip()
    
    optValues = [v.strip() for v in titlePart.split('/')]
    
    isMatch = True
    for i in range(len(selectedValues)):
        if i < len(optValues):
            if optValues[i] != selectedValues[i]:
                isMatch = False
                break
        else:
            isMatch = False
            break
            
    print(f"Option: {repr(opt)} -> titlePart: {repr(titlePart)} -> optValues: {optValues} -> Match: {isMatch}")
