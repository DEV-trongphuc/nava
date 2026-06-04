with open("assets/main.js", "r", encoding="utf-8") as f:
    content = f.read()

import re
lines = content.split('\n')
product_lines = []
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ["product", "variant", "addtocart", "buynow", "qty", "quantity", "price"]):
        product_lines.append(f"{i+1}: {line}")

with open("scratch/mainjs_product_lines.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(product_lines))

# Also search for "js-" selectors
js_classes = set(re.findall(r'\.js-[a-zA-Z0-9_-]+', content))
print(f"js- classes in main.js: {js_classes}")
