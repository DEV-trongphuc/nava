import urllib.request
import re

url = "https://navastore.vn/mini-pc-ho-tro-ai-asus-nuc-14-pro-rnuc14rvhu700001i-ultra-7-155h-2xnvme-sata-2x-hdmi-2-1-2x-dp-1-4a-vesa-mount"
try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    specs_section = re.findall(r'<div class="specs-content-scrollable"[^>]*>(.*?)</div>\s*</div>', html, re.DOTALL)
    if specs_section:
        text = specs_section[0].lower()
        print("Specs text length:", len(text))
        print("Contains brand?", 'thuong hieu' in text or 'brand' in text or 'thương hiệu' in text)
        print("Contains power?", 'power' in text)
        print("Contains warranty?", 'bao hanh' in text or 'bảo hành' in text)
        print("Contains os?", 'os' in text or 'hệ điều hành' in text or 'he dieu hanh' in text)
        print("Contains status?", 'tinh trang' in text or 'tình trạng' in text)
    else:
        print("Specs section not found")
except Exception as e:
    print("Error:", e)
