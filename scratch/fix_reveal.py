import re

with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Remove 'reveal' class from shopee-comment-item
js_content = js_content.replace("div.className = 'shopee-comment-item reveal';", "div.className = 'shopee-comment-item';")

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Removed reveal class to fix visibility issue.")
