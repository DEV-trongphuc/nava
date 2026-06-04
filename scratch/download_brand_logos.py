import os
import urllib.request

def download_logos():
    assets_dir = r"f:\BAO_SAPO\sapo_new\assets"
    os.makedirs(assets_dir, exist_ok=True)
    
    logos = {
        "beelink.png": "https://bizweb.dktcdn.net/100/543/817/files/beelink.png",
        "beikong.png": "https://bizweb.dktcdn.net/100/543/817/files/beikong.png",
        "bmax.png": "https://bizweb.dktcdn.net/100/543/817/files/bmax.png",
        "gmktec.png": "https://bizweb.dktcdn.net/100/543/817/files/gmktec.png",
        "minisforum.png": "https://bizweb.dktcdn.net/100/543/817/files/minisforum.png"
    }
    
    for filename, url in logos.items():
        dest_path = os.path.join(assets_dir, filename)
        print(f"Downloading {url} -> {dest_path}")
        try:
            # Add user-agent header to bypass simple blocks
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'}
            )
            with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Successfully downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    download_logos()
