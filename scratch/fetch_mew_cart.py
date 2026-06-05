import urllib.request
import ssl

def main():
    url = "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/mew_cart.js?1778729235331"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            js = response.read().decode('utf-8')
        with open('scratch/mew_cart.js', 'w', encoding='utf-8') as f:
            f.write(js)
        print("Successfully fetched mew_cart.js and saved to scratch/mew_cart.js")
    except Exception as e:
        print("Error fetching URL:", e)

if __name__ == '__main__':
    main()
