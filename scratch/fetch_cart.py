import urllib.request
import ssl

def main():
    url = "https://navastore.vn/cart"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
        with open('scratch/live_cart.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Successfully fetched live cart HTML and saved to scratch/live_cart.html")
    except Exception as e:
        print("Error fetching URL:", e)

if __name__ == '__main__':
    main()
