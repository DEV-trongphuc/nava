import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find('class="swatch-element 512GB')
if idx != -1:
    print("Found parent tags of swatch-element:")
    print(html[idx-1500:idx])
else:
    print("Not found swatch-element 512GB")
