import urllib.request
import os

os.makedirs("assets", exist_ok=True)

icons = {
    "assets/shopee.png": "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/shopee.png",
    "assets/lazada.png": "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/lazada.jpg",
    "assets/tiktok.png": "https://bizweb.dktcdn.net/100/543/817/files/tiktok_3247c513-7e3d-4fff-adec-fd98e4ee41c9.png",
    "assets/facebook.png": "https://bizweb.dktcdn.net/100/543/817/files/facebook.png",
    "assets/youtube.png": "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_head_2.png"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for local_path, url in icons.items():
    try:
        print(f"Downloading {url} to {local_path}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(local_path, "wb") as f:
                f.write(response.read())
        print(f"Success: {local_path} downloaded.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")
