import re

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    html = f.read()

# Tìm tất cả các class chứa từ "swatch"
matches = re.findall(r'class="([^"]*swatch[^"]*)"', html)
print("Found classes containing 'swatch':", set(matches))

# Tìm các đoạn HTML chứa swatch-element để xem thẻ cha của nó là gì
idx = html.find("swatch-element")
if idx != -1:
    print("\nHTML snippet around swatch-element:")
    print(html[idx-300:idx+500])
else:
    print("Not found swatch-element")
