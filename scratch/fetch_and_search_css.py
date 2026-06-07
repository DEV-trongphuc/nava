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

for url in css_urls:
    print(f"Fetching: {url}")
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            css = response.read().decode('utf-8')
            
            # Search for spec-tables, special-content
            for query in ["special-content", "spec-tables"]:
                matches = list(re.finditer(query, css))
                if matches:
                    print(f"  Found '{query}' in {url.split('/')[-1].split('?')[0]}:")
                    for m in matches[:5]: # print first 5 occurrences
                        idx = m.start()
                        # print 150 chars around
                        context = css[max(0, idx-80):min(len(css), idx+150)]
                        print(f"    ... {context.strip()} ...")
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
