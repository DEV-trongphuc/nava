import urllib.request
import ssl

def main():
    url = "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/cart_style.scss.css?1780642765118"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            css = response.read().decode('utf-8')
        with open('scratch/cart_style.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("Successfully fetched cart style CSS and saved to scratch/cart_style.css")
        
        # search for ux-card in it
        if 'ux-card' in css:
            print("Found 'ux-card' in CDN CSS!")
    except Exception as e:
        print("Error fetching URL:", e)

if __name__ == '__main__':
    main()
