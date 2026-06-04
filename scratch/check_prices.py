with open("demo_product.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for any <del> tag or price elements
import re
del_tags = re.findall(r'<del.*?>.*?</del>', content, re.IGNORECASE)
print(f"Found del tags: {del_tags}")

# Search around "main-price"
idx = content.find("main-price")
if idx != -1:
    print("Around main-price:")
    print(content[idx-200:idx+300])
