import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

css_urls = [
    "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/swiper.scss.css?1780666203046",
    "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/mew_style_gb.scss.css?1780666203046",
    "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/product_style.scss.css?1780666203046",
    "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/style.css?1780666203046"
]

with open("scratch/css_debug.txt", "w", encoding="utf-8") as f_out:
    for url in css_urls:
        f_out.write(f"=== URL: {url} ===\n")
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                css = response.read().decode('utf-8')
                # Find all occurrences of anything matching class selectors
                for pattern in [r'\.special-content[^{]*\{[^}]*\}', r'\.spec-tables[^{]*\{[^}]*\}', r'\.specs-content-scrollable[^{]*\{[^}]*\}']:
                    matches = re.findall(pattern, css)
                    for match in matches:
                        f_out.write(f"Match: {match}\n")
        except Exception as e:
            f_out.write(f"Error: {e}\n")
        f_out.write("\n")

print("Saved output to scratch/css_debug.txt successfully!")
