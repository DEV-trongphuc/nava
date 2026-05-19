import urllib.request
import re

def get_images():
    try:
        req = urllib.request.Request(
            'https://navastore.vn/nava-mini-pc-gaming-um880-pro-minisforum-amd-ryzen-8845hs-radeon-780m-rdna3-may-tinh-r7-8000-3', 
            headers={'User-Agent': 'Mozilla'}
        )
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # find any bizweb image links
        imgs = re.findall(r'//bizweb.dktcdn.net/[^\s"\'\>]+', html)
        print("Found images:")
        for img in set(imgs):
            if 'product' in img or 'thumb' in img:
                print(img)
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    get_images()
