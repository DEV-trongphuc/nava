import urllib.request
import os

os.makedirs("assets", exist_ok=True)

logos = {
    "assets/beikong.png": "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/beikong.png",
    "assets/gmktec.png": "https://bizweb.dktcdn.net/100/543/817/files/logo-1-1536x297.png",
    "assets/bmax.png": "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_brand_4.png"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for local_path, url in logos.items():
    try:
        print(f"Downloading {url} to {local_path}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(local_path, "wb") as f:
                f.write(response.read())
        print(f"Success: {local_path} downloaded.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")
