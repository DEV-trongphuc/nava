import urllib.request
import ssl
import re

def main():
    url = "https://navastore.vn/mini-pc-ho-tro-ai-asus-nuc-14-pro-rnuc14rvhu700001i-ultra-7-155h-2xnvme-sata-2x-hdmi-2-1-2x-dp-1-4a-vesa-mount"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print("Error fetching URL:", e)
        return

    lines = html.splitlines()
    in_script = False
    script_lines = []
    
    # We want the last script block which starts after line 3000
    for idx, line in enumerate(lines):
        if '<script>' in line or '<script ' in line:
            if '</script>' in line:
                pass
            else:
                if idx + 1 >= 3400:
                    in_script = True
                    script_lines = []
        elif '</script>' in line:
            if in_script:
                in_script = False
                with open('scratch/live_script.js', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(script_lines))
                print("Written live script to scratch/live_script.js")
                break
        elif in_script:
            script_lines.append(line)

if __name__ == '__main__':
    main()
