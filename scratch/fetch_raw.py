import urllib.request
import ssl

def main():
    url = "https://navastore.vn/mini-pc-asus-nuc-15-pro-plus-rnuc15crsu500000i-ultra-5-225h"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
        lines = html.splitlines()
        
        start = max(0, 4117 - 50)
        end = min(len(lines), 4117 + 50)
        
        with open('scratch/live_lines.txt', 'w', encoding='utf-8') as f:
            for i in range(start, end):
                f.write(f"{i+1}: {lines[i]}\n")
        print("Lines saved to scratch/live_lines.txt")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    main()
