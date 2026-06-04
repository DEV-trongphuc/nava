with open("assets/main.js", "r", encoding="utf-8") as f:
    content = f.read()

print(f"File size: {len(content)}")
import re
cart_matches = re.findall(r'.{0,50}cart.{0,50}', content, re.IGNORECASE)
print(f"Found {len(cart_matches)} matches for 'cart' in main.js")
for m in cart_matches[:5]:
    print(m)
