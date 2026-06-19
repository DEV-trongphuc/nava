import urllib.request
import ssl
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://navastore.vn/ram-lexar-ddr5-sodimm-4800mt-s-dung-cho-mini-pc-laptop?nocache=1',
    'https://navastore.vn/ssd24?nocache=1'
]

for url in urls:
    print('='*50)
    print('URL:', url)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            html = r.read().decode('utf-8')
        print('HTML length:', len(html))
        
        # Search for selectors
        selectors_idx = html.find('id="product-selectors"')
        if selectors_idx != -1:
            print('Found id="product-selectors". Context:')
            print(html[selectors_idx:selectors_idx+2000])
        else:
            # Check for name="variantId"
            idx_v = html.find('name="variantId"')
            if idx_v != -1:
                print('Found name="variantId". Context:')
                print(html[idx_v-100:idx_v+400])
            else:
                print('Neither product-selectors nor variantId found!')
                
        # Search for swatches in HTML
        swatches = re.findall(r'<div[^>]*class="[^"]*swatch[^"]*"[^>]*>.*?</div>', html, re.DOTALL)
        print(f'Found {len(swatches)} swatch class divs in HTML')
        for i, sw in enumerate(swatches[:5]):
            print(f'Swatch {i+1}:')
            print(sw[:600])
            print('-'*20)
            
    except Exception as e:
        print('Error:', e)
